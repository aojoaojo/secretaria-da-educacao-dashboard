from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# Inicializando app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Mudando as cores
colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}

#importando dados
caminho_arquivo = "sedfevasao.csv"
dados = pd.read_csv(caminho_arquivo, sep=";")
data = pd.read_csv('CoordenadasEscolas2.csv')

#limpando dados
dadosLimpos = dados[dados['turma'].isna() == False]
dadosLimpos['coordenacao_regional'] = dadosLimpos['coordenacao_regional'].str[6:]
pd.DataFrame(dadosLimpos)


#dados.info()
#linhas_vazias = dados[dados['cod_turma'].isnull()]

# Há 41645 linhas com valores faltantes, no entanto, para a criação do dashboard,
# esses valores não são tão relevantes. Portanto, prefere-se nesse caso,
# continuar com as linhas com os valores 
# faltantes, não realizando um "dados = dados.drop(linhas_vazias,index)"

# mapa inicio

df = pd.DataFrame(data ,columns=["0","1","2"])

fig = go.Figure()
fig.add_trace(go.Scattermapbox(
    mode = "markers",
    lat = df['1'].tolist(),
    lon = df['2'].tolist(),
    hovertext = df['0'].tolist(),
    marker = {'color': "red",
              "size": 5},
))
fig.update_layout(margin ={'l':0,'t':0,'b':0,'r':0},
                  mapbox = {
                      'zoom': 9.8,
                      'center':{"lat": -15.793845, "lon": -47.882740},
                      'style': "open-street-map"}
                  )

# mapa fim

# gráfico pizza situação alunos todas escolas inicio

fig2 = px.pie(dadosLimpos, "situacao")

# gráfico pizza situação alunos todas escolas fim

# botão dropdown inicio

listaDropdown = list(dadosLimpos['escola'].unique())
listaDropdown.append("Todas as Escolas")

# botão dropdown fim

# Número de Alunos por região inicio

fig3 = px.histogram(dadosLimpos, x = 'coordenacao_regional', color = 'coordenacao_regional', title = 'Número de Alunos por Região', labels = {'coordenacao_regional': 'Regiões do DF', 'count': 'Número de Alunos'})

# Número de Alunos por região fim

# Número de Escolas por região início

escolas_por_regiao = dadosLimpos.groupby('coordenacao_regional')['escola'].count().reset_index()
escolas_por_regiao.columns = ['coordenacao_regional', 'quantidade']

fig4 = dadosLimpos.groupby('escola')['coordenacao_regional'].max().reset_index().value_counts("coordenacao_regional").plot.barh()

## antiga fig4 px.histogram(escolas_por_regiao, x = 'coordenacao_regional', y = 'quantidade', color = 'coordenacao_regional', title = 'Número de Escolas por Região (errado)')

# Número de escolas por região fim

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1(children='Escolas Públicas do Distrito Federal em 2016', style={'textAlign': 'center'}),
            html.H3(children='Este dashboard apresenta insights sobre as escolas públicas do DF.', style={'textAlign': 'center'})
        ], width=12)
    ]),

    dbc.Row([
        
        dbc.Col([
            dcc.Dropdown(listaDropdown, value='Todas as Escolas', id='lista_escolas'),
            dcc.Graph(
            id='graficoDePizza',
            figure=fig2
        )], width=6),
        
        dbc.Col([
            dcc.Graph(
            id='mapa',
            figure=fig
        )], width=6),
        
        dbc.Col([
            dcc.Graph(
            id='numAlunosRegiao',
            figure=fig3
        )], width=6),
        
        dbc.Col([
            dcc.Graph(
            id='numEscolasRegiao',
            figure=fig4
        )], width=6)
        
    ])
])

@app.callback(
    Output('graficoDePizza', 'figure'),
    Input('lista_escolas', 'value')
)
def update_output(value):
    if value == 'Todas as Escolas':
        fig2 = px.pie(dadosLimpos, "situacao")
    else:
        tabelaFiltrada = dadosLimpos.loc[dadosLimpos["escola"] == value,:]
        fig2 = px.pie(tabelaFiltrada, "situacao")
    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)