# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from web_app.models import Keyword

# database information
host = os.environ.get('DB_HOST', 'localhost')
port = os.environ.get('DB_PORT', 5432)
user = os.environ.get('DB_USER', 'postgres')
password = os.environ.get('DB_PASSWORD', 'rootpass')
database = os.environ.get('DB_NAME', 'rank-search')
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
Session = sessionmaker(bind = engine)
session = Session()


class RankPipeline:
    def process_item(self, item, spider):
        keyword = session.query(Keyword).filter_by(id=item['id']).first()
        if not keyword:
            return item
        if item['error'] != '':
            keyword['error_code'] = 1
        elif keyword.target_site in item['url']:
            keyword.rank = item['rank']
            keyword.url = item['url']
            keyword.last_update = datetime.datetime.now()
        else:
            return item
        session.commit()
        
        return item
