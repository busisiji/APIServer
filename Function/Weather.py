"""
反馈气象事件

"""

from flask_restful import Resource
from flask import request
from tinydb import Query
from DB_TinyDB import db_Weather_info,db_Weather_Check,db_Crop,db_Solution
from tinydb import TinyDB

Q = Query()


class Weather(Resource):

    # 获取气象灾害数据
    def get(self, prefix):

        if prefix == 'info':

            try:

                Data = db_Weather_info.all()

                return {
                    'Start': True,
                    'message': '已获取气象数据',
                    'data': Data
                }, 200

            except:

                return {
                    'Start': False,
                    'message': '获取气象数据失败',
                }, 200

        else:
            return {
                'Start': False,
                'message': 'URL错误'
            }, 200


    def post(self, prefix):

        if prefix == 'start':

            data = request.json
            Crop = data['Crop']  # 种植作物
            Region = data['Region']  # 种植区域
            Stage = data['Stage']  # 生长阶段


            # 查询气象事件
            data = db_Weather_Check.search((Q.Crop == Crop) & (Q.Region == Region) & (Q.Stage == Stage))
            # 获取解决方案

            if len(data) >= 1:

                Qx_Name = []
                Ftion_list = []

                for i in data:

                    Aim = i['Aim']
                    Name = i['Name']
                    Qx_Name.append(Name)

                    if Aim == 'P':

                        DB = TinyDB(f'DB/db_{Region[0]}.json')
                        old_data = float(DB.all()[0]['Qx_cut'])
                        DB.update({'Qx_cut': old_data + float(i['Reduce'])})

                    else:

                        Des = db_Crop.search(Q.ID == Crop)[0]['Des']
                        ID = (TinyDB(f'Crop_DB/{Des}/{Des}_Info.json')).search(Q.ID == Stage)[0][f'Check_{Aim}']
                        DB = TinyDB(f'Crop_DB/{Des}/{Des}_Check_{Aim}.json')
                        Ftion = DB.search(Q.ID == Stage)[0]['Ftion']

                        for v in Ftion:
                            Ftion_list.append(v)
                        for v in i['Cure']:
                            Ftion_list.append(v)

                        DB.update({'Ftion': Ftion_list}, Q.ID == ID)

                        print(Ftion_list)

                return {
                    'Start': True,
                    'Weather': True,
                    'message': Qx_Name
                }, 200

            else:
                return {
                    'Start': True,
                    'Weather': False,
                    'message': '气象状态正常'
                }, 200

        elif prefix == 'add/info':

            data = request.json

            Name = data['Name']



            try:
                # 生成ID
                ID = str(int(db_Weather_info.all()[-1]['ID'][-1]) + 1)

                db_Weather_info.insert({
                    'ID': ID,
                    'Name': Name,

                })
                return {
                    'Start': True,
                    'message': '已写入'
                }, 200

            except:
                return {
                    'Start': False,
                    'message': '写入失败'
                }, 200

        elif prefix == 'add/check':

            data = request.json
            ID = data['ID']
            Name = data['Name']
            Region = data['Region']
            Crop = data['Crop']
            Stage = data['Stage']
            Odds = data['Odds']
            Reduce = data['Reduce']  # 获取减产系数

            Aim = data['Aim']
            Cure = data['Cure']
            T = float(data['T'])
            H = float(data['H'])
            S = float(data['S'])
            D = float(data['D'])
            G = float(data['G'])
            PM2 = float(data['PM2'])
            PM10 = float(data['PM10'])
            KPA = float(data['KPA'])


            try:
                # # 生成ID
                # ID = str(int(db_Insect_info.all()[-1]['ID'][-1]) + 1 )

                db_Weather_Check.insert({
                    'ID': ID,
                    'Name': Name,
                    'Region': Region,
                    'Crop': Crop,
                    'Stage': Stage,
                    'Odds': Odds,
                    'Reduce': Reduce,

                    'Aim': Aim,
                    'Cure': Cure,
                    'T': T,
                    'H': H,
                    'S': S,
                    'D': D,
                    'G': G,
                    'PM2': PM2,
                    'PM10': PM10,
                    'KPA': KPA
                })

                return {
                    'Start': True,
                    'message': '已写入'
                }, 200

            except:
                return {
                    'Start': False,
                    'message': '写入失败'
                }, 200

        else:
            return {
                'Start': False,
                'message': 'URL错误'
            }, 200

    # 更新随机事件数据
    def put(self, prefix):

        if prefix == 'info':

            data = request.json
            ID = data['ID']
            Key = data['Key']
            Value = data['Value']
            try:
                db_Weather_info.update({f"{Key}": f"{Value}"}, Q.ID == ID)

                return {
                    'Start': True,
                    'message': '已写入'
                }, 200

            except:

                return {
                    'Start': False,
                    'message': '写入失败'
                }, 200

        elif prefix == 'check':

            data = request.json
            ID = data['ID']
            Key = data['Key']
            Value = data['Value']

            try:
                db_Weather_Check.update({f"{Key}": f"{Value}"}, Q.ID == ID)

                return {
                    'Start': True,
                    'message': '已写入'
                }, 200

            except:

                return {
                    'Start': False,
                    'message': '写入失败'
                }, 200

        else:
            return {
                'Start': False,
                'message': 'URL错误'
            }, 200

    def delete(self, prefix):

        if prefix == 'info':

            data = request.json
            ID = data['ID']
            try:
                # 查询是否存在该ID
                if db_Weather_info.search(Q.ID == ID):
                    db_Weather_info.delete(Q.ID == ID)
                    return {
                        'Start': True,
                        'message': '已删除',
                        'data': db_Weather_info.all()

                    }, 200
                else:
                    return {
                        'Start': False,
                        'message': '删除失败',
                        'data': db_Weather_info.all()

                    }, 200
            except:

                return {
                    'Start': False,
                    'message': '参数错误',
                    'data': db_Weather_info.all()

                }, 200

        elif prefix == 'check':

            data = request.json
            ID = data['ID']
            try:
                # 查询是否存在该ID
                if db_Weather_Check.search(Q.ID == ID):
                    db_Weather_Check.delete(Q.ID == ID)
                    return {
                        'Start': True,
                        'message': '已删除',
                        'data': db_Weather_Check.all()

                    }, 200
                else:
                    return {
                        'Start': False,
                        'message': '删除失败',
                        'data': db_Weather_Check.all()

                    }, 200
            except:

                return {
                    'Start': False,
                    'message': '参数错误',
                    'data': db_Weather_Check.all()

                }, 200

        else:
            return {
                'Start': False,
                'message': 'URL错误'
            }, 200