# -*- coding: utf-8 -*-

import _pickle as pickle


if __name__ == '__main__':
    ret1 = dict()
    ret1["notime-A"] = {
        # model 是必须的
        # biz30day（或total_sold_price）用来决定圈的大小，所以biz30day（或total_sold_price）在所有model下不能为空。
        # 即biz30day在所有model下不为空，或total_sold_price在所有model下不为空，！！！交替不为空是不行的！！！
        'model': ['A'],
        'biz30day': [100],
        'total_sold_price': [100],


        'aver_price': [1],
        'brand': ['notime'],
        'material': ["玻璃", "不锈钢"],
        "function": ["多功能", "辅食", "绞肉"],
        # "function": ["多功能、辅食、绞肉"] 这样是错误的，即使在同一个字段下也要切开来
    }

    ret1["notime-B"] = {
        'model': ['B'],
        'biz30day': [100],
        'total_sold_price': [1000],

        'brand': ['notime'],
        # 除了model、biz30day（或total_sold_price）其他属性类别可以不一致，有什么写什么
        "volume": ["3L"],
        "style": ["潮流"],

        # 如果你想把两个属性类别合并，也可以
        # "volume-style": ["3L", "潮流"]
    }

    ret1["notime-C"] = {
        'model': ['C'],
        'biz30day': [100],
        'total_sold_price': [10000],

        'brand': ['notime'],
        "volume": ["3L"],
        "style": ["潮流"],
    }

    ret1["notime-D"] = {
        'model': ['D'],
        'biz30day': [100],
        'total_sold_price': [10],

        'brand': ['notime'],
        "volume": ["4L"],
        "style": ["潮流", "Fashion"],
    }

    # 除了model，biz30day，total_sold_price的二级key（即属性类别）
    ret2 = list()
    ret2.append("aver_price")
    ret2.append("brand")
    ret2.append("material")
    ret2.append("function")
    ret2.append("volume")
    ret2.append("style")
    # ret2.append("volume-style")

    with open("interface/ret1.pkl", mode="wb") as fp:
        pickle.dump(ret1, fp)

    with open("interface/ret2.pkl", mode="wb") as fp:
        pickle.dump(ret2, fp)

    print("\nret1:")
    with open("interface/ret1.pkl", mode="rb") as fp:
        data = pickle.load(fp)
        for k, v in data.items():
            print(k, v)

    print("\nret2:")
    with open("interface/ret2.pkl", mode="rb") as fp:
        data = pickle.load(fp)
        print(data)
