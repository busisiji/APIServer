from flask_restful import Resource
from flask import request
from tinydb import Query
from tinydb import TinyDB
import DB_TinyDB
import os
Q = Query()



# def add(Name):
#
#     # Data = Data
#     Data = [
#
#             {"ID": "S1", "Name": "东北地区", "Join": "Soil_Northeast_region"},
#             {"ID": "S2", "Name": "华北地区", "Join": "Soil_North_China"},
#             {"ID": "S3", "Name": "西南地区", "Join": "Soil_Southwest_China"},
#             {"ID": "S4", "Name": "华南地区", "Join": "Soil_South_China"},
#             {"ID": "S5", "Name": "西北地区", "Join": "Soil_Northwest_China"},
#             {"ID": "S6", "Name": "华中地区", "Join": "Soil_Central_China"}
#
#     ]
#
#     DB = TinyDB(f'DB/db_{Name}.json')
#     DB.insert_multiple(Data)
#
#
# def delete(Name):
#
#     DB = TinyDB(f'DB/db_{Name}.json')
#     DB.remove()
#
#
#
# add('Soil')

Data = [
    {"ID": "C01","Name": "蝗虫","Number": 0},
    {"ID": "C02","Name": "蝼蛄","Number": 0},
    {"ID": "C03","Name": "蟋蟀","Number": 0},
    {"ID": "C04","Name": "蚜虫","Number": 0},
    {"ID": "C05","Name": "粉虱","Number": 0},
    {"ID": "C06","Name": "种蝇","Number": 0},
    {"ID": "C07","Name": "吸浆虫","Number": 0},
    {"ID": "C08","Name": "叶蜂","Number": 0},
    {"ID": "C09","Name": "甲虫","Number": 0},
    {"ID": "C10","Name": "蜜蜂","Number": 0}
]
# DB = TinyDB('DB/db_Soil.json')
(DB_TinyDB.db_Insect_info.insert_multiple(Data))
# TinyDB('DB/db_Soil.json')