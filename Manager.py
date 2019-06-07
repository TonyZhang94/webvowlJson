# -*- coding: utf-8 -*-
import WebJson
import Tencent

import numpy as np
import pandas as pd


num = 100

# ￥￥可以是统一的名字
# css一个基础文件，一个新文件
# 编号可能不需要了

sort_key = "biz30day"
# sort_key = "total_sold_price"
file = "biztop{}".format(str(num))

with open("node.txt", mode="r", encoding="utf-8") as fp:
    line = fp.readline()
    classid, propertyid = line.split(" ")
    classid = int(classid)
    propertyid = int(propertyid)

print("classId", classid)
print("propertyId", propertyid)


class Manager:
    def __init__(self):
        self.webjson = WebJson.WebJson()
        self.webjson.classid = classid
        self.webjson.propertyid = propertyid
        self.db = Tencent.Tencent()

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

    def select_rank(self, models):
        # baseline = ["model_rank", True]
        # baseline = ["biz30day", False]
        baseline = ["total_sold_price", False]

        models = models.sort_values(by=sort_key, ascending=True)
        select_models = pd.DataFrame(columns=list(models.columns)+["rank", "total"])
        rank_df, total = self.db.get_rank()
        print("rank df has", len(rank_df), "rows")
        cnt = 0
        for k, v in models.iterrows():
            piece = rank_df[(rank_df["brand"] == v["brand"]) & (rank_df["model"] == v["model"])]
            if 0 != len(piece):
                v["rank"] = piece[baseline[0]].values[0]
                select_models = select_models.append(v)
                cnt += 1
            if cnt == num:
                break

        select_models = select_models.sort_values(by="rank", ascending=baseline[1])
        rank = 0
        for k, v in select_models.iterrows():
            rank += 1
            print(v["rank"])
            select_models.at[k, "rank"] = rank
        select_models["total"] = min(num, len(select_models))
        # print(select_models)

        return select_models

    def process(self):
        self.webjson.delete()
        models = self.db.get_model_infos()
        print(models.size)
        models = self.select_rank(models)
        submarkets = self.db.get_model_submarkets()
        data = self.make(models, submarkets)
        self.webjson.store(data, file)
        print("classid", self.webjson.classid)
        print("propertyid", self.webjson.propertyid)

    def save_node(self):
        class_id_node = self.webjson.classid
        property_id_node = self.webjson.propertyid
        with open("node.txt", mode="w", encoding="utf-8") as fp:
            fp.write("{id1} {id2}".format(id1=class_id_node, id2=property_id_node))

    def start(self):
        self.process()
        self.save_node()


if __name__ == "__main__":
    obj = Manager()
    obj.start()
