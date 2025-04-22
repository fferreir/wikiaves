#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from lxml import etree
import pandas as pd
from tqdm import tqdm

id_min = 1
id_max = 6804287 #21/04/2025 20:22


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
for i in tqdm(range(id_min, id_max)):
    url = f"https://www.wikiaves.com.br/{i}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    dom = etree.HTML(str(soup))
    if dom.xpath('/html/body/div/div[1]/div/div[1]/div[2]/text()'):
        pass
    else:
        id.append(i)
        for div in soup.find_all('div', class_='wa-lista-detalhes'):
            paragraph = div.find('p')
            a_tag = paragraph.find('a')
            if a_tag:
                nome_comum.append(a_tag.text.strip())
            i_tag = paragraph.find('i')
            if i_tag:
                nome_cientifico.append(i_tag.text.strip())
        for div in soup.find_all('div'):
            label = div.find('label')
            if label and label.get_text(strip=True) == 'Município:':
                a_tag = div.find('a')
                if a_tag:
                    mun = a_tag.text.strip()
                    cod_mun = a_tag.get('href')
        municipio.append(mun)
        if '=' in cod_mun:
            codigo = cod_mun.split('=')[1]
        elif '_' in cod_mun:
            codigo = cod_mun.split('_')[1]
        cod_municipio.append(codigo)
        for div in soup.find_all('div'):
            label = div.find('label')
            if label and ((label.get_text(strip=True) == 'Feita em:') or (label.get_text(strip=True) == 'Gravado em:')):
                contents = label.find_all_next(string=True)
                data_registro.append(contents[1])

dados = pd.DataFrame({'id': id,
                      'nome comum': nome_comum,
                      'nome cientfico': nome_cientifico,
                      'município': municipio,
                      'código municipio': cod_municipio,
                      'data do registro': data_registro})
dados['data do registro'] = pd.to_datetime(dados['data do registro'])
dados.to_csv('dados.csv', index=False)

