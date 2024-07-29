
import geopandas
import mlrun
import os

@mlrun.handler()
def convert_list(context, list: mlrun.DataItem):
    data = list.as_df()
    data = data.to_dict(orient='records')
    for index, item in enumerate(data):
        name = item['title_en']
        context.logger.info(f"Converting {name} to parquet (link {item['link']})")
        try:
            gdf = geopandas.read_file(item['link'])
        except:
            context.logger.error(f"Error reading file: {item['link']}")
            continue
        # convert name to lower case and replace spaces with underscores
        name = name.lower().replace(" ", "_")
        gdf.to_parquet('./'+name+'.parquet')
        with open('./'+name+'.parquet', 'rb') as in_file:
            content = in_file.read()
            context.log_artifact(name, body=content, format="parquet", db_key=name)
            os.remove('./'+name+'.parquet')
