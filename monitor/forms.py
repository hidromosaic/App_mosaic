from django import forms
from .models import  MonitoramentoEfluente, Parametro, UnidadeMedicao, UnidadeEmpresarial, PontoMonitoramento, EducacaoAmbiental, ListaPresenca, ControleResiduo, Relatorio


class MonitoramentoEfluenteForm(forms.ModelForm):
    class Meta:
        model = MonitoramentoEfluente
        exclude = ['conformidade']
        widgets = {
            'data_medicao': forms.DateInput(attrs={'type': 'date'}),
            'justificativa': forms.Textarea(attrs={'rows': 3}),
        }

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
        fields = '__all__'
        widgets = {
            'data_planejada': forms.DateInput(attrs={'type': 'date'}),
            'data_executada': forms.DateInput(attrs={'type': 'date'}),
            'atividade': forms.Textarea(attrs={'rows': 3}),
        }

class ListaPresencaForm(forms.ModelForm):
    class Meta:
        model = ListaPresenca
        fields = '__all__'

class ControleResiduoForm(forms.ModelForm):
    class Meta:
        model = ControleResiduo
        fields = '__all__'
        widgets = {
            'data_emissao': forms.DateInput(attrs={'type': 'date'}),
        }

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
