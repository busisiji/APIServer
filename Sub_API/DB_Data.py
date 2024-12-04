import json

from flask_restful import Resource
from flask import request
from tinydb import Query

import IS_Job
from DB_TinyDB import *
from tinydb import TinyDB
import os
Q = Query()
Is_read ={'A':False,'B':False,'C':False}

# 基础地块
class Basics_Field(Resource):

    def get(self, prefix):
        global Is_read

        if prefix == 'info':

            Aim = request.args.get('Aim')
            Key = request.args.get('Key')
            if  Is_read[Aim]:
                return
            Is_read[Aim] = True

            if  (Aim not in ['A','B','C']) or (Aim == None):
                return {
                    'Status': False,
                    'message': 'Aim参数有误！'}, 400
            if Aim == 'A':
                qy = 'A1'
            elif Aim == 'B':
                qy = 'B2'
            elif Aim == 'C':
                qy = 'C3'
            try:
                Data_N = IS_Job.Job_data(qy=qy, feiliao_type='N')
                Data_P = IS_Job.Job_data(qy=qy, feiliao_type='P')
                Data_K = IS_Job.Job_data(qy=qy, feiliao_type='K')
                Data_D = IS_Job.Job_data(qy=qy, feiliao_type='D')
                Data_E = IS_Job.Job_data(qy=qy, feiliao_type='E')
                Data_PH = IS_Job.Job_data(qy=qy, feiliao_type='PH')
                Data_T = IS_Job.Job_data(qy=qy, feiliao_type='T')/10
                Data_H = IS_Job.Job_data(qy=qy, feiliao_type='H')

                DB_Aim = TinyDB(f'DB/db_{Aim}.json')
                DB_Aim.update({'N': Data_N}, doc_ids=[1])
                DB_Aim.update({'P': Data_P}, doc_ids=[1])
                DB_Aim.update({'K': Data_K}, doc_ids=[1])
                DB_Aim.update({'D': Data_D}, doc_ids=[1])
                DB_Aim.update({'E': Data_E}, doc_ids=[1])
                DB_Aim.update({'PH': Data_PH}, doc_ids=[1])
                DB_Aim.update({'T': Data_T}, doc_ids=[1])
                DB_Aim.update({'H': Data_H}, doc_ids=[1])
            except Exception as e:
                print('读取错误',e)
            DB_Aim = TinyDB(f'DB/db_{Aim}.json')
            if Aim == "A":
                Is_read["B"] = False
            elif Aim == "B":
                Is_read["C"] = False
            elif Aim == "C":
                Is_read["A"] = False
            if Key == 'all' or Key == None:

                return {'Datas': DB_Aim.all()[0]}

            elif Key == 'Soil':

                return {
                    'Status': True,
                    'N': DB_Aim.all()[0]['N'],
                    'P': DB_Aim.all()[0]['P'],
                    'K': DB_Aim.all()[0]['K'],
                    'D': DB_Aim.all()[0]['D'],
                    'E': DB_Aim.all()[0]['E'],
                    'PH': DB_Aim.all()[0]['PH'],
                    'T': DB_Aim.all()[0]['T'],
                    'H': DB_Aim.all()[0]['H']
                }, 200


            elif Key in DB_Aim.all()[0]:

                return {
                    'Status': True,
                    'Data': DB_Aim.all()[0][Key]
                }, 200

            else:
                return {
                    'Status': False,
                    'message': '参数有误！'}, 200

        elif prefix == 'stop':

            Aim = request.args.get('Aim')

            if  (Aim not in ['A','B','C']) or (Aim == None):
                return {
                    'Status': False,
                    'message': 'Aim参数有误！'}, 400

            try:

                DB_Aim = TinyDB(f'DB/db_{Aim}.json')

                return {
                    'Stop': DB_Aim.all()[0]['IS_Job_Stop'],
                    'message': '获取成功！'
                }, 200

            except:

                return {
                    'Stop': True,
                    'message': '获取失败！'
                }, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500


    def post(self,prefix):


        if prefix == 'add':

            data = request.json
            Aim = data['Aim']   #目标表
            Key = data['Key']   #字段
            Value = data['Value']    #参数


            if  (Aim not in ['A','B','C']) or (Aim == None) or (Key == None):
                return {
                    'Status': False,
                    'message': '参数有误！'}, 400

            DB_Aim = TinyDB(f'DB/db_{Aim}.json')

            # def update_key(doc):
            #     doc[Key] = Key  # 更新email字段的值
            #     return doc
            #
            # DB_Aim.update(update_key, doc_ids=[1])
            try:

                if Value ==  None:
                    Value = ''
                DB_Aim.update({Key: Value},doc_ids=[1])
                return {
                    'Status': True,
                    'message': '新增成功！',
                    'Data' : DB_Aim.all()[0]
                }, 200
            except:
                return {
                    'Status': False,
                    'message': '新增失败！'}, 400

        elif prefix == 'del':

            data = request.json
            Aim = data['Aim']   #目标表
            Key = data['Key']   #字段

            if  (Aim not in ['A','B','C']) or (Aim == None) or (Key == None):
                return {
                    'Status': True,
                    'message': '参数有误！'}, 400

            try:
                DB_Aim = TinyDB(f'DB/db_{Aim}.json')

                def remove_key(doc):
                    if Key in doc:
                        del doc[Key]
                    return doc

                DB_Aim.update(remove_key,doc_ids=[1])
                return {
                    'Status': True,
                    'message': '已删除'
                }, 200

            except:

                return {
                    'Status': False,
                    'message': '删除失败！'}, 400

        elif prefix == 'put':

            data = request.json

            Aim = data['Aim']   #目标表
            Key = data['Key']   #字段
            Value = data['Value']    #参数

            if  Aim not in ['A','B','C']:
                return {
                    'Status': False,
                    'message': 'Aim参数有误！'}, 400

            try:

                DB_Aim = TinyDB(f'DB/db_{Aim}.json')
                DB_Aim.update({Key: Value}, doc_ids=[1])
                return {
                    'Status': True,
                    'message': '更新成功！'}, 200

            except:

                return {
                    'Status': True,
                    'message': '更新失败！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

# 基础农作物
class Basics_Corp(Resource):

    def get(self, prefix):


        if prefix == 'info':

            Corp = request.args.get('Corp')
            Key = request.args.get('Key')

            if Corp == None :
                return {
                    'Status': False,
                    'message': '缺少必要的参数'}, 400

            # DB = TinyDB(f'DB/db_Crop.json')
            Names = [user['Name'] for user in db_Crop.search(Q.Name.exists())]

            if Corp == 'all':

                return {'Datas': db_Crop.all()}, 200

            elif Corp in Names:

                if Key == 'all' or Key == None:

                    return {
                        'Status': True,
                        'Data': db_Crop.search(Q.Name == Corp)[0]}, 200

                else:

                    try:
                        return {
                            'Status': True,
                            'Data': db_Crop.search(Q.Name == Corp)[0][Key]}, 200
                    except:
                        return {
                            'Status': False,
                            'message': '参数有误！'}, 400

            else:
                return {
                    'Status': False,
                    'message': '参数有误！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500


    def post(self,prefix):

        if prefix == 'add':

            data = request.json
            Name = data['Name']
            Type = data['Type']
            N = data['N']
            P = data['P']
            K = data['K']
            Stage = data['Stage']


            if  (Name == None or Type == None or (N == None or P == None or K == None)):
                return {
                    'Status': False,
                    'message': '新增失败！参数有误！或为空！'}, 400



            else:
                # DB = TinyDB(f'DB/db_Crop.json')
                ID = 'CR' + str(int(db_Crop.all()[-1]['ID'][2:5]) + 1)
                try:
                    Datas = {
                        'ID': ID,
                        'Name': Name,
                        'Type': Type,
                        'Des': Name,
                        'Com_info' : f'{Name}_Info',
                        'Com_soil': f'{Name}_Soil_Back',
                        'Check_config': f'{Name}_Check_Config',
                        'CK_F': f'{Name}_Check_F',
                        'CK_S': f'{Name}_Check_S',
                        'CK_G': f'{Name}_Check_G',
                        'CK_Y': f'{Name}_Check_Y',
                        'CK_M': f'{Name}_Check_M',
                        'N': N,
                        'P': P,
                        'K': K,
                        'Stage':Stage,
                        'Greenhouse': f'{Name}_Greenhouse_Info'
                    }

                    # DB = TinyDB(f'DB/db_Crop.json')
                    db_Crop.insert(Datas)

                    folder_path = f'Crop_Check/{Name}'
                    os.makedirs(folder_path, exist_ok=True)

                    TinyDB(f'Crop_DB/{Name}/{Name}_Info.json')
                    TinyDB(f'Crop_DB/{Name}/{Name}_Soil_Back.json')
                    TinyDB(f'Crop_DB/{Name}/{Name}_Check_Config.json')
                    TinyDB(f'Crop_DB/{Name}/{Name}_Check_F.json')
                    TinyDB(f'Crop_DB/{Name}/{Name}_Check_S.json')
                    TinyDB(f'Crop_DB/{Name}/{Name}_Check_G.json')
                    TinyDB(f'Crop_DB/{Name}/{Name}_Check_Y.json')
                    TinyDB(f'Crop_DB/{Name}/{Name}_Check_M.json')
                    TinyDB(f'Crop_DB/{Name}/{Name}_Greenhouse_Info.json')


                    return {
                        'Status': True,
                        'message': '新增成功！',
                        'ID': ID,
                        'Name': Name,
                        'Type': Type,
                        'Des': Name,
                        'Com_info': f'{Name}_Info',
                        'Com_soil': f'{Name}_Soil_Back',
                        'Check_config': f'{Name}_Check_Config',
                        'CK_F': f'{Name}_Check_F',
                        'CK_S': f'{Name}_Check_S',
                        'CK_G': f'{Name}_Check_G',
                        'CK_Y': f'{Name}_Check_Y',
                        'CK_M': f'{Name}_Check_M',
                        'N': N,
                        'P': P,
                        'K': K,
                        'Stage': Stage,
                        'Greenhouse': f'{Name}_Greenhouse_Info'
                    }, 200
                except:
                    return {
                        'Status': False,
                        'message': '新增失败！'}, 400


        elif prefix == 'del':

            data = request.json
            ID = data['ID']


            if ID is None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数！'}), 400

            try:
                IDs = [i['ID'] for i in db_Crop.search(Q.ID.exists())]
                # DB = TinyDB(f'DB/db_Crop.json')

                if ID not in IDs:
                    data = db_Crop.search(Q.ID == ID)[0]
                    Name = data['Des']
                    Com_info = data['Com_info']
                    Com_soil = data['Com_soil']
                    Check_config = data['Check_config']
                    CK_F = data['CK_F']
                    CK_S = data['CK_S']
                    CK_G = data['CK_G']
                    CK_Y = data['CK_Y']
                    CK_M = data['CK_M']
                    Greenhouse = data['Greenhouse']

                    db_path_1 = f'Crop_DB/{Name}/{Com_info}.json'
                    db_path_2 = f'Crop_DB/{Name}/{Com_soil}.json'
                    db_path_3 = f'Crop_DB/{Name}/{Check_config}.json'
                    db_path_4 = f'Crop_DB/{Name}/{CK_F}.json'
                    db_path_5 = f'Crop_DB/{Name}/{CK_S}.json'
                    db_path_6 = f'Crop_DB/{Name}/{CK_G}.json'
                    db_path_7 = f'Crop_DB/{Name}/{CK_Y}.json'
                    db_path_8 = f'Crop_DB/{Name}/{CK_M}.json'
                    db_path_9 = f'Crop_DB/{Name}/{Greenhouse}.json'

                    db_paths = [
                        db_path_1,
                        db_path_2,
                        db_path_3,
                        db_path_4,
                        db_path_5,
                        db_path_6,
                        db_path_7,
                        db_path_8,
                        db_path_9
                    ]


                    try:
                        db_Crop.remove(Q.ID == ID)
                        for i in db_paths:
                            if os.path.exists(i):
                                os.remove(i)
                        folder_path = f'Crop_Check/{Name}'
                        folder_path.unlink()
                        return {
                            'Status': True,
                            'message': '已删除'
                        }, 200
                    except:
                        return {
                            'Status': False,
                            'message': '删除失败！'}, 400


            except:

                return {
                    'Status': False,
                    'message': '删除失败！'}, 400


        elif prefix == 'put':

            data = request.json

            ID = data['ID']
            Key = data['Key']  # 字段
            Value = data['Value']  # 参数

            if ID is None or Key is None or Value is None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数'}), 400

            # DB = TinyDB(f'DB/db_Crop.json')
            IDs = [i['ID'] for i in db_Crop.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400

            else:

                try:

                    db_Crop.update({Key: Value}, (Q.ID == ID))
                    return {
                        'Status': True,
                        'message': '更新成功！',
                        'Data': db_Crop.search(Q.ID == ID)[0]
                    }, 200

                except:

                    return {
                        'Status': False,
                        'message': '更新失败！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

# 基础肥料
class Basics_Feiliao(Resource):

    def get(self, prefix):


        if prefix == 'info':

            Name = request.args.get('Name')
            Key = request.args.get('Key')

            if Name == None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数'}), 400

            DB = TinyDB(f'DB/db_Feiliao.json')
            Names = [user['Name'] for user in db_Feiliao.search(Q.Name.exists())]


            if Name == 'all':

                return {
                    'Status': True,
                    'Datas': DB.all()}, 200

            elif Name in Names:

                if Key == 'all' or Key == None:

                    return {
                        'Status': True,
                        'Data': DB.search(Q.Name == Name)[0]}, 200

                else:

                    try:
                        return {
                            'Status': True,
                            'Data': DB.search(Q.Name == Name)[0][Key]}, 200
                    except:
                        return {
                            'Status': False,
                            'message': '参数有误！'}, 400

            else:
                return {
                    'Status': False,
                    'message': '参数有误！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500


    def post(self,prefix):

        if prefix == 'add':

            data = request.json

            Name = data['Name']
            Content = data['Content']
            Eff = data['Eff']
            Raise = data['Raise']
            Type = data['Type']

            if  (Name == None or Content == None or Eff == None or Raise == None or Type == None):
                return {
                    'Status': False,
                    'message': '新增失败！参数错误！或为空！'}, 400

            else:
                # DB = TinyDB(f'DB/db_Feiliao.json')
                ID = 'L' + str(int(db_Feiliao.all()[-1:]['ID'][1:3]) + 1)

                try:
                    Datas = {
                        'ID': ID,
                        'Name': Name,
                        'Content' : float(Content),
                        'Eff': float(Eff),
                        'Raise': float(Raise),
                        'Type': Type
                    }


                    DB = TinyDB(f'DB/db_Feiliao.json')
                    DB.insert(Datas)
                    return {
                        'Status': True,
                        'message': '新增成功！',
                        'ID': ID,
                        'Name': Name,
                        'Content': float(Content),
                        'Eff': float(Eff),
                        'Raise': float(Raise),
                        'Type': Type

                    }, 200

                except:
                    return {
                        'Status': False,
                        'message': '新增失败！'}, 400


        elif prefix == 'del':

            data = request.json
            ID = data['ID']

            # DB = TinyDB(f'DB/db_Feiliao.json')
            IDs = [i['ID'] for i in db_Feiliao.search(Q.ID.exists())]


            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400

            else:

                try:

                    db_Feiliao.remove(Q.ID == ID)
                    return {
                        'Status': True,
                        'message': '已删除'
                    }, 200

                except:

                    return {
                        'Status': False,
                        'message': '删除失败！'}, 400


        elif prefix == 'put':

            data = request.json

            ID = data['ID']
            Key = data['Key']  # 字段
            Value = data['Value']  # 参数

            if ID is None or Key is None or Value is None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数'}), 400


            # DB = TinyDB(f'DB/db_Feiliao.json')
            IDs = [i['ID'] for i in db_Feiliao.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400

            else:

                try:

                    db_Feiliao.update({Key: Value}, (Q.ID == ID) )
                    return {
                        'Status': True,
                        'message': '更新成功！',
                        'Data': db_Feiliao.search(Q.ID == ID)[0]
                    }, 200

                except:

                    return {
                        'Status': False,
                        'message': '更新失败！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

# 基础药剂
class Basics_Yaoji(Resource):

    def get(self, prefix):

        if prefix == 'info':

            Name = request.args.get('Name')
            Key = request.args.get('Key')

            DB = TinyDB(f'DB/db_Yaoji.json')
            Names = [i['Name'] for i in db_Yaoji.search(Q.Name.exists())]

            if Name == 'all':

                return {
                    'Status': True,
                    'Datas': DB.all()}, 200

            elif Name in Names:

                if Key == 'all':

                    return {
                        'Status': True,
                        'Data': DB.search(Q.Name == Name)[0]}, 200

                else:

                    try:
                        return {
                            'Status': False,
                            'Data': DB.search(Q.Name == Name)[0][Key]}, 200
                    except:
                        return {
                            'Status': False,
                            'message': '参数有误！'}, 400

            else:
                return {
                    'Status': False,
                    'message': '参数有误！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

    def post(self, prefix):

        if prefix == 'add':

            data = request.json

            Name = data['Name']
            Type = data['Type']
            Effect = data['Effect']
            Des = data['Des']


            if (Type != 'Y' or Type != 'G') or (Name is None or Effect is None or Des is None):
                return {
                    'Status': False,
                    'message': '新增失败！ID参数有误！'}, 400



            else:
                # DB = TinyDB(f'DB/db_Yaoji.json')
                ID = 'Y' + str(int(db_Yaoji.all()[-1:]['ID'][1:3]) + 1)
                try:
                    Datas = {
                        'ID': ID,
                        'Name': Name,
                        'Effect': Effect,
                        'Des': Des
                    }

                    # DB = TinyDB(f'DB/db_Yaoji.json')
                    db_Yaoji.insert(Datas)
                    return {
                        'Status': True,
                        'message': '新增成功！',
                        'ID': ID,
                        'Name': Name,
                        'Effect': Effect,
                        'Des': Des
                    }, 200

                except:
                    return {
                        'Status': False,
                        'message': '新增失败！'}, 400

        elif prefix == 'del':

            data = request.json
            ID = data['ID']

            # DB = TinyDB(f'DB/db_Yaoji.json')
            IDs = [i['ID'] for i in db_Yaoji.search(Q.ID.exists())]

            if ID not in IDs :
                return ({
                    'Status': False,
                    'message': 'ID参数错误!'}), 400

            try:

                db_Yaoji.remove(Q.ID == ID)
                return {
                    'Status': True,
                    'message': '已删除'
                }, 200

            except:

                return {
                    'Status': False,
                    'message': '删除失败！'}, 400

        elif prefix == 'put':

            data = request.json

            ID = data['ID']
            Key = data['Key']  # 字段
            Value = data['Value']  # 参数

            if ID is None or Key is None or Value is None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数'}), 400

            # DB = TinyDB(f'DB/db_Yaoji.json')
            IDs = [i['ID'] for i in db_Yaoji.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400

            else:

                try:
                    db_Yaoji.update({Key: Value}, (Q.ID == ID))
                    return {
                        'Status': True,
                        'message': '更新成功！',
                        'Data': db_Yaoji.search(Q.ID == ID)[0]
                    }, 200

                except:

                    return {
                        'Status': False,
                        'message': '更新失败！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

# 基础药剂功能
class Basics_Yaoji_Effect(Resource):

    def get(self, prefix):

        if prefix == 'info':

            ID = request.args.get('ID')
            Effect = request.args.get('Effect')

            DB = TinyDB(f'DB/db_Yaoji_Effect.json')
            IDs = [i['ID'] for i in db_Yaoji_Effect.search(Q.ID.exists())]

            if ID == 'all':

                return {
                    'Status': True,
                    'Datas': DB.all()}, 200

            elif ID in IDs:

                if Effect == 'all':

                    return {
                        'Status': True,
                        'Data': DB.search(Q.ID == ID)[0]}, 200

                else:

                    try:
                        return {
                            'Status': True,
                            'Data': DB.search(Q.ID == ID)[0][Effect]}, 200

                    except:
                        return {
                            'Status': False,
                            'message': '参数有误！'}, 400

            else:
                return {
                    'Status': False,
                    'message': '参数有误！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

    def post(self, prefix):

        if prefix == 'add':

            data = request.json
            Des = data['Des']


            if Des == None :
                return {
                    'Status': False,
                    'message': '新增失败！ID参数有误！'}, 400

            else:

                #获取数据
                db_Yaoji_Effect_Lsatone = TinyDB('DB/db_Yaoji_Effect.json').all()[-1:][0]
                ID = 'E' + str(int((db_Yaoji_Effect_Lsatone['ID'])[1:3]) + 1)
                Effect = int(db_Yaoji_Effect_Lsatone['Effect']) + 1

                try:
                    Datas = {
                        'ID': ID,
                        'Effect': Effect,
                        'Des': Des
                    }

                    DB = TinyDB(f'DB/db_Yaoji_Effect.json')
                    DB.insert(Datas)
                    return {
                        'Status': True,
                        'message': '新增成功！',
                        'ID': ID,
                        'Effect': Effect,
                        'Des': Des
                    }, 200

                except:
                    return {
                        'Status': False,
                        'message': '新增失败！'}, 400

        elif prefix == 'del':

            data = request.json
            ID = data['ID']


            # DB = TinyDB(f'DB/db_Yaoji_Effect.json')
            IDs = [i['ID'] for i in db_Yaoji_Effect.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数错误!'}, 400

            else:
                try:
                    db_Yaoji_Effect.remove(Q.ID == ID)
                    return {
                        'Status': True,
                        'message': '已删除'
                    }, 200

                except:

                    return {
                        'Status': False,
                        'message': '删除失败！'}, 400

        elif prefix == 'put':

            data = request.json

            ID = data['ID']
            Key = data['Key']  # 字段
            Value = data['Value']  # 参数

            if ID is None or Key is None or Value is None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数'}), 400

            # DB = TinyDB(f'DB/db_Yaoji_Effect.json')
            IDs = [i['ID'] for i in db_Yaoji_Effect.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400
            else:
                try:

                    db_Yaoji_Effect.update({Key: Value}, (Q.ID == ID))
                    return {
                        'message': '更新成功！',
                        'Data': db_Yaoji_Effect.search(Q.ID == ID)[0]
                    }, 200


                except:

                    return {
                        'Status': False,
                        'message': '更新失败！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

# 全国土壤区域
class Soil(Resource):


    def get(self, prefix):

        if prefix == 'info':

            Name = request.args.get('Name')
            Key = request.args.get('Key')

            DB = TinyDB(f'DB/db_Soil.json')
            Names = [i['Name'] for i in db_Soil.search(Q.Name.exists())]

            if Name == 'all':

                return {
                    'Status': True,
                    'Datas': DB.all()}, 200

            elif Name in Names:

                if Key == 'all':

                    return {
                        'Status': True,
                        'Data': DB.search(Q.Name == Name)[0]}, 200

                else:

                    try:
                        return {
                            'Status': True,
                            'Data': DB.search(Q.Name == Name)[0][Key]}, 200
                    except:
                        return {
                            'Status': False,
                            'message': '参数有误！'}, 400

            else:
                return {
                    'Status': False,
                    'message': '参数有误！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

    def post(self, prefix):

        if prefix == 'add':

            data = request.json

            Name = data['Name']
            Join = data['Join']



            if Name == None or Join == None:
                return {
                    'Status': False,
                    'message': '新增失败！ID参数有误！'}, 400
            else:

                #获取数据
                db_Yaoji_Effect_Lsatone = TinyDB('DB/db_Soil.json').all()[-1:][0]
                ID = 'S' + str(int((db_Yaoji_Effect_Lsatone['ID'])[1]) + 1)


                try:
                    Datas = {
                        'ID': ID,
                        'Name': Name,
                        'Join': Join,
                    }


                    DB = TinyDB(f'DB/db_Soil.json')
                    DB.insert(Datas)

                    TinyDB(f'DB/db_{Join}.json')

                    return {
                        'Status': True,
                        'message': '新增成功！',
                        'ID': ID,
                        'Name': Name,
                        'Join': Join
                        }, 200

                except:
                    return {
                        'Status': False,
                        'message': '新增失败！'}, 400

        elif prefix == 'del':

            data = request.json
            ID = data['ID']

            # DB = TinyDB(f'DB/db_Soil.json')
            IDs = [i['ID'] for i in db_Soil.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数错误!'}, 400
            else:

                try:

                    Join = db_Soil.search(Q.ID == ID)[0]['Join']
                    db_Soil.remove(Q.ID == ID)

                    db_path = f'DB/db_{Join}.json'
                    if os.path.exists(db_path):
                        os.remove(db_path)

                    else:
                        return {
                            'Status': False,
                            'message': '删除失败！为找到指定文件'}, 400

                    return {
                        'Status': True,
                        'message': '已删除'
                    }, 200


                except:

                    return {
                        'Status': False,
                        'message': '删除失败！'}, 400

        elif prefix == 'put':

            data = request.json

            ID = data['ID']
            Key = data['Key']  # 字段
            Value = data['Value']  # 参数

            if ID is None  or Key is None or Value is None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数'}), 400

            # DB = TinyDB(f'DB/db_Soil.json')
            IDs = [i['ID'] for i in db_Soil.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400
            else:

                try:

                    db_Soil.update({Key: Value}, (Q.ID == ID))
                    return {
                        'Status': True,
                        'message': '更新成功！',
                        'Data': db_Soil.search(Q.ID == ID)[0]
                    }, 200

                except:

                    return {
                        'Status': False,
                        'message': '更新失败！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

# 土壤区域相关土壤种类
class Soil_info(Resource):


    def get(self, prefix):

        if prefix == 'info':


            ID = request.args.get('ID')  #地区编号
            Name = request.args.get('Name')
            Rank = request.args.get('Rank')


            if ID == None or Name == None or Rank == None:
                return {
                    'Status': False,
                    'message': '新增失败！参数有空！'}, 400

            db_Soil = TinyDB('DB/db_Soil.json')
            IDs = [i['ID'] for i in db_Soil.search(Q.ID.exists())]

            if ID in IDs:
                DB_Name = db_Soil.search(Q.ID == ID)[0]['Join']
                DB = TinyDB(f'DB/db_{DB_Name}.json')
                Names = [i['Name'] for i in DB.search(Q.Name.exists())]

                if Name == 'all':

                    return {
                        'Status': True,
                        'Datas': DB.all()}, 200

                elif Name in Names:

                    if Rank == 'all':

                        return {
                            'Status': True,
                            'Data': DB.search(Q.Name == Name)}, 200

                    else:

                        try:
                            return {
                                'Status': True,
                                'Data': DB.search((Q.Name == Name) & (Q.ID == Rank ))}, 200
                        except:
                            return {
                                'Status': False,
                                'message': '参数有误！'}, 400

            else:
                return {
                    'Status': False,
                    'message': '参数有误！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500


    def post(self,prefix):

        if prefix == 'add':

            data = request.json

            ID = data['ID']  # 地区编号
            Name = data['Name']
            RankID = data['Rank']

            if ID == None or Name == None or RankID == None:
                return {
                    'Status': False,
                    'message': '新增失败！参数有空！'}, 400

            # DB = TinyDB('DB/db_Soil.json')
            IDs = [i['ID'] for i in db_Soil.search(Q.ID.exists())]


            if ID in IDs:
                DB_Name = db_Soil.search(Q.ID == ID)[0]['Join']
                DB = TinyDB(f'DB/db_{DB_Name}.json')

                Des = 'S' + str(int(DB.all()[-1]['Des']) + 1)

                try:
                    DB.insert_multiple([

                        {'ID': f'{RankID}_L', 'Des': Des, 'Name': Name, 'NB': '', 'PB': '', 'KB': '', 'NS': '', 'PS': '', 'KS': ''},
                        {'ID': f'{RankID}_M', 'Des': Des, 'Name': Name, 'NB': '' ,'PB': '', 'KB': '' ,'NS': '', 'PS': '', 'KS': ''},
                        {'ID': f'{RankID}_H', 'Des': Des, 'Name': Name, 'NB': '', 'PB': '', 'KB': '', 'NS': '', 'PS': '', 'KS': ''}

                    ])

                    return {
                        'Status': True,
                        'message': '新增成功！',

                        }, 200
                except:
                    return {
                        'Status': False,
                        'message': '新增失败！'}, 400

            else:
                return {
                    'Status': False,
                    'message': '新增失败！ID参数有误！'}, 400

        elif prefix == 'del':

            data = request.json

            SoilID = data['ID']  # 地区编号
            Dec = data['Dec']

            DB = TinyDB(f'DB/db_Soil.json')
            SoilIDs = [i['ID'] for i in DB.search(Q.ID.exists())]

            if SoilID not in SoilIDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400

            else:
                try:
                    # db_Soil = TinyDB('DB/db_Soil.json')
                    DB_Name = db_Soil.search(Q.ID == SoilID)[0]['Join']
                    DB = TinyDB(f'DB/db_{DB_Name}.json')

                    Decs = [i['ID'] for i in DB.search(Q.Dec.exists())]
                    if Dec not in Decs:
                        return {
                            'Status': False,
                            'message': 'Dec参数有误！'}, 400
                    else:
                        DB.remove(Q.Dec == Dec)

                        return {
                            'Status': True,
                            'message': '已删除'
                        }, 200

                except:

                    return {
                        'Status': False,
                        'message': '删除失败！'}, 400

        elif prefix == 'put':

            data = request.json

            SoilID = data['SoilID']
            ID = data['ID']
            Key = data['Key']  # 字段
            Value = data['Value']  # 参数

            if SoilID is None or ID is None or Key is None or Value is None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数'}), 400

            # DB = TinyDB(f'DB/db_Soil.json')
            SoilIDs = [i['ID'] for i in db_Soil.search(Q.SoilID.exists())]

            if SoilID not in SoilIDs:
                return {
                    'Status': False,
                    'message': 'SoilID参数有误！'}, 400

            else:

                try:

                    DB_Name = db_Soil.search(Q.ID == ID)[0]['Join']
                    DB = TinyDB(f'DB/db_{DB_Name}.json')
                    IDs = [i['ID'] for i in DB.search(Q.ID.exists())]
                    if ID not in IDs:
                        return {'message': 'ID参数有误！'}, 400
                    else:
                        DB.update({Key: Value},(Q.ID == ID))
                        return {
                            'Status': True,
                            'message': '更新成功！',
                            'Data': DB.search(Q.ID == ID)[0]
                        }, 200


                except:

                    return {
                        'Status': False,
                        'message': '更新失败！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

# 用于土壤的设备信息
class Soil_Device_info(Resource):


    def get(self,prefix):

        if prefix == 'info':


            ID = request.args.get('ID')  #地区编号
            Place = request.args.get('Place')



            if ID == None or Place == None:
                return {
                    'Status': False,
                    'message': '参数有空！'}, 400

            # DB = TinyDB('DB/db_Soil_Device_info.json')

            if ID == 'all':
                return {'Datas': db_Soil_Device_info.all()}, 200

            else:

                IDs = [i['ID'] for i in db_Soil_Device_info.search(Q.ID.exists())]

                if ID in IDs:

                    if Place == 'all':

                        return {
                            'Status': True,
                            'Data': db_Soil_Device_info.search(Q.ID == ID)[0]}, 200

                    else:

                        try:
                            return {'Data': db_Soil_Device_info.search((Q.ID == ID) & (Q.Place == Place))[0]}, 200
                        except:
                            return {
                                'Status': False,
                                'message': '参数有误！'}, 400

                else:
                    return {
                        'Status': False,
                        'message': '参数有误！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500


    def post(self,prefix):

        if prefix == 'add':

            data = request.json

            Place = data['Place']
            Type = data['Type']
            Name = data['Name']
            Gateway = data['Gateway']
            IP = data['IP']
            Port = data['Port']
            Addr = data['Addr']
            Start = data['Start']
            End = data['End']

            if Place == None or Type == None or Name == None or Gateway == None or IP == None or Port == None or Addr == None or Start == None or End == None:
                return {
                    'Status': False,
                    'message': '新增失败！参数有空！'}, 400


            else:

                try:
                    # DB = TinyDB('DB/db_Soil_Device_info.json')
                    ID = 'Dev' + str(int(db_Soil_Device_info.all()[-1:]['ID'][1:4]) + 1)

                    db_Soil_Device_info.insert({
                        'ID': ID,
                        'Place': Place,
                        'Type': Type,
                        'Name': Name,
                        'Gateway': Gateway,
                        'IP': IP,
                        'Port': Port,
                        'Addr': Addr,
                        'Start': Start,
                        'End': End

                    })


                    return {
                        'Status': True,
                        'message': '已新增',
                        'ID': ID,
                        'Place': Place,
                        'Type': Type,
                        'Name': Name,
                        'Gateway': Gateway,
                        'IP': IP,
                        'Port': Port,
                        'Addr': Addr,
                        'Start': Start,
                        'End': End
                            }, 200
                except:
                    return {
                        'Status': False,
                        'message': '新增失败！'}, 400

        if prefix == 'del':

            data = request.json
            ID = data['ID']

            # DB = TinyDB('DB/db_Soil.json')
            IDs = [i['ID'] for i in db_Soil.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400

            else:

                try:
                    db_Soil.remove(Q.ID == ID)
                    return {
                        'Status': True,
                        'message': '已删除'
                    }, 200
                except:
                    return {
                        'Status': False,
                        'message': '删除失败'
                    }, 200

        elif prefix == 'put':

            data = request.json

            ID = data['ID']
            Key = data['Key']  # 字段
            Value = data['Value']  # 参数

            if ID is None  or Key is None or Value is None:
                return ({'message': '缺少必要的参数'}), 400

            # DB = TinyDB('DB/db_Soil_Device_info.json')
            IDs = [i['ID'] for i in db_Soil_Device_info.search(Q.ID.exists())]
            if ID not in IDs:
                return {'message': 'ID参数有误！'}, 400
            else:

                try:

                    db_Soil_Device_info.update({Key: Value}, (Q.ID == ID))
                    return {
                        'message': '更新成功！',
                        'Data': db_Soil_Device_info.search(Q.ID == ID)[0]
                        }, 200

                except:

                    return {'message': '更新失败！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

# 土壤的土测值
class Soil_Start(Resource):

    def get(self,prefix):

        if prefix == 'info':

            ID = request.args.get('ID')
            Key = request.args.get('Key')

            if ID == None:
                return {
                    'Status': False,
                    'message': '参数有空！'}, 400

            # DB = TinyDB('DB/db_Soil_Start.json')

            if ID == 'all':
                return {'Datas': db_Soil_Start.all()}, 200

            else:

                IDs = [i['ID'] for i in db_Soil_Start.search(Q.ID.exists())]

                if ID in IDs:

                    if Key == 'all' or Key == None:

                        return {
                            'Status': True,
                            'Data': db_Soil_Start.search(Q.ID == ID)[0]}, 200

                    else:

                        try:
                            return {'Data': db_Soil_Start.search((Q.ID == ID) & (Q.Place == Key))[0]}, 200
                        except:
                            return {
                                'Status': False,
                                'message': '参数有误！'}, 400

                else:
                    return {
                        'Status': False,
                        'message': '参数有误！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

    def post(self,prefix):


        if prefix == 'add':
            data = request.json

            ID = data['ID']
            Des = data['Des']
            N = data['N']
            P = data['P']
            K = data['K']
            S = data['S']
            E = data['E']
            PH = data['PH']
            T = data['T']
            H = data['H']
            N_eff = data['N_eff']
            P_eff = data['P_eff']
            K_eff = data['K_eff']

            if ID == None or Des == None or N == None or P == None or K == None or S == None or E == None or PH == None or T == None or H == None or N_eff == None or P_eff == None or K_eff == None:
                return {
                    'Status': False,
                    'message': '新增失败！参数有空！'}, 400

            # DB = TinyDB('DB/db_Soil_Start.json')
            IDs = [i['ID'] for i in db_Soil_Start.search(Q.ID.exists())]

            if ID in IDs:
                return {
                        'Status': False,
                        'message': '已有冲突的ID'
                    }, 200

            else:
                try:

                    db_Soil_Device_info.insert({
                        'ID': ID,
                        'Des': Des,
                        'N': N,
                        'P': P,
                        'K': K,
                        'S': S,
                        'E': E,
                        'PH': PH,
                        'T': T,
                        'H': H,
                        'N_eff': N_eff,
                        'P_eff': P_eff,
                        'K_eff': K_eff
                    })

                    return {
                        'Status': True,
                        'message': '已新增'}, 200
                except:
                    return {
                        'Status': False,
                        'message': '新增失败！'}, 400

        elif prefix == 'del':

            data = request.json
            ID = data['ID']



            # DB = TinyDB('DB/db_Soil_Start.json')
            IDs = [i['ID'] for i in db_Soil_Start.search(Q.ID.exists())]

            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400

            else:
                try:
                    db_Soil_Device_info.remove(Q.ID == ID)
                    return {
                        'Status': True,
                        'message': '已删除'
                    }, 200


                except:
                    return {
                        'Status': False,
                        'message': '删除失败'
                    }, 200

        elif prefix == 'put':

            data = request.json

            ID = data['ID']
            Key = data['Key']  # 字段
            Value = data['Value']  # 参数

            if ID is None  or Key is None or Value is None:
                return ({
                    'Status': False,
                    'message': '缺少必要的参数'}), 400

            # DB = TinyDB('DB/db_Soil_Start.json')
            IDs = [i['ID'] for i in db_Soil_Start.search(Q.ID.exists())]
            if ID not in IDs:
                return {
                    'Status': False,
                    'message': 'ID参数有误！'}, 400
            else:

                try:

                    # DB = TinyDB('DB/db_Soil_Start.json')
                    db_Soil_Start.update({Key: Value}, (Q.ID == ID))

                    return {
                        'Status': True,
                        'message': '更新成功！',
                        'Data': db_Soil_Start.search(Q.ID == ID)[0]
                        }, 200

                except:

                    return {
                        'Status': False,
                        'message': '更新失败！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500

class Sundry(Resource):

    def get(self,prefix):

        if prefix == 'info':

            try:
                data = db_Soil_Start.all()[0]

                return {
                    'Status': True,
                    'Data': data}, 200
            except:

                return {
                    'Status': False,
                    'message': '参数有误！'}, 400

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500


    def post(self,prefix):

        if prefix == 'add':
            data = request.json

            Key = data['Key']
            Value = data['Value']

            if (Key == None) or (Value == None):
                return {
                    'Status': False,
                    'message': '新增失败！参数有空！'}, 400

            if Key in db_Sundry.all()[0]:
                return {
                    'Status': False,
                    'message': '新增失败！已有冲突的Key！'}, 400
            else:
                db_Sundry.update({Key: Value},doc_ids=[1])
                return {
                    'Status': True,
                    'message': '已新增',
                    'Data': db_Sundry.all()[0]
                }, 200

        elif prefix == 'put':
            data = request.json
            Key = data['Key']
            Value = data['Value']

            if (Key == None) or (Value == None):
                return {
                    'Status': False,
                    'message': '更新失败！参数有空！'}, 400

            if Key not in db_Sundry.all()[0]:
                return {
                    'Status': False,
                    'message': '更新失败！Key不存在！'}, 400
            else:
                db_Sundry.update({Key: Value},doc_ids=[1])
                return {
                    'Status': True,
                    'message': '已更新',
                    'Data': db_Sundry.all()[0]
                }, 200

        elif prefix == 'del':
            data = request.json
            Key = data['Key']
            # Value = data['Value']

            if (Key == None):
                return {
                    'Status': False,
                    'message': '删除失败！参数有空！'}, 400

            if Key not in db_Sundry.all()[0]:
                return {
                    'Status': False,
                    'message': '删除失败！Key不存在！'}, 400
            else:

                def remove_key(doc):
                    if Key in doc:
                        del doc[Key]
                    return doc

                db_Sundry.update(remove_key,doc_ids=[1])
                return {
                    'Status': True,
                    'message': '已删除',
                    'Data': db_Sundry.all()[0]
                }, 200

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 500