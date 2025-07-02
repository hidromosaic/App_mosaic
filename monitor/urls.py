from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.listar_monitoramentos), name='listar_monitoramentos'),
    path('novo/', login_required(views.adicionar_monitoramento), name='adicionar_monitoramento'),
    path('editar/<int:pk>/', login_required(views.editar_monitoramento), name='editar_monitoramento'),
    path('excluir/<int:pk>/', login_required(views.excluir_monitoramento), name='excluir_monitoramento'),

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
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
