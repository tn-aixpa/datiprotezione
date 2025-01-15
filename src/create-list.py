
import requests
import pandas as pd
from deep_translator import GoogleTranslator
import json

# translation
translator = GoogleTranslator(source='it', target='en')
def translate_text(text):
    if text is not None:
        text = str(text)
        text = translator.translate(str(text))
    return text

def givemelink(x):
    datakeywords = ['siat','urbanistica-dati','catasto']
    urlitems = []
    rd = x
    if isinstance(x, list):
        for urlist in x:
            for datakey in datakeywords:
                if datakey.lower() in urlist.lower():
                    urlitems = urlist.split("||")
                    break
    else:
        urlitems = x.split("||")
    
    for urlitem in urlitems:
        for datakey in datakeywords:
            if datakey.lower() in urlitem.lower():
                rd = urlitem
                break

    return(rd.replace("||",""))

def create_list(project): #context
    start = 1
    to = 20
    maxPageSize = 100
    url = "https://siat.provincia.tn.it/geonetwork/srv/ita/q?_content_type=json&any=&bucket=s101&facet.q=&fast=index&from=START&resultType=details&sortBy=relevance&sortOrder=&to=TO" 
    url = url.replace("START",str(start)).replace("TO",str(to))
    response = requests.get(url)
    data = response.json()
    start = int(data['@from'])
    to = int(data['@to'])
    total = int(data['summary']['@count'])
    rest = total % maxPageSize
    steps = (total - rest) / 100    
    
    dfs = []
    for start in range(int(steps)):
        start = 1 + start * 100
        to = start + 100 -1
        url = "https://siat.provincia.tn.it/geonetwork/srv/ita/q?_content_type=json&any=&bucket=s101&facet.q=&fast=index&from=START&resultType=details&sortBy=relevance&sortOrder=&to=TO" 
        url = url.replace("START",str(start)).replace("TO",str(to))
        response = requests.get(url)
        data = response.json()
        records = data.get('metadata', [])
        df = pd.DataFrame(records)
        dfs.append(df)
    
    start = to +1
    to = start + rest -1
    url = "https://siat.provincia.tn.it/geonetwork/srv/ita/q?_content_type=json&any=&bucket=s101&facet.q=&fast=index&from=START&resultType=details&sortBy=relevance&sortOrder=&to=TO" 
    url = url.replace("START",str(start)).replace("TO",str(to))
    response = requests.get(url)
    data = response.json()
    records = data.get('metadata', [])
    df = pd.DataFrame(records)
    dfs.append(df)
    
    # create a dataset with all the entries
    siatdata = pd.concat(dfs, ignore_index=True)
    # because these kind of attributes contain in some cases list I extract only the first value
    # (change it if you want have more information)
    siatdata['type'] = siatdata['type'].apply(lambda x: x[0] if isinstance(x, list) else x) 
    siatdata['identifier'] = siatdata['identifier'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    siatdata['format'] = siatdata['format'].apply(lambda x: x[0] if isinstance(x, list) else x)    
    
    siatdata['link'] = siatdata['link'].apply(givemelink)
    
    data = siatdata[['title','abstract','lineage','resourceConstraints','type',
          'legalConstraints','identifier',"crsDetails","maintenanceAndUpdateFrequency_text",
          'spatialRepresentationType_text','denominator',
          'tempExtentBegin','tempExtentEnd','serviceType',
          'updateFrequency','revisionDate','classification_text','defaultTitle',
          'publicationDate','creationDate','crs',"parentId",'link']]
    
    data['title_en'] = data['defaultTitle'].apply(translate_text)
    
    project.log_dataitem("siat_trentino", data=data, kind='table', index=False)
