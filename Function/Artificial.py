"""
人工干预系统


气象灾害方案处理
虫情灾害方案处理
随机事件方案处理
土壤改善处理（有机肥、水分、盐分、酸碱）

"""


from flask_restful import Resource, reqparse
from flask import request
from tinydb import Query
from DB_TinyDB import db_Solution
from tinydb import TinyDB

Q = Query()


class Artificial(Resource):

    # 获取随机事件数据
    def post(self, prefix):

        parser = reqparse.RequestParser()

        parser.add_argument('Crop', type=str, required=False, location='json')
        parser.add_argument('Region', type=str, required=True, location='json')
        parser.add_argument('Stage', type=str, required=False, location='json')
        parser.add_argument('Type', type=str, required=True, location='json')
        parser.add_argument('Plan', type=str, required=True, location='json')


        args = parser.parse_args()


        if prefix == 'start':

            Nzw = args['Crop']  # 种植作物
            Szjd = args['Stage']  # 生长阶段

            Zzqy = args['Region']  # 种植区域
            Type = float(args['Type'])
            Plan = args['Plan']

            print(type(Type))

            DB = TinyDB(f'DB/db_{Zzqy[0]}.json')

            if (Szjd == DB.all()[0]['stage']) or (Szjd == None):

                #气象灾害方案处理
                if Type == 1:

                    try:

                        DB = TinyDB(f'DB/db_{Zzqy[0]}.db')
                        # 获取对应解决方案
                        Plan_info = db_Solution.search(Q.ID == Plan)[0]
                        if Plan_info['Des'] == '抢收':
                            DB.upsert({
                                'On': False
                            })
                        if 'Qx' in Plan_info['Object']:
                            DB.update({
                                'Qx_cut': 0
                            })

                        return {
                            'Start': True,
                            "message": "气象灾害方案处理传输完成"}, 200
                    except:

                        return {
                            'Start': False,
                            "message": "气象灾害方案处理传输失败"}, 200

                #虫情灾害方案处理
                elif Type == 2:

                    try:

                        DB = TinyDB(f'DB/db_{Zzqy[0]}.db')
                        # 获取对应解决方案
                        Plan_info = db_Solution.search(Q.ID == Plan)[0]
                        if Plan_info['Des'] == '抢收':
                            DB.upsert({
                                'On': False
                            })
                        if 'Cq' in Plan_info['Object']:
                            DB.update({
                                'Cq_cut': 0
                            })

                        return {
                            'Start': True,
                            "message": "虫情灾害方案处理传输完成"}, 200
                    except:

                        return {
                            'Start': False,
                            "message": "虫情灾害方案处理传输失败"}, 200

                #随机事件方案处理
                elif Type == 3:

                    try:

                        DB = TinyDB(f'DB/db_{Zzqy[0]}.db')
                        # 获取对应解决方案
                        Plan_info = db_Solution.search(Q.ID == Plan)[0]

                        if Plan_info['Des'] == '抢收':
                            DB.upsert({
                                'On': False
                            })
                        if 'Sj' in Plan_info['Object']:
                            DB.update({
                                'Sj_cut': 0
                            })

                        return {
                            'Start': True,
                            "message": "随机事件方案处理传输完成"}, 200
                    except:

                        return {
                            'Start': False,
                            "message": "随机事件方案处理传输失败"}, 200

                #土壤改善方案处理 (土壤改善处理（有机肥、水分、盐分、酸碱）)
                elif Type == 4:

                    try:

                        DB = TinyDB(f'DB/db_{Zzqy[0]}.db')
                        #获取对应解决方案
                        Plan_info = db_Solution.search(Q.ID == Plan)[0]

                        if Plan_info['Des'] == '抢收':
                            DB.upsert({
                                'On': False
                            })

                        if Plan_info['Object'] == 'Yjf':
                            DB.update({
                                Plan_info['Yjf']: True
                            })
                        elif Plan_info['Object'] == 'H':

                            DB.update({
                                'H_way': True,
                                'H_cut': 0
                            })
                        elif Plan_info['Object'] == 'E':

                            DB.update({
                                'E_way': True,
                                'E_cut': 0
                            })
                        elif Plan_info['Object'] == 'H':

                            DB.update({
                                'PH_way': True,
                                'PH_cut': 0
                            })
                        else:
                            return {
                                'Start': False,
                                "message": "土壤改善方案处理传输失败"}, 200

                        return {
                            'Start': True,
                            "message": "土壤改善方案处理传输完成"}, 200
                    except:

                        return {
                            'Start': False,
                            "message": "土壤改善方案处理传输失败"}, 200

                #应急方案处理
                elif Type == 5:

                    try:

                        DB = TinyDB(f'DB/db_{Zzqy[0]}.db')
                        # 获取对应解决方案
                        Plan_info = db_Solution.search(Q.ID == Plan)[0]

                        if Plan_info['Des'] == '抢收':
                            DB.upsert({
                                'On': False
                            })


                        return {
                            'Start': True,
                            "message": "应急方案处理传输完成"}, 200
                    except:

                        return {
                            'Start': False,
                            "message": "应急方案处理传输失败"}, 200

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 200

