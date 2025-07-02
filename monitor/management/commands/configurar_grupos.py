from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from monitor.models import MonitoramentoEfluente

class Command(BaseCommand):
    help = 'Cria grupos Técnicos e Gerenciadores com permissões apropriadas'

    def handle(self, *args, **kwargs):
        tecnico_group, _ = Group.objects.get_or_create(name='Tecnico')
        gerenciador_group, _ = Group.objects.get_or_create(name='Gerenciador')

        content_type = ContentType.objects.get_for_model(MonitoramentoEfluente)

        # Permissões padrão
        add_perm = Permission.objects.get(codename='add_monitoramentoefluente', content_type=content_type)
        change_perm = Permission.objects.get(codename='change_monitoramentoefluente', content_type=content_type)
        delete_perm = Permission.objects.get(codename='delete_monitoramentoefluente', content_type=content_type)
        view_perm = Permission.objects.get(codename='view_monitoramentoefluente', content_type=content_type)

        tecnico_group.permissions.set([add_perm, view_perm])
        gerenciador_group.permissions.set([add_perm, change_perm, delete_perm, view_perm])

        self.stdout.write(self.style.SUCCESS('Grupos e permissões configurados com sucesso.'))
