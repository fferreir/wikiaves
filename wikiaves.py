#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from lxml import etree
from datetime import datetime
import pandas as pd

id_min = 1
id_max = 8#6802457


headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'pt-BR,pt;q=0.5'
}
id = []
nome_comum = []
nome_cientifico = []
municipio = []
cod_municipio = []
data_registro = []
for i in range(id_min, id_max):
    url = f"https://www.wikiaves.com.br/{i}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    dom = etree.HTML(str(soup))
    if dom.xpath('/html/body/div/div[1]/div/div[1]/div[2]/text()'):
        pass
    else:
        id.append(i)
        nome_comum.append(dom.xpath('/html/body/div[1]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/p/a[1]/text()')[0])
        nome_cientifico.append(dom.xpath('/html/body/div[1]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/p/a[3]/i[1]/text()')[0])
        municipio.append(dom.xpath('/html/body/div[1]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[7]/div[2]/div/a[1]/text()')[0])
        cod_mun = dom.xpath('/html/body/div[1]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[7]/div[2]/div/a')[0]
        if '=' in cod_mun.get('href'):
            codigo = cod_mun.get('href').split('=')[1]
        elif '_' in cod_mun.get('href'):
            codigo = cod_mun.get('href').split('_')[1]
        cod_municipio.append(codigo)
        data_registro.append(dom.xpath('/html/body/div[1]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[8]/text()')[0])
dados = pd.DataFrame({'id': id,
                      'nome comum': nome_comum,
                      'nome cientfico': nome_cientifico,
                      'município': municipio,
                      'código municipio': cod_municipio,
                      'data do regristro': data_registro})
dados.to_csv('dados.csv', index=False)

