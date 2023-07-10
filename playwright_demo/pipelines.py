# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from mdutils.mdutils import MdUtils
from mdutils import Html
import pandas as pd
import os

db_file = 'db.csv'

class PlaywrightDemoPipeline(object):

    def open_spider(self, spider):
        self.mdFile = MdUtils(file_name='Recent Article',title='Recent Article')
        if os.path.exists(db_file):
            with open(db_file, 'r') as f:
                self.db = f.read().splitlines()
                print(self.db)
        else:
            self.db = []

    def close_spider(self, spider):
        self.mdFile.create_md_file()
        with open(db_file, 'w') as f:
            for doi in self.db:
                f.write(f"{doi}\n")

    def process_item(self, item, spider):
        self.mdFile.new_header(level=2, title=item['title'], add_table_of_contents="n")
        self.mdFile.new_line(item['author'], bold_italics_code='cib', align='center')
        self.mdFile.new_paragraph(item['content'], bold_italics_code='bi', color='purple')
        self.mdFile.new_paragraph(Html.image(path=item['toc_figure'], size='x300', align='center'))
        self.mdFile.new_line('')
        self.mdFile.new_line(' - ' + self.mdFile.new_inline_link(text='doi link', link=item['doi']))
        self.mdFile.new_line('')
        if item['doi'] not in self.db:
            # save item to my database
            self.db.append(item['doi'])
        else:
            print("already in database.")

        return item