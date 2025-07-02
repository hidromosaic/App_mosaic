from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import plotly.express as px
import pandas as pd
from monitor.models import MonitoramentoEfluente
from pyproj import Transformer
from django_pandas.io import read_frame

app = DjangoDash('dashboard_monitoramento', external_stylesheets=[dbc.themes.BOOTSTRAP])

def create_layout():
    # Carregar dados
    queryset = MonitoramentoEfluente.objects.select_related('ponto_monitorado')
    df = read_frame(queryset, fieldnames=['ponto_monitorado__nome', 'data_medicao', 'parametro', 'resultado', 'ponto_monitorado__latitude', 'ponto_monitorado__longitude'])

    if df.empty:
        return html.Div("Nenhum dado disponível.")

    # Gráfico de linha
    fig_linha = px.line(df, x='data_medicao', y='resultado', color='ponto_monitorado__nome', title='Tendência dos Resultados')

    # Gráfico de barras (médias por ponto)
    df_medias = df.groupby('ponto_monitorado__nome')['resultado'].mean().reset_index()
    fig_barras = px.bar(df_medias, x='ponto_monitorado__nome', y='resultado', title='Média de Resultados por Ponto')

    # Mapa (Plotly scatter mapbox)
    fig_mapa = px.scatter_mapbox(
        df.drop_duplicates('ponto_monitorado__nome'),
        lat='ponto_monitorado__latitude',
        lon='ponto_monitorado__longitude',
        hover_name='ponto_monitorado__nome',
        zoom=10
    )
    fig_mapa.update_layout(mapbox_style="open-street-map")
    fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return dbc.Container([
        dbc.Row(dbc.Col(html.H2("Dashboard de Monitoramento de Efluentes", className="text-center my-4"))),

        dbc.Row([dbc.Col(dcc.Graph(figure=fig_linha), md=12)], className="mb-4"),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_barras), md=12)], className="mb-4"),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_mapa), md=12)], className="mb-4"),

        dbc.Row(dbc.Col(html.H4("Tabela de Dados Monitorados", className="my-3"))),

        dbc.Row([
            dbc.Col(
                dash_table.DataTable(
                    columns=[{'name': col, 'id': col} for col in df.columns],
                    data=df.to_dict('records'),
                    page_size=10,
                    filter_action='native',
                    sort_action='native',
                    style_table={'overflowX': 'auto', 'maxHeight': '500px', 'overflowY': 'scroll'},
                    style_cell={'textAlign': 'left', 'padding': '5px'},
                    style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                ),
                width=12
            )
        ], className="mb-5"),
    ], fluid=True)

app.layout = create_layout
