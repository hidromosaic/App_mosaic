from django import forms
from .models import  MonitoramentoEfluente, Parametro, UnidadeMedicao, UnidadeEmpresarial, PontoMonitoramento, EducacaoAmbiental, ListaPresenca, ControleResiduo, Relatorio


class MonitoramentoEfluenteForm(forms.ModelForm):
    class Meta:
        model = MonitoramentoEfluente
        exclude = ['conformidade', 'inserido_por', 'unidade_empresarial']
        widgets = {
            'data_medicao': forms.DateInput(attrs={'type': 'date'}),
            'justificativa': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pega o user passado pela view
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'unidade'):
            self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.filter(unidade_empresarial=user.unidade)
        else:
            self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.none()

class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = '__all__'

class UnidadeMedicaoForm(forms.ModelForm):
    class Meta:
        model = UnidadeMedicao
        fields = '__all__'

class UnidadeEmpresarialForm(forms.ModelForm):
    class Meta:
        model = UnidadeEmpresarial
        fields = '__all__'

class PontoMonitoradoForm(forms.ModelForm):
    class Meta:
        model = PontoMonitoramento
        fields = '__all__'

class EducacaoAmbientalForm(forms.ModelForm):
    class Meta:
        model = EducacaoAmbiental
        exclude = ['unidade_empresarial', 'inserido_por']
        widgets = {
            'data_planejada': forms.DateInput(attrs={'type': 'date'}),
            'data_executada': forms.DateInput(attrs={'type': 'date'}),
            'atividade': forms.Textarea(attrs={'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        #if user and hasattr(user, 'unidade'):
        #    self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.filter(unidade_empresarial=user.unidade)

class ListaPresencaForm(forms.ModelForm):
    class Meta:
        model = ListaPresenca
        fields = '__all__'

class ControleResiduoForm(forms.ModelForm):
    class Meta:
        model = ControleResiduo
        exclude = ['unidade_empresarial', 'inserido_por']
        widgets = {
            'data_emissao': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        #if user and hasattr(user, 'unidade'):
        #    self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.filter(unidade_empresarial=user.unidade)

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        exclude = ['unidade', 'inserido_por']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        #if user and hasattr(user, 'unidade'):
        #    self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.filter(unidade=user.unidade)
