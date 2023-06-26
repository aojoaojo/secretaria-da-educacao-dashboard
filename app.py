from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# Inicializando app OK
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Mudando as cores OK
colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}

#importando dados OK
caminho_arquivo = "sedfevasao.csv"
dados = pd.read_csv(caminho_arquivo, sep=";")
data = pd.read_csv('CoordenadasEscolas2.csv')

#limpando dados OK
dadosLimpos = dados[dados['turma'].isna() == False]
dadosLimpos['coordenacao_regional'] = dadosLimpos['coordenacao_regional'].str[6:]
pd.DataFrame(dadosLimpos)

# mapa OK

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
                      'zoom': 9.4,
                      'center':{"lat": -15.793845, "lon": -47.882740},
                      'style': "open-street-map"},
                  width=600,
                  height=400)

# gráfico pizza situação alunos todas escolas OK com botão dropdown na frente do título

fig2 = px.pie(dadosLimpos, "situacao", title = 'Situação dos Alunos por Escola')

# botão dropdown OK

listaDropdown = list(dadosLimpos['escola'].unique())
listaDropdown.append("Todas as Escolas")

# Número de Alunos por região OK

dadosLimpos['cod_aluno'] = pd.to_numeric(dadosLimpos['cod_aluno'], errors='coerce')
students_by_region = dadosLimpos.groupby('coordenacao_regional')['cod_aluno'].count().reset_index(name='num_alunos')
fig3 = px.bar(students_by_region, x='coordenacao_regional', y='num_alunos', title='Número de Alunos por Região DF', color='coordenacao_regional', labels={
                     "coordenacao_regional": "Regiões (DF)",
                     "num_alunos": "Número de Alunos"
                 },)
fig3.update_layout(showlegend=False)

# Restaurar dadosLimpos OK

dadosLimpos = dados[dados['turma'].isna() == False]
dadosLimpos['coordenacao_regional'] = dadosLimpos['coordenacao_regional'].str[6:]
pd.DataFrame(dadosLimpos)

# Número de Escolas por região OK

schools_by_region = dadosLimpos.groupby('coordenacao_regional')['cod_escola'].nunique().reset_index(name='num_escolas')

fig4 = px.bar(schools_by_region, x='coordenacao_regional', y='num_escolas', title='Número de Escolas por Região DF', color = 'coordenacao_regional', labels={
                     "coordenacao_regional": "Regiões (DF)",
                     "num_escolas": "Número de Escolas"
                 },)
fig4.update_layout(showlegend=False)

# Região mais reprovados OK

regiaoMaisReprovados = dadosLimpos[dadosLimpos['situacao'] == 'reprovado']

fig5 = px.histogram(regiaoMaisReprovados, 'coordenacao_regional', color = 'coordenacao_regional', title = 'Alunos reprovados por região', labels={
                     "coordenacao_regional": "Regiões (DF)"
                 },)
fig5.update_layout(showlegend=False, yaxis_title="Alunos Reprovados")

# Porcentagem de reprovação por região OK

todosAlunos = dadosLimpos.groupby('coordenacao_regional').count()['cod_aluno']
alunosReprovados = regiaoMaisReprovados.groupby('coordenacao_regional').count()['cod_aluno']
porcentagemReprovacao =  (alunosReprovados * 100) / todosAlunos
df6 = pd.DataFrame({'regiao': porcentagemReprovacao.index, 'porcentagem': porcentagemReprovacao.values})
fig6 = px.histogram(df6, x='regiao', y='porcentagem', color = 'porcentagem', title = 'Porcentagem de reprovação por região').update_xaxes(categoryorder='total descending')
fig6.update_layout(showlegend=False, xaxis_title="Regiões (DF)", yaxis_title="Porcentagem de Reprovados")

# Média de alunos por escola OK

todosAlunos = dadosLimpos.groupby('coordenacao_regional').count()['cod_aluno']
escolasPorRegiao = dadosLimpos.groupby('coordenacao_regional')['cod_escola'].nunique()
mediaAlunoEscola = todosAlunos/escolasPorRegiao
df7 = pd.DataFrame({'regiao': mediaAlunoEscola.index, 'mediaAlunosEscola': mediaAlunoEscola.values})
fig7 = px.histogram(df7, 'regiao', 'mediaAlunosEscola', color = 'mediaAlunosEscola', title = 'Média de Alunos por Escola por Região').update_xaxes(categoryorder='total descending')
fig7.update_layout(showlegend=False, xaxis_title="Regiões (DF)", yaxis_title="Média de Alunos por Escola")

# Aplicação OK

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
            id='numAlunosRegiao',
            figure=fig3
        )], width=6),
        
        dbc.Col([
            dcc.Graph(
            id='numEscolasRegiao',
            figure=fig4
        )], width=6),
        
        dbc.Col([
            dcc.Graph(
            id='mapa',
            figure=fig
        )], width=6),
        
        dbc.Col([
            dcc.Graph(
            id='RegiaoMaisReprovados',
            figure=fig5
        )], width=12),
        
        dbc.Col([
            dcc.Graph(
            id='MediaAlunosEscola',
            figure=fig7
        )], width=6),
        
        dbc.Col([
            dcc.Graph(
            id='ReprovacaoPorRegiao',
            figure=fig6
        )], width=6),
        
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