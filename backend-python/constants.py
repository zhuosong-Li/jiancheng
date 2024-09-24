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

FILE_STORAGE_PATH = "D:/temp"
IMAGE_STORAGE_PATH = "http://localhost:12667/"
IMAGE_UPLOAD_PATH = "D:/imgtmp"

PRODUCTION_LINES = {
    "cutting": [1, 2, 3, 4],
    "pre_sewing": [1, 2, 3, 4],
    "sewing": [1, 2, 3, 4, 5, 6],
    "molding": [1, 2, 3, 4]
}

ORDER_SHOE_STATUS_REFERENCE = {
    '生产开始': 18,
    '裁断开始': 23,
    '针车预备开始': 30,
    '针车开始': 32,
    '成型开始': 40,
    '生产结束': 41
}
