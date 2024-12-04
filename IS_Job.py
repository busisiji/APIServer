from tinydb import Query
from Mod import Get_Modbus_Data
from DB_TinyDB import db_Soil_Device_info
from Mod.Get_Modbus_Data import read_modbus_tcp, read_modbus_udp


def Job(qy,feiliao_type,Sfsl=1):

    Q = Query()
    #获取土壤传感器配置信息
    Datas = db_Soil_Device_info.search((Q.Type == feiliao_type) & (Q.Place == qy))[0]

    print('进入子线程：')

    print('调用土壤设备的数据：', Datas)

    IP = Datas['IP']
    Port = int(Datas['Port'])
    Addr = int(Datas['Addr'])
    Start = int(Datas['Start'])
    End = int(Datas['End'])
    # print(IP,Port,Addr,Start,End)

    if Sfsl == 0:
        return False


    return Get_Modbus_Data.Get_Modbus_TCP_Datas(IP, Port,Addr, Start, End, qy, feiliao_type)
    # return False

def Job_data(qy,feiliao_type,Sfsl=1):

    Q = Query()
    #获取土壤传感器配置信息
    Datas = db_Soil_Device_info.search((Q.Type == feiliao_type) & (Q.Place == qy))
    if not Datas:
        return False
    else:
        Datas = Datas[0]

    print('进入子线程：')

    print('调用土壤设备的数据：', Datas)

    IP = Datas['IP']
    Port = int(Datas['Port'])
    Addr = int(Datas['Addr'])
    Start = int(Datas['Start'])
    End = int(Datas['End'])
    # print(IP,Port,Addr,Start,End)

    if Sfsl == 0:
        return False

    if qy == 'C3':
        data = read_modbus_tcp(IP, Port, Addr, Start, End)
    elif qy in ['A1', 'B2']:
        data = read_modbus_udp(IP, Port, Addr, Start, End)
    return data[0] if data else False
    # return False
# Job('B2','N')
