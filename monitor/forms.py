from django import forms
from .models import  EfluentesLiquidos, Emissoes, Ruidos, Parametro, UnidadeMedicao, UnidadeEmpresarial, PontoMonitoramento, EducacaoAmbiental, ListaPresenca, ControleResiduo, Relatorio


class EfluentesLiquidosForm(forms.ModelForm):
    class Meta:
        model = EfluentesLiquidos
        exclude = ['conformidade', 'inserido_por']
        widgets = {
            'data_medicao': forms.DateInput(attrs={'type': 'date'}),
            'justificativa': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o user passado pela view
        super().__init__(*args, **kwargs)

        self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.none()

        if user and hasattr(user, 'unidade'):
            unidades = user.unidade.all()  # Assume ManyToManyField

            # Filtra pontos monitorados conforme unidades do usuário
            self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.filter(unidade_empresarial__in=unidades)

            #Filtra os Parâmetros conforme o programa
            #self.fields['parametro'].queryset = Parametro.objects.none()

            # Adiciona campo 'unidade_empresarial' dinamicamente se não estiver no exclude
            self.fields['unidade_empresarial'] = forms.ModelChoiceField(
                queryset=unidades,
                required=True,
                label="Unidade Empresarial"
            )

            if unidades.count() == 1:
                # Se só tem uma, oculta o campo e define o valor
                self.fields['unidade_empresarial'].widget = forms.HiddenInput()
                self.initial['unidade_empresarial'] = unidades.first()

class EmissoesForm(forms.ModelForm):
    class Meta:
        model = Emissoes
        exclude = ['conformidade', 'inserido_por']
        widgets = {
            'data_medicao': forms.DateInput(attrs={'type': 'date'}),
            'justificativa': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o user passado pela view
        super().__init__(*args, **kwargs)

        self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.none()

        if user and hasattr(user, 'unidade'):
            unidades = user.unidade.all()  # Assume ManyToManyField

            # Filtra pontos monitorados conforme unidades do usuário
            self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.filter(unidade_empresarial__in=unidades)
            #self.fields['parametro'].queryset = Parametro.objects.none()
            # Adiciona campo 'unidade_empresarial' dinamicamente se não estiver no exclude
            self.fields['unidade_empresarial'] = forms.ModelChoiceField(
                queryset=unidades,
                required=True,
                label="Unidade Empresarial"
            )

            if unidades.count() == 1:
                # Se só tem uma, oculta o campo e define o valor
                self.fields['unidade_empresarial'].widget = forms.HiddenInput()
                self.initial['unidade_empresarial'] = unidades.first()

class RuidosForm(forms.ModelForm):
    class Meta:
        model = Ruidos
        exclude = ['conformidade', 'inserido_por']
        widgets = {
            'data_medicao': forms.DateInput(attrs={'type': 'date'}),
            'justificativa': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o user passado pela view
        super().__init__(*args, **kwargs)

        self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.none()

        if user and hasattr(user, 'unidade'):
            unidades = user.unidade.all()  # Assume ManyToManyField

            # Filtra pontos monitorados conforme unidades do usuário
            self.fields['ponto_monitorado'].queryset = PontoMonitoramento.objects.filter(unidade_empresarial__in=unidades)
            self.fields['parametro'].queryset = Parametro.objects.filter(subcategoria__categoria__iexact='Ruídos')
            # Define queryset do campo unidade_empresarial com base nas unidades do usuário
            self.fields['unidade_empresarial'].queryset = unidades
            self.fields['unidade_empresarial'].required = True
            self.fields['unidade_empresarial'].label = "Unidade Empresarial"

            if unidades.count() == 1:
                # Se só tem uma, oculta o campo e define o valor
                self.fields['unidade_empresarial'].widget = forms.HiddenInput()
                self.initial['unidade_empresarial'] = unidades.first()



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
        exclude = ['inserido_por']
        widgets = {
            'data_planejada': forms.DateInput(attrs={'type': 'date'}),
            'data_executada': forms.DateInput(attrs={'type': 'date'}),
            'atividade': forms.Textarea(attrs={'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o user passado pela view
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'unidade'):
            unidades = user.unidade.all()  # Assume ManyToManyField

            # Adiciona campo 'unidade_empresarial' dinamicamente se não estiver no exclude
            self.fields['unidade_empresarial'].queryset = unidades
            self.fields['unidade_empresarial'].required = True
            self.fields['unidade_empresarial'].label = "Unidade Empresarial"

            if unidades.count() == 1:
                # Se só tem uma, oculta o campo e define o valor
                self.fields['unidade_empresarial'].widget = forms.HiddenInput()
                self.initial['unidade_empresarial'] = unidades.first()

class ListaPresencaForm(forms.ModelForm):
    class Meta:
        model = ListaPresenca
        fields = '__all__'

class ControleResiduoForm(forms.ModelForm):
    class Meta:
        model = ControleResiduo
        exclude = ['inserido_por']
        widgets = {
            'data_emissao': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o user passado pela view
        super().__init__(*args, **kwargs)


        if user and hasattr(user, 'unidade'):
            unidades = user.unidade.all()  # Assume ManyToManyField

            # Adiciona campo 'unidade_empresarial' dinamicamente se não estiver no exclude
            self.fields['unidade_empresarial'] = forms.ModelChoiceField(
                queryset=unidades,
                required=True,
                label="Unidade Empresarial"
            )

            if unidades.count() == 1:
                # Se só tem uma, oculta o campo e define o valor
                self.fields['unidade_empresarial'].widget = forms.HiddenInput()
                self.initial['unidade_empresarial'] = unidades.first()

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        exclude = [ 'inserido_por']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o user passado pela view
        super().__init__(*args, **kwargs)


        if user and hasattr(user, 'unidade'):
            unidades = user.unidade.all()  # Assume ManyToManyField

            # Adiciona campo 'unidade_empresarial' dinamicamente se não estiver no exclude
            self.fields['unidade_empresarial'] = forms.ModelChoiceField(
                queryset=unidades,
                required=True,
                label="Unidade Empresarial"
            )

            if unidades.count() == 1:
                # Se só tem uma, oculta o campo e define o valor
                self.fields['unidade_empresarial'].widget = forms.HiddenInput()
                self.initial['unidade_empresarial'] = unidades.first()
