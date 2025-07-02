from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages

from datetime import timedelta

from .models import MonitoramentoEfluente
from .forms import MonitoramentoEfluenteForm
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


@login_required
def adicionar_monitoramento(request):
    if request.method == 'POST':
        form = MonitoramentoEfluenteForm(request.POST)
        if form.is_valid():
            monitoramento = form.save()
            messages.success(
                request,
                f"Monitoramento salvo com sucesso. Conformidade: {monitoramento.conformidade}"
            )
            return redirect('listar_monitoramentos')
    else:
        form = MonitoramentoEfluenteForm()
    return render(request, 'monitor/adicionar.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def editar_monitoramento(request, pk):
    monitoramento = get_object_or_404(MonitoramentoEfluente, pk=pk)
    form = MonitoramentoEfluenteForm(request.POST, instance=monitoramento)
    if form.is_valid():
        form.save()
        return redirect('listar_monitoramentos')
    else:
        form = EducacaoAmbientalForm(instance=monitoramento)
    return render(request, 'monitor/form.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def excluir_monitoramento(request, pk):
    monitoramento = get_object_or_404(MonitoramentoEfluente, pk=pk)
    monitoramento.delete()
    return redirect('listar_monitoramentos')

@login_required
def listar_monitoramentos(request):
    monitoramentos = MonitoramentoEfluente.objects.all()
    return render(request, 'monitor/listar.html', {'monitoramentos': monitoramentos})


#Educação Ambiental
@login_required
def listar_educacao(request):
    educacoes = EducacaoAmbiental.objects.all()
    return render(request, 'monitor/listar_educacao.html', {'educacoes': educacoes})

@login_required
def adicionar_educacao(request):
    if request.method == 'POST':
        form = EducacaoAmbientalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_educacao')
    else:
        form = EducacaoAmbientalForm()
    return render(request, 'monitor/form_educacao.html', {'form': form})

@login_required
@user_passes_test(is_gerenciador)
def editar_educacao(request, pk):
    educacao = get_object_or_404(EducacaoAmbiental, pk=pk)
    if request.method == 'POST':
        form = EducacaoAmbientalForm(request.POST, instance=educacao)
        if form.is_valid():
            form.save()
            return redirect('listar_educacao')
    else:
        form = EducacaoAmbientalForm(instance=educacao)
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
    residuos = ControleResiduo.objects.all()
    return render(request, 'monitor/listar_residuos.html', {'residuos': residuos})

@login_required
def adicionar_residuo(request):
    if request.method == 'POST':
        form = ControleResiduoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_residuos')
    else:
        form = ControleResiduoForm()
    return render(request, 'monitor/form_residuo.html', {'form': form})

@login_required
def editar_residuo(request, pk):
    residuo = get_object_or_404(ControleResiduo, pk=pk)
    if request.method == 'POST':
        form = ControleResiduoForm(request.POST, instance=residuo)
        if form.is_valid():
            form.save()
            return redirect('listar_residuos')
    else:
        form = ControleResiduoForm(instance=residuo)
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
    relatorios = Relatorio.objects.all()
    return render(request, 'monitor/listar_relatorios.html', {'relatorios': relatorios})

@login_required
def adicionar_relatorio(request):
    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_relatorios')
    else:
        form = RelatorioForm()
    return render(request, 'monitor/form_relatorio.html', {'form': form})

@login_required
def editar_relatorio(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if request.method == 'POST':
        form = RelatorioForm(request.POST, instance=relatorio)
        if form.is_valid():
            form.save()
            return redirect('listar_relatorios')
    else:
        form = RelatorioForm(instance=relatorio)
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
    conformes = MonitoramentoEfluente.objects.filter(
        conformidade='Conforme',
        data_medicao__range=(data_inicial, data_final)
    ).count()

    nao_conformes = MonitoramentoEfluente.objects.filter(
        conformidade='Não Conforme',
        data_medicao__range=(data_inicial, data_final)
    ).count()

    # Dados por tipo de efluente
    por_tipo = (
        MonitoramentoEfluente.objects
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
