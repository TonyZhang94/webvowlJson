# -*- coding: utf-8 -*-
import csv
import json

from gevent import os

classtype = list()
# classtype.append("owl:unionOf")  # 中间带两个圈，蓝色
# classtype.append("rdfs:Class")  # 紫红色
# classtype.append("owl:equivalentClass")  # 蓝色，外双圈
# classtype.append("rdfs:Datatype")  # 蓝色，外单圈
# classtype.append("owl:Class")  # 黄色方框

for _ in range(20):
    classtype.append("rdfs:Class")

propertytype = list()
# propertytype.append("owl:datatypeproperty")  # 绿色属性框
# propertytype.append("owl:objectProperty")  # 蓝色属性框
# propertytype.append("rdfs:SubClassOf")  # 虚线箭头

propertytype.append("owl:datatypeproperty")
propertytype.append("owl:datatypeproperty")
propertytype.append("owl:datatypeproperty")

css_appendix = "files/append.css"
colorlist = list()
colorlist.append("#CD3333")  # 大红色
colorlist.append("#ADFF2F")  # 青绿色
colorlist.append("#EE7AE9")  # 桃紫色
colorlist.append("#EEEE00")  # 亮黄色
colorlist.append("#0000FF")  # 海蓝色
colorlist.append("#00FFFF")  # 天蓝色
colorlist.append("#B8860B")  # 浅棕色
colorlist.append("#DB7093")  # 暗红色
colorlist.append("#FFB90F")  # 橘黄色
colorlist.append("#87CEFF")  # 浅蓝色
colorlist.append("#CD2990")  # 桃红色
colorlist.append("#FFB6C1")  # 浅肉色
colorlist.append("#A52A2A")  # 深棕色
colorlist.append("#7A67EE")  # 浅紫色
colorlist.append("#009ACD")  # 蓝绿色
colorlist.append("#CD5B45")  # 深肤色
colorlist.append("#008B00")  # 深绿色
colorlist.append("#B8860B")  # 浅棕色
colorlist.append("#8968CD")  # 浅紫色
colorlist.append("#388E8E")  # 墨绿色
print("color list", len(colorlist))



class WebJson:
    def __init__(self):
        self.classid = 0
        self.propertyid = 0

    @staticmethod
    def delete():
        try:
            os.remove(css_appendix)
        except Exception as e:
            print("no {}".format(css_appendix))
        with open(css_appendix, mode="w", encoding="utf-8") as fp:
            pass

    @staticmethod
    def store(data, file, base_path):
        path = 'files\{}.json'.format(file)
        # print("json store path1", path)
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

        path = f"{base_path}data\{file}.json"
        # print("json store path2", path)
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

    @staticmethod
    def merge_css(base_path):
        dst_css = base_path + "css\webvowl.css"
        # print("dst css path", dst_css)
        with open(dst_css, mode="w", encoding="utf-8") as dst_fp:
            with open("files/base.css", mode="r", encoding="utf-8") as src_fp:
                for line in src_fp.readlines():
                    dst_fp.write(line)

            with open("files/append.css", mode="r", encoding="utf-8") as src_fp:
                for line in src_fp.readlines():
                    dst_fp.write(line)

    @staticmethod
    def load():
        with open('G:\webvowlJson\demo2.json') as json_file:
            data = json.load(json_file)
            return data

    def init_json(self):
        data = {}
        data["comment"] = "料理机demo"
        data["namespace"] = ""

        data["header"] = {}
        data["header"]["languages"] = ["undefined"]
        data["header"]["title"] = {}
        data["header"]["title"]["undefined"] = "料理机demo"
        data["header"]["iri"] = "none"
        data["header"]["version"] = "0.0000000001"
        data["header"]["author"] = ["cheyun"]
        data["header"]["description"] = "料理机"

        data["metrics"] = {}
        data["metrics"]["classCount"] = 8
        data["metrics"]["propertyCount"] = 7
        data["metrics"]["nodeCount"] = 8
        data["metrics"]["axiomCount"] = 4000

        return data

    def make_class(self, type, label, description="", color="default", rank=0, total=0):
        self.classid += 1
        id = str(self.classid)

        classDef = {}
        classDef["id"] = "class" + id
        classDef["type"] = classtype[type]

        classAttr = {}
        classAttr["id"] = "class" + id
        classAttr["label"] = {}
        classAttr["label"]["undefined"] = label

        if description != "":
            classAttr["description"] = {}
            classAttr["description"]["undefined"] = description
        
        if color != "default":
            color = color % 20
            if color >= 0:
                max_diff = 25
                base_r = 50 + max_diff
                r = base_r - max_diff * rank / total
                css = "#class%s .class {fill: %s; r: %s !important;}" % (id, colorlist[color], str(r))
            else:
                css = "#class%s .class {fill: %s;}" % (id, colorlist[color])
            file_obj = open(css_appendix, 'a', encoding="utf-8")
            file_obj.write(css+"\n")

        return id, classDef, classAttr

    def make_property(self, type, label, range, domain):
        self.propertyid += 1
        id = str(self.propertyid)

        propertyDef = {}
        propertyDef["id"] = "property" + id
        propertyDef["type"] = propertytype[type]

        propertyAttr = {}
        propertyAttr["id"] = "property" + id
        propertyAttr["label"] = {}
        propertyAttr["label"]["IRI-based"] = label
        propertyAttr["range"] = "class" + range
        propertyAttr["domain"] = "class" + domain
        return propertyDef, propertyAttr

    def process(self):
        pass

    def start(self):
        self.process()


if __name__ == "__main__":
    obj = WebJson()
    obj.start()
