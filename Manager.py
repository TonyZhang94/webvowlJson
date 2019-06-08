# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import copy
import _pickle as pickle

from webvowlJson.WebJson import *


"""
说明：
1. base_path 在http://139.199.159.124上要指向/var/www/html/showgraph
2. 由于我的脚本是被调用的，可能打开文件路径会有影响。会受影响的函数有：
（1）Manager().get_info()，两处open
（2）WebJson().store()，第一处open
（3）WebJson().merge_css()，第二第三处open
（4）WebJson.py 中 css_appendix 变量
其中（2）（3）（4）设置的路径是一样的

"""


class Manager(object):
    def __init__(self, limit=100, sort_key="total_sold_price", file="datum",
                 base_path="G:\zjDetect\webvowl\\"):
        self.webjson = WebJson()
        self.webjson.classid = 0
        self.webjson.propertyid = 0

        self.limit = limit
        self.sort_key = sort_key
        self.file = file
        self.base_path = base_path

    def get_info(self):
        with open("interface/ret1.pkl", mode="rb") as fp:
            data = pickle.load(fp)

        with open("interface/ret2.pkl", mode="rb") as fp:
            attrs = pickle.load(fp)

        return data, attrs

    def make(self, models, submarkets):
        data = self.webjson.init_json()

        data["class"] = list()
        data["classAttribute"] = list()
        data["property"] = list()
        data["propertyAttribute"] = list()
        classidcid = dict()
        classidmodel = dict()
        classidbrand = dict()
        classidsubmarket = dict()
        classidpower = dict()
        classidspeedad = dict()
        classidcup = dict()
        classidspeed = dict()
        classidfunction = dict()
        classidcapacity = dict()

        # classid, idjson, attrjson = self.webjson.make_class(0, "料理机50012097")
        # data["class"].append(idjson)
        # data["classAttribute"].append(attrjson)
        # classidcid["50012097"] = classid

        # model
        for index, row in models.iterrows():
            description = "total_sold_price: {}; biz30day: {}; aver_price: {}; rank: {}; total: {}" \
                .format(str(row["total_sold_price"]), str(row["biz30day"]),
                        str(row["aver_price"]), str(row["rank"]), str(row["total"]))
            rank, total = row["rank"], row["total"]
            classid, idjson, attrjson = self.webjson.make_class(1, row["model"], description=description, color=0,
                                                                rank=rank, total=total)
            data["class"].append(idjson)
            data["classAttribute"].append(attrjson)
            classidmodel[row["model"]+row["brand"]] = classid

            # idjson, attrjson = self.webjson.make_property(0, "model", classid, classidcid["50012097"])
            # data["property"].append(idjson)
            # data["propertyAttribute"].append(attrjson)

        # brand
        for index, row in models.iterrows():
            if row["brand"] == "" or row["brand"] is None:
                continue
            if row["brand"] not in classidbrand:
                classid, idjson, attrjson = self.webjson.make_class(2, row["brand"], color=1)
                data["class"].append(idjson)
                data["classAttribute"].append(attrjson)
                classidbrand[row["brand"]] = classid

            idjson, attrjson = self.webjson.make_property(1, "brand", classidbrand[row["brand"]], classidmodel[row["model"]+row["brand"]])
            data["property"].append(idjson)
            data["propertyAttribute"].append(attrjson)

        # submarket
        for index, row in models.iterrows():
            submarket = submarkets[(submarkets['model'] == row["model"]) & (submarkets['brand'] == row["brand"])]
            if submarket.size == 0:
                continue
            for iindex, irow in submarket.iterrows():
                if irow["submarket"] not in classidsubmarket:
                    classid, idjson, attrjson = self.webjson.make_class(3, irow["submarket"], color=2)
                    data["class"].append(idjson)
                    data["classAttribute"].append(attrjson)
                    classidsubmarket[irow["submarket"]] = classid

                idjson, attrjson = self.webjson.make_property(2, "submarket", classidsubmarket[irow["submarket"]],
                                                              classidmodel[row["model"]+row["brand"]])
                data["property"].append(idjson)
                data["propertyAttribute"].append(attrjson)

        # power
        for index, row in models.iterrows():
            if row["power"] == "" or row["power"] is None:
                continue
            if row["power"] not in classidpower:
                classid, idjson, attrjson = self.webjson.make_class(4, row["power"], color=3)
                data["class"].append(idjson)
                data["classAttribute"].append(attrjson)
                classidpower[row["power"]] = classid

            idjson, attrjson = self.webjson.make_property(0, "power", classidpower[row["power"]], classidmodel[row["model"]+row["brand"]])
            data["property"].append(idjson)
            data["propertyAttribute"].append(attrjson)

        # speed_adjustment
        for index, row in models.iterrows():
            if row["speed_adjustment"] == "" or row["speed_adjustment"] is None:
                continue
            if row["speed_adjustment"] not in classidspeedad:
                classid, idjson, attrjson = self.webjson.make_class(4, row["speed_adjustment"], color=4)
                data["class"].append(idjson)
                data["classAttribute"].append(attrjson)
                classidspeedad[row["speed_adjustment"]] = classid

            idjson, attrjson = self.webjson.make_property(0, "speed_adjustment", classidspeedad[row["speed_adjustment"]], classidmodel[row["model"]+row["brand"]])
            data["property"].append(idjson)
            data["propertyAttribute"].append(attrjson)

        # cup_material
        for index, row in models.iterrows():
            if row["cup_material"] == "" or row["cup_material"] is None:
                continue
            if row["cup_material"] not in classidcup:
                classid, idjson, attrjson = self.webjson.make_class(4, row["cup_material"], color=5)
                data["class"].append(idjson)
                data["classAttribute"].append(attrjson)
                classidcup[row["cup_material"]] = classid

            idjson, attrjson = self.webjson.make_property(0, "cup_material", classidcup[row["cup_material"]], classidmodel[row["model"]+row["brand"]])
            data["property"].append(idjson)
            data["propertyAttribute"].append(attrjson)

        # speed
        for index, row in models.iterrows():
            if row["speed"] == "" or row["speed"] is None:
                continue
            if row["speed"] not in classidspeed:
                classid, idjson, attrjson = self.webjson.make_class(4, row["speed"], color=6)
                data["class"].append(idjson)
                data["classAttribute"].append(attrjson)
                classidspeed[row["speed"]] = classid

            idjson, attrjson = self.webjson.make_property(0, "speed", classidspeed[row["speed"]], classidmodel[row["model"]+row["brand"]])
            data["property"].append(idjson)
            data["propertyAttribute"].append(attrjson)

        # function
        for index, row in models.iterrows():
            if row["function"] == "" or row["function"] is None:
                continue
            # row["function"] = row["function"].replace("，", ",").replace("；", ",").replace(";", ",")
            functions = row["function"].split(",")
            for item in functions:
                if item not in classidfunction:
                    classid, idjson, attrjson = self.webjson.make_class(4, item, color=7)
                    data["class"].append(idjson)
                    data["classAttribute"].append(attrjson)
                    classidfunction[item] = classid

                idjson, attrjson = self.webjson.make_property(0, "function", classidfunction[item], classidmodel[row["model"]+row["brand"]])
                data["property"].append(idjson)
                data["propertyAttribute"].append(attrjson)

        # capacity
        for index, row in models.iterrows():
            if row["capacity"] == "" or row["capacity"] is None:
                continue
            if row["capacity"] not in classidcapacity:
                classid, idjson, attrjson = self.webjson.make_class(4, row["capacity"], color=8)
                data["class"].append(idjson)
                data["classAttribute"].append(attrjson)
                classidcapacity[row["capacity"]] = classid

            idjson, attrjson = self.webjson.make_property(0, "capacity", classidcapacity[row["capacity"]], classidmodel[row["model"]+row["brand"]])
            data["property"].append(idjson)
            data["propertyAttribute"].append(attrjson)

        return data

    def prune(self, data):
        if len(data) <= self.limit:
            return data, len(data)
        else:
            records = list()
            for k, v in data.items():
                records.append([k, v["total_sold_price"][0]])
            records.sort(key=lambda x: x[1], reverse=True)

            new_data = dict()
            for seq in range(self.limit):
                key = records[seq][0]
                new_data[key] = copy.deepcopy(data[key])

            del data
            return new_data, self.limit

    def rank_ontology(self, data, attrs):
        records = dict()
        for model, info in data.items():
            sall = float(info["total_sold_price"][0])
            records[model] = sall
            for attr in attrs:
                try:
                    for item in info[attr]:
                        records[item] = records.setdefault(item, 0) + sall
                except KeyError:
                    pass

        records = sorted(records.items(), key=lambda x: x[1], reverse=True)

        ranks = dict()
        for rank, record in enumerate(records, start=1):
            ranks[record[0]] = rank

        return ranks, len(ranks)

    def fill_graph(self, data, attrs, ranks, total):
        graph = self.webjson.init_json()

        graph["class"] = list()
        graph["classAttribute"] = list()
        graph["property"] = list()
        graph["propertyAttribute"] = list()

        classid2model = dict()
        for model, info in data.items():
            description = ""
            for key, values in info.items():
                description += f"{key}: {', '.join(map(str, values))}\n"

            classid, idjson, attrjson = self.webjson.make_class(1, info["model"][0], description=description, color=0,
                                                                rank=ranks[model], total=total)
            graph["class"].append(idjson)
            graph["classAttribute"].append(attrjson)
            classid2model[model] = classid

        color_map = dict()
        for color_seq, attr in enumerate(attrs, start=1):
            color_map[attr] = color_seq
        for seq, attr in enumerate(attrs, start=1):
            classid2attr = dict()
            color = color_map[attr]
            for model, info in data.items():
                if attr not in info:
                    continue
                for value in info[attr]:
                    if value not in classid2attr:
                        classid, idjson, attrjson = self.webjson.make_class(4, value, seq, color=color,
                                                                            rank=ranks[value], total=total)
                        graph["class"].append(idjson)
                        graph["classAttribute"].append(attrjson)
                        classid2attr[value] = classid

                    idjson, attrjson = self.webjson.make_property(1, attr, classid2attr[value],
                                                                  classid2model[model])
                    graph["property"].append(idjson)
                    graph["propertyAttribute"].append(attrjson)

            del classid2attr

        return graph

    def process(self):
        self.webjson.delete()
        data, attrs = self.get_info()
        print(f"get {len(data)} model")
        print(f"get {len(attrs)} attributes")
        data, size = self.prune(data)
        print(f"present {size} model")
        ranks, total = self.rank_ontology(data, attrs)
        graph = self.fill_graph(data, attrs, ranks, total)
        self.webjson.store(graph, self.file, self.base_path)
        self.webjson.merge_css(self.base_path)


if __name__ == "__main__":
    obj = Manager()
    obj.process()
