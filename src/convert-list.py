
# import geopandas
import os
import urllib.request
import pandas as pd

# def read_geopandas(name, url, project):
#     gdf = geopandas.read_file(url)
#     gdf.to_parquet('./'+name+'.parquet')
#     with open('./'+name+'.parquet', 'rb') as in_file:
#         content = in_file.read()
#         project.log_dataitem(name=name, kind="table", data=content)
#         os.remove('./'+name+'.parquet')
        

def read_file(name, url, project):
    # get extension from url
    extension = url.split(".")[-1]
    path = f"./{name}.{extension}"
    urllib.request.urlretrieve(url, path)
    project.log_artifact(name=name, kind="artifact", source=path)
    os.remove(path)
 
def convert_list(project, list):
    data = list.as_df()
    data = data.to_dict(orient='records')
    error_data = []
    for index, item in enumerate(data): # after [:180],last 200 items [-200:]
        name = item['title_en']
        link = item['link']
        print(f"Converting {name} to artifact (link {link})")
        # convert name to lower case and replace spaces with underscores
        name = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        if link.endswith(".zip"):
            # try:
                # read_geopandas(name, link, project)
            # except Exception as e: 
                # print(f"{type(e).__name__} was raised")
                try:
                    # os.remove('./'+name+'.parquet')
                    # print(f"Retrying {name} to save as artifact({link})")
                    read_file(name, link, project)
                except:
                    print(f"Error reading file: {item['link']}")                    
                    continue
        elif link.endswith(".png"):
            try:
                read_file(name, link, project)
            except:
                print(f"Error reading file: {item['link']}")
                continue
        else:    
            print(f"Error reading file: {item['link']}")
            error_data.append(item)

    project.log_dataitem(name="error_data", kind="table", data=pd.DataFrame(error_data))
