from tinydb import Query
from Mod.Check import Soil_H_back
from Mod.Check import S_Greater_than,S_Less_than
"""
:param Crop_Info:作物信息
:param Szjd:阶段
:param Crop_Check_S:阶段校验
:param Ggfs:灌注方式
:param Datas:当前农作物共享数据表
:param mubiaocl:目标产量
:param Sfsl:实际施水量
"""



def Check(Plot_map,Crop_Info,Szjd,Crop_Check_config,Crop_Check_S,Datas,expect):


    Q = Query()


    Check_S = Crop_Info.search(Q.ID == Szjd)[0].get('Check_S', None)  # 获取校验
    Check_Data = Crop_Check_config.search(Q.ID == 'Check_S')[0]
    Check_S_data = Crop_Check_S.search(Q.ID == Check_S)[0]

    print('校验标签：',Check_S)
    print('校验倍数：',Check_Data)
    print('校验系数：',Check_S_data)

    Mu = Plot_map.all()[0]['Mu']
    Amount = float(Check_S_data.get('Amount', None)) * float(Mu)  # 获取标准施水量
    expect = float(expect)

    print('当前准施水量:', Amount)
    print('已经补给过的水量: ', Datas['All_S'])
    print('是否进行过校验: ',Datas['Is_Check_S'])


    # Ty_pe = Check_S_data.get('Type', None)
    B01 = float(Check_S_data.get('B01', None))
    B02 = float(Check_S_data.get('B02', None))
    B03 = float(Check_S_data.get('B03', None))
    B04 = float(Check_S_data.get('B04', None))
    B05 = float(Check_S_data.get('B05', None))
    B06 = float(Check_S_data.get('B06', None))
    # B07 = float(Check_S_data.get('B07', None))
    # B08 = float(Check_S_data.get('B08', None))

    S01 = float(Check_S_data.get('S01', None))
    S02 = float(Check_S_data.get('S02', None))
    S03 = float(Check_S_data.get('S03', None))
    S04 = float(Check_S_data.get('S04', None))
    S05 = float(Check_S_data.get('S05', None))
    S06 =float(Check_S_data.get('S06', None))
    # S07 = Check_S_data.get('S07', None)
    # S08 = Check_S_data.get('S08', None)



    #检查是否校验过:
    if Datas['Is_Check_S'] != 'T':

        #获取全部补水量
        all_s = float(sum(Plot_map.all()[0]['All_S']))

        print('全部补水量：',all_s)

        #补水量过多
        if all_s > Amount:

            S_Greater_than(Plot_map,Check_Data,all_s,Amount,expect,S01,S02,S03,S04,S05,S06)

            # if Check_Data['R01'] <= ((all_s - Amount) / Amount) < Check_Data['R02']:
            #     expect_cl = mubiaocl - mubiaocl * S01
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif Check_Data['R02'] <= ((all_s - Amount) / Amount) < Check_Data['R03']:
            #     expect_cl = mubiaocl - mubiaocl * S02
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif Check_Data['R03'] <= ((all_s - Amount) / Amount) < Check_Data['R04']:
            #     expect_cl = mubiaocl - mubiaocl * S03
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif Check_Data['R04'] <= ((all_s - Amount) / Amount) < Check_Data['R05']:
            #     expect_cl = mubiaocl - mubiaocl * S04
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif Check_Data['R05'] <= ((all_s - Amount) / Amount) < Check_Data['R06']:
            #     expect_cl = mubiaocl - mubiaocl * S05
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif ((all_s - Amount) / Amount) >= Check_Data['R06']:
            #     expect_cl = mubiaocl - mubiaocl * S06
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})


        # 补水量过少
        elif all_s <= Amount:

            S_Less_than(Plot_map, Check_Data, all_s, Amount, expect, B01, B02, B03, B04, B05, B06)

            # if float(Check_Data['R01']) <= ((Amount - all_s) / Amount) < float(Check_Data['R02']):
            #     expect_cl = mubiaocl - mubiaocl * B01
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif float(Check_Data['R02']) <= ((Amount - all_s) / Amount) < float(Check_Data['R03']):
            #     expect_cl = mubiaocl - mubiaocl * B02
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif float(Check_Data['R03']) <= ((Amount - all_s) / Amount) < float(Check_Data['R04']):
            #     expect_cl = mubiaocl - mubiaocl * B03
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif float(Check_Data['R04']) <= ((Amount - all_s) / Amount) < float(Check_Data['R05']):
            #     expect_cl = mubiaocl - mubiaocl * B04
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif float(Check_Data['R05']) <= ((Amount - all_s) / Amount) < float(Check_Data['R06']):
            #     expect_cl = mubiaocl - mubiaocl * B05
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})
            #
            # elif ((Amount - all_s) / Amount) >= float(Check_Data['R06']):
            #     expect_cl = mubiaocl - mubiaocl * B06
            #     # 更新数据
            #     Plot_map.update({'expect': expect_cl})


        # 更改校验信息、清空补水量
        Plot_map.update({
            'All_S': [],
            'Is_Check_S': 'T'
        })


    return {"灌溉已实施"}, 201


def Storage_info(Plot_map,Crop_Info,Szjd,Crop_Check_S,Ggfs,Datas,Crop_Soil_Back,Sfsl):


    print("没有监测到补水动作")

    Q = Query()
    try:
        Check_S = Crop_Info.search(Q.ID == Szjd)[0].get('Check_S', None)  # 获取校验
        print(Check_S)
        Check_S_data = Crop_Check_S.search(Q.ID == Check_S)[0]
        print(Check_S_data)



        Irrigate_S_d = Check_S_data[Ggfs]
        print(Irrigate_S_d)

        # 比较作业类型   #判断喷灌、滴灌
        if Irrigate_S_d == 'F':
            Sfsl_new = Sfsl * 0.5
        else:
            Sfsl_new = Sfsl



        # 储存补水量
        S_V = Datas['All_S']
        S_V.append(Sfsl_new)
        Plot_map.update({
            'All_S': S_V,
            'IS_Job_Stop':True
        })

        print('已储存补水量！')

        # 反馈土壤数据
        Soil_S = Crop_Soil_Back.search(Q.ID == Szjd)[0] # 获取土壤值
        print(Soil_S)
        # 计算新土壤数据：根据施肥量
        H = Soil_H_back(Sfsl, Soil_S['H'])
        print(H)
        # 存储新的土壤数据到数据库
        Plot_map.update({'H': H})

        print('已储存补水量！已更新土壤数据！')

    except:

        print('参数错误！')




