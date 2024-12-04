from Crop_Check import Crop_Check_F, Crop_Check_S, Crop_Check_G, Crop_Check_Y, Crop_Check_M
# from Mod import Get_Modbus_Data
import IS_Job


from tinydb import TinyDB
from DB_TinyDB import db_A,db_B,db_Crop
from tinydb import Query


def Cultivate_F_Thread(qy,Crop_Info,Plot_map,Szjd,Crop_Check,feiliao_type,Sfsl,hanliang,liyonglv,tisheng,F_eff,Ggfs):


    if IS_Job.Job(qy, feiliao_type,Sfsl) == True:

        print('进行了有效补给')

        Crop_Check_F.Storage_info(

            Crop_Info = Crop_Info,
            Plot_map = Plot_map,
            Szjd = Szjd,
            Crop_Check_F = Crop_Check,
            feiliao_type = feiliao_type,
            Sfsl = Sfsl,
            hanliang = hanliang,
            liyonglv = liyonglv,
            tisheng = tisheng,
            F_eff = F_eff,
            Ggfs = Ggfs,
        )

        # print('监测到传感器数值变化')


    else:

        print('进行了无效补给')

        Crop_Check_F.Storage_info(

            Crop_Info = Crop_Info,
            Plot_map = Plot_map,
            Szjd = Szjd,
            Crop_Check_F = Crop_Check,
            feiliao_type = feiliao_type,
            Sfsl = 0,
            hanliang = hanliang,
            liyonglv = liyonglv,
            tisheng = tisheng,
            F_eff = F_eff,
            Ggfs = Ggfs,
        )


    print('----------  大量元素肥料作业结束  ----------')

def Cultivate_S_Thread(qy,Plot_map,Crop_Info,Szjd,Crop_Check,Ggfs,Datas,Crop_Soil_Back,Sfsl):



    if IS_Job.Job(qy, 'E',Sfsl) == True:

        Crop_Check_S.Storage_info(
            Plot_map=Plot_map,
            Crop_Info=Crop_Info,
            Szjd=Szjd,
            Crop_Check_S=Crop_Check,
            Ggfs=Ggfs,
            Datas=Datas,
            Crop_Soil_Back=Crop_Soil_Back,
            Sfsl=Sfsl,
        )

    else:


        Crop_Check_S.Storage_info(

            Plot_map=Plot_map,
            Crop_Info=Crop_Info,
            Szjd=Szjd,
            Crop_Check_S=Crop_Check,
            Ggfs=Ggfs,
            Datas=Datas,
            Crop_Soil_Back=Crop_Soil_Back,
            Sfsl=0
        )

        # print("没有监测到补水动作")


def Cultivate_G_Thread(qy,Plot_map,Crop_Info,Szjd,Crop_Check,Sfzl,Ggfs,Sfsl):

    if IS_Job.Job(qy, 'E',Sfsl) == True:

        Crop_Check_G.Storage_info(
            Plot_map=Plot_map,
            Crop_Info=Crop_Info,
            Szjd=Szjd,
            Crop_Check_G=Crop_Check,
            Sfzl=Sfzl,
            Ggfs=Ggfs,
            Sfsl=Sfsl,
        )
    else:

        Crop_Check_G.Storage_info(
            Plot_map=Plot_map,
            Crop_Info=Crop_Info,
            Szjd=Szjd,
            Crop_Check_G=Crop_Check,
            Sfzl=Sfzl,
            Ggfs=Ggfs,
            Sfsl=0,
        )

def Cultivate_Y_Thread(qy,Plot_map,Crop_Info,Szjd,Crop_Check,Sfzl,Ggfs,Sfsl):

    if IS_Job.Job(qy, 'E',Sfsl) == True:

        Crop_Check_Y.Storage_info(
            Plot_map=Plot_map,
            Crop_Info=Crop_Info,
            Szjd=Szjd,
            Crop_Check_Y=Crop_Check,
            Sfzl=Sfzl,
            Ggfs=Ggfs,
            Sfsl=Sfsl,
        )
    else:

        Crop_Check_Y.Storage_info(
            Plot_map=Plot_map,
            Crop_Info=Crop_Info,
            Szjd=Szjd,
            Crop_Check_Y=Crop_Check,
            Sfzl=Sfzl,
            Ggfs=Ggfs,
            Sfsl=0,
        )

def Cultivate_M_Thread(qy,Plot_map,Crop_Info,Szjd,Crop_Check,Sfzl,Ggfs,Sfsl):

    if IS_Job.Job(qy, 'E',Sfsl) == True:

        Crop_Check_M.Storage_info(
            Plot_map=Plot_map,
            Crop_Info=Crop_Info,
            Szjd=Szjd,
            Crop_Check_M=Crop_Check,
            Sfzl=Sfzl,
            Ggfs=Ggfs,
            Sfsl=Sfsl,
        )
    else:

        Crop_Check_M.Storage_info(
            Plot_map=Plot_map,
            Crop_Info=Crop_Info,
            Szjd=Szjd,
            Crop_Check_M=Crop_Check,
            Sfzl=Sfzl,
            Ggfs=Ggfs,
            Sfsl=0,
        )


def Greenhouse_Thread(T, H, CO2, LLX, Szjd):

    Q = Query()

    T = float(T)
    H = float(H)
    CO2 = float(CO2)
    LLX = float(LLX)




    # #获取传感器信息
    # IP = db_Lora_Device_info.all()[0]['IP']
    # Port = db_Lora_Device_info.all()[0]['Port']
    #
    # T_Addr = db_Lora_Device_info.search(Q.Type == 'T')[0]['Addr']
    # T_Start = db_Lora_Device_info.search(Q.Type == 'T')[0]['Start']
    # T_End = db_Lora_Device_info.search(Q.Type == 'T')[0]['End']
    #
    # H_Addr = db_Lora_Device_info.search(Q.Type == 'T')[0]['Addr']
    # H_Start = db_Lora_Device_info.search(Q.Type == 'T')[0]['Start']
    # H_End = db_Lora_Device_info.search(Q.Type == 'T')[0]['End']
    #
    # CO2_Addr = db_Lora_Device_info.search(Q.Type == 'T')[0]['Addr']
    # CO2_Start = db_Lora_Device_info.search(Q.Type == 'T')[0]['Start']
    # CO2_End = db_Lora_Device_info.search(Q.Type == 'T')[0]['End']
    #
    # LLX_Addr = db_Lora_Device_info.search(Q.Type == 'T')[0]['Addr']
    # LLX_Start = db_Lora_Device_info.search(Q.Type == 'T')[0]['Start']
    # LLX_End = db_Lora_Device_info.search(Q.Type == 'T')[0]['End']

    # client = ModbusTcpClient(IP, port=Port)
    # connection = client.connect()

    # def read_modbus_tcp(addr, start, end):
    #
    #     try:
    #         if connection:
    #
    #             # 读取保持寄存器
    #             response = client.read_holding_registers(address=start, count=end, slave=addr)
    #             # 检查响应是否成功
    #             if not response.isError():
    #                 # 获取寄存器值
    #                 registers = response.registers
    #                 # print(f"Data: {registers}")
    #                 return registers
    #             else:
    #                 # print("Failed to read registers:", response)
    #                 return None
    #         else:
    #             # print("Failed to connect")
    #             return None
    #     except :
    #
    #         return None
    #获取大棚当前温度
    # T = float(read_modbus_tcp(T_Addr, T_Start, T_End))
    #获取当前生长阶段大棚理想温度上限下限

    # 获取A B区种植作物温度


    A_Crop = db_A.all()[0]['Nzw']
    A_Com_file = db_Crop.search(Q.ID == A_Crop)[0]
    A_Greenhouse_Info = TinyDB(f"Crop_DB/{A_Com_file['Des']}/{A_Com_file['Greenhouse']}.json")
    A_Greenhouse_Info_data = A_Greenhouse_Info.search(Q.ID == Szjd)[0]

    A_T_max = float(A_Greenhouse_Info_data['T_max'])
    A_T_min = float(A_Greenhouse_Info_data['T_min'])
    A_H_max = float(A_Greenhouse_Info_data['H_min'])
    A_H_min = float(A_Greenhouse_Info_data['H_min'])
    A_CO2_max = float(A_Greenhouse_Info_data['CO2_min'])
    A_CO2_min = float(A_Greenhouse_Info_data['CO2_min'])
    A_LLX_max = float(A_Greenhouse_Info_data['LLX_min'])
    A_LLX_min = float(A_Greenhouse_Info_data['LLX_min'])


    B_Crop = db_B.all()[0]['Nzw']
    B_Com_file = db_Crop.search(Q.ID == B_Crop)[0]
    B_Greenhouse_Info = TinyDB(f"Crop_DB/{B_Com_file['Des']}/{B_Com_file['Greenhouse']}.json")
    B_Greenhouse_Info_data = B_Greenhouse_Info.search(Q.ID == Szjd)[0]

    B_T_max = float(B_Greenhouse_Info_data['T_max'])
    B_T_min = float(B_Greenhouse_Info_data['T_min'])
    B_H_max = float(A_Greenhouse_Info_data['H_min'])
    B_H_min = float(B_Greenhouse_Info_data['H_min'])
    B_CO2_max = float(B_Greenhouse_Info_data['CO2_min'])
    B_CO2_min = float(B_Greenhouse_Info_data['CO2_min'])
    B_LLX_max = float(B_Greenhouse_Info_data['LLX_min'])
    B_LLX_min = float(B_Greenhouse_Info_data['LLX_min'])


    def check(Plot_map,Data,max,min,s1,s2,s3,s4,s5,b1,b2,b3,b4,b5):

        Plot_map_data = Plot_map.all()[0]

        if (Data < min) & (Plot_map_data['On'] == True):

            print('当前温度过低')

            if Data / min >= 0.8:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(s1))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

            elif 0.8 < Data / min >= 0.6:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(s2))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

            elif 0.6 < Data / min >= 0.4:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(s3))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

            elif 0.4 < Data / min >= 0.2:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(s4))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

            elif 0.2 < Data / min >= 0:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(s5))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

        elif (Data > max) & (Plot_map_data['On'] == True):

            print('当前温度过高')

            if Data / max >= 1.2:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(b1))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

            elif 0.8 < Data / max >= 1.4:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(b2))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

            elif 0.6 < Data / max >= 1.6:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(b3))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

            elif 0.4 < Data / max >= 1.8:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(b4))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

            elif 0.2 < Data / max >= 2:
                expect_cl = float(Plot_map_data['expect']) - (float(Plot_map_data['expect']) * float(b5))
                # 更新数据
                Plot_map.update({
                    'expect': expect_cl
                })

    check(db_A,T,A_T_max,A_T_min,0.02,0.10,0.18,0.35,0.5,0.04,0.25,0.5,0.75,0.9)
    check(db_B,T,B_T_max,B_T_min,0.02,0.10,0.18,0.35,0.5,0.04,0.25,0.5,0.75,0.9)

    check(db_A,H,A_H_max,A_H_min,0.02,0.10,0.18,0.35,0.5,0.04,0.25,0.5,0.75,0.9)
    check(db_B,H,B_H_max,B_H_min,0.02,0.10,0.18,0.35,0.5,0.04,0.25,0.5,0.75,0.9)

    check(db_A,CO2,A_CO2_max,A_CO2_min,0.02,0.10,0.18,0.35,0.5,0.04,0.25,0.5,0.75,0.9)
    check(db_B,CO2,B_CO2_max,B_CO2_min,0.02,0.10,0.18,0.35,0.5,0.04,0.25,0.5,0.75,0.9)

    check(db_A,LLX,A_LLX_max,A_LLX_min,0.02,0.10,0.18,0.35,0.5,0.04,0.25,0.5,0.75,0.9)
    check(db_B,LLX,B_LLX_max,B_LLX_min,0.02,0.10,0.18,0.35,0.5,0.04,0.25,0.5,0.75,0.9)



    # read_modbus_tcp(H_Addr, H_Start, H_End)

    # read_modbus_tcp(CO2_Addr, CO2_Start, CO2_End)

    # read_modbus_tcp(LLX_Addr, LLX_Start, LLX_End)


    # client.close()  # 确保在函数退出时关闭连接

