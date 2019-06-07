# -*- coding:utf-8 -*-
import time

import Tencent
import dbGraph

label_version = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


class Process():
    def __init__(self):
        self.Tencent = Tencent.Tencent()
        self.dbGraph = dbGraph.DBGraph()

    def link_pcid_cid(self, pcid, cid):
        pcid_node = self.dbGraph.insert_node("pcid", "pcid"+pcid)
        cid_node = self.dbGraph.insert_node("cid", "cid"+cid)
        self.dbGraph.build_relation(pcid_node, cid_node, "has_cid", "belong_pcid")

        return cid_node

    def link_cid_model(self, cid_node, models):
        models_nodes = []
        inx = 0
        for index, row in models.iterrows():
            model_node = self.dbGraph.insert_node(row["model"], row["model"] + "//" + row["brand"],
                                                   [{"key": "title", "value": row["title"]},
                                                    {"key": "url", "value": row["url"]},
                                                    {"key": "imageurl", "value": row["imageurl"]},
                                                    {"key": row["datamonth"] + "_biz30day", "value": row["biz30day"]},
                                                    {"key": row["datamonth"] + "_total_sold_price", "value": row["total_sold_price"]}])
            models_nodes.append(model_node)
            self.dbGraph.build_relation(cid_node, model_node, "has_model", "belong_cid")

            inx += 1
            print "insert model nodes: " + str(inx)

        return models_nodes

    def link_model_brand(self, model_nodes, models):
        inx = 0
        for index, row in models.iterrows():
            model_node = model_nodes[inx]
            brand = row["brand"]
            brand_node = self.dbGraph.insert_node("brand", brand)
            self.dbGraph.build_relation(model_node, brand_node, "brand_is", "has_model")

            inx += 1
            print "insert brand nodes: " + str(inx)

    def link_itemid_sales(self, itemid_nodes, infos):
        inx = 0
        for itemid, info in infos.iterrows():
            itemid_node = itemid_nodes[inx]
            biz30day = info["biz30day"]
            total_sold_price = info["total_sold_price"]
            sales_node = self.dbGraph.insert_node("sales_" + str(itemid), "sales",
                                                   [{"key": info["datamonth"]+"_biz30day", "value": biz30day},
                                                    {"key": info["datamonth"]+"_total_sold_price", "value": total_sold_price}])
            self.dbGraph.build_relation(itemid_node, sales_node, "its_sales", "whos_sales")

            inx += 1
            print "insert sales nodes: " + str(inx)

    def link_model_submarket(self, model_nodes, infos, submarkets, cid):
        models = infos["model"].values
        inx = 0
        for model in models:
            model_node = model_nodes[inx]
            try:
                info = submarkets[submarkets["model"] == model]
            except:
                print "submarket lack model: " + str(model)
                inx += 1
                print "insert submarket nodes: " + str(inx)
                continue
            try:
                for x, submarket in info.iterrows():
                    break
            except:
                print "submarket exception"
                submarket = info
                submarket_node = self.dbGraph.find_node("submarket_" + submarket["submarket"], "cid", str(cid))
                if submarket_node is None:
                    submarket_node = self.dbGraph.insert_node("submarket_" + submarket["submarket"],
                                                              submarket["submarket"],
                                                              [{"key": "sm_id", "value": submarket["sm_id"]},
                                                               {"key": "cid", "value": str(cid)}])
                self.dbGraph.build_relation(model_node, submarket_node, "belong_submarket", "has_model")
                inx += 1
                print "insert submarket nodes: " + str(inx)
                continue

            for x, submarket in info.iterrows():
                submarket_node = self.dbGraph.find_node("submarket_" + submarket["submarket"], "cid", str(cid))
                if submarket_node is None:
                    submarket_node = self.dbGraph.insert_node("submarket_" + submarket["submarket"], submarket["submarket"],
                                                              [{"key": "sm_id", "value": submarket["sm_id"]},
                                                               {"key": "cid", "value": str(cid)}])
                self.dbGraph.build_relation(model_node, submarket_node, "belong_submarket", "has_model")

            inx += 1
            print "insert submarket nodes: " + str(inx)

    def link_itemid_brand_model(self, itemid_nodes, infos, brand_models, cid):
        itemids = infos.index
        brand_model_nodes = dict()
        inx = 0
        for itemid in itemids:
            itemid_node = itemid_nodes[inx]
            try:
                brand_model = brand_models.loc[itemid]
            except:
                print "brand-model lack itemid: " + str(itemid)
                inx += 1
                print "insert brand-model nodes: " + str(inx)
                continue
            brand_model_node = self.dbGraph.find_node(brand_model["model"] + brand_model["brand"], "cid", str(cid))
            if brand_model_node is None:
                brand_model_node = self.dbGraph.insert_node(brand_model["model"] + brand_model["brand"],
                                                            brand_model["model"],
                                                            [{"key": "brand", "value": brand_model["brand"]},
                                                             {"key": "cid", "value": str(cid)},
                                                             {"key": "status", "value": str(brand_model["status"])}])
            self.dbGraph.build_relation(itemid_node, brand_model_node, "belong_model", "has_itemid")
            brand_model_nodes[str(itemid)] = brand_model_node
            inx += 1
            print "insert brand-model nodes: " + str(inx)

        return brand_model_nodes

    # Index([u'datamonth', u'brand', u'biz30day', u'total_sold_price', u'price',
    #        u'aver_price', u'score', u'sellernick', u'title', u'url', u'imageurl',
    #        u'model', u'power', u'liner_material', u'operation_mode',
    #        u'speed_adjustment', u'cup_material', u'applicable_number',
    #        u'cooking_function', u'body_material', u'type', u'speed', u'function',
    #        u'capacity', u'feed_opening_shape'],
    #       dtype='object')
    def link_model_sku(self, model_nodes, models, cid):
        sku_list = ["power", "liner_material", "operation_mode", "speed_adjustment", "cup_material",
                    "applicable_number", "cooking_function", "body_material", "type", "speed", "function",
                    "capacity", "feed_opening_shape"]
        inx = 0
        for itemid, info in models.iterrows():
            itemid_node = model_nodes[inx]
            for sku in sku_list:
                if 0 == len(info[sku]):
                    continue
                if "function" == sku:
                    funcs = info[sku].split(",")
                    for func in funcs:
                        sku_node = self.dbGraph.find_node("sku_" + sku + ":" + func, "cid", str(cid))
                        if sku_node is None:
                            sku_node = self.dbGraph.insert_node("sku_" + sku + ":" + func, "func:" + func,
                                                                [{"key": "cid", "value": str(cid)},
                                                                 {"key": "sku", "value": func}])
                        self.dbGraph.build_relation(itemid_node, sku_node, sku, "has_model")
                        # try:
                        #     self.dbGraph.build_relation(brand_model_nodes[str(itemid)], sku_node, "its_sku", "has_model")
                        # except:
                        #     pass
                else:
                    sku_node = self.dbGraph.find_node("sku_" + sku + ":" + info[sku], "cid", str(cid))
                    if sku_node is None:
                        sku_node = self.dbGraph.insert_node("sku_" + sku + ":" + info[sku], info[sku],
                                                            [{"key": "cid", "value": str(cid)},
                                                             {"key": "sku", "value": info[sku]}])
                    self.dbGraph.build_relation(itemid_node, sku_node, sku, "has_model")
                    # try:
                    #     self.dbGraph.build_relation(brand_model_nodes[str(itemid)], sku_node, "its_sku", "has_model")
                    # except:
                    #     pass

            inx += 1
            print "insert sku nodes: " + str(inx)

    def process(self):
        pcid = "4"
        cid = "50012097"
        datamonth = "201709"

        cid_node = self.link_pcid_cid(pcid, cid)

        models = self.Tencent.get_model_infos(pcid, cid, datamonth)
        # models = models.sort_values(by="biz30day", ascending=True).tail(10)
        model_nodes = self.link_cid_model(cid_node, models)

        # brand
        self.link_model_brand(model_nodes, models)

        # # sales
        # self.link_itemid_sales(itemid_nodes, infos)

        # # submarket
        submarkets = self.Tencent.get_model_submarkets(pcid, cid)
        self.link_model_submarket(model_nodes, models, submarkets, cid)
        #
        # # brand_model
        # # Index([u'cid', u'model', u'brand', u'status'], dtype='object')
        # brand_models = self.db99.get_brand_model(pcid, cid)
        # brand_model_nodes = self.link_itemid_brand_model(itemid_nodes, infos, brand_models, cid)

        # # skus
        self.link_model_sku(model_nodes, models, cid)

    def start(self):
        self.process()


if __name__ == '__main__':
    obj = Process()
    obj.start()
