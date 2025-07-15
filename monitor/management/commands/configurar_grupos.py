from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from monitor.models import EfluentesLiquidos, Emissoes, Ruidos

class Command(BaseCommand):
    help = 'Cria grupos Técnicos e Gerenciadores com permissões apropriadas'

    def handle(self, *args, **kwargs):
        tecnico_group, _ = Group.objects.get_or_create(name='Tecnico')
        gerenciador_group, _ = Group.objects.get_or_create(name='Gerenciador')

        modelos = [EfluentesLiquidos, Emissoes, Ruidos]

        # Limpa permissões anteriores
        tecnico_group.permissions.clear()
        gerenciador_group.permissions.clear()

        for modelo in modelos:
            content_type = ContentType.objects.get_for_model(modelo)

            add_perm = Permission.objects.get(codename=f'add_{modelo.__name__.lower()}', content_type=content_type)
            change_perm = Permission.objects.get(codename=f'change_{modelo.__name__.lower()}', content_type=content_type)
            delete_perm = Permission.objects.get(codename=f'delete_{modelo.__name__.lower()}', content_type=content_type)
            view_perm = Permission.objects.get(codename=f'view_{modelo.__name__.lower()}', content_type=content_type)

            # Técnicos podem adicionar e visualizar
            tecnico_group.permissions.add(add_perm, view_perm)

            # Gerenciadores podem tudo
            gerenciador_group.permissions.add(add_perm, change_perm, delete_perm, view_perm)

        self.stdout.write(self.style.SUCCESS('Grupos e permissões configurados com sucesso.'))
