import plotly.graph_objs as go
import plotly.offline as opy

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages

from datetime import timedelta

from .models import EfluentesLiquidos, Emissoes, Ruidos
from .forms import EfluentesLiquidosForm, EmissoesForm, RuidosForm
from .models import EducacaoAmbiental, Parametro
from .forms import EducacaoAmbientalForm
from .models import ControleResiduo, ListaPresenca, Relatorio
from .forms import ControleResiduoForm, ListaPresencaForm, RelatorioForm

from django.db.models import Count, Q, Avg, StdDev
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

def gerar_grafico_historico(modelo, usuario, titulo):
    unidades = usuario.unidade.all()
    dados = modelo.objects.filter(unidade_empresarial__in=unidades)

    graficos = []
    parametros = dados.values_list('parametro__nome', flat=True).distinct()

    for parametro_nome in parametros:
        fig = go.Figure()
        pontos = dados.filter(parametro__nome=parametro_nome).values_list('ponto_monitorado__nome', flat=True).distinct()

        # Recuperar os limites do parâmetro (pegando um registro para extrair)
        parametro_obj = modelo.objects.filter(parametro__nome=parametro_nome).first()
        limite_aceitavel = parametro_obj.parametro.limite_aceitavel if parametro_obj else None
        limite_max = parametro_obj.parametro.limite_max if parametro_obj else None

        for ponto in pontos:
            registros = dados.filter(parametro__nome=parametro_nome, ponto_monitorado__nome=ponto).order_by('data_medicao')
            datas = [r.data_medicao for r in registros]
            resultados = [r.resultado for r in registros]

            fig.add_trace(go.Scatter(
                x=datas,
                y=resultados,
                mode='lines+markers',
                name=ponto,
                hovertemplate=(
                    "Data: %{x|%d/%m/%Y}<br>" +
                    "Resultado: %{y}<br>" +
                    f"Parâmetro: {parametro_nome}<extra></extra>"
                )
            ))

        # Adicionar linhas horizontais dos limites
        if limite_aceitavel is not None:
            fig.add_hline(y=limite_aceitavel, line_dash="dash", line_color="green",
                          annotation_text="Limite Aceitável", annotation_position="top left")
        if limite_max is not None:
            fig.add_hline(y=limite_max, line_dash="dot", line_color="red",
                          annotation_text="Limite Máximo", annotation_position="top left")

        fig.update_layout(
            title=f'{titulo} - {parametro_nome}',
            xaxis_title='Data',
            yaxis_title='Resultado',
            hovermode='closest',
            legend_title='Ponto Monitorado',
            showlegend=True
        )

        graficos.append(opy.plot(fig, auto_open=False, output_type='div'))

    return graficos

def gerar_grafico_barras_media(modelo, usuario, titulo):
    unidades = usuario.unidade.all()
    dados = modelo.objects.filter(unidade_empresarial__in=unidades)

    graficos = []
    parametros = dados.values_list('parametro__nome', flat=True).distinct()

    for parametro in parametros:
        fig = go.Figure()

        # Calcula média e desvio padrão por ponto
        estatisticas = dados.filter(parametro__nome=parametro) \
            .values('ponto_monitorado__nome') \
            .annotate(
                media_resultado=Avg('resultado'),
                desvio_padrao=StdDev('resultado')
            ) \
            .order_by('ponto_monitorado__nome')

        pontos = [item['ponto_monitorado__nome'] for item in estatisticas]
        medias_resultado = [item['media_resultado'] for item in estatisticas]
        desvios = [item['desvio_padrao'] if item['desvio_padrao'] is not None else 0 for item in estatisticas]

        fig.add_trace(go.Bar(
            x=pontos,
            y=medias_resultado,
            name=parametro,
            error_y=dict(
                type='data',
                array=desvios,
                visible=True
            ),
            hovertemplate=(
                'Ponto: %{x}<br>'
                'Média Resultado: %{y:.2f}<br>'
                'Desvio Padrão: %{customdata:.2f}<br>'
                'Parâmetro: ' + parametro + '<extra></extra>'
            ),
            customdata=desvios
        ))

        fig.update_layout(
            title=f'{titulo} - Média dos Resultados por Ponto - {parametro}',
            xaxis_title='Ponto de Monitoramento',
            yaxis_title='Média do Resultado',
            showlegend=True,
            hovermode='closest'
        )

        graficos.append(opy.plot(fig, auto_open=False, output_type='div'))

    return graficos

def gerar_grafico_violino(modelo, usuario, titulo):
    unidades = usuario.unidade.all()
    dados = modelo.objects.filter(unidade_empresarial__in=unidades)

    graficos = []
    parametros = dados.values_list('parametro__nome', flat=True).distinct()

    for parametro in parametros:
        fig = go.Figure()
        dados_param = dados.filter(parametro__nome=parametro)

        # Agrupa os valores por ponto de monitoramento
        pontos = dados_param.values_list('ponto_monitorado__nome', flat=True).distinct()

        for ponto in pontos:
            valores = dados_param.filter(ponto_monitorado__nome=ponto).values_list('resultado', flat=True)
            fig.add_trace(go.Violin(
                y=list(valores),
                name=ponto,
                box_visible=True,
                meanline_visible=True,
                points='all',  # pode ser 'suspectedoutliers', 'outliers', ou False para esconder
                #line_color='green',
                hoveron='points+kde',
                hovertemplate=(
                    'Ponto: ' + ponto + '<br>' +
                    'Valor: %{y}<extra></extra>'
                )
            ))

        fig.update_layout(
            title=f'{titulo} - Distribuição (Violino) por Ponto - {parametro}',
            yaxis_title='Resultado',
            xaxis_title='Ponto de Monitoramento',
            violingap=0.3,
            violinmode='group',
            showlegend=True
        )

        graficos.append(opy.plot(fig, auto_open=False, output_type='div'))

    return graficos


def is_gerenciador(user):
    return user.groups.filter(name='Gerenciador').exists()

def is_tecnico(user):
    return user.groups.filter(name='Tecnico').exists()

def home(request):
    return render(request, 'monitor/home.html')

@login_required
def adicionar_efluente_liquido(request):
    if request.method == 'POST':
        form = EfluentesLiquidosForm(request.POST, user=request.user)
        if form.is_valid():
            monitoramento = form.save(commit=False)
            monitoramento.inserido_por = request.user
            if not monitoramento.unidade_empresarial:
                monitoramento.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            monitoramento.save()
            messages.success(
                request,
                f"Monitoramento de efluente liquido salvo com sucesso. Conformidade: {monitoramento.conformidade}"
            )
            return redirect('listar_efluentes')
    else:
        form = EfluentesLiquidosForm(user=request.user)
    return render(request, 'monitor/adicionar_efluentes_liquidos.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def editar_efluente_liquido(request, pk):
    obj = get_object_or_404(EfluentesLiquidos, pk=pk)
    if request.method == 'POST':
        form = EfluentesLiquidosForm(request.POST, instance=obj, user=request.user)
        if form.is_valid():
            monitoramento = form.save(commit=False)
            monitoramento.inserido_por = request.user  # Se quiser atualizar também na edição
            if not monitoramento.unidade_empresarial:
                monitoramento.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            monitoramento.save()
            return redirect('listar_efluentes')
    else:
        form = EfluentesLiquidosForm(instance=obj, user=request.user)
    return render(request, 'monitor/form_efluente_liquido.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_efluente_liquido(request, pk):
    monitoramento = get_object_or_404(EfluentesLiquidos, pk=pk)
    if request.method == 'POST':
        monitoramento.delete()
        return redirect('listar_efluentes')
    return render(request, 'monitor/confirmar_exclusao.html', {'obj': monitoramento})

@login_required
def listar_efluentes(request):
    usuario = request.user
    unidade = usuario.unidade.all()
    query = request.GET.get('q')

    if unidade.count() == 1:
        unidade = unidade.first()
        monitoramentos = EfluentesLiquidos.objects.filter(unidade_empresarial=unidade)
    else:
        monitoramentos = EfluentesLiquidos.objects.filter(unidade_empresarial__in=unidade)

    if query:
        monitoramentos = monitoramentos.filter(
            Q(ponto_monitorado__nome__icontains=query) |
            Q(parametro__nome__icontains=query) |
            Q(data_medicao__icontains=query) |
            Q(conformidade__icontains=query)
        )
    monitoramentos = monitoramentos.order_by('-data_medicao')

    paginator = Paginator(monitoramentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'monitor/listar_efluentes.html', {'page_obj': page_obj, 'query': query})


#Emissões Atmosféricas
@login_required
def adicionar_emissoes(request):
    if request.method == 'POST':
        form = EmissoesForm(request.POST, user=request.user)
        if form.is_valid():
            monitoramento = form.save(commit=False)
            monitoramento.inserido_por = request.user
            if not monitoramento.unidade_empresarial:
                monitoramento.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            monitoramento.save()
            messages.success(
                request,
                f"Monitoramento de emissões atmosféricas salvo com sucesso. Conformidade: {monitoramento.conformidade}"
            )
            return redirect('listar_emissoes')
    else:
        form = EmissoesForm(user=request.user)
    return render(request, 'monitor/adicionar_emissoes.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def editar_emissoes(request, pk):
    obj = get_object_or_404(Emissoes, pk=pk)
    if request.method == 'POST':
        form = EmissoesForm(request.POST, instance=obj, user=request.user)
        if form.is_valid():
            monitoramento = form.save(commit=False)
            monitoramento.inserido_por = request.user  # Se quiser atualizar também na edição
            if not monitoramento.unidade_empresarial:
                monitoramento.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            monitoramento.save()
            return redirect('listar_emissoes')
    else:
        form = EmissoesForm(instance=obj, user=request.user)
    return render(request, 'monitor/form_emissoes.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_emissoes(request, pk):
    monitoramento = get_object_or_404(Emissoes, pk=pk)
    if request.method == 'POST':
        monitoramento.delete()
        return redirect('listar_emissoes')
    return render(request, 'monitor/confirmar_exclusao.html', {'obj': monitoramento})

@login_required
def listar_emissoes(request):
    usuario = request.user
    unidade = usuario.unidade.all()
    query = request.GET.get('q')

    if unidade.count() == 1:
        unidade = unidade.first()
        monitoramentos = Emissoes.objects.filter(unidade_empresarial=unidade)
    else:
        monitoramentos = Emissoes.objects.filter(unidade_empresarial__in=unidade)

    if query:
        monitoramentos = monitoramentos.filter(
            Q(ponto_monitorado__nome__icontains=query) |
            Q(parametro__nome__icontains=query) |
            Q(data_medicao__icontains=query) |
            Q(conformidade__icontains=query)
        )

    monitoramentos = monitoramentos.order_by('-data_medicao')

    paginator = Paginator(monitoramentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'monitor/listar_emissoes.html', {'page_obj': page_obj, 'query': query})

#Ruídos
@login_required
def adicionar_ruido(request):
    if request.method == 'POST':
        form = RuidosForm(request.POST, user=request.user)
        if form.is_valid():
            monitoramento = form.save(commit=False)
            monitoramento.inserido_por = request.user
            if not monitoramento.unidade_empresarial:
                monitoramento.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            monitoramento.save()
            messages.success(
                request,
                f"Monitoramento de ruido salvo com sucesso. Conformidade: {monitoramento.conformidade}"
            )
            return redirect('listar_ruidos')
    else:
        form = RuidosForm(user=request.user)
    return render(request, 'monitor/adicionar_ruido.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def editar_ruido(request, pk):
    obj = get_object_or_404(Ruidos, pk=pk)
    if request.method == 'POST':
        form = RuidosForm(request.POST, instance=obj, user=request.user)
        if form.is_valid():
            monitoramento = form.save(commit=False)
            monitoramento.inserido_por = request.user  # Se quiser atualizar também na edição
            if not monitoramento.unidade_empresarial:
                monitoramento.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            monitoramento.save()
            return redirect('listar_ruidos')
    else:
        form = RuidosForm(instance=obj, user=request.user)
    return render(request, 'monitor/form_ruido.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_ruidos(request, pk):
    monitoramento = get_object_or_404(Ruidos, pk=pk)
    if request.method == 'POST':
        monitoramento.delete()
        return redirect('listar_ruidos')
    return render(request, 'monitor/confirmar_exclusao.html', {'obj': monitoramento})

@login_required
def listar_ruidos(request):
    usuario = request.user
    unidade = usuario.unidade.all()
    query = request.GET.get('q')

    if unidade.count() == 1:
        unidade = unidade.first()
        monitoramentos = Ruidos.objects.filter(unidade_empresarial=unidade)
    else:
        monitoramentos = Ruidos.objects.filter(unidade_empresarial__in=unidade)

    if query:
        monitoramentos = monitoramentos.filter(
            Q(ponto_monitorado__nome__icontains=query) |
            Q(parametro__nome__icontains=query) |
            Q(data_medicao__icontains=query) |
            Q(conformidade__icontains=query)
        )

    monitoramentos = monitoramentos.order_by('-data_medicao')

    paginator = Paginator(monitoramentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'monitor/listar_ruidos.html', {'page_obj': page_obj, 'query': query})


#Educação Ambiental
@login_required
def listar_educacao(request):
    usuario = request.user
    unidade = usuario.unidade.all()
    query = request.GET.get('q')

    if unidade.count() == 1:
        unidade = unidade.first()
        educacoes = EducacaoAmbiental.objects.filter(unidade_empresarial=unidade)
    else:
        educacoes = EducacaoAmbiental.objects.filter(unidade_empresarial__in=unidade)

    if query:
        educacoes = educacoes.filter(
            Q(tema__icontains=query)
        )

    educacoes = educacoes.order_by('-data_executada')

    paginator = Paginator(educacoes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'monitor/listar_educacao.html', {'page_obj': page_obj, 'query':query})

@login_required
def adicionar_educacao(request):
    if request.method == 'POST':
        form = EducacaoAmbientalForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.unidade_empresarial:
                instance.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            instance.inserido_por = request.user
            instance.save()
            return redirect('listar_educacao')
    else:
        form = EducacaoAmbientalForm(user=request.user)
    return render(request, 'monitor/form_educacao.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def editar_educacao(request, pk):
    educacao = get_object_or_404(EducacaoAmbiental, pk=pk)
    if request.method == 'POST':
        form = EducacaoAmbientalForm(request.POST, instance=educacao, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.unidade_empresarial:
                instance.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            instance.inserido_por = request.user
            instance.save()
            return redirect('listar_educacao')
    else:
        form = EducacaoAmbientalForm(instance=educacao, user=request.user)
    return render(request, 'monitor/form_educacao.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_educacao(request, pk):
    educacao = get_object_or_404(EducacaoAmbiental, pk=pk)
    if request.method == 'POST':
        educacao.delete()
        return redirect('listar_educacao')
    return render(request, 'monitor/confirmar_exclusao.html', {'obj': educacao})


# Controle de Resíduos
@login_required
def listar_residuos(request):
    usuario = request.user
    unidade = usuario.unidade.all()
    query = request.GET.get('q')

    if unidade.count() == 1:
        unidade = unidade.first()
        residuos = ControleResiduo.objects.filter(unidade_empresarial=unidade)
    else:
        residuos = ControleResiduo.objects.filter(unidade_empresarial__in=unidade)

    if query:
        residuos = residuos.filter(
            Q(codigo_residuo__icontains=query) |
            Q(nome_residuo__icontains=query)
        )

    residuos = residuos.order_by('-data_emissao')

    paginator = Paginator(residuos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'monitor/listar_residuos.html', {'page_obj': page_obj, 'query':query})

@login_required
def adicionar_residuo(request):
    if request.method == 'POST':
        form = ControleResiduoForm(request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.unidade_empresarial:
                instance.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            instance.inserido_por = request.user
            instance.save()
            return redirect('listar_residuos')
    else:
        form = ControleResiduoForm(user=request.user)
    return render(request, 'monitor/form_residuo.html', {'form': form})

@login_required
def editar_residuo(request, pk):
    residuo = get_object_or_404(ControleResiduo, pk=pk)
    if request.method == 'POST':
        form = ControleResiduoForm(request.POST, instance=residuo, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.unidade_empresarial:
                instance.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            instance.inserido_por = request.user
            instance.save()
            return redirect('listar_residuos')
    else:
        form = ControleResiduoForm(instance=residuo, user=request.user)
    return render(request, 'monitor/form_residuo.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_residuo(request, pk):
    residuo = get_object_or_404(ControleResiduo, pk=pk)
    if request.method == 'POST':
        residuo.delete()
        return redirect('listar_residuos')
    return render(request, 'monitor/confirmar_exclusao.html', {'obj': residuo})


# Lista de Presença
@login_required
def listar_presencas(request):
    presencas = ListaPresenca.objects.all()
    return render(request, 'monitor/listar_lista_presenca.html', {'presencas': presencas})

@login_required
def adicionar_presenca(request):
    if request.method == 'POST':
        form = ListaPresencaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_presencas')
    else:
        form = ListaPresencaForm()
    return render(request, 'monitor/form_presenca.html', {'form': form})

@login_required
def editar_presenca(request, pk):
    presenca = get_object_or_404(ListaPresenca, pk=pk)
    if request.method == 'POST':
        form = ListaPresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            return redirect('listar_presencas')
    else:
        form = ListaPresencaForm(instance=presenca)
    return render(request, 'monitor/form_presenca.html', {'form': form})

@login_required
def excluir_presenca(request, pk):
    presenca = get_object_or_404(ListaPresenca, pk=pk)
    if request.method == 'POST':
        presenca.delete()
        return redirect('listar_presencas')
    return render(request, 'monitor/confirmar_exclusao.html', {'obj': presenca})


# Relatórios
@login_required
def listar_relatorios(request):
    usuario = request.user
    unidade = usuario.unidade.all()

    query = request.GET.get('q')

    if unidade.count() == 1:
        unidade = unidade.first()
        relatorios = Relatorio.objects.filter(unidade_empresarial=unidade)
    else:
        relatorios = Relatorio.objects.filter(unidade_empresarial__in=unidade)

    if query:
        relatorios = relatorios.filter(
            Q(nome__icontains=query)
        )
    relatorios = relatorios.order_by('-data')

    paginator = Paginator(relatorios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'monitor/listar_relatorios.html', {'page_obj': page_obj})

@login_required
def adicionar_relatorio(request):
    if request.method == 'POST':
        form = RelatorioForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.unidade_empresarial:
                instance.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            instance.inserido_por = request.user
            instance.save()
            return redirect('listar_relatorios')
    else:
        form = RelatorioForm(user=request.user)
    return render(request, 'monitor/form_relatorio.html', {'form': form})

@login_required
def editar_relatorio(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if request.method == 'POST':
        form = RelatorioForm(request.POST, instance=relatorio, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.unidade_empresarial:
                instance.unidade_empresarial = request.user.unidade or request.user.unidade.first()
            instance.inserido_por = request.user
            instance.save()
            return redirect('listar_relatorios')
    else:
        form = RelatorioForm(instance=relatorio, user=request.user)
    return render(request, 'monitor/form_relatorio.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_relatorio(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if request.method == 'POST':
        relatorio.delete()
        return redirect('listar_relatorios')
    return render(request, 'monitor/confirmar_exclusao.html', {'obj': relatorio})



def is_gerenciador(user):
    return user.groups.filter(name='Gerenciador').exists() or user.is_superuser

@login_required
@user_passes_test(is_gerenciador)
def dashboard_efluentes(request):
    usuario = request.user
    graficos_efluentes = gerar_grafico_historico(EfluentesLiquidos, usuario, 'Efluentes Líquidos')
    graficos_barra_efluentes = gerar_grafico_barras_media(EfluentesLiquidos, usuario, 'Efluentes Líquidos')
    graficos_violino_efluentes = gerar_grafico_violino(EfluentesLiquidos, usuario, 'EfluentesLiquidos')
    contexto = {
        'graficos_efluentes': graficos_efluentes,
        'graficos_barra_efluentes': graficos_barra_efluentes,
        'graficos_violino_efluentes': graficos_violino_efluentes
    }

    return render(request, 'monitor/dashboard_efluentes.html', contexto)

@login_required
@user_passes_test(is_gerenciador)
def dashboard_emissoes(request):
    usuario = request.user
    graficos_emissoes = gerar_grafico_historico(Emissoes, usuario, 'Emissões Atmosféricas')
    graficos_barra_emissoes = gerar_grafico_barras_media(Emissoes, usuario, 'Emissões Atmosféricas')
    graficos_violino_emissoes = gerar_grafico_violino(Emissoes, usuario, 'Emissões Atmosféricas')
    contexto = {
        'graficos_emissoes': graficos_emissoes,
        'graficos_barra_emissoes': graficos_barra_emissoes,
        'graficos_violino_emissoes': graficos_violino_emissoes
    }
    return render(request, "monitor/dashboard_emissoes.html", contexto)

@login_required
@user_passes_test(is_gerenciador)
def dashboard_ruidos(request):
    usuario = request.user
    graficos_ruidos = gerar_grafico_historico(Ruidos, usuario, 'Ruídos Ambientais')
    graficos_barra_ruidos = gerar_grafico_barras_media(Ruidos, usuario, 'Ruídos Ambientais')
    graficos_violino_ruidos = gerar_grafico_violino(Ruidos, usuario, 'Ruídos Ambientais')
    contexto = {
        'graficos_ruidos': graficos_ruidos,
        'graficos_barra_ruidos': graficos_barra_ruidos,
        'graficos_violino_ruidos': graficos_violino_ruidos
    }
    return render(request, "monitor/dashboard_ruidos.html", contexto)
