# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import subprocess
import os


class MyPipeline(object):
    
    def process_item(self, item, spider):

        # Agregar la ruta del proyecto al PYTHONPATH
        project_path = 'C:/Users/Guadalupe/OneDrive/Escritorio/impactia-main/impactia-main/impactia/impactia'
        os.environ['PYTHONPATH'] = f'{project_path};{os.environ.get("PYTHONPATH", "")}'

        # Ejecutar el spider
        spider_process = subprocess.Popen(['scrapy', 'crawl', 'tenders', '-a', f'start_url={item["url"]}'])
        spider_process.communicate()  # Esperar a que el proceso del spider termine
        #print('hhhhhhhhhhhhhhhhh')
        
        # Ejecutar el proceso ETL
        etl_process = subprocess.Popen(['python3', 'etl.py'])
        etl_process.communicate()  # Esperar a que el proceso ETL termine
        
        return item
