from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    UnidadeMedicao, Parametro, UnidadeEmpresarial, PontoMonitoramento, Usuario,
    Relatorio, MonitoramentoEfluente, ListaPresenca, EducacaoAmbiental, ControleResiduo
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
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "unidade")
    search_fields = ("username", "email", "unidade__nome")

class MonitoramentoEfluenteAdmin(admin.ModelAdmin):
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
admin.site.register(MonitoramentoEfluente, MonitoramentoEfluenteAdmin)
admin.site.register(ListaPresenca)
admin.site.register(EducacaoAmbiental)
admin.site.register(ControleResiduo)
