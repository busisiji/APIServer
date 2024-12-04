from tinydb import Query
from DB_TinyDB import db_Feiliao, db_Sundry




def Check(Plot_map, Crop_Info, Szjd, Crop_Check_config, Crop_Check_M, Datas, expect):

    Q = Query()

    Check_M = Crop_Info.search(Q.ID == Szjd)[0].get('Check_M', None)  # 获取当前校验

    if int(Check_M[-1]) == 0:
        Check_M = Check_M
    else:
        Check_M = ('CK0'+ str(int(Check_M[-1])-1))

    Check_Data = Crop_Check_config.search(Q.ID == 'Check_M')[0]

    # 获取已经喷施过的农药
    M_list = Datas['All_M']

    for i in M_list:

        Check_M_data = Crop_Check_M.search(Q.ID == Check_M)[0]

        Mu = Plot_map.all()[0]['Mu']
        Amount = float(db_Feiliao.search(Q.ID == i)[0]['Content']) * float(Mu)  # 获取该微量元素的标准量


        B01 = float(Check_M_data.get('B01', None))
        B02 = float(Check_M_data.get('B02', None))
        B03 = float(Check_M_data.get('B03', None))
        B04 = float(Check_M_data.get('B04', None))
        B05 = float(Check_M_data.get('B05', None))
        B06 = float(Check_M_data.get('B06', None))
        # B07 = float(Check_M_data.get('B07', None))
        # B08 = float(Check_M_data.get('B08', None))

        S01 = float(Check_M_data.get('S01', None))
        S02 = float(Check_M_data.get('S02', None))
        S03 = float(Check_M_data.get('S03', None))
        S04 = float(Check_M_data.get('S04', None))
        S05 = float(Check_M_data.get('S05', None))
        S06 = float(Check_M_data.get('S06', None))
        # S07 = float(Check_M_data.get('S07', None))
        # S08 = float(Check_M_data.get('S08', None))
        print(Datas['Is_Check_M'])
        # 检查是否校验过:
        if Datas['Is_Check_M'] != 'T':

            all_m = sum(M_list[i])  # 获取该微量元素的喷施总量

            # 补给量过多
            if all_m > Amount:

                if Check_Data['R01'] <= ((all_m - Amount) / Amount) < Check_Data['R02']:
                    expect_cl = expect - expect * S01
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R02'] <= ((all_m - Amount) / Amount) < Check_Data['R03']:
                    expect_cl = expect - expect * S02
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R03'] <= ((all_m - Amount) / Amount) < Check_Data['R04']:
                    expect_cl = expect - expect * S03
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R04'] <= ((all_m - Amount) / Amount) < Check_Data['R05']:
                    expect_cl = expect - expect * S04
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R05'] <= ((all_m - Amount) / Amount) < Check_Data['R06']:
                    expect_cl = expect - expect * S05
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif ((all_m - Amount) / Amount) >= Check_Data['R06']:
                    expect_cl = expect - expect * S06
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})


            # 补给量过少
            elif all_m <= Amount:

                if Check_Data['R01'] <= ((Amount - all_m) / Amount) < Check_Data['R02']:
                    expect_cl = expect - expect * B01
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R02'] <= ((Amount - all_m) / Amount) < Check_Data['R03']:
                    expect_cl = expect - expect * B02
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R03'] <= ((Amount - all_m) / Amount) < Check_Data['R04']:
                    expect_cl = expect - expect * B03
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R04'] <= ((Amount - all_m) / Amount) < Check_Data['R05']:
                    expect_cl = expect - expect * B04
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif Check_Data['R05'] <= ((Amount - all_m) / Amount) < Check_Data['R06']:
                    expect_cl = expect - expect * B05
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

                elif ((Amount - all_m) / Amount) >= Check_Data['R06']:
                    expect_cl = expect - expect * B06
                    # 更新数据
                    Plot_map.update({'expect': expect_cl})

            # 更改校验信息、清空补给量
            Plot_map.update({
                'All_M': {},
                'Is_Check_M': 'T'
            })



def Storage_info(Plot_map, Crop_Info, Szjd, Crop_Check_M, Sfzl, Ggfs, Sfsl):



    Q = Query()
    try:
        Check_M = Crop_Info.search(Q.ID == Szjd)[0].get('Check_M', None)  # 获取校验
        Check_M_data = Crop_Check_M.search(Q.Ftion == Check_M)  # 获取当前阶段需要的微量元素

        # 比较作业类型   #判断喷灌、滴灌
        Irrigate_G_d = Check_M_data[Ggfs]
        if Irrigate_G_d == 'F':
            Sfsl_new = Sfsl * float(db_Sundry.all()[0]['M_water'])
        else:
            Sfsl_new = Sfsl

        # 检查该肥料是否符合要求

        if Sfzl in Check_M_data:

            # 获取字典
            doc = Plot_map.all()[0]['All_M']

            # 如果字典内没有该种类则创建
            if Sfzl not in doc:
                doc[Sfzl] = []

            # 存储阶段肥料量
            doc[Sfzl].append(Sfsl_new)
            Plot_map.update({
                'All_M': doc,
                'IS_Job_Stop': True

            })

        # 不符合
        else:

            expect = Plot_map.all()[0]['expect']
            expect_cl = expect - expect * float(db_Sundry.all()[0]['M_disa'])
            # 更新数据
            Plot_map.update({
                'expect': expect_cl,
                'IS_Job_Stop': True

            })
        Plot_map.update({'IS_Job_Stop': True})
        print('微量元素成功')

    except:
        print('微量元素失败')
