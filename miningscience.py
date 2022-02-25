
import re
import csv 
from Bio import SeqIO
import pandas as pd 
from Bio import Entrez
import re
from collections 
import Counter

def download_pubmed(keyword): 
   
    Entrez.email = 'jefferson.sanchez@est.ikiam.edu.ec'
    handle = Entrez.esearch(db = 'pubmed', term= keyword + "[title/abstract]", usehistory = 'y')
    record = Entrez.read(handle)
    id_list = record['IdList']
    print('El número de artículos es:')
    print(record['Count'])

    
def mining_pubs(tipo):
   
    with open("E2_ExamenParcial_Python/pubmed-ferrooxida.txt", errors="ignore") as f: 
        texto = f.read() 
    if tipo == "DP":
        PMID = re.findall("PMID- (\d*)", texto) 
        year = re.findall("DP\s{2}-\s(\d{4})", texto)
        pmid_y = pd.DataFrame()
        pmid_y["PMID"] = PMID
        pmid_y["Año"] = year
        return (pmid_y)
    elif tipo == "AU": 
        PMID = re.findall("PMID- (\d*)", texto) 
        autores = texto.split("PMID- ")
        autores.pop(0)
        num_autores = []
        for i in range(len(autores)):
            numero = re.findall("AU -", autores[i])
            n = (len(numero))
            num_autores.append(n)
        pmid_a = pd.DataFrame()
        pmid_a["PMID"] = PMID 
        pmid_a["Numero de autores"] = num_autores
        return (pmid_a)
    elif tipo == "AD": 
        texto = re.sub(r" [A-Z]{1}\.","", texto)
        texto = re.sub(r"Av\.","", texto)
        texto = re.sub(r"Vic\.","", texto)
        texto = re.sub(r"Tas\.","", texto)
        AD = texto.split("AD  - ")
        n_paises = []
        for i in range(len(AD)): 
            pais = re.findall("\S, ([A-Za-z]*)\.", AD[i])
            if not pais == []: 
                if not len(pais) >= 2:  
                    if re.findall("^[A-Z]", pais[0]): 
                        n_paises.append(pais[0])
        conteo=Counter(n_paises)
        resultado = {}
        for clave in conteo:
            valor = conteo[clave]
            if valor != 1: 
                resultado[clave] = valor 
        numero_pais = pd.DataFrame()
        numero_pais["pais"] = resultado.keys()
        numero_pais["cuantos autores"] = resultado.values()
        return (numero_pais)


    