from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    UnidadeMedicao, Parametro, UnidadeEmpresarial, PontoMonitoramento, Usuario,
    Residuos, Relatorio, EfluentesLiquidos, Emissoes, Ruidos, ListaPresenca,
    EducacaoAmbiental, ControleResiduo, Tratamento, Classificacao
)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Informações Adicionais", {
            "fields": ("unidade",),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações Adicionais", {
            "fields": ("unidade",),
        }),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "listar_unidades")
    search_fields = ("username", "email", "unidade__unidade")

    def listar_unidades(self, obj):
        return ", ".join([str(u) for u in obj.unidade.all()])
    listar_unidades.short_description = "Unidades"

class MonitoramentosAdmin(admin.ModelAdmin):
    list_display = ('ponto_monitorado', 'data_medicao', 'parametro', 'resultado', 'inserido_por')
    readonly_fields = ('inserido_por',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # novo registro
            obj.inserido_por = request.user
        elif not obj.inserido_por:  # edição de algo criado via shell/admin sem usuário
            obj.inserido_por = request.user
        super().save_model(request, obj, form, change)




admin.site.register(UnidadeMedicao)
admin.site.register(Parametro)
admin.site.register(UnidadeEmpresarial)
admin.site.register(PontoMonitoramento)
admin.site.register(Relatorio)
admin.site.register(EfluentesLiquidos, MonitoramentosAdmin)
admin.site.register(Emissoes, MonitoramentosAdmin)
admin.site.register(Ruidos, MonitoramentosAdmin)
admin.site.register(ListaPresenca)
admin.site.register(EducacaoAmbiental)
admin.site.register(ControleResiduo)
admin.site.register(Residuos)
admin.site.register(Tratamento)
admin.site.register(Classificacao)
