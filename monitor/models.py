from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



class UnidadeMedicao(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Parametro(models.Model):
    nome = models.CharField(max_length=100)
    limite_aceitavel = models.FloatField()
    unidade_medicao = models.ForeignKey(UnidadeMedicao, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=100)
    requisito = models.TextField()
    periodicidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class UnidadeEmpresarial(models.Model):
    unidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    codigo = models.CharField(max_length=3, null=True)

    def __str__(self):
        return f"{self.unidade} - {self.uf}"

class Usuario(AbstractUser):
    unidade = models.ForeignKey(UnidadeEmpresarial, on_delete=models.SET_NULL, null=True, blank=True)


class PontoMonitoramento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    classificacao = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    zona_utm = models.CharField(max_length=50)
    unidade_empresarial = models.ForeignKey(UnidadeEmpresarial, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome


class Relatorio(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.ForeignKey(UnidadeEmpresarial, on_delete=models.CASCADE, null=True, blank=True)
    revisao = models.CharField(max_length=50)
    data = models.DateField()
    inserido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name='relatorios_inseridos'
    )

    def __str__(self):
        return self.nome


class MonitoramentoEfluente(models.Model):
    parametro = models.ForeignKey(Parametro, on_delete=models.CASCADE)
    unidade_empresarial = models.ForeignKey(UnidadeEmpresarial, on_delete=models.CASCADE, null=True, blank=True)
    ponto_monitorado = models.ForeignKey(PontoMonitoramento, on_delete=models.CASCADE)
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE, null=True, blank=True)
    data_medicao = models.DateField()
    resultado = models.FloatField()
    conformidade = models.CharField(max_length=20, choices=[('Conforme', 'Conforme'), ('Não Conforme', 'Não Conforme')])
    justificativa = models.TextField(blank=True, null=True)
    tipo_efluente = models.CharField(max_length=100, null=True, blank=True)
    inserido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='efluentes_inseridos'
    )

    def save(self, *args, **kwargs):
        if self.parametro and self.resultado is not None:
            if self.resultado <= self.parametro.limite_aceitavel:
                self.conformidade = 'Conforme'
            else:
                self.conformidade = 'Não Conforme'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parametro.nome} - {self.data_medicao}"


class ListaPresenca(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=50)
    inserido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name='presenca_inseridos'
    )

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"


class EducacaoAmbiental(models.Model):
    tema = models.CharField(max_length=100)
    atividade = models.TextField()
    data_planejada = models.DateField()
    data_executada = models.DateField()
    unidade_empresarial = models.ForeignKey(UnidadeEmpresarial, on_delete=models.CASCADE, null=True, blank=True)
    total_participantes = models.IntegerField()
    lista_presenca = models.ForeignKey(ListaPresenca, on_delete=models.CASCADE, null=True, blank=True)
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE, null=True, blank=True)
    inserido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name='educacao_inseridos'
    )

    def __str__(self):
        return self.tema


class ControleResiduo(models.Model):
    codigo_residuo = models.CharField(max_length=100)
    unidade_empresarial = models.ForeignKey(UnidadeEmpresarial, on_delete=models.CASCADE, null=True, blank=True)
    nome_residuo = models.CharField(max_length=100)
    data_emissao = models.DateField(null=True, blank=True)
    armazenagem_temporaria = models.CharField(max_length=200, null=True, blank=True)
    disposicao_final = models.CharField(max_length=200, null=True, blank=True)
    transportador = models.CharField(max_length=100, null=True, blank=True)
    receptor_residuo = models.CharField(max_length=100, null=True, blank=True)
    mtr = models.CharField(max_length=100, null=True, blank=True)
    cdf = models.CharField(max_length=100, null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE, null=True, blank=True)
    inserido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name='resiuo_inseridos'
    )


    def __str__(self):
        return self.nome_residuo
