from django.core.management.base import BaseCommand
from monitor.models import (
    UnidadeMedicao,
    UnidadeEmpresarial,
    Parametro,
    PontoMonitoramento,
    EfluentesLiquidos,
    Emissoes,
    Ruidos,
)
import pandas as pd

class Command(BaseCommand):
    help = 'Importa dados ambientais a partir de um arquivo Excel'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Caminho para o arquivo Excel')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Leitura dos dados
        self.stdout.write('Lendo planilhas do Excel...')
        uni_medicao = pd.read_excel(file_path, sheet_name='Unidade medicaos')
        uni_empresa = pd.read_excel(file_path, sheet_name='Unidade empresarials')
        para = pd.read_excel(file_path, sheet_name='Parametros')
        pt_monitoramentos = pd.read_excel(file_path, sheet_name='Ponto monitoramentos')
        moni_eflu = pd.read_excel(file_path, sheet_name='Efluentes liquidos')
        moni_emi = pd.read_excel(file_path, sheet_name='Emissoes')
        moni_ruido = pd.read_excel(file_path, sheet_name='Ruidos')

        self.stdout.write('Importando Unidade de Medição...')
        for _, row in uni_medicao.iterrows():
            UnidadeMedicao.objects.get_or_create(
                nome=row['Nome'],
                sigla=row['Sigla'],
            )

        self.stdout.write('Importando Unidade Empresarial...')
        for _, row in uni_empresa.iterrows():
            UnidadeEmpresarial.objects.get_or_create(
                unidade=row['Unidade'],
                uf=row['Uf'],
                codigo=row['Codigo'],
            )

        self.stdout.write('Importando Parâmetros...')
        for _, row in para.iterrows():
            unidade_med = UnidadeMedicao.objects.get(nome=row['Unidade medicao'])
            Parametro.objects.get_or_create(
                nome=row['Nome'],
                limite_aceitavel=row['Limite aceitavel'],
                unidade_medicao=unidade_med,
                requisito=row['Requisito'],
                periodicidade=row['Periodicidade'],
            )

        self.stdout.write('Importando Pontos de Monitoramento...')
        for _, row in pt_monitoramentos.iterrows():
            unidade_emp = UnidadeEmpresarial.objects.get(unidade=row['Unidade empresarial'])
            PontoMonitoramento.objects.get_or_create(
                nome=row['Nome'],
                descricao=row['Descricao'],
                classificacao=row['Classificacao'],
                latitude=row['Latitude'],
                longitude=row['Longitude'],
                zona_utm=row['Zona utm'],
                unidade_empresarial=unidade_emp,
            )

        def buscar_relacionamentos(row):
            try:
                parametro = Parametro.objects.get(nome=row['Parametro'])
                unidade = UnidadeEmpresarial.objects.get(unidade=row['Unidade empresarial'])
                ponto = PontoMonitoramento.objects.filter(
                    nome=row['Ponto monitorado'],
                    unidade_empresarial=unidade,

                ).first()
                if not ponto:
                    self.stdout.write(self.style.WARNING(
                        f"Ponto não encontrado: '{row['Ponto monitorado']}' "
                    ))
                return parametro, unidade, ponto
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao buscar dados relacionados: {e}'))
                return None, None, None

        self.stdout.write('Importando Efluentes Líquidos...')
        for _, row in moni_eflu.iterrows():
            parametro, unidade, ponto = buscar_relacionamentos(row)
            if ponto:
                EfluentesLiquidos.objects.create(
                    parametro=parametro,
                    unidade_empresarial=unidade,
                    ponto_monitorado=ponto,
                    data_medicao=row['Data medicao'],
                    resultado=row['Resultado'],
                    tipo_efluente=row['Tipo efluente'],
                    justificativa=row['Justificativa'],
                )

        self.stdout.write('Importando Emissões...')
        for _, row in moni_emi.iterrows():
            parametro, unidade, ponto = buscar_relacionamentos(row)
            if ponto:
                Emissoes.objects.create(
                    parametro=parametro,
                    unidade_empresarial=unidade,
                    ponto_monitorado=ponto,
                    data_medicao=row['Data medicao'],
                    resultado=row['Resultado'],
                    tipo_emissao=row['Tipo emissoes'],
                    justificativa=row['Justificativa'],
                )

        self.stdout.write('Importando Ruídos...')
        for _, row in moni_ruido.iterrows():
            parametro, unidade, ponto = buscar_relacionamentos(row)
            if ponto:
                Ruidos.objects.create(
                    parametro=parametro,
                    unidade_empresarial=unidade,
                    ponto_monitorado=ponto,
                    data_medicao=row['Data medicao'],
                    resultado=row['Resultado'],
                    tipo_ruido=row['Tipo ruido'],
                    justificativa=row['Justificativa'],
                )

        self.stdout.write(self.style.SUCCESS('✅ Dados importados com sucesso!'))
