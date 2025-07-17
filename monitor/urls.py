from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #Efluentes Liquidos
    path('efluentes/', login_required(views.listar_efluentes), name='listar_efluentes'),
    path('efluentes/novo/', login_required(views.adicionar_efluente_liquido), name='adicionar_efluente_liquido'),
    path('efluentes/editar/<int:pk>/', login_required(views.editar_efluente_liquido), name='editar_efluente_liquido'),
    path('efluentes/excluir/<int:pk>/', login_required(views.excluir_efluente_liquido), name='excluir_efluente_liquido'),

    #Emissões Atmosfericas
    path('emissoes/', login_required(views.listar_emissoes), name='listar_emissoes'),
    path('emissoes/novo/', login_required(views.adicionar_emissoes), name='adicionar_emissoes'),
    path('emissoes/editar/<int:pk>/', login_required(views.editar_emissoes), name='editar_emissoes'),
    path('emissoes/excluir/<int:pk>/', login_required(views.excluir_emissoes), name='excluir_emissoes'),

    #Ruídos
    path('ruidos/', login_required(views.listar_ruidos), name='listar_ruidos'),
    path('ruidos/novo/', login_required(views.adicionar_ruido), name='adicionar_ruido'),
    path('ruidos/editar/<int:pk>/', login_required(views.editar_ruido), name='editar_ruido'),
    path('ruidos/excluir/<int:pk>/', login_required(views.excluir_ruidos), name='excluir_ruidos'),

    # Educação Ambiental
    path('educacao/', views.listar_educacao, name='listar_educacao'),
    path('educacao/novo/', views.adicionar_educacao, name='adicionar_educacao'),
    path('educacao/editar/<int:pk>/', views.editar_educacao, name='editar_educacao'),
    path('educacao/excluir/<int:pk>/', views.excluir_educacao, name='excluir_educacao'),

    # Controle de Resíduos
    path('residuos/', views.listar_residuos, name='listar_residuos'),
    path('residuos/novo/', views.adicionar_residuo, name='adicionar_residuo'),
    path('residuos/editar/<int:pk>/', views.editar_residuo, name='editar_residuo'),
    path('residuos/excluir/<int:pk>/', views.excluir_residuo, name='excluir_residuo'),

    # Lista de Presença
    path('presencas/', views.listar_presencas, name='listar_presencas'),
    path('presencas/novo/', views.adicionar_presenca, name='adicionar_presenca'),
    path('presencas/editar/<int:pk>/', views.editar_presenca, name='editar_presenca'),
    path('presencas/excluir/<int:pk>/', views.excluir_presenca, name='excluir_presenca'),

    # Relatórios
    path('relatorios/', views.listar_relatorios, name='listar_relatorios'),
    path('relatorios/novo/', views.adicionar_relatorio, name='adicionar_relatorio'),
    path('relatorios/editar/<int:pk>/', views.editar_relatorio, name='editar_relatorio'),
    path('relatorios/excluir/<int:pk>/', views.excluir_relatorio, name='excluir_relatorio'),

    #dashboard
    #path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
