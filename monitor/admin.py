from django.contrib import admin
from .models import (
    UnidadeMedicao, Parametro, UnidadeEmpresarial, PontoMonitoramento,
    Relatorio, MonitoramentoEfluente, ListaPresenca, EducacaoAmbiental, ControleResiduo
)

admin.site.register(UnidadeMedicao)
admin.site.register(Parametro)
admin.site.register(UnidadeEmpresarial)
admin.site.register(PontoMonitoramento)
admin.site.register(Relatorio)
admin.site.register(MonitoramentoEfluente)
admin.site.register(ListaPresenca)
admin.site.register(EducacaoAmbiental)
admin.site.register(ControleResiduo)
