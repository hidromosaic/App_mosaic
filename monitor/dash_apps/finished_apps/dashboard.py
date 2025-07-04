import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
from monitor.models import MonitoramentoEfluente

# Coleta os dados
def get_data():
    dados = MonitoramentoEfluente.objects.all().values('ponto_monitorado__nome', 'data_coleta', 'ph', 'dbo', 'dq0')
    df = pd.DataFrame(dados)
    return df

app = DjangoDash('DashboardEfluente')

df = get_data()

app.layout = html.Div([
    html.H2("Dashboard - Parâmetros de Efluentes"),
    dcc.Dropdown(
        id='parametro',
        options=[
            {'label': 'pH', 'value': 'ph'},
            {'label': 'DBO', 'value': 'dbo'},
            {'label': 'DQO', 'value': 'dq0'}
        ],
        value='ph'
    ),
    dcc.Graph(id='grafico-parametro')
])

@app.callback(
    Output('grafico-parametro', 'figure'),
    [Input('parametro', 'value')]
)
def atualizar_grafico(parametro):
    df = get_data()
    fig = px.line(df, x='data_coleta', y=parametro, color='ponto_monitorado__nome', markers=True)
    return fig
