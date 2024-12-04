from tinydb import Query
from DB_TinyDB import db_Yaoji, db_Sundry

"""
:param Plot_map:种植区域信息表
:param Crop_Info:作物信息
:param Szjd:阶段
:param Crop_Check_config:作物校验参数配置
:param Crop_Check_Y:阶段校验
:param Ggfs:灌注方式
:param Sfzl:补给种类
:param Datas:当前农作物共享数据表
:param expect:预计产量
"""

def Check(Plot_map,Crop_Info, Szjd, Crop_Check_config, Crop_Check_Y, Datas, expect):


    Q = Query()


    Check_Y = Crop_Info.search(Q.ID == Szjd)[0].get('Check_Y', None)  # 获取当前校验

    if int(Check_Y[-1]) == 0:
        Check_Y = Check_Y
    else:
        Check_Y = ('CK0'+ str(int(Check_Y[-1])-1))
    # Check_Y = ('CK0'+ str(int(Check_Y[-1])-1))

    Check_Data = Crop_Check_config.search(Q.ID == 'Check_Y')[0]



    #获取已经喷施过的农药
    Y_list = Datas['All_Y']
    print('已经喷施过的农药',Y_list)

    Y_Effect_list = []

    #获取已经补给过的农药功能
    for i in Y_list:
        # 获取该药剂的功能作用
        Y_Effect = db_Yaoji.search(Q.ID == i)[0]['Effect']
        for i in Y_Effect:
            Y_Effect_list.append(i)

    #获取必要的药剂功能列表
    Y_Ftion_list = Crop_Check_Y.search(Q.ID == Check_Y)[0]['Ftion']

    def find_differences(list1, list2):
        set1 = set(list1)
        set2 = set(list2)

        # 找出在list1但不在list2中的元素
        diff1 = set1 - set2
        return diff1


    #计算差异
    list_y = find_differences(Y_Ftion_list, Y_Effect_list)

    for i in list_y:
        expect = Plot_map.all()[0]['expect']
        expect_cl = expect - expect * float(db_Sundry.all()[0]['Y_lack'])
        # 更新数据
        Plot_map.update({
            'expect': expect_cl,
            'IS_Job_Stop': True
        })




    for i in Y_list:

        # 获取该药剂的信息
        Check_Y_data = Crop_Check_Y.search(Q.ID == Check_Y)[0]

        Mu = Plot_map.all()[0]['Mu']
        Amount = float(db_Yaoji.search(Q.ID == i)[0]['Amount']) * float(Mu)  #获取该农药的标准量

        # Ty_pe = Check_Y_data.get('Type', None)
        B01 = float(Check_Y_data.get('B01', None))
        B02 = float(Check_Y_data.get('B02', None))
        B03 = float(Check_Y_data.get('B03', None))
        B04 = float(Check_Y_data.get('B04', None))
        B05 = float(Check_Y_data.get('B05', None))
        B06 = float(Check_Y_data.get('B06', None))
        # B07 = float(Check_Y_data.get('B07', None))
        # B08 = float(Check_Y_data.get('B08', None))

        S01 = float(Check_Y_data.get('S01', None))
        S02 = float(Check_Y_data.get('S02', None))
        S03 = float(Check_Y_data.get('S03', None))
        S04 = float(Check_Y_data.get('S04', None))
        S05 = float(Check_Y_data.get('S05', None))
        S06 = float(Check_Y_data.get('S06', None))
        # S07 = float(Check_Y_data.get('S07', None))
        # S08 = float(Check_Y_data.get('S08', None))

        # 检查是否校验过:
        if Datas['Is_Check_Y'] != 'T':

            all_y = sum(Y_list[i])  # 获取该农药的喷施总量

            # 补给量过多
            if all_y > Amount:

                if Check_Data['R01'] <= ((all_y - Amount) / Amount) < Check_Data['R02']:
                    expect_cl = expect - expect * S01
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R02'] <= ((all_y - Amount) / Amount) < Check_Data['R03']:
                    expect_cl = expect - expect * S02
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R03'] <= ((all_y - Amount) / Amount) < Check_Data['R04']:
                    expect_cl = expect - expect * S03
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R04'] <= ((all_y - Amount) / Amount) < Check_Data['R05']:
                    expect_cl = expect - expect * S04
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R05'] <= ((all_y - Amount) / Amount) < Check_Data['R06']:
                    expect_cl = expect - expect * S05
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif ((all_y - Amount) / Amount) >= Check_Data['R06']:
                    expect_cl = expect - expect * S06
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})


            # 补给量过少
            elif all_y <= Amount:
                if Check_Data['R01'] <= ((Amount - all_y) / Amount) < Check_Data['R02']:
                    expect_cl = expect - expect * B01
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R02'] <= ((Amount - all_y) / Amount) < Check_Data['R03']:
                    expect_cl = expect - expect * B02
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R03'] <= ((Amount - all_y) / Amount) < Check_Data['R04']:
                    expect_cl = expect - expect * B03
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R04'] <= ((Amount - all_y) / Amount) < Check_Data['R05']:
                    expect_cl = expect - expect * B04
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R05'] <= ((Amount - all_y) / Amount) < Check_Data['R06']:
                    expect_cl = expect - expect * B05
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif ((Amount - all_y) / Amount) >= Check_Data['R06']:
                    expect_cl = expect - expect * B06
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

            # 更改校验信息、清空补水量
            Plot_map.update({
                'All_Y': {},
                'Is_Check_Y': 'T'
            })



def Storage_info(Plot_map,Crop_Info, Szjd, Crop_Check_Y, Sfzl, Ggfs, Sfsl):


    Q = Query()

    try:
        Check_Y = Crop_Info.search(Q.ID == Szjd)[0].get('Check_Y', None)  # 获取校验
        Check_Y_data = Crop_Check_Y.search(Q.ID == Check_Y)  #获取当前校验阶段信息   需要进行的农药策略
        Y_info = db_Yaoji.search(Q.ID == Sfzl)[0]['Effect']
        Mu = Plot_map.all()[0]['Mu']  #获取地块亩数

        if len(Check_Y_data[0]['Ftion']) > 0 :


            print('当前阶段需要使用药剂')

            # 比较作业类型   #判断喷灌、滴灌
            Irrigate_Y_d = Check_Y_data[0][Ggfs]
            if Irrigate_Y_d == 'F':
                Sfsl_new = Sfsl * float(db_Sundry.all()[0]['Y_water'])
            else:
                Sfsl_new = Sfsl

            def contains_all_elements(arr1, arr2):
                set1 = set(arr1)
                set2 = set(arr2)
                return set1.issubset(set2)



            #检查该农药功能是否符合要求：符合
            if contains_all_elements(Y_info, Check_Y_data[0]['Ftion']) == True:

                print('当前药剂适合在该阶段使用: ',Sfzl)

                #获取农药字典
                doc = Plot_map.all()[0]['All_Y']

                #如果字典内没有该种类则创建
                if Sfzl not in doc:
                    doc[Sfzl] = []

                # 存储阶段农药量
                doc[Sfzl].append(Sfsl_new)
                Plot_map.update({
                    'All_Y': doc,
                    'IS_Job_Stop': True
                })

            # 检查该农药是否符合要求：不符合
            else:
                print('当前药剂不适合在该阶段使用')

                # 获取改药剂的标准使用量/亩
                SL = float(db_Yaoji.search(Q.ID == Sfzl)[0]['Amount']) * float(Mu)
                # 判断不合适的药剂使用量是否占标准使用量的两成：超过两成减产
                if float(Sfsl) / float(SL) > float(db_Sundry.all()[0]['Y_door']):
                    expect = Plot_map.all()[0]['expect']
                    expect_cl = expect - expect * float(db_Sundry.all()[0]['Y_disa'])
                    # 更新数据
                    Plot_map.update({
                        'expect': expect_cl
                    })
                Plot_map.update({
                    'IS_Job_Stop': True
                })
        else:

            print('当前药剂不适合在该阶段使用')

            #获取改药剂的标准使用量/亩
            SL = float(db_Yaoji.search(Q.ID == Sfzl)[0]['Amount']) * float(Mu)
            print(SL,Sfsl)


            if float(Sfsl) / float(SL) > float(db_Sundry.all()[0]['Y_door']):
                expect = Plot_map.all()[0]['expect']
                expect_cl = expect - expect * float(db_Sundry.all()[0]['Y_disa'])

                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })
                print(Plot_map.all)

            Plot_map.update({
                'IS_Job_Stop': True
            })

        print('农药成功')
    except:
        print('农药失败')


