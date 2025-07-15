from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import plotly.express as px
import pandas as pd
from monitor.models import EfluentesLiquidos, Emissoes, Ruidos
from django.db.models import QuerySet

app = DjangoDash('dashboard_monitoramento', external_stylesheets=[dbc.themes.BOOTSTRAP])

def get_df_from_model(model: QuerySet, tipo_nome: str) -> pd.DataFrame:
    queryset = model.objects.select_related('ponto_monitorado')
    data = list(queryset.values(
        'ponto_monitorado__nome',
        'data_medicao',
        'parametro',
        'resultado',
        'ponto_monitorado__latitude',
        'ponto_monitorado__longitude'
    ))
    df = pd.DataFrame(data)
    if not df.empty:
        df["tipo"] = tipo_nome
    return df

def create_layout():
    # Carregar dados de todos os modelos
    df_efluentes = get_df_from_model(EfluentesLiquidos, "Efluentes Líquidos")
    df_emissoes = get_df_from_model(Emissoes, "Emissões Atmosféricas")
    df_rios = get_df_from_model(Ruidos, "Ruídos")

    # Concatenar todos os DataFrames
    df = pd.concat([df_efluentes, df_emissoes, df_rios], ignore_index=True)

    if df.empty:
        return html.Div("Nenhum dado disponível.")

    # Gráfico de linha
    fig_linha = px.line(df, x='data_medicao', y='resultado', color='ponto_monitorado__nome', line_dash='tipo',
                        title='Tendência dos Resultados por Tipo')

    # Gráfico de barras (médias por ponto)
    df_medias = df.groupby(['ponto_monitorado__nome', 'tipo'])['resultado'].mean().reset_index()
    fig_barras = px.bar(df_medias, x='ponto_monitorado__nome', y='resultado', color='tipo',
                        title='Média de Resultados por Ponto e Tipo')

    # Mapa dos pontos monitorados
    df_mapa = df.drop_duplicates(['ponto_monitorado__nome', 'tipo'])
    fig_mapa = px.scatter_mapbox(
        df_mapa,
        lat='ponto_monitorado__latitude',
        lon='ponto_monitorado__longitude',
        hover_name='ponto_monitorado__nome',
        color='tipo',
        zoom=10
    )
    fig_mapa.update_layout(mapbox_style="open-street-map")
    fig_mapa.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Layout completo
    return html.Div([
        html.H2("Dashboard de Monitoramento Ambiental", style={"textAlign": "center", "margin": "40px 0"}),

        html.H4("Histórico de cada ponto monitorado", style={"margin": "20px 0"}),
        dcc.Graph(figure=fig_linha, style={"height": "600px", "width": "100%"}),

        html.H4("Gráfico de barra das médias em cada ponto", style={"margin": "40px 0 20px"}),
        dcc.Graph(figure=fig_barras, style={"height": "600px", "width": "100%"}),

        html.H4("Mapa dos Pontos de Monitoramento", style={"margin": "40px 0 20px"}),
        dcc.Graph(figure=fig_mapa, style={"height": "600px", "width": "100%"}),

        html.H4("Tabela de Dados Monitorados", style={"margin": "40px 0 20px"}),
        dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            filter_action='native',
            sort_action='native',
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        )
    ], style={"padding": "0px", "margin": "0px"})

app.layout = create_layout()
