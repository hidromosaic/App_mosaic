import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
from django_plotly_dash import DjangoDash
from monitor.models import EfluentesLiquidos

app = DjangoDash("DashboardApp")

app.layout = html.Div([
    dcc.Store(id='unidade-store'),
    dcc.Dropdown(id='parametro-dropdown', placeholder='Selecione o parâmetro'),
    dcc.Graph(id='grafico-efluentes')
])

# Inicializa os parâmetros assim que a unidade for carregada
@app.callback(
    Output('parametro-dropdown', 'options'),
    Input('unidade-store', 'data')
)
def atualizar_parametros(unidade_id):
    if not unidade_id:
        return []
    parametros = (
        EfluentesLiquidos.objects
        .filter(unidade_empresarial_id=unidade_id)
        .values_list('parametro', flat=True)
        .distinct()
    )
    return [{'label': p, 'value': p} for p in parametros if p]

# Atualiza gráfico com base no parâmetro selecionado
@app.callback(
    Output('grafico-efluentes', 'figure'),
    Input('parametro-dropdown', 'value'),
    State('unidade-store', 'data')
)
def atualizar_grafico(parametro, unidade_id):
    if not parametro or not unidade_id:
        return px.line(title="Nenhum dado disponível")

    dados = EfluentesLiquidos.objects.filter(
        parametro=parametro,
        unidade_empresarial_id=unidade_id
    ).values('ponto_monitorado__nome', 'data_medicao', 'resultado')

    if not dados:
        return px.line(title="Sem dados para o parâmetro selecionado")

    import pandas as pd
    df = pd.DataFrame(dados)
    fig = px.line(df, x='data_medicao', y='resultado', color='ponto_monitorado__nome', markers=True)
    fig.update_layout(title=f"Efluentes Líquidos - Parâmetro: {parametro}")
    return fig
