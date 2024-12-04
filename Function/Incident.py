"""
反馈随机事件

"""

from flask_restful import Resource
from flask import request
from tinydb import Query
from DB_TinyDB import db_Incident_info,db_Incident_Check,db_Crop
from tinydb import TinyDB

Q = Query()


class Incident(Resource):

    # 获取随机事件数据
    def get(self, prefix):

        if prefix == 'info':

            try:

                Data = db_Incident_info.all()

                return {
                    'Start': True,
                    'message': '已获取随机事件数据',
                    'data': Data
                }, 200

            except:

                return {
                    'Start': False,
                    'message': '获取随机事件数据失败',
                }, 200

        else:
            return {
                'Start': False,
                'message': 'URL错误'
            }, 200

    # 写入随机事件数据
    def post(self, prefix):


        if prefix == 'start':

            data = request.json
            Crop = data['Crop']  #种植作物
            Region = data['Region']  #种植区域
            Stage = data['Stage']  #生长阶段


            #查询随机事件
            data = db_Incident_Check.search((Q.Crop == Crop) & (Q.Region == Region) & (Q.Stage == Stage))
            #获取解决方案

            if len(data) >= 1:

                Sj_Name = []
                Ftion_list = []

                for i in data:

                    Aim = i['Aim']
                    Name = i['Name']
                    Sj_Name.append(Name)

                    if Aim == 'P':

                        DB = TinyDB(f'DB/db_{Region[0]}.json')
                        old_data = float(DB.all()[0]['Cq_cut'])
                        DB.update({'Cq_cut': old_data + float(data['Reduce'])})

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

                return {
                    'Start': True,
                    'Incident': True,
                    'message': Sj_Name
                }, 200
            else:
                return {
                    'Start': True,
                    'Incident': False,
                    'message': '随机事件状态正常'
                }, 200


        elif prefix == 'add/info':

            data = request.json

            Name = data['Name']



            try:
                # 生成ID
                ID = str(int(db_Incident_info.all()[-1]['ID'][-1]) + 1 )

                db_Incident_info.insert({
                    'ID': ID,
                    'Name': Name

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



            try:
                # # 生成ID
                # ID = str(int(db_Insect_info.all()[-1]['ID'][-1]) + 1 )

                db_Incident_Check.insert({
                    'ID': ID,
                    'Name': Name,
                    'Region': Region,
                    'Crop': Crop,
                    'Stage': Stage,
                    'Odds': Odds,
                    'Reduce': Reduce,

                    'Aim': Aim,
                    'Cure': Cure
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
                db_Incident_info.update({f"{Key}": f"{Value}"}, Q.ID == ID)

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
                db_Incident_Check.update({f"{Key}": f"{Value}"}, Q.ID == ID)

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
                #查询是否存在该ID
                if db_Incident_info.search(Q.ID == ID):
                    db_Incident_info.delete(Q.ID == ID)
                    return {
                        'Start': True,
                        'message': '已删除',
                        'data': db_Incident_info.all()

                    }, 200
                else:
                    return {
                        'Start': False,
                        'message': '删除失败',
                        'data': db_Incident_info.all()

                    }, 200
            except:

                return {
                    'Start': False,
                    'message': '参数错误',
                    'data': db_Incident_info.all()

                }, 200

        elif prefix == 'check':

            data = request.json
            ID = data['ID']
            try:
                # 查询是否存在该ID
                if db_Incident_Check.search(Q.ID == ID):
                    db_Incident_Check.delete(Q.ID == ID)
                    return {
                        'Start': True,
                        'message': '已删除',
                        'data': db_Incident_Check.all()

                    }, 200
                else:
                    return {
                        'Start': False,
                        'message': '删除失败',
                        'data': db_Incident_Check.all()

                    }, 200
            except:

                return {
                    'Start': False,
                    'message': '参数错误',
                    'data': db_Incident_Check.all()

                }, 200

        else:
            return {
                'Start': False,
                'message': 'URL错误'
            }, 200