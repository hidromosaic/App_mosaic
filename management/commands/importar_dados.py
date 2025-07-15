import pandas as pd
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'App_Mosaic.settings')
django.setup()

from monitor.models import EfluentesLiquidos, Emissoes, Ruidos, Parametro, UnidadeEmpresarial, PontoMonitoramento, UnidadeMedicao

# gerando os dataframes
arquivo = 'import_data/dados_efluentes.xlsx'
uni_medicao = pd.read_excel(arquivo, sheet_name='Unidade medicaos')
uni_empresa = pd.read_excel(arquivo, sheet_name='Unidade empresarials')
para = pd.read_excel(arquivo, sheet_name='Parametro')
pt_monitoramentos = pd.read_excel(arquivo, sheet_name='Ponto monitoramentos')
moni_eflu = pd.read_excel(arquivo, sheet_name='Efluentes liquidos')
moni_ruido = pd.read_excel(arquivo, sheet_name='Ruidos')
moni_emi = pd.read_excel(arquivo, sheet_name='Emissoes')

# Cadastro das tabelas auxiliares
for _, row in uni_medicao.iterrows():
    UnidadeMedicao.objects.get_or_create(
        nome=row['Nome'],
        sigla=row['Sigla']
    )

for _, row in uni_empresa.iterrows():
    UnidadeEmpresarial.objects.get_or_create(
        unidade=row['Unidade'],
        uf=row['Uf'],
        codigo=row['Codigo']
    )

for _, row in para.iterrows():
    unidade_med = UnidadeMedicao.objects.get(nome=row['Unidade medicao'])
    Parametro.objects.get_or_create(
        nome=row['Nome'],
        limite_aceitavel=row['Limite aceitavel'],
        unidade_medicao=unidade_med,
        categoria=row['Catgoria'],
        requisito=row['Requisito'],
        periodicidade=row['Periodicidade']
    )

for _, row in pt_monitoramentos.iterrows():
    unidade_emp = UnidadeEmpresarial.objects.get(unidade=row['Unidade empresarial'])
    PontoMonitoramento.objects.get_or_create(
        nome=row['Nome'],
        descricao=row['Descricao'],
        classificacao=row['classificacao'],
        latitude=row['Latitude'],
        longitude=row['Longitude'],
        zona_utm=row['Zona utm'],
        unidade_empresarial=unidade_emp
    )

# Efluentes Líquidos
for _, row in moni_eflu.iterrows():
    parametro = Parametro.objects.get(nome=row['Parametro'])
    unidade = UnidadeEmpresarial.objects.get(unidade=row['Unidade empresarial'])
    ponto = PontoMonitoramento.objects.get(nome=row['Ponto monitorado'])

    EfluentesLiquidos.objects.create(
        tipo_efluente=row['Tipo efluente'],
        parametro=parametro,
        unidade_empresarial=unidade,
        ponto_monitorado=ponto,
        data_medicao=row['Data medicao'],
        resultado=row['Resultado']
    )

# Ruídos
for _, row in moni_ruido.iterrows():
    parametro = Parametro.objects.get(nome=row['Parametro'])
    unidade = UnidadeEmpresarial.objects.get(unidade=row['Unidade empresarial'])
    ponto = PontoMonitoramento.objects.get(nome=row['Ponto monitorado'])

    Ruidos.objects.create(
        tipo_ruido=row['Tipo ruido'],
        parametro=parametro,
        unidade_empresarial=unidade,
        ponto_monitorado=ponto,
        data_medicao=row['Data medicao'],
        resultado=row['Resultado']
    )

# Emissões
for _, row in moni_emi.iterrows():
    parametro = Parametro.objects.get(nome=row['Parametro'])
    unidade = UnidadeEmpresarial.objects.get(unidade=row['Unidade empresarial'])
    ponto = PontoMonitoramento.objects.get(nome=row['Ponto monitorado'])

    Emissoes.objects.create(
        tipo_emissoes=row['Tipo emissoes'],
        parametro=parametro,
        unidade_empresarial=unidade,
        ponto_monitorado=ponto,
        data_medicao=row['Data medicao'],
        resultado=row['Resultado']
    )
