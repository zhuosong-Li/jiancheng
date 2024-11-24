PRODUCTION_LINE_REFERENCE = [0, 1, 2]

PRICE_REPORT_REFERENCE = {
    "裁断": {
        "status_number": 20,
        "operation_id": [78, 79],
    },
    "针车预备": {
        "status_number": 27,
        "operation_id": [92, 93],
    },
    "针车": {
        "status_number": 27,
        "operation_id": [92, 93],
    },
    "成型": {
        "status_number": 37,
        "operation_id": [112, 113],
    },
}

QUANTTIY_REPORT_REFERENCE = {"裁断": 23, "针车预备": 30, "针车": 32, "成型": 40}

SHOESIZERANGE = [i for i in range(34, 47)]

IN_PRODUCTION_ORDER_NUMBER = 9
END_OF_ORDER_NUMBER = 18
END_OF_PRODUCTION_NUMBER = 42


ORDER_SHOE_STATUS_REFERENCE = {
    "生产开始": 18,
    "裁断开始": 23,
    "针车预备开始": 30,
    "针车开始": 32,
    "成型开始": 40,
    "裁断结束": 24,
    "针车预备结束": 31,
    "针车结束": 33,
    "成型结束": 41,
    "生产结束": 42,
}

OUTSOURCE_STATUS_MAPPING = {
    0: "未提交",
    1: "已提交",
    2: "已审批",
    3: "被驳回",
    4: "材料出库",
    5: "正在生产",
    6: "成品入库",
    7: "外包完成",
    8: "外包终止",
}
