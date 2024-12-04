
from DB_TinyDB import *
from Mod.Check import *


def Check( Check_F_N,Check_F_P,Check_F_K,Nzw,Crop_Info,Plot_map,Szjd,Crop_Check_F,mubiaocl,expect,Soil_element_N,Soil_element_P,Soil_element_K,F_eff_N,F_eff_P,F_eff_K):


    mubiaocl = float(mubiaocl)  # 目标产量
    expect = float(expect)
    Soil_element_N = float(Soil_element_N) #土壤预设数据-氮/磷/钾
    Soil_element_P = float(Soil_element_P) #土壤预设数据-氮/磷/钾
    Soil_element_K = float(Soil_element_K) #土壤预设数据-氮/磷/钾

    F_eff_N = float(F_eff_N)  # 土壤矫正系数-氮/磷/钾
    F_eff_P = float(F_eff_P)  # 土壤矫正系数-氮/磷/钾
    F_eff_K = float(F_eff_K)  # 土壤矫正系数-氮/磷/钾


    # print(Nzw,Crop_Info,Plot_map,Szjd,Crop_Check_F,mubiaocl,expect,Soil_element,hanliang,liyong_lv,tisheng,F_eff)


    Datas = Plot_map.all()[0]  #获取种植区域信息数据字典
    # print(Datas)

    Q = Query()
    Check_F = (Crop_Info.search(Q.ID == Szjd)[0].get('Check_F', None))  # 获取校验类型
    print('校验类型: ',Check_F)

    #获取校验表信息
    Verify_data = Crop_Check_F.search(Q.ID == Check_F)[0]
    print('校验表信息: ',Verify_data)

    Mu = Plot_map.all()[0]['Mu']
    Name = db_Crop.search(Q.ID == Nzw)[0]['Des']
    Check_config = db_Crop.search(Q.ID == Nzw)[0]['Check_config']
    Check_Data = (TinyDB(f'Crop_DB/{Name}/{Check_config}.json').search(Q.ID == 'Check_F'))[0]


    #有氮肥校验
    if Check_F_N != 'F':

        #判断是否校验过：
        if Datas['Is_Check_N'] != 'T':



            print('开始氮肥校验')
            Ratio = sum(Datas['Ratio_N'])  # 氮肥料量占比
            print('氮肥料量占比: ', Ratio)

            B01 = float(Verify_data['B01'])
            B02 = float(Verify_data['B02'])
            B03 = float(Verify_data['B03'])
            B04 = float(Verify_data['B04'])
            B05 = float(Verify_data['B05'])
            B06 = float(Verify_data['B06'])
            # B07 = float(Verify_data['B07'])
            # B08 = float(Verify_data['B08'])

            S01 = float(Verify_data['S01'])
            S02 = float(Verify_data['S02'])
            S03 = float(Verify_data['S03'])
            S04 = float(Verify_data['S04'])
            S05 = float(Verify_data['S05'])
            S06 = float(Verify_data['S06'])
            # S07 = float(Verify_data['S07'])
            # S08 = float(Verify_data['S08'])

            #获取全部生长阶段氮肥上限
            max_r = MAX(db_Crop.search(Q.ID == Nzw)[0].get('N', '0'), (mubiaocl / 2 / 100),
                        Soil_element_N,F_eff_N, Ratio)  # 肥料上限
            # 获取全部生长阶段氮肥下限
            min_r = MIN(db_Crop.search(Q.ID == Nzw)[0].get('N', '0'), (mubiaocl / 2 / 100),
                        Soil_element_N,F_eff_N, Ratio)  # 肥料下限

            max_r = max_r * float(Mu)
            min_r = min_r * float(Mu)

            print('当前需要肥料上限: ',max_r)
            print('当前需要肥料下限: ',min_r)
            print('当前有效肥料总量: ',(Datas['All_N']))

            # 判断施肥量是否过量
            if sum(Datas['All_N']) > max_r:

                print("施肥量过多")
                value = (sum(Datas['All_N']) - max_r) / max_r
                F_Greater_than(Plot_map,Check_Data,S01,S02,S03,S04,S05,S06,value,expect)


            # 判断施肥量是否缺少
            elif sum(Datas['All_N']) < min_r:

                print("施肥量过少")
                value = ((min_r - sum(Datas['All_N'])) / min_r)
                print('缺少占比：', value)
                F_Less_than(Plot_map, Check_Data, B01, B02, B03, B04, B05, B06, value, expect)


            # 施肥量在合理区间
            else:

                Plot_map.update({
                    'expect': expect,
                    'Is_Check_N' : 'T',
                })

            # 更新当前阶段是否进行了氮肥校验：是
            Plot_map.update({
                'Is_Check_N': 'T',
                'All_N': [0],
                'Ratio_N': [0]
            })

            # 判断是否最后一个校验期
            if Check_F_N == 'E':

                # N_ALL = sum(Datas['All_N'])  # 全部施氮量
                # P_ALL = sum(Datas['All_P'])  # 全部施磷量
                # K_ALL = sum(Datas['All_K'])  # 全部施钾量
                # G_ALL = sum(Datas['All_G'])  # 全部生长调节剂
                # Y_ALL = sum(Datas["All_Y"])  # 全部农药
                # M_ALL = sum(Datas["All_M"])  # 全部微量肥
                # S_ALL = sum(Datas["All_S"])  # 全部灌溉量
                Yield = Datas['expect']  # 产量
                print('最终产量: ', Yield)


                # 更新当前阶段是否进行了氮肥校验：是
                Plot_map.update({
                    'Is_Check_N': 'T',
                    'On': False
                })

    # 有磷肥校验
    if Check_F_P != 'F':

        #判断是否校验过：
        if Datas['Is_Check_P'] != 'T':


            Ratio = sum(Datas['Ratio_P'])  # 氮肥料量占比

            B01 = float(Verify_data['B01'])
            B02 = float(Verify_data['B02'])
            B03 = float(Verify_data['B03'])
            B04 = float(Verify_data['B04'])
            B05 = float(Verify_data['B05'])
            B06 = float(Verify_data['B06'])
            # B07 = float(Verify_data['B07'])
            # B08 = float(Verify_data['B08'])

            S01 = float(Verify_data['S01'])
            S02 = float(Verify_data['S02'])
            S03 = float(Verify_data['S03'])
            S04 = float(Verify_data['S04'])
            S05 = float(Verify_data['S05'])
            S06 = float(Verify_data['S06'])
            # S07 = float(Verify_data['S07'])
            # S08 = float(Verify_data['S08'])


            # 获取全部生长阶段氮肥上限
            max_r = MAX(db_Crop.search(Q.ID == Nzw)[0].get('P', '0'), (mubiaocl / 2 / 100),
                        Soil_element_P, F_eff_P, Ratio)  # 肥料上限
            # 获取全部生长阶段氮肥下限
            min_r = MIN(db_Crop.search(Q.ID == Nzw)[0].get('P', '0'), (mubiaocl / 2 / 100),
                        Soil_element_P, F_eff_P, Ratio)  # 肥料下限

            max_r = max_r * float(Mu)
            min_r = min_r * float(Mu)


            # 判断施肥量是否过量
            if sum(Datas['All_P']) > max_r:

                print("施肥量过多")
                value = (sum(Datas['All_P']) - max_r) / max_r
                F_Greater_than(Plot_map,Check_Data,S01,S02,S03,S04,S05,S06,value,expect)


            # 判断施肥量是否缺少
            elif sum(Datas['All_P']) < min_r:

                print("施肥量过少")
                value = ((min_r - sum(Datas['All_P'])) / min_r)
                print('缺少占比：', value)
                F_Less_than(Plot_map, Check_Data, B01, B02, B03, B04, B05, B06, value, expect)

            # 施肥量在合理区间
            else:

                Plot_map.update({
                    'expect': expect,
                    'Is_Check_P' : 'T'
                })

            # 更新当前阶段是否进行了氮肥校验：是
            Plot_map.update({'Is_Check_P': 'T'})

        # 判断是否最后一个校验期
        if Check_F_P == 'E':

            N_ALL = sum(Datas['All_N'])  # 全部施氮量
            P_ALL = sum(Datas['All_P'])  # 全部施磷量
            K_ALL = sum(Datas['All_K'])  # 全部施钾量
            G_ALL = sum(Datas['All_G'])  # 全部生长调节剂
            Y_ALL = sum(Datas["All_Y"])  # 全部农药
            M_ALL = sum(Datas["All_M"])  # 全部微量肥
            S_ALL = sum(Datas["All_S"])  # 全部灌溉量
            Yield = Datas['expect']  # 产量

            print(N_ALL, P_ALL, K_ALL, Yield)


            # 更新当前阶段是否进行了氮肥校验：是
            Plot_map.update({'Is_Check_P': 'T'})

    # 有钾肥校验
    if Check_F_K != 'F':

        #判断是否校验过：
        if Datas['Is_Check_K'] != 'T':


            Ratio = sum(Datas['Ratio_K'])  # 氮肥料量占比

            B01 = float(Verify_data['B01'])
            B02 = float(Verify_data['B02'])
            B03 = float(Verify_data['B03'])
            B04 = float(Verify_data['B04'])
            B05 = float(Verify_data['B05'])
            B06 = float(Verify_data['B06'])
            # B07 = float(Verify_data['B07'])
            # B08 = float(Verify_data['B08'])

            S01 = float(Verify_data['S01'])
            S02 = float(Verify_data['S02'])
            S03 = float(Verify_data['S03'])
            S04 = float(Verify_data['S04'])
            S05 = float(Verify_data['S05'])
            S06 = float(Verify_data['S06'])
            # S07 = float(Verify_data['S07'])
            # S08 = float(Verify_data['S08'])


            # 获取全部生长阶段氮肥上限
            max_r = MAX(db_Crop.search(Q.ID == Nzw)[0].get('K', '0'), (mubiaocl / 2 / 100),
                        Soil_element_K, F_eff_K, Ratio)  # 肥料上限
            # 获取全部生长阶段氮肥下限
            min_r = MIN(db_Crop.search(Q.ID == Nzw)[0].get('K', '0'), (mubiaocl / 2 / 100),
                        Soil_element_K, F_eff_K, Ratio)  # 肥料下限

            max_r = max_r * float(Mu)
            min_r = min_r * float(Mu)

            # 判断施肥量是否过量
            if sum(Datas['All_K']) > max_r:

                print("施肥量过多")
                value = (sum(Datas['All_K']) - max_r) / max_r
                F_Greater_than(Plot_map,Check_Data,S01,S02,S03,S04,S05,S06,value,expect)

            # 判断施肥量是否缺少
            elif sum(Datas['All_K']) < min_r:

                print("施肥量过少")
                value = ((min_r - sum(Datas['All_K'])) / min_r)
                print('缺少占比：', value)
                F_Less_than(Plot_map, Check_Data, B01, B02, B03, B04, B05, B06, value, expect)



            # 施肥量在合理区间
            else:

                Plot_map.update({
                    'expect': expect,
                    'Is_Check_K' : 'T'
                })

            # 更新当前阶段是否进行了氮肥校验：是
            Plot_map.update({'Is_Check_K': 'T'})

            # 判断是否最后一个校验期
        if Check_F_K == 'E':

            N_ALL = sum(Datas['All_N'])  # 全部施氮量
            P_ALL = sum(Datas['All_P'])  # 全部施磷量
            K_ALL = sum(Datas['All_K'])  # 全部施钾量
            G_ALL = sum(Datas['All_G'])  # 全部生长调节剂
            Y_ALL = sum(Datas["All_Y"])  # 全部农药
            M_ALL = sum(Datas["All_M"])  # 全部微量肥
            S_ALL = sum(Datas["All_S"])  # 全部灌溉量
            Yield = Datas['expect']  # 产量

            print(N_ALL, P_ALL, K_ALL, Yield)

            # 更新当前阶段是否进行了氮肥校验：是
            Plot_map.update({'Is_Check_K': 'T'})

    #计算新土壤数据：根据施肥量


    print('----------  大量元素肥料校验结束  ----------')


def Storage_info(Crop_Info,Plot_map,Szjd,Crop_Check_F,feiliao_type,Sfsl,hanliang,liyonglv,tisheng,F_eff,Ggfs):



    try:

        Sfsl = float(Sfsl)
        hanliang = float(hanliang)
        liyonglv = float(liyonglv)
        tisheng = float(tisheng)
        F_eff = float(F_eff)


        Datas = Plot_map.all()[0]
        print('Datas: ',Datas)

        Q = Query()
        Check_F = (Crop_Info.search(Q.ID == Szjd)[0].get('Check_F', None))  # 获取校验类型
        print('校验类型: ',Check_F)
        Verify_data = Crop_Check_F.search(Q.ID == Check_F)[0]



        # 判断灌溉方式是否错误：如果有错误进行减产
        if Ggfs in Verify_data and Verify_data[Ggfs] == 'F':
            Sfsl_new = Sfsl * 0.5 * hanliang * (liyonglv + tisheng)
        else:
            Sfsl_new = Sfsl * hanliang * (liyonglv + tisheng)

        print('有效补给量：',Sfsl_new)

        # 储存阶段施肥量
        List_v = Datas[f'All_{feiliao_type}']
        List_v.append(Sfsl_new)

        print('全部补给量列表：',List_v)

        Plot_map.update(
            {f'All_{feiliao_type}': List_v},
        )


        print(Datas)
        Soil_v2 = float(Datas[feiliao_type])#获取旧土壤数据
        print('旧土壤数据: ',Soil_v2)

        #计算新土壤数据：根据施肥量
        Back_data = Soil_v2 +  Soil_F_back(Sfsl_new, F_eff)
        print('反馈的土壤数据：', round(Back_data, 2))

        #存储新的土壤数据到数据库
        Plot_map.update({
            f'{feiliao_type}': round(Back_data, 2),
            'IS_Job_Stop': True
        })
        print('土壤增幅数据：',Soil_F_back(Sfsl_new, F_eff))
        print('土壤增幅后的数据：', Back_data)


    except Exception as e:
        print(f'土壤反馈失败{e}')







