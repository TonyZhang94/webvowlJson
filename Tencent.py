# -*- coding:utf-8 -*-


# import psycopg2 as psycopg2
import tushare as ts
import sqlalchemy as sa
import pandas as pd


# # config for Tencent
ENGINE = "postgresql"
HOST = "postgres-lkr70ecv.gz.cdb.myqcloud.com"
PORT = "62"
USER = "zczx_admin"
PASS = "zczx112211"
DB = "fact_library"


dynamic_ip = "125.120.144.72"

# # 外网访问99
Outer_DB99 = {
    "HOST": dynamic_ip,
    "PORT": 28943,
    "USER": 'zczx_write',
    "PASS": 'zczxTech2012',
    "DB": {
        "standard_library": 'standard_library',
        "fact_library": 'fact_library',
        "zhuican_web": 'zhuican_web',
        "raw_mj_category": "raw_mj_category",
        "report_dg": "report_dg",
        "raw_tb_comment_notag": "raw_tb_comment_notag",
    },
}

DBDefault = Outer_DB99


class Tencent:
    def __init__(self):
        self.engine = sa.create_engine('{}://{}:{}@{}:{}/{}'.format(ENGINE, USER, PASS, HOST, PORT, DB))

    def get_model_infos(self, pcid="4", cid="50012097", datamonth="201709"):
        schema = "fact_model_pcid" + pcid
        table = schema + ".cid" + cid
        # pgSQL = "SELECT * FROM {} where datamonth = '{}' LIMIT 1".format(table, datamonth)
        # pgSQL = "SELECT * FROM {} where datamonth = '{}' LIMIT 10".format(table, datamonth)
        pgSQL = "SELECT * FROM {} where datamonth = '{}'".format(table, datamonth)
        df = pd.read_sql_query(pgSQL, self.engine)

        return df

    def get_model_submarkets(self, pcid="4", cid="50012097", datamonth="201709"):
        schema = "fact_model_submarket"
        table = schema + ".pcid" + pcid
        pgSQL = "SELECT * FROM {} where cid = '{}' and datamonth='{}'".format(table, cid, datamonth)
        df = pd.read_sql_query(pgSQL, self.engine)

        return df

    @staticmethod
    def get_99_engine(db):
        engine = sa.create_engine("postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}".
                                  format(USER=DBDefault["USER"], PASS=DBDefault["PASS"], HOST=DBDefault["HOST"],
                                         PORT=DBDefault["PORT"], DB=DBDefault["DB"][db]))
        return engine

    def get_rank(self, pcid="4", cid="50012097", datamonth="201805"):
        sql = (
            "SELECT model, brand, model_rank, biz30day, total_sold_price FROM product_brain.product_brain_pcid{}"
            " WHERE datamonth = '{}'"
        ).format(pcid, datamonth)
        engine = self.get_99_engine("report_dg")
        df = pd.read_sql_query(sql, engine)
        df = df.drop_duplicates(["brand", "model"])
        return df, len(df)

    def process(self):
        pass

    def start(self):
        self.process()


if __name__ == '__main__':
    obj = Tencent()
    obj.start()
