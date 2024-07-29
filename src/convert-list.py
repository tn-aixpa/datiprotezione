
import geopandas
import mlrun
import os
import urllib.request
import pandas as pd

def read_geopandas(name, url, context):
    gdf = geopandas.read_file(url)
    gdf.to_parquet('./'+name+'.parquet')
    with open('./'+name+'.parquet', 'rb') as in_file:
        content = in_file.read()
        context.log_artifact(name, body=content, format="parquet", db_key=name)
        os.remove('./'+name+'.parquet')

def read_file(name, url, context):
    # get extension from url
    extension = url.split(".")[-1]
    urllib.request.urlretrieve(url, f"./{name}.{extension}")
    with open(f"./{name}.{extension}", "rb") as in_file:
        content = in_file.read()
        context.log_artifact(name, body=content, format=extension, db_key=name)
        os.remove(f"./{name}.{extension}")
        
@mlrun.handler()
def convert_list(context, list: mlrun.DataItem):
    data = list.as_df()
    data = data.to_dict(orient='records')
    error_data = []
    for index, item in enumerate(data):
        name = item['title_en']
        link = item['link']
        context.logger.info(f"Converting {name} to parquet (link {link})")
        # convert name to lower case and replace spaces with underscores
        name = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        if link.endswith(".zip"):
            try:
                read_geopandas(name, link, context)
            except:
                try:
                    read_file(name, link, context)
                except:
                    context.logger.error(f"Error reading file: {item['link']}")
                    continue
        elif link.endswith(".png"):
            try:
                read_file(name, link, context)
            except:
                context.logger.error(f"Error reading file: {item['link']}")
                continue
        else:    
            context.logger.error(f"Error reading file: {item['link']}")
            error_data.append(item)
            continue

    context.log_dataset("error_data", df=pd.DataFrame(error_data), index=False)
