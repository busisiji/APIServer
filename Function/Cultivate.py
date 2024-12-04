"""
土壤种植系统

肥料方案处理（氮磷钾、水、微量元素）
药剂方案处理（农药、调节剂）

反馈土壤问题

"""

from flask_restful import Resource
from flask import request
from tinydb import Query
from DB_TinyDB import *
from Mod.Check import Soil_back  #Soil_E_back,Soil_PH_back,Soil_H_back
import Crop_Check
from Thread import Cultivate_F_Thread,Cultivate_S_Thread,Cultivate_G_Thread,Cultivate_Y_Thread,Cultivate_M_Thread
# from tinydb import TinyDB



Q = Query()
T = int(db_Sundry.all()[0]['Thread'])
from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor(max_workers = T)

#模拟种植API
class Cultivate(Resource):



    def post(self, prefix):

        #种植前准备
        if prefix == 'ready':

            data = request.json
            Nzw = data['Crop']   #种植农作物
            Qy = data['Region']   #种植区域
            Cl = data['Expect']    #目标产量



            # 根据不同区域插入数据到不同的数据库
            db_map = {'A1': db_A, 'B2': db_B, 'C3': db_C}
            if Qy in db_map:

                Soil_v = db_Soil_Start.search(Q.ID == Qy)[0]



                if db_map[f'{Qy}'].all()[0]['On'] == True:
                    return {
                        'Ready': False,
                        'message': '土地正在种植中！'
                    }, 200
                else:
                    # 清空老数据
                    db_map[f'{Qy}'].truncate()

                db_map[f'{Qy}'].insert({
                    # 生成json: 农作物、区域、目标产量、有机肥、状态
                    'Nzw': Nzw, 'Qy': Qy, 'Cl': float(Cl), 'Yjf': False, 'On': True,
                    # 土壤反馈数据：氮磷钾、含水、电导率、PH、温度、湿度、
                    'Mu' : Soil_v.get('Mu',None),
                    'N': Soil_v.get('N',None),
                    'P': Soil_v.get('P',None),
                    'K': Soil_v.get('K',None),
                    'D': Soil_v.get('D',None),
                    'E': Soil_v.get('E',None),
                    'PH': Soil_v.get('PH',None),
                    'T': Soil_v.get('T',None),
                    'H': Soil_v.get('H',None),
                    # 总量
                    'All_N': [0], 'All_P': [0], 'All_K': [0],
                    'All_S': [0], 'All_G': {}, 'All_Y': {},
                    'All_M': [],
                    # 预期产量,加成,
                    'expect': float(Cl),'boost': 0,'stage':'','IS_Job_Stop':True,
                    #肥料阶段占比
                    'Ratio_N':[0],'Ratio_P':[0],'Ratio_K':[0],
                    #肥料锁
                    'lock_N': 'F', 'lock_P': 'F', 'lock_K': 'F',
                    #是否校验
                    'Is_Check_N':'F', 'Is_Check_P':'F', 'Is_Check_K':'F',
                    'Is_Check_S':'F', 'Is_Check_G':'F', 'Is_Check_Y':'F', 'Is_Check_M':'F',

                    'H_cut': 0, 'E_cut': 0, 'PH_cut': 0, 'Qx_cut': 0, 'Cq_cut': 0, 'Sj_cut': 0,
                    'H_way': False, 'E_way': False, 'PH_way': False

                })

                # print(len(db_map[f'{Qy}']))
                #获取土壤初始值
                # Soil_S_D = db_Soil_Start.search(Q.ID == Qy)[0]
                # soil_data = {
                #     'Mu': Soil_S_D['Mu'],
                #     'N': Soil_S_D['N'],
                #     'P': Soil_S_D['P'],
                #     'K': Soil_S_D['K'],
                #     'S': Soil_S_D['S'],
                #     'E': Soil_S_D['E'],
                #     'PH': Soil_S_D['PH'],
                #     'T': Soil_S_D['T'],
                #     'H': Soil_S_D['H']
                # }
                # db_map[f'{Qy}'].update(soil_data)
                # print(db_map[f'{Qy}'].all())

                return {
                    'Ready': True,
                    'message': '开始模拟'
                }, 200
            else:
                return {
                    'Ready': False,
                    'message': '参数传入错误'
                }, 200


        #种植开始
        if prefix == 'start':


            data = request.json
            Zzqy = data['Region']  #种植区域
            Szjd = data['Stage']  #生长阶段
            Sflx = data['Type']  #补给类型
            Sfzl = data['Species']  #补给种类
            Sfsl = data['Amount']  #补给量
            Ggfs = data['Water']  #灌溉方式

            try:

                Plot_map = TinyDB(f'DB/db_{Zzqy[0]}.json')

                if Plot_map.all()[0]['On'] == False :
                    return {
                        'Start': False,
                        "message": "没有提前种植准备"}, 200

                if Plot_map.all()[0]['IS_Job_Stop'] == False:
                    return {
                        'Start': False,
                        "message": "有方案进行中"}, 200

                Plot_map.update({'IS_Job_Stop': False})



                if Plot_map.all()[0]['stage'] != Szjd:

                    Data_cut = Plot_map.all()[0]

                    #判断是否有土壤改善
                    H_cut = float(Data_cut['H_cut'])
                    E_cut = float(Data_cut['E_cut'])
                    PH_cut = float(Data_cut['PH_cut'])

                    Qx_cut = float(Data_cut['Qx_cut'])
                    Cq_cut = float(Data_cut['Cq_cut'])
                    Sj_cut = float(Data_cut['Sj_cut'])


                    expect = Data_cut['PH_cut'] - (Data_cut['PH_cut'] * H_cut)
                    expect = expect - (expect * E_cut)
                    expect = expect - (expect * PH_cut)

                    expect = expect - (expect * Qx_cut)
                    expect = expect - (expect * Cq_cut)
                    expect = expect - (expect * Sj_cut)


                    Plot_map.update({
                        'expect': expect,

                        'lock_N': 'F',
                        'lock_P': 'F',
                        'lock_K': 'F',

                        'Is_Check_N':'F', 'Is_Check_P':'F', 'Is_Check_K':'F',
                        'Is_Check_S':'F', 'Is_Check_G':'F', 'Is_Check_Y':'F', 'Is_Check_M':'F',

                        'H_cut': 0, 'E_cut': 0, 'PH_cut': 0, 'Qx_cut': 0, 'Cq_cut': 0, 'Sj_cut': 0,
                        'H_way': False, 'E_way': False, 'PH_way': False

                    })


                    print('更新是否校验')


                # 查询数据库
                Datas = Plot_map.all()[0]
                print('数据表数据：',Datas)
                nzw = Datas.get('Nzw', '0')  # 当前农作物
                print('当前农作物: ',nzw)
                print('补给量: ',Sfsl)


                Com_file = db_Crop.search(Q.ID == nzw)[0] # 当前农作物对应数据表
                print('对应农作物数据表: ',Com_file)

                Crop_Info = TinyDB(f"Crop_DB/{Com_file['Des']}/{Com_file['Com_info']}.json")
                Crop_Soil_Back = TinyDB(f"Crop_DB/{Com_file['Des']}/{Com_file['Com_soil']}.json")
                Crop_Check_config = TinyDB(f"Crop_DB/{Com_file['Des']}/{Com_file['Check_config']}.json")
                Crop_Check_F = TinyDB(f"Crop_DB/{Com_file['Des']}/{Com_file['CK_F']}.json")
                Crop_Check_S = TinyDB(f"Crop_DB/{Com_file['Des']}/{Com_file['CK_S']}.json")
                Crop_Check_G = TinyDB(f"Crop_DB/{Com_file['Des']}/{Com_file['CK_G']}.json")
                Crop_Check_Y = TinyDB(f"Crop_DB/{Com_file['Des']}/{Com_file['CK_Y']}.json")
                Crop_Check_M = TinyDB(f"Crop_DB/{Com_file['Des']}/{Com_file['CK_M']}.json")

                # 拉取所有检验时刻
                Check_F = Crop_Info.search(Q.ID == Szjd)[0]['Check_F']  # 获取肥料检验
                Check_S = Crop_Info.search(Q.ID == Szjd)[0]['Check_S']  # 获取肥料检验
                Check_G = Crop_Info.search(Q.ID == Szjd)[0]['Check_G']  # 获取肥料检验
                Check_Y = Crop_Info.search(Q.ID == Szjd)[0]['Check_Y']  # 获取肥料检验
                Check_M = Crop_Info.search(Q.ID == Szjd)[0]['Check_M']  # 获取肥料检验


                qy = Datas['Qy']  # 当前农作物种植区域
                print('当前农作物种植区域: ',qy)
                mubiaocl = float(Datas.get('Cl', '0'))  # 目标产量
                print('目标产量: ',mubiaocl)
                expect = float(Datas.get('expect', '0'))  # 预计产量
                print('预计产量: ',expect)



                if Datas['stage'] != Szjd:
                    Soil_back(Q, Datas, Szjd, Crop_Soil_Back, Plot_map)



                #当前需要校验
                Check_F_N = Crop_Check_F.search(Q.ID == Check_F)[0]['N']
                Check_F_P = Crop_Check_F.search(Q.ID == Check_F)[0]['P']
                Check_F_K = Crop_Check_F.search(Q.ID == Check_F)[0]['K']



                #检查是否有氮磷钾校验
                if Check_F_N != 'F' or Check_F_P != 'F' or Check_F_K != 'F':

                    print('\n----------  进入大量元素肥料校验  ----------')




                    Soil_element_N = float(db_Soil_Start.search(Q.ID == qy)[0].get('N', '0'))  # 土壤预设数据-氮
                    Soil_element_P = float(db_Soil_Start.search(Q.ID == qy)[0].get('P', '0'))  # 土壤预设数据-磷
                    Soil_element_K = float(db_Soil_Start.search(Q.ID == qy)[0].get('K', '0'))  # 土壤预设数据-钾

                    # print('土壤预设数据: ', Soil_element)

                    F_eff_N = float(db_Soil_Start.search(Q.ID == qy)[0].get('N_eff', '0'))  # 土壤矫正系数-氮
                    F_eff_P = float(db_Soil_Start.search(Q.ID == qy)[0].get('P_eff', '0'))  # 土壤矫正系数-磷
                    F_eff_K = float(db_Soil_Start.search(Q.ID == qy)[0].get('K_eff', '0'))  # 土壤矫正系数-钾

                    # print('土壤矫正系数: ', F_eff)

                    ZB_N = float(Crop_Info.search(Q.ID == Szjd)[0].get('N', '0'))  # 当前阶段肥料量占比
                    ZB_P = float(Crop_Info.search(Q.ID == Szjd)[0].get('P', '0'))  # 当前阶段肥料量占比
                    ZB_K = float(Crop_Info.search(Q.ID == Szjd)[0].get('K', '0'))  # 当前阶段肥料量占比

                    # print('当前阶段肥料量占比: ', ZB_N)

                    print('当前生长阶段:', Datas['stage'])
                    print('新的生长阶段:', Szjd)

                    # 检查是否储存过肥料系数占比  检查当前肥料是否上锁
                    if Datas[f'lock_N'] != 'T':
                        # 储存阶段施肥量占比
                        Scale_list = Plot_map.all()[0]['Ratio_N']
                        Scale_list.append(ZB_N)

                        # 更新肥料系数、当前生长阶段、肥料锁
                        Plot_map.update({
                            'Ratio_N': Scale_list,
                            'lock_N': 'T'
                        })

                    if Datas[f'lock_P'] != 'T':
                        # 储存阶段施肥量占比
                        Scale_list = Plot_map.all()[0]['Ratio_P']
                        Scale_list.append(ZB_P)

                        # 更新肥料系数、当前生长阶段、肥料锁
                        Plot_map.update({
                            'Ratio_P': Scale_list,
                            'lock_P': 'T'
                        })

                    if Datas[f'lock_K'] != 'T':
                        # 储存阶段施肥量占比
                        Scale_list = Plot_map.all()[0]['Ratio_K']
                        Scale_list.append(ZB_K)

                        # 更新肥料系数、当前生长阶段、肥料锁
                        Plot_map.update({
                            'Ratio_K': Scale_list,
                            'lock_K': 'T'
                        })

                        print('++++++++++++++++++++++++++++++  已储存阶段施肥量占比: ', Plot_map.all()[0]['Ratio_N'])


                    Crop_Check.Crop_Check_F.Check(
                        Check_F_N,
                        Check_F_P,
                        Check_F_K,
                        Nzw = nzw,
                        Crop_Info = Crop_Info,
                        Plot_map = Plot_map,
                        Szjd = Szjd,
                        Crop_Check_F = Crop_Check_F,
                        mubiaocl = mubiaocl,
                        expect = expect,
                        Soil_element_N = Soil_element_N,
                        Soil_element_P=Soil_element_P,
                        Soil_element_K=Soil_element_K,
                        F_eff_N = F_eff_N,
                        F_eff_P = F_eff_P,
                        F_eff_K = F_eff_K,

                    )

                if Check_S != 'F':
                    print('+++  进入补水校验  +++')

                    Crop_Check.Crop_Check_S.Check(
                        Plot_map=Plot_map,
                        Crop_Info=Crop_Info,
                        Szjd=Szjd,
                        Crop_Check_config=Crop_Check_config,
                        Crop_Check_S=Crop_Check_S,
                        Datas=Datas,
                        expect=expect,
                    )

                if Check_G != 'F':
                    print('+++  进入调节剂校验  +++')

                    Crop_Check.Crop_Check_G.Check(
                        Plot_map=Plot_map,
                        Crop_Info=Crop_Info,
                        Szjd=Szjd,
                        Crop_Check_config=Crop_Check_config,
                        Crop_Check_G=Crop_Check_G,
                        Datas=Datas,
                        expect=expect,
                    )

                if Check_Y != 'F':
                    print('+++  进入农药校验  +++')
                    Crop_Check.Crop_Check_Y.Check(
                        Plot_map=Plot_map,
                        Crop_Info=Crop_Info,
                        Szjd=Szjd,
                        Crop_Check_config=Crop_Check_config,
                        Crop_Check_Y=Crop_Check_Y,
                        Datas=Datas,
                        expect=expect,
                    )

                if Check_M != 'F':
                    print('+++  进入微量元素肥料校验  +++')

                    Crop_Check.Crop_Check_M.Check(
                        Plot_map=Plot_map,
                        Crop_Info=Crop_Info,
                        Szjd=Szjd,
                        Crop_Check_config=Crop_Check_config,
                        Crop_Check_M = Crop_Check_M,
                        Datas=Datas,
                        expect=expect,
                    )
                    # 如果需要返回查询结果



                #判断是否为大量元素肥料
                if Sflx == 'F1':

                    print('\n----------  进入大量元素肥料作业  ----------')


                    hanliang = float(db_Feiliao.search(Q.ID == Sfzl)[0].get('Content', '0'))  # 当前肥料有效含量
                    print('当前肥料有效含量: ', hanliang)
                    liyonglv = float(db_Feiliao.search(Q.ID == Sfzl)[0].get('Eff', '0'))  # 当前肥料土壤利用率
                    print('当前肥料土壤利用率: ', liyonglv)
                    tisheng = float(Datas.get('boost', '0'))  # 当前肥料土壤效率提升
                    print('当前肥料土壤效率提升: ', tisheng)
                    feiliao_type = db_Feiliao.search(Q.ID == Sfzl)[0].get('Type', '0')  # 当前肥料类型
                    print('当前肥料类型: ', feiliao_type)
                    F_eff = float(db_Soil_Start.search(Q.ID == qy)[0].get(f'{feiliao_type}_eff', '0'))  # 土壤矫正系数-氮/磷/钾
                    print('土壤矫正系数: ', F_eff)

                    pool.submit(
                        Cultivate_F_Thread,
                        qy,Crop_Info,Plot_map,Szjd,Crop_Check_F,
                        feiliao_type,Sfsl,hanliang,liyonglv,tisheng,F_eff,Ggfs
                    )


                    print('++++++++++++++++++++++++++++++  当前最高产量: ', Plot_map.all()[0]['expect'])


                    return {
                        'Start': True,
                        "message": "施肥方案传输完成"}, 200

                # 补水校验
                elif Sflx == 'F4':

                    print('----------  当前为补水作业  ----------')


                    pool.submit(
                        Cultivate_S_Thread,
                        qy,Plot_map,Crop_Info,Szjd,Crop_Check_S,Ggfs,Datas,Crop_Soil_Back,Sfsl
                    )

                    return {
                        'Start': True,
                        "message": "补水方案传输完成"}, 200

                # 调节剂校验
                elif Sflx == 'Y4':

                    print('----------  当前为调节剂作业  ----------')

                    pool.submit(
                        Cultivate_G_Thread,
                        qy,Plot_map,Crop_Info,Szjd,Crop_Check_G,Sfzl,Ggfs,Sfsl
                    )

                    return {
                        'Start': True,
                        "message": "调节剂方案传输完成"}, 200

                # 农药校验
                elif Sflx == 'Y1' or Sflx == 'Y2' or Sflx == 'Y3':

                    print('----------  当前为农药作业  ----------')

                    pool.submit(
                        Cultivate_Y_Thread,
                        qy,Plot_map,Crop_Info,Szjd,Crop_Check_Y,Sfzl,Ggfs,Sfsl
                    )

                    return {
                        'Start': True,
                        "message": "农药方案传输完成"}, 200

                # 微量元素校验
                elif Sflx == 'F2' or Sflx == 'F3':

                    print('----------  当前为微量元素作业  ----------')

                    pool.submit(
                        Cultivate_M_Thread,
                        qy,Plot_map,Crop_Info,Szjd,Crop_Check_M,Sfzl,Ggfs,Sfsl
                    )

                    return {
                        'Start': True,
                        "message": "微量元素方案传输完成"}, 200

                return {
                    'Start': True,
                    "message": "方案传输完成"}, 200
            except:

                return {
                    'Start': False,
                    "message": "方案传输失败"}, 200


        #种植结束
        if prefix == 'end':

            data = request.json

            Qy = data['Region']   #种植区域

            # 根据不同区域插入数据到不同的数据库
            db_map = {'A1': db_A, 'B2': db_B, 'C3': db_C}

            if Qy in db_map:

                Datas = db_map[f'{Qy}'].all()[0]
                Nzw = Datas['Nzw']  # 种植农作物

                # 检查数据类型并转换
                def convert_to_float(value):
                    try:
                        return float(value)
                    except ValueError:
                        return 0  # 如果转换失败，返回0或其他默认值

                # 转换并计算总和
                S_ALL = sum(convert_to_float(value) for value in Datas["All_S"])

                # 同样的方法可以应用于其他变量
                N_ALL = sum(convert_to_float(value) for value in Datas['All_N'])
                P_ALL = sum(convert_to_float(value) for value in Datas['All_P'])
                K_ALL = sum(convert_to_float(value) for value in Datas['All_K'])

                G_ALL = (Datas['All_G'])  # 全部生长调节剂
                Y_ALL = (Datas["All_Y"])  # 全部农药
                M_ALL = (Datas["All_M"])  # 全部微量肥
                Yield = Datas['expect']  # 产量

                #更改土地使用状态
                db_map[f'{Qy}'].update({'On': False})


                return {
                    'End': True,
                    '种植农作物': Nzw,
                    '种植区域': Qy,
                    '全部施氮量': N_ALL,
                    '全部施磷量': P_ALL,
                    '全部施钾量': K_ALL,
                    '全部生长调节剂': G_ALL,
                    '全部农药': Y_ALL,
                    '全部微量肥': M_ALL,
                    '全部灌溉量': S_ALL,
                    '种植产量': Yield,
                    'message': '种植结束'
                }, 200
            else:
                return {
                    'End': False,
                    'message': '参数传入错误'
                }, 200

        else:

            return {
                'Status': False,
                'message': 'URL地址有误！'}, 200


