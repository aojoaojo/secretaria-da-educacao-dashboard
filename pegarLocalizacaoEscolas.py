import requests
from ast import literal_eval
import pandas as pd

dados = pd.read_csv("sedfevasao.csv", sep= ';')
dadosLimpos = dados[dados['turma'].isna() == False]
pd.DataFrame(dadosLimpos)

URL_BASE = "https://www.google.com:443/s?tbm=map&suggest=p&gs_ri=maps&psi=1VSUZMTPN8ic5OUP1J-wsA0.1687442660200.1&gl=br&hl=pt-BR&authuser=0&q={}&ech=18&pb=!2i11!4m12!1m3!1d3339.870684154478!2d-47.88062422554191!3d-15.759002384876451!2m3!1f0!2f0!3f0!3m2!1i1294!2i668!4f13.1!7i20!10b1!12m17!1m1!18b1!2m3!5m1!6e2!20e3!10b1!12b1!13b1!16b1!17m1!3e1!20m4!5e2!6b1!8b1!14b1!19m4!2m3!1i360!2i120!4i8!20m57!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!22m3!1s1VSUZMTPN8ic5OUP1J-wsA0!7e81!17s1VSUZMTPN8ic5OUP1J-wsA0%3A152!23m2!4b1!10b1!24m81!1m29!13m9!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!25b1!18m18!3b1!4b1!5b1!6b1!9b1!12b1!13b1!14b1!15b1!17b1!20b1!21b1!22b0!25b1!27m1!1b0!28b0!30b0!2b1!5m5!2b1!5b1!6b1!7b1!10b1!10m1!8e3!11m1!3e1!14m1!3b1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!29b1!30m1!2b1!36b1!39m3!2m2!2i1!3i1!43b1!52b1!54m1!1b1!55b1!56m2!1b1!3b1!65m5!3m4!1m3!1m2!1i224!2i298!71b1!72m4!1m2!3b1!5b1!4b1!89b1!103b1!113b1!26m4!2m3!1i80!2i92!4i8!34m18!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!37m1!1e81!47m0!49m6!3b1!6m2!1b1!2b1!7m1!1e3!67m2!7b1!10b1!69i651"
headers = {"User-Agent": "Urubu do Pix", "Accept": "*/*", "Referer": "https://www.google.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}

escolas_infos = []
for i, escola in enumerate(dadosLimpos["escola"].unique()):
    print(f'-> {i:3d} - {escola}')
    # url encode espaços
    req = requests.get(URL_BASE.format(escola + ', Brasilia, DF'), headers=headers)
    conteudo = req.text.split('\n')[1].replace('null', 'None')
    # Transforma o conteúdo tratado em uma lista
    try:
        L = literal_eval(conteudo)
        endereco_completo = L[0][1][0][22][2][0]
        _, _, latitude, longitude = L[0][1][0][22][11]
    except:
        endereco_completo = None
        latitude, longitude = None, None
    escolas_infos.append([escola, latitude, longitude])

    print(f'       - Endereço: {endereco_completo}')
    print(f'       - Coordenadas: {latitude}, {longitude}')

df = pd.DataFrame(escolas_infos)
df.to_csv('CoordenadasEscolas.csv')