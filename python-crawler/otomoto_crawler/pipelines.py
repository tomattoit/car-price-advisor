# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import os

import psycopg2


class OtomotoCrawlerPipeline:
    def __init__(self):
        db_params = {
            "host": os.environ["POSTGRES_SERVICE"],
            "port": 5432,
            "user": os.environ["POSTGRES_USER"],
            "password": os.environ["POSTGRES_PASSWORD"],
            "database": os.environ["POSTGRES_DB"],
        }
        self.conn = psycopg2.connect(**db_params)
        self.cur = self.conn.cursor()

        # @TODO: remove create table to postgres init script in k8s
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cars (
                id SERIAL PRIMARY KEY,
                brand VARCHAR(255),
                year INTEGER,
                mileage INTEGER,
                capacity INTEGER,
                horse_power INTEGER,
                fuel_type VARCHAR(255),
                transmission VARCHAR(255),
                number_of_doors INTEGER,
                origin_country VARCHAR(255),
                color VARCHAR(255),
                no_accidents BOOLEAN,
                aso BOOLEAN,
                is_used BOOLEAN,
                price INTEGER NOT NULL
            )
        """
        )

    def _process_binary_features(self, item, features):
        for feature_name, feature_true in features:
            if feature_name not in item:
                continue
            item[feature_name] = item[feature_name] == feature_true

    def _process_numeric_features(self, item, features):
        for feature in features:
            if feature not in item:
                continue
            numeric_string = re.search(r"^(\d+)", item[feature].replace(" ", ""))
            item[feature] = int(numeric_string.group(0)) if numeric_string else None

    def _save_item_to_db(self, item, spider):
        not_null_fields = [field for field in item.fields if item[field] != "None"]
        # check if item exists in db
        self.cur.execute(
            f"""
            SELECT id FROM cars WHERE {' AND '.join([f'{field}=%s' for field in not_null_fields])}
        """,
            [item[field] for field in not_null_fields],
        )
        result = self.cur.fetchone()

        if result:
            spider.logger.info("This item already exists in db.")
            return

        self.cur.execute(
            f"""
            INSERT INTO cars ({', '.join(not_null_fields)}) VALUES ({', '.join(['%s'] * len(not_null_fields))})
        """,
            [item[field] for field in not_null_fields],
        )
        self.conn.commit()

    def process_item(self, item, spider):
        self._process_binary_features(
            item,
            [("no_accidents", "Tak"), ("aso", "Tak"), ("is_used", "Używane")],
        )
        self._process_numeric_features(
            item,
            [
                "price",
                "year",
                "mileage",
                "capacity",
                "horse_power",
                "number_of_doors",
            ],
        )

        for field in item.fields:
            item.setdefault(field, "None")

        self._save_item_to_db(item, spider)

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
