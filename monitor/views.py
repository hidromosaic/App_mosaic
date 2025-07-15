from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages

from datetime import timedelta

from .models import EfluentesLiquidos, Emissoes, Ruidos
from .forms import EfluentesLiquidosForm, EmissoesForm, RuidosForm
from .models import EducacaoAmbiental
from .forms import EducacaoAmbientalForm
from .models import ControleResiduo, ListaPresenca, Relatorio
from .forms import ControleResiduoForm, ListaPresencaForm, RelatorioForm

from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test

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
            monitoramento.unidade_empresarial = request.user.unidade
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
            monitoramento.unidade_empresarial = request.user.unidade
            monitoramento.save()
            return redirect('listar_efluentes')
    else:
        form = EfluentesLiquidosForm(instance=obj, user=request.user)
    return render(request, 'monitor/form_efluente_liquido.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_efluente_liquido(request, pk):
    monitoramento = get_object_or_404(EfluentesLiquidos, pk=pk)
    monitoramento.delete()
    return redirect('listar_efluentes')

@login_required
def listar_efluentes(request):
    usuario = request.user
    unidade = usuario.unidade

    query = request.GET.get('q')

    monitoramentos = EfluentesLiquidos.objects.filter(ponto_monitorado__unidade_empresarial=unidade)

    if query:
        monitoramentos = monitoramentos.filter(
            Q(ponto_monitorado__nome__icontains=query) |
            Q(parametro__nome__icontains=query) |
            Q(data_medicao__icontains=query) |
            Q(conformidade__icontains=query)
        )

    return render(request, 'monitor/listar_efluentes.html', {'monitoramentos': monitoramentos, 'query': query})


#Emissões Atmosféricas
@login_required
def adicionar_emissoes(request):
    if request.method == 'POST':
        form = EmissoesForm(request.POST, user=request.user)
        if form.is_valid():
            monitoramento = form.save(commit=False)
            monitoramento.inserido_por = request.user
            monitoramento.unidade_empresarial = request.user.unidade
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
            monitoramento.unidade_empresarial = request.user.unidade
            monitoramento.save()
            return redirect('listar_emissoes')
    else:
        form = EmissoesForm(instance=obj, user=request.user)
    return render(request, 'monitor/form_emissoes.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_emissoes(request, pk):
    monitoramento = get_object_or_404(Emissoes, pk=pk)
    monitoramento.delete()
    return redirect('listar_emissoes')

@login_required
def listar_emissoes(request):
    usuario = request.user
    unidade = usuario.unidade

    query = request.GET.get('q')

    monitoramentos = Emissoes.objects.filter(ponto_monitorado__unidade_empresarial=unidade)

    if query:
        monitoramentos = monitoramentos.filter(
            Q(ponto_monitorado__nome__icontains=query) |
            Q(parametro__nome__icontains=query) |
            Q(data_medicao__icontains=query) |
            Q(conformidade__icontains=query)
        )

    return render(request, 'monitor/listar_emissoes.html', {'monitoramentos': monitoramentos, 'query': query})

#Ruídos
@login_required
def adicionar_ruido(request):
    if request.method == 'POST':
        form = RuidosForm(request.POST, user=request.user)
        if form.is_valid():
            monitoramento = form.save(commit=False)
            monitoramento.inserido_por = request.user
            monitoramento.unidade_empresarial = request.user.unidade
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
            monitoramento.unidade_empresarial = request.user.unidade
            monitoramento.save()
            return redirect('listar_ruidos')
    else:
        form = RuidosForm(instance=obj, user=request.user)
    return render(request, 'monitor/form_ruido.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_ruidos(request, pk):
    monitoramento = get_object_or_404(Ruidos, pk=pk)
    monitoramento.delete()
    return redirect('listar_ruidos')

@login_required
def listar_ruidos(request):
    usuario = request.user
    unidade = usuario.unidade

    query = request.GET.get('q')

    monitoramentos = Ruidos.objects.filter(ponto_monitorado__unidade_empresarial=unidade)

    if query:
        monitoramentos = monitoramentos.filter(
            Q(ponto_monitorado__nome__icontains=query) |
            Q(parametro__nome__icontains=query) |
            Q(data_medicao__icontains=query) |
            Q(conformidade__icontains=query)
        )

    return render(request, 'monitor/listar_ruidos.html', {'monitoramentos': monitoramentos, 'query': query})


#Educação Ambiental
@login_required
def listar_educacao(request):
    usuario = request.user
    unidade = usuario.unidade

    query = request.GET.get('q')

    educacoes = EducacaoAmbiental.objects.filter(unidade_empresarial=unidade)

    if query:
        educacoes = educacoes.filter(
            Q(tema__icontains=query)
        )

    return render(request, 'monitor/listar_educacao.html', {'educacoes': educacoes, 'query':query})

@login_required
def adicionar_educacao(request):
    if request.method == 'POST':
        form = EducacaoAmbientalForm(request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.unidade_empresarial = request.user.unidade
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
            instance.unidade_empresarial = request.user.unidade
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
    unidade = usuario.unidade

    query = request.GET.get('q')

    residuos = ControleResiduo.objects.filter(unidade_empresarial=unidade)

    if query:
        residuos = residuos.filter(
            Q(codigo_residuo__icontains=query) |
            Q(nome_residuo__icontains=query)
        )

    return render(request, 'monitor/listar_residuos.html', {'residuos': residuos, 'query':query})

@login_required
def adicionar_residuo(request):
    if request.method == 'POST':
        form = ControleResiduoForm(request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.unidade_empresarial = request.user.unidade
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
            instance.unidade_empresarial = request.user.unidade
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
    unidade = usuario.unidade

    query = request.GET.get('q')

    relatorios = Relatorio.objects.filter(unidade_empresarial=unidade)

    if query:
        relatorios = relatorios.filter(
            Q(nome__icontains=query)
        )
    return render(request, 'monitor/listar_relatorios.html', {'relatorios': relatorios})

@login_required
def adicionar_relatorio(request):
    if request.method == 'POST':
        form = RelatorioForm(request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.unidade_empresarial = request.user.unidade
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
            instance.unidade_empresarial = request.user.unidade
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
def dashboard(request):
    # Período dos últimos 30 dias
    data_final = timezone.now()
    data_inicial = data_final - timedelta(days=30)

    # Contagem de conformidade e não conformidade no período
    conformes = EfluentesLiquidos.objects.filter(
        conformidade='Conforme',
        data_medicao__range=(data_inicial, data_final)
    ).count()

    nao_conformes = EfluentesLiquidos.objects.filter(
        conformidade='Não Conforme',
        data_medicao__range=(data_inicial, data_final)
    ).count()

    # Dados por tipo de efluente
    por_tipo = (
        EfluentesLiquidos.objects
        .filter(data_medicao__range=(data_inicial, data_final))
        .values('tipo_efluente')
        .order_by('tipo_efluente')
        .annotate(qtd=Count('id'))
    )

    context = {
        'conformes': conformes,
        'nao_conformes': nao_conformes,
        'por_tipo': por_tipo,
    }

    return render(request, 'monitor/dashboard.html', context)

def dashboard_view(request):
    return render(request, "monitor/dashboard.html")
