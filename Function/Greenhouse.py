"""
温室系统环境

环境方案处理（温度、湿度、光照、二氧化碳）
"""


from flask_restful import Resource, reqparse
from flask import request
from tinydb import Query
from DB_TinyDB import db_Crop
from Thread import Greenhouse_Thread
from tinydb import TinyDB

from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor(max_workers = 2)


Q = Query()

#模拟种植API
class Greenhouse(Resource):



    def get(self, prefix):

        parser = reqparse.RequestParser()
        parser.add_argument('Crop', type=str, required=True)
        args = parser.parse_args()

        if prefix == 'info':

            Crop = args['Crop']

            try:

                Name = db_Crop.search(Q.ID == Crop)[0]['Des']
                DB = TinyDB(f'Crop_DB/{Name}/{Name}_Greenhouse_Info.json')
                Data = DB.all()[0]
                return {
                    'Status': True,
                    'message': '获取成功!',
                    'Data': Data}, 200
            except:
                return {
                    'Status': False,
                    'message': '获取失败!'}, 200

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 200


    def post(self, prefix):

        parser = reqparse.RequestParser()


        if prefix == 'start':

            parser.add_argument('Crop', type=str, required=True, location='json')
            parser.add_argument('Region', type=str, required=True, location='json')
            parser.add_argument('Stage', type=str, required=True, location='json')
            parser.add_argument('T', required=False, default=30, location='json')
            parser.add_argument('H', required=False, default=60, location='json')
            parser.add_argument('CO2', required=False, default=800, location='json')
            parser.add_argument('LLX', required=False, default=500, location='json')

            args = parser.parse_args()

            Nzw = args['Crop']  # 种植作物
            Zzqy = args['Region']  # 种植区域
            Szjd = args['Stage']  # 生长阶段

            T = args['T']
            H = args['H']
            CO2 = args['CO2']
            LLX = args['LLX']

            try:
                print(db_Crop.search(Q.ID == Nzw)[0]['Type'])
                #判断作物是否为温室作物 & 判断种植区域是否在A B
                if (Zzqy != 'A1' and Zzqy != 'B2') :

                    return {
                        'Start': False,
                        'message': f'种植作物错误,种植区域不在A1B2，而是{Zzqy}'
                    }, 200
                elif (db_Crop.search(Q.ID == Nzw)[0]['Type'] != 'WS') :

                    return {
                        'Start': False,
                        'message': f'种植作物错误,作物{db_Crop.search(Q.ID == Nzw)[0]["Des"]}不是温室作物'
                    }, 200

                else:


                    pool.submit(
                        Greenhouse_Thread,
                        T, H, CO2, LLX, Szjd
                    )

                    return {
                        'Start': True,
                        'message': '环境方案传输成功'
                    }, 200
            except:

                return {
                    'Start': False,
                    'message': '环境方案传输失败'
                }, 200

        elif prefix == 'add':

            parser.add_argument('Crop', type=str, required=True, location='json')
            parser.add_argument('Stage', type=str, required=True, location='json')

            parser.add_argument('Name', type=str, required=True, location='json')
            parser.add_argument('T_max', required=True, location='json')
            parser.add_argument('T_min', required=True, location='json')
            parser.add_argument('H_max', required=True, location='json')
            parser.add_argument('H_min', required=True, location='json')
            parser.add_argument('C_max', required=True, location='json')
            parser.add_argument('C_min', required=True, location='json')
            parser.add_argument('G_max', required=True, location='json')
            parser.add_argument('G_min', required=True, location='json')
            parser.add_argument('Cover', type=str, required=True, location='json')

            args = parser.parse_args()

            Nzw = args['Corp']  # 种植作物
            Szjd = args['Stage']  # 生长阶段

            ID = args['Stage']
            Name = args['Name']
            T_max = args['T_max']
            T_min = args['T_min']
            H_max = args['H_max']
            H_min = args['H_min']
            C_max = args['C_max']
            C_min = args['C_min']
            G_max = args['G_max']
            G_min = args['G_min']
            Cover = args['Cover']

            try:

                Names = db_Crop.search(Q.ID == Nzw)[0]['Des']
                DB = TinyDB(f'DB/{Names}/{Names}_Greenhouse_Info.json')
                DB.update({
                    ID: ID,
                    Name: Name,
                    T_max: T_max,
                    T_min: T_min,
                    H_max: H_max,
                    H_min: H_min,
                    C_max: C_max,
                    C_min: C_min,
                    G_max: G_max,
                    G_min: G_min,
                    Cover: Cover
                },(Q.ID == Szjd))

                return {
                    'Status': True,
                    'message': '新增成功！',
                    'Data': DB.search(Q.ID == Szjd)[0]
                }, 200

            except:
                return {
                    'Status': False,
                    'message': '新增失败！',
                    'Data': DB.search(Q.ID == Szjd)[0]
                }, 200



        elif prefix == 'del':

            parser.add_argument('Crop', type=str, required=True, location='json')
            parser.add_argument('Stage', type=str, required=True, location='json')
            args = parser.parse_args()

            Nzw = args['Corp']  # 种植作物
            ID = args['Stage']


            Names = db_Crop.search(Q.ID == Nzw)[0]['Des']
            DB = TinyDB(f'DB/{Names}/{Names}_Greenhouse_Info.json')
            DB.remove(Q.ID == ID)

            return {
                'Status': True,
                'message': '删除成功！',
                'Data': DB.search(Q.ID == ID)[0]
            }, 200


        elif prefix == 'put':

            data = request.json
            Nzw = data['crop']  # 种植作物

            ID = data['ID']
            Key = data['Key']  # 字段
            Value = data['Value']  # 参数

            if ID is None or Key is None or Value is None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数'}), 200

            Names = db_Crop.search(Q.ID == Nzw)[0]['Des']
            DB = TinyDB(f'DB/{Names}/{Names}_Greenhouse_Info.json')
            IDs = [i['ID'] for i in DB.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 200

            else:

                try:
                    DB.update({Key: Value}, (Q.ID == ID))
                    return {
                        'Status': True,
                        'message': '更新成功！',
                        'Data': DB.search(Q.ID == ID)[0]
                    }, 200

                except:

                    return {
                        'Status': False,
                        'message': '更新失败！'}, 200

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 200
