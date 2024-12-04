# from tinydb import TinyDB
from tinydb import Query
from DB_TinyDB import db_Soil_Start

Q = Query()

# A：每100kg需要的元素量
# B：目标产量（kg/亩）
# C：土测值
# D：土壤矫正系数
# E：肥料养分含量
# F：肥料利用率
# G：有机肥提升肥料利用率
max_params = 0.15
min_params = 0.08



def MAX(A,B,C,D,E):
    print(A,B,C,D,E)

    X = float(A) * float(B)    #有效需肥量
    T = (float(C)*2.25*float(D))/15    #土壤提供肥料量/亩
    print('有效需肥量',X)
    print('土壤提供肥料量/亩',T)

    # data = (X-T)/float(E)/(float(F)+float(G)) + (X-T)/float(E)/(float(F)+float(G))*max_params    #化肥上限
    data = ((X - T) * E) + ((X - T) * E * max_params)
    return round(data,2)

def MIN(A,B,C,D,E):
    print(A,B,C,D,E)

    X = float(A) * float(B)    #有效需肥量
    T = (float(C)*2.25*float(D))/15
    # data = (X-T)/float(E)/(float(F)+float(G)) - (X-T)/float(E)/(float(F)+float(G))*min_params

    data = ((X - T) * E) - ((X - T) * E * min_params)

    return round(data,2)


def SUI(A,B,C,D,E,F,G):
    X = A*B
    T = (C*2.25*D)/15
    data = (X-T)/E/(F+G)
    # print(round(data,2))
    return round(data,2)


def Soil_F_back(P,D):

    # print(P,E,F,G,D)


    #土测值提升幅度
    # return round(float(P)*float(E)*(float(F)+float(G))*15/float(D)/2.25,2)
    return round((float(P)*15)/2.25/float(D),2)

#反馈土壤 氮、磷、钾、温度、湿度、盐分、酸碱数据
def Soil_back(Q,Datas,Szjd,Crop_Soil_Back,Plot_map):
    # 获取旧土壤数据

    #获取有效施肥量
    # db_Soil_Start = TinyDB('DB/db_Soil_Start.json')
    F_eff_N = float(db_Soil_Start.search(Q.ID == Datas['Qy'])[0].get(f'N_eff', '0'))  # 土壤矫正系数-氮/磷/钾
    print('土壤矫正系数: ', F_eff_N)
    F_eff_P = float(db_Soil_Start.search(Q.ID == Datas['Qy'])[0].get(f'P_eff', '0'))  # 土壤矫正系数-氮/磷/钾
    print('土壤矫正系数: ', F_eff_P)
    F_eff_K = float(db_Soil_Start.search(Q.ID == Datas['Qy'])[0].get(f'K_eff', '0'))  # 土壤矫正系数-氮/磷/钾
    print('土壤矫正系数: ', F_eff_P)

    old_N_data = float(Datas['N'])  # 获取旧土壤数据
    old_P_data = float(Datas['P'])  # 获取旧土壤数据
    old_K_data = float(Datas['K'])  # 获取旧土壤数据

    N = float(sum(Datas[f'All_N']))
    P = float(sum(Datas[f'All_P']))
    K = float(sum(Datas[f'All_K']))

    T = Crop_Soil_Back.search(Q.ID == Szjd)[0]['T']
    # H = Crop_Soil_Back.search(Q.ID == Szjd)[0]['H']
    # E = Crop_Soil_Back.search(Q.ID == Szjd)[0]['E']
    # PH = Crop_Soil_Back.search(Q.ID == Szjd)[0]['PH']


    # 计算新土壤数据：根据施肥量
    N_Back_data = old_N_data - old_N_data * float(
        Crop_Soil_Back.search(Q.ID == Szjd)[0].get('N', '0')) + float(
        Soil_F_back(N,F_eff_N))

    P_Back_data = old_P_data - old_P_data * float(
        Crop_Soil_Back.search(Q.ID == Szjd)[0].get('P', '0')) + float(
        Soil_F_back(P,F_eff_P))

    K_Back_data = old_K_data - old_K_data * float(
        Crop_Soil_Back.search(Q.ID == Szjd)[0].get('K', '0')) + float(
        Soil_F_back(K,F_eff_K))

    print('反馈的氮土壤数据：', round(N_Back_data, 2))
    print('反馈的磷土壤数据：', round(P_Back_data, 2))
    print('反馈的钾土壤数据：', round(K_Back_data, 2))
    print('反馈的土壤温度数据：', T)
    # print('反馈的土壤湿度数据：', H)
    # print('反馈的土壤盐分数据：', E)
    # print('反馈的土壤酸碱数据：', PH)


    # 存储新的土壤数据到数据库
    Plot_map.update({
        'N': round(N_Back_data, 2),
        'P': round(P_Back_data, 2),
        'K': round(K_Back_data, 2),
        'T': T,
        # 'H': H,
        # 'E': E,
        # 'PH': PH,
        'stage': Szjd,

    })
    print('土壤反馈成功')


#反馈土壤湿度数据
def Soil_H_back(Sfsl,Soil_H,Way):

    Sfsl= float(Sfsl)
    Soil_H= float(Soil_H)
    print(Sfsl,Soil_H)

    if Way == True:

        return  '适中'

    TS = Sfsl * 0.75


    if 0 <= TS + Soil_H < 20 :

        return  '干旱'

    elif 20 <= TS + Soil_H < 40 :

        return  '缺水'

    elif 40 <= TS + Soil_H < 60 :

        return  '适中'

    elif 60 <= TS + Soil_H < 80 :

        return  '湿润'

    elif 80 <= TS + Soil_H < 100 :

        return  '潮湿'

    else:

        return  '积水'
#反馈土壤盐分数据
def Soil_E_back(Soil_E,Way):

    Soil_E= float(Soil_E)
    print(Soil_E)

    if Way == True:

        return  '适度盐分'


    if 0 <= Soil_E < 20 :

        return  '适度盐分'

    elif 20 <= Soil_E < 40 :

        return  '轻度盐分'

    elif 40 <= Soil_E < 60 :

        return  '中度盐分'

    elif 60 <= Soil_E < 80 :

        return  '重度盐分'

    elif 80 <= Soil_E:

        return  '极度盐分'

    else:

        return  '未知盐分'
#反馈土壤酸碱数据
def Soil_PH_back(Soil_PH,Way):

    Soil_PH= float(Soil_PH)
    print(Soil_PH)

    if Way == True:

        return  '适宜酸碱'


    if 0 <= Soil_PH < 4.0 :

        return  '重度酸化'

    elif 4.0 <= Soil_PH < 4.5 :

        return  '中度酸化'

    elif 4.5 <= Soil_PH < 5.5 :

        return  '轻度酸化'

    elif 5.5 <= Soil_PH < 8.5 :

        return  '适宜酸碱'

    elif 8.5 <= Soil_PH < 9.0 :

        return  '轻度碱化'

    elif 9.0 <= Soil_PH < 9.5 :

        return  '轻度碱化'

    elif 9.5 <= Soil_PH :

        return  '重度碱化'

    else:

        return  '未知酸碱'



def S_Greater_than(Plot_map,Check_Data,all_s,Amount,expect,S01,S02,S03,S04,S05,S06):

    try:

        R1 = float(Check_Data['R01'])
        R2 = float(Check_Data['R02'])
        R3 = float(Check_Data['R03'])
        R4 = float(Check_Data['R04'])
        R5 = float(Check_Data['R05'])
        R6 = float(Check_Data['R06'])

        all_s = float(all_s)
        Amount = float(Amount)
        expect = float(expect)

        S1 = float(S01)
        S2 = float(S02)
        S3 = float(S03)
        S4 = float(S04)
        S5 = float(S05)
        S6 = float(S06)


        if R1 <= ((all_s - Amount) / Amount) < R2:
            expect_cl = expect - expect * S1
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R2 <= ((all_s - Amount) / Amount) < R3:
            expect_cl = expect - expect * S2
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R3 <= ((all_s - Amount) / Amount) < R4:
            expect_cl = expect - expect * S3
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R4 <= ((all_s - Amount) / Amount) < R5:
            expect_cl = expect - expect * S4
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R5 <= ((all_s - Amount) / Amount) < R6:
            expect_cl = expect - expect * S5
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif ((all_s - Amount) / Amount) >= R6:
            expect_cl = expect - expect * S6
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})


    except:

        return False


def S_Less_than(Plot_map, Check_Data, all_s, Amount, expect, B01, B02, B03, B04, B05, B06):
    try:

        R1 = float(Check_Data['R01'])
        R2 = float(Check_Data['R02'])
        R3 = float(Check_Data['R03'])
        R4 = float(Check_Data['R04'])
        R5 = float(Check_Data['R05'])
        R6 = float(Check_Data['R06'])

        all_s = float(all_s)
        Amount = float(Amount)
        expect = float(expect)

        B1 = float(B01)
        B2 = float(B02)
        B3 = float(B03)
        B4 = float(B04)
        B5 = float(B05)
        B6 = float(B06)

        if R1 <= ((Amount - all_s) / Amount) < R2:
            expect_cl = expect - expect * B1
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R2 <= ((Amount - all_s) / Amount) < R3:
            expect_cl = expect - expect * B2
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R3 <= ((Amount - all_s) / Amount) < R4:
            expect_cl = expect - expect * B3
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R4 <= ((Amount - all_s) / Amount) < R5:
            expect_cl = expect - expect * B4
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R5 <= ((Amount - all_s) / Amount) < R6:
            expect_cl = expect - expect * B5
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif ((Amount - all_s) / Amount) >= R6:
            expect_cl = expect - expect * B6
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})


    except:

        return {"参数错误！！！"}, 500




def F_Greater_than(Plot_map,Check_Data,S01,S02,S03,S04,S05,S06,value,expect):

    try:

        R1 = float(Check_Data['R01'])
        R2 = float(Check_Data['R02'])
        R3 = float(Check_Data['R03'])
        R4 = float(Check_Data['R04'])
        R5 = float(Check_Data['R05'])
        R6 = float(Check_Data['R06'])

        value = float(value)
        expect = float(expect)

        S1 = float(S01)
        S2 = float(S02)
        S3 = float(S03)
        S4 = float(S04)
        S5 = float(S05)
        S6 = float(S06)


        if R1 <= value < R2:
            expect_cl = expect - expect * S1
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R2 <= value < R3:
            expect_cl = expect - expect * S2
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R3 <= value < R4:
            expect_cl = expect - expect * S3
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R4 <= value < R5:
            expect_cl = expect - expect * S4
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R5 <= value < R6:
            expect_cl = expect - expect * S5
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif value >= R6:
            expect_cl = expect - expect * S6
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})


    except:

        return


def F_Less_than(Plot_map, Check_Data, B01, B02, B03, B04, B05, B06,value,expect):
    try:

        R1 = float(Check_Data['R01'])
        R2 = float(Check_Data['R02'])
        R3 = float(Check_Data['R03'])
        R4 = float(Check_Data['R04'])
        R5 = float(Check_Data['R05'])
        R6 = float(Check_Data['R06'])

        value = float(value)
        expect = float(expect)

        B1 = float(B01)
        B2 = float(B02)
        B3 = float(B03)
        B4 = float(B04)
        B5 = float(B05)
        B6 = float(B06)

        if R1 <= value < R2:
            expect_cl = expect - expect * B1
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R2 <= value < R3:
            expect_cl = expect - expect * B2
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R3 <= value < R4:
            expect_cl = expect - expect * B3
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R4 <= value < R5:
            expect_cl = expect - expect * B4
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif R5 <= value < R6:
            expect_cl = expect - expect * B5
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})

        elif value >= R6:
            expect_cl = expect - expect * B6
            # 更新数据
            print('最高预计产量：', expect_cl)
            Plot_map.update({'expect': expect_cl})


    except:

        return






# MIN(3.33,6,120,0.7,0.46,0.35,0.15)
# SUI(3.33,6,120,0.7,0.46,0.35,0.15)
# Soil_back(0,0.46,0.35,0.15,0.7)