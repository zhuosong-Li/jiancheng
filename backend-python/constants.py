PRODUCTION_LINE_REFERENCE = ['F', 'S', 'M']

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

QUANTTIY_REPORT_REFERENCE = {
    "裁断": 23,
    "针车预备": 30,
    "针车": 32,
    "成型": 40
}

SHOESIZEINFO = [
    {
        'shoe_size': '34',
        'internal_size': '6.5',
        'external_size': '6.5',
    },
    {
        'shoe_size': '35',
        'internal_size': '7',
        'external_size': '7',
    },
    {
        'shoe_size': '36',
        'internal_size': '7',
        'external_size': '7.5',
    },
    {
        'shoe_size': '37',
        'internal_size': '8',
        'external_size': '8',
    },
    {
        'shoe_size': '38',
        'internal_size': '8',
        'external_size': '8.5',
    },
    {
        'shoe_size': '39',
        'internal_size': '9',
        'external_size': '9.5',
    },
    {
        'shoe_size': '40',
        'internal_size': '10',
        'external_size': '10',
    },
    {
        'shoe_size': '41',
        'internal_size': '10',
        'external_size': '10.5',
    },
    {
        'shoe_size': '42',
        'internal_size': '11',
        'external_size': '11',
    },
    {
        'shoe_size': '43',
        'internal_size': '12',
        'external_size': '12',
    },
    {
        'shoe_size': '44',
        'internal_size': '13',
        'external_size': '13',
    },
    {
        'shoe_size': '45',
        'internal_size': '13',
        'external_size': '13.5',
    },
    {
        'shoe_size': '46',
        'internal_size': '14',
        'external_size': '14',
    },
]

IN_PRODUCTION_ORDER_NUMBER = 9
END_OF_ORDER_NUMBER = 18
END_OF_PRODUCTION_NUMBER = 42

FILE_STORAGE_PATH = "/home/desktop/Desktop/imageserver/imgtmp"
IMAGE_STORAGE_PATH = "http://localhost:12667/"
IMAGE_UPLOAD_PATH = "/home/desktop/Desktop/imageserver/temp"

PRODUCTION_LINES = {
    "裁断": [1, 2, 3, 4],
    "针车预备": [1, 2, 3, 4],
    "针车": [1, 2, 3, 4, 5, 6],
    "成型": [1, 2, 3, 4]
}

ORDER_SHOE_STATUS_REFERENCE = {
    '生产开始': 18,
    '裁断开始': 23,
    '针车预备开始': 30,
    '针车开始': 32,
    '成型开始': 40,
    '裁断结束': 24,
    '针车预备结束': 31,
    '针车结束': 33,
    '成型结束': 41,
    '生产结束': 42
}

OUTSOURCENEEDED = {
    "投产指令单创建": False,
    "投产指令单下发": False,
    "一次BOM填写": False,
    "一次BOM下发": False,
    "面料单位用量计算": False,
    "面料单位用量下发": False,
    "一次采购订单创建": False,
    "一次采购订单下发": False,
    "一次采购入库": False,
    "技术部调版分配": False,
    "技术部调版下发": False,
    "二次BOM填写": False,
    "二次BOM下发": False,
    "二次采购订单创建": False,
    "二次采购订单下发": False,
    "二次采购入库": False,
    "材料到齐通知": False,
    "生产排期，分配": False,
    "生产开始": False,
    "裁断材料出库": False,
    "裁断，批皮工价填报": False,
    "财务部审核": False,
    "生产副总审核": False,
    "裁断开始": False,
    "裁断结束": False,
    "半成品中转入库": False,
    "半成品中转针车材料出库": False,
    "针车及预备工序填报": False,
    "财务部审核": False,
    "生产副总审核": False,
    "针车预备开始": False,
    "针车预备结束": False,
    "针车开始": False,
    "针车结束": False,
    "鞋包中转仓入库": False,
    "鞋包中转仓出库": False,
    "成型材料出库": False,
    "成型工价填报": False,
    "财务部审核": False,
    "生产副总审核": False,
    "成型开始": False,
    "成型结束": False,
    "生产结束": False,
}
