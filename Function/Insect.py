"""
反馈虫情事件
"""
import time

from flask_restful import Resource
from flask import request
from tinydb import Query

from DB_TinyDB import db_Insect_info,db_Insect_Check,db_Crop
from tinydb import TinyDB

from modbus_config import modbus_server

Q = Query()


def update_insect_info(index, number):
    Insect = Query()
    # 查找对应编号的记录
    insect = db_Insect_info.get(Insect.ID == f'C{index:02d}')
    if insect:
        # 更新Number字段
        db_Insect_info.update({'Number': number}, doc_ids=[insect.doc_id])


class Insect(Resource):

    #获取虫情数据
    def get(self, prefix):

        if prefix == 'info':
            try:
                Data = db_Insect_info.all()

                return {
                    'Start': True,
                    'message': '已获取虫情数据',
                    'data': Data
                }, 200
            except:
                return {
                    'Start': False,
                    'message': '获取虫情数据失败'
                }, 200

        else:
            return {
                'Start': False,
                'message': 'URL错误'
            }, 200

    # 拍照，更新虫情数据
    def post(self, prefix):

        if prefix == 'clap':

            try:
                # 写入1
                modbus_server.runServer(type='写', fc_as_hex=0x03, address=0, values=1)

                # 等待30秒
                # time.sleep(10)
                # 循环读取10次，每次等待5秒
                for i in range(10):
                    read_result = modbus_server.runServer(type='读', fc_as_hex=0x03, address=0)
                    if read_result and read_result[0] == 0:
                        break
                    if i == 9:
                        return {
                            'Start': False,
                            'message': f'拍照超时失败'
                        }, 200

                    time.sleep(5)



                # 获取地址1之后的20个数据
                data_start_address = 1
                data_count = 20
                data_result = modbus_server.runServer(type='读', fc_as_hex=0x03, address=data_start_address,
                                                      count=data_count)

                # 解析data_result
                for i in range(0, len(data_result), 2):
                    index = data_result[i]
                    number = data_result[i + 1]
                    update_insect_info(index, number)

                Data = db_Insect_info.all()

                return {
                    'Start': True,
                    'message': '已拍照',
                    'data': Data
                }, 200
            except Exception as e:
                return {
                    'Start': False,
                    'message': f'拍照失败: {str(e)}'
                }, 200


        elif prefix == 'start':

            data = request.json
            Crop = data['Crop']  #种植作物
            Region = data['Region']  #种植区域
            Stage = data['Stage']  #生长阶段

            try:
                #查询虫情灾害
                data = db_Insect_Check.search((Q.Crop == Crop) & (Q.Region == Region) & (Q.Stage == Stage))
                print(data)


                if len(data) >= 1:

                    Cq_Name = []
                    Ftion_list = []

                    for i in data:


                        Aim = i['Aim']
                        Name = i['Name']
                        Cq_Name.append(Name)


                        if Aim == 'P':

                            DB = TinyDB(f'DB/db_{Region[0]}.json')
                            old_data = float(DB.all()[0]['Cq_cut'])
                            DB.update({'Cq_cut': old_data + float(data['Reduce'])})

                        else:

                            Des = db_Crop.search(Q.ID == Crop)[0]['Des']
                            ID = (TinyDB(f'Crop_DB/{Des}/{Des}_Info.json')).search(Q.ID == Stage)[0][f'Check_{Aim}']
                            DB = TinyDB(f'Crop_DB/{Des}/{Des}_Check_{Aim}.json')
                            Ftion = DB.search(Q.ID == ID)[0]['Ftion']

                            for v in Ftion:
                                Ftion_list.append(v)
                            for v in i['Cure']:
                                Ftion_list.append(v)

                            DB.update({'Ftion': Ftion_list}, Q.ID == ID)

                    return {
                        'Start': True,
                        'Insect_': True,
                        'message': Cq_Name
                    }, 200
                else:
                    return {
                        'Start': True,
                        'Insect_': False,
                        'message': '虫情状态正常'
                    }, 200
            except:
                return {
                    'Start': False,
                    'message': '参数错误'
                }, 200

        elif prefix == 'add/info':

            data = request.json

            Name = data['Name']
            Number = 0



            try:
                # 生成ID
                ID = str(int(db_Insect_info.all()[-1]['ID'][-1]) + 1 )

                db_Insect_info.insert({
                    'ID': ID,
                    'Name': Name,
                    'Number': Number

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

                db_Insect_Check.insert({
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

    # 写入虫情数据
    def put(self, prefix):

        if prefix == 'info':

            data = request.json
            ID = data['ID']
            Key = data['Key']
            Value = data['Value']
            try:
                db_Insect_info.update({f"{Key}": f"{Value}"}, Q.ID == ID)


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
                db_Insect_Check.update({f"{Key}": f"{Value}"}, Q.ID == ID)

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
                if db_Insect_info.search(Q.ID == ID):
                    db_Insect_info.delete(Q.ID == ID)
                    return {
                        'Start': True,
                        'message': '已删除',
                        'data': db_Insect_info.all()

                    }, 200
                else:
                    return {
                        'Start': False,
                        'message': '删除失败',
                        'data': db_Insect_info.all()

                    }, 200
            except:

                return {
                    'Start': False,
                    'message': '参数错误',
                    'data': db_Insect_info.all()

                }, 200

        elif prefix == 'check':

            data = request.json
            ID = data['ID']
            try:
                # 查询是否存在该ID
                if db_Insect_Check.search(Q.ID == ID):
                    db_Insect_Check.delete(Q.ID == ID)
                    return {
                        'Start': True,
                        'message': '已删除',
                        'data': db_Insect_Check.all()

                    }, 200
                else:
                    return {
                        'Start': False,
                        'message': '删除失败',
                        'data': db_Insect_Check.all()

                    }, 200
            except:

                return {
                    'Start': False,
                    'message': '参数错误',
                    'data': db_Insect_Check.all()

                }, 200

        else:
            return {
                'Start': False,
                'message': 'URL错误'
            }, 200