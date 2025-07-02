import pandas as pd
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'App_Mosaic.settings')
django.setup()

from monitor.models import MonitoramentoEfluente, Parametro, UnidadeEmpresarial, PontoMonitorado, UnidadeMedicao

# gerando os dataframes
uni_medicao = pd.read_excel('import_data/dados_efluentes.xlsx', sheet_name='Unidade medicaos')
uni_empresa = pd.read_excel('import_data/dados_efluentes.xlsx', sheet_name='Unidade empresarials')
para = pd.read_excel('import_data/dados_efluentes.xlsx', sheet_name='Parametro')
pt_monitoramentos = pd.read_excel('import_data/dados_efluentes.xlsx', sheet_name='Ponto monitoramentos')
moni_eflu = pd.read_excel('import_data/dados_efluentes.xlsx', sheet_name='Monitoramento efluentes')


for _, row in uni_medicao.iterrows():
    UnidadeMedicao.objects.create(
        nome=row['Nome'],
        sigla=row['Sigla'],
    )

for _, row in uni_empresa.iterrows():
    UnidadeEmpresarial.objects.create(
        unidade=row['Unidade'],
        uf=row['Uf'],
        codigo=row['Codigo'],
    )

for _, row in para.iterrows():
    unidade_med = UnidadeMedicao.objects.get(nome=row['Unidade medicao'])
    Parametro.objects.create(
        nome=row['Nome'],
        limite_aceitavel=row['Limite aceitavel'],
        unidade_medicao=unidade_med,
        categoria=row['Catgoria'],
        requisito=row['Requisito'],
        periodicidade=row['Periodicidade'],
    )

for _, row in pt_monitoramentos.iterrows():
    unidade_emp = UnidadeEmpresarial.objects.get(nome=row['Unidade empresarial'])
    PontoMonitoramento.objects.create(
        nome=row['Nome'],
        descricao=row['Descricao'],
        classificacao=row['classificacao'],
        latitude=row['Latitude'],
        longitude=row['Longitude'],
        zona_utm=row['Zona utm'],
        unidade_empresarial=unidade_emp,
    )

for _, row in moni_eflu.interrows():
    parametro = Parametro.objects.get(nome=row['Parametro'])
    unidade = UnidadeEmpresarial.objects.get(nome=row['Unidade empresarial'])
    ponto = PontoMonitorado.objects.get(nome=row['Ponto monitorado'])

    MonitoramentoEfluente.objects.create(
        parametro=parametro,
        unidade_empresarial=unidade,
        ponto_monitorado=ponto,
        data_medicao=row['Data medicao'],
        resultado=row['Resultado'],
    )
