import struct
import time
import datetime
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusException
import socket

A1_Soil = {'T': [], 'H': [], 'N': [], 'P': [], 'K': [], 'S': [], 'E': [], 'PH': []}
B2_Soil = {'T': [], 'H': [], 'N': [], 'P': [], 'K': [], 'S': [], 'E': [], 'PH': []}
C3_Soil = {'T': [], 'H': [], 'N': [], 'P': [], 'K': [], 'S': [], 'E': [], 'PH': []}

# # 创建UDP套接字
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # 绑定本机端口7111
# sock.bind(('0.0.0.0', 7111))

def read_modbus_tcp(ip, port, addr, start, end):
    client = ModbusTcpClient(ip, port=port)
    try:
        connection = client.connect()
        if connection:
            response = client.read_holding_registers(address=start, count=end, slave=addr)
            if not response.isError():
                registers = response.registers
                print(f"获取数据：{registers}")
                return registers
            else:
                return None
        else:
            return None
    except (ConnectionException, ModbusException) as e:
        print(f"Connection or Modbus error: {e}")
        return None
    finally:
        client.close()


def read_modbus_udp(ip, port, addr, start, end=1,client_ip = 7113):
    # 定义不同Addr的请求数据包
    request_data = {
        1: '01 03 00 00 00 0A C5 CD',
        2: '02 03 00 00 00 0A C5 FE',
        3: '03 03 00 00 00 0A C4 2F',
        4: '04 03 00 00 00 0A C5 98',
        5: '05 03 00 00 00 0A C4 49',
        6: '06 03 00 00 00 0A C4 7A'
    }

    # 获取对应Addr的请求数据包
    request = request_data.get(addr)
    if not request:
        print(f"Invalid address: {addr}")
        return None

    # 将请求数据包从十六进制字符串转换为字节
    request_bytes = bytes.fromhex(request.replace(" ", ""))

    # # 打印请求数据包的字节表示
    # print(f"Request bytes: {request_bytes.hex()}")

    # # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定本机端口7111
    sock.bind(('0.0.0.0', client_ip))
    try:
        # 发送请求数据包
        sock.sendto(request_bytes, (ip, port))
        sock.settimeout(5)  # 设置超时时间

        # 接收响应数据
        response, _ = sock.recvfrom(1024)

        # 解析响应数据
        if response and len(response.hex()) == 50:  # 功能码0x03
            registers = []
            data = response.hex()
            # 去掉空格并转换为字节
            byte_data = bytes.fromhex(data[6+start*4:10+start*4].replace(" ", ""))
            for i in range(end):
                registers.append(int.from_bytes(byte_data, byteorder='big'))
            print(f"获取数据：{registers}")
            return registers
        else:
            return None
    except socket.timeout:
        print("UDP timeout")
        return None
    except Exception as e:
        print(f"UDP error: {e}")
        return None
    finally:
        sock.close()



def Get_Modbus_TCP_Datas(IP, Port, Addr, Start, End, QY, Type):
    da_map = {'A1': A1_Soil, 'B2': B2_Soil, 'C3': C3_Soil}

    if QY not in da_map.keys():
        return False

    try:
        if QY == 'C3':
            data = read_modbus_tcp(IP, Port, Addr, Start, End)
        elif QY in ['A1', 'B2']:
            data = read_modbus_udp(IP, Port,Addr, Start, End)
        else:
            return False

        if data is None:
            print('----------  读取传感器数值错误  ----------')
            return False

        data_value = data[0]
        da_map[QY][Type].append(data_value)

        if len(da_map[QY][Type]) > 1:
            da_map[QY][Type].pop(0)

        print('\n----------  开始监测到传感器数值  ----------')
        for _ in range(4):

            try:
                if QY == 'C3':
                    new_data = read_modbus_tcp(IP, Port, Addr, Start, End)
                    time.sleep(5)
                elif QY in ['A1', 'B2']:
                    new_data = read_modbus_udp(IP, Port, Start, End)
                else:
                    return False

                if new_data is None:
                    continue

                new_data_value = new_data[0]
                print('新数据：', new_data_value)
                print('老数据：', da_map[QY][Type][0])

                if new_data_value > da_map[QY][Type][0] and (new_data_value - da_map[QY][Type][0] >= 3):
                    da_map[QY][Type].append(new_data_value)
                    print(da_map[QY][Type])
                    print('----------  监测到传感器数值明显变化  ----------')
                    return True
            except Exception as e:
                print(f"异常：{e}")

        print('----------  传感器数值未发生明显变化  ----------')
        return False

    except Exception as e:
        print(f"发生异常-连接错误：{e}")
        print('----------  读取传感器数值错误  ----------')
        return False