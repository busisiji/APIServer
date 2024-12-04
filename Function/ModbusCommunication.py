import asyncio
import socket
import threading
import time
from struct import pack

import modbus_tk.defines as md
import serial
from modbus_tk import modbus_rtu
from modbus_tk import modbus_tcp
import modbus_tk.defines as cst
from pymodbus.constants import Endian
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.server import StartAsyncTcpServer, ServerAsyncStop, StartTcpServer


class ModbusServer():
    """modbus tcp ip 服务端"""
    def __init__(self):
        self.fun = {
            'Read(01) 线圈状态': 0x01,
            'Read(02) 输入状态': 0x02,
            'Read(03) 保持寄存器': 0x03,
            'Read(04) 输入寄存器': 0x04,
            'Wirte(05) 单线圈': 0x05,
            'Wirte(06) 单寄存器': 0x06,
            'Wirte(15) 多线圈': 0x15,
            'Wirte(16) 多寄存器': 0x16,
        }
    def connect_tcp_server(self,ip='127.0.0.1', port=502, time=5,address=0,num=100):
        """modbus tcp ip 从站 服务端"""
        try:
            # 创建从站总服务器
            server = modbus_tcp.TcpServer(ip)  # address必须设置,port默认为502
            server.start()

            # 创建一个数据存储区，用于存储从客户端读取的数据
            self.store = ModbusSlaveContext(
                hr=ModbusSequentialDataBlock(address, [0] * num)
            )

            # 创建一个服务器上下文，用于处理客户端的请求
            context = ModbusServerContext(slaves=self.store, single=True)
            # 启动ModBusTCP服务器
            # 创建并启动线程（启动异步服务器）
            # StartTcpServer(context=context, address=(server_ip, port))
            modbus_server_thread = threading.Thread(target=StartTcpServer,
                                                    kwargs=({"context": context, "address": (ip, port)}))
            modbus_server_thread.start()

            return server
        except Exception as e:
            print('wrong')

    def runServer(self,type,fc_as_hex,address,values=None,count=1):
        """
        通讯操作

        :param type: 读/写
        :param fc_as_hex: 功能码 0x03
        :param address: 起始地址
        :param values:  触发指令s 要设置的多个值列表,如[10, 20, 30]

        """
        if type == '写':
            # 调用函数,设置0地址为触发指令s
            if not isinstance(values,list):
                values = [values]
            self.store.setValues(fc_as_hex, address, values)
            return
        else:
            # 获取保持寄存器的值并打印
            hr_values = self.store.getValues(3, address, count=count)
            print("Hold Register Values:", hr_values)
            return hr_values

    def StartTcpServer(self,**kwargs):  # pylint: disable=invalid-name
        """开始从站服务端"""
        return asyncio.run(StartAsyncTcpServer(**kwargs))

    def CloseTcpServer(self,**kwargs):  # pylint: disable=invalid-name
        """结束从站服务端"""
        return asyncio.run(ServerAsyncStop())

class ModbusMaster():
    '''
    modbus 客户端

    功能码                         编号              含义
    READ_COILS                   H01               读线圈
    READ_DISCRETE_INPUTS         H02               读离散输入
    READ_HOLDING_REGISTERS       H03              读保持寄存器
    READ_INPUT_REGISTERS         H04              读输入寄存器（模拟量）
    WRITE_SINGLE_COIL            H05              写单一线圈
    WRITE_SINGLE_REGISTER        H06              写单一寄存器
    WRITE_MULTIPLE_COILS         H15              写多个线圈
    WRITE_MULTIPLE_REGISTERS     H16              写多个寄存器
    '''

    # VERSION 2.0 引入单例模式

    def __init__(self):
        self.fun = {
            'Read(01) 线圈状态' : self.get_01,
            'Read(02) 输入状态' : self.get_02,
            'Read(03) 保持寄存器' : self.get_03,
            'Read(04) 输入寄存器' : self.get_04,
            'Wirte(05) 单线圈' : self.set_05,
            'Wirte(06) 单寄存器' : self.set_06,
            'Wirte(15) 多线圈' : self.set_15,
            'Wirte(16) 多寄存器' : self.set_16,
        }

    def connect_tcp_master(self,ip='127.0.0.0', port=502, time=1):
        """modbus tcp ip 主站 客户端"""
        try:
            self.master = modbus_tcp.TcpMaster(ip, port)
            self.master.set_timeout(time)
            return self.master
        except Exception as e:
            print('wrong')

    def connect_rtu(self,port='com1', baudrate=9600, bytesize=8, parity='None', stopbits=1, timeout=5):
        """
        串口通讯

        # port：串口
        # baudrate：波特率
        # bytesize：字节大小
        # parity：校验位
        # stopbits：停止位
        # timeout：读超时设置
        # writeTimeout：写超时
        # xonxoff：软件流控
        # rtscts：硬件流控
        # dsrdtr：硬件流控
        """
        try:
            if parity == "None":
                parity = serial.PARITY_NONE
            elif parity == "Odd":
                parity = serial.PARITY_ODD
            else:
                parity = serial.PARITY_EVEN

            xonxoff = False  # 软件流控
            dsrdtr = False  # 硬件流控 DTR
            rtscts = False  # 硬件流控 RTS

            self.master = modbus_rtu.RtuMaster(
                serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits,
                              xonxoff=xonxoff))
            # master.set_verbose(True)
            self.master.set_timeout(timeout)
            return self.master
        except Exception as e:
            print('wrong')
            raise  # 重新引发异常

    def get_01(self, slave=1, adr=0, num=0 ,data_format='H'):  # 读线圈Q区
        db = self.master.execute(slave=slave, function_code=md.READ_COILS, starting_address=adr, quantity_of_x=num,data_format = None)
        return db

    def get_02(self, slave=1, adr=0, num=0,data_format='H'):  # 读输入信号
        db = self.master.execute(slave=slave, function_code=md.READ_DISCRETE_INPUTS, starting_address=adr,
                                 quantity_of_x=num)
        return db

    def get_03(self, slave=1, adr=0, num=0,data_format='H'):  # 读保持寄存器
        db = self.master.execute(slave=slave, function_code=md.READ_HOLDING_REGISTERS, starting_address=adr,
                                 quantity_of_x=num,data_format=data_format)
        return db

    def get_04(self, slave=1, adr=0, num=0,data_format='H'):  # 读输入寄存器
        db = self.master.execute(slave=slave, function_code=md.READ_INPUT_REGISTERS, starting_address=adr,
                                 quantity_of_x=num,data_format=data_format)
        return db

    def set_05(self, slave=1, adr=0, value=0,data_format='H'):  # 写单个线圈
        db = self.master.execute(slave=slave, function_code=md.WRITE_SINGLE_COIL, starting_address=adr, output_value=value)

    def set_06(self, slave=1, adr=0, value=0,data_format='H'):  # 写单个寄存器
        db = self.master.execute(slave=slave, function_code=md.WRITE_SINGLE_REGISTER, starting_address=adr,output_value=value)

    def set_15(self, slave=1, adr=0, value=[],data_format='H'):  # 写多个线圈
        db = self.master.execute(slave=slave, function_code=md.WRITE_MULTIPLE_COILS, starting_address=adr,output_value=value)

    def set_16(self, slave=1, adr=0, value=[],data_format='H'):  # 写多个寄存器
        # db = self.master.execute(slave=slave, function_code=md.WRITE_MULTIPLE_REGISTERS,
        #                                           starting_address=adr, output_value=value, data_format=data_format)
        # return

        # 列表根据None拆分
        result_dict = {}
        temp_list = []
        start_index = 0
        data_format_list = []
        data_format_type = data_format[1]

        for index, item in enumerate(value):
            if item != '' and (isinstance(item,int) or isinstance(item,float)):
                temp_list.append(item)
            else:
                data_format_list.append(data_format[0]+data_format_type*len(temp_list))
                result_dict[start_index] = temp_list
                temp_list = []
                start_index = index + 1

        # 添加最后一个子列表
        data_format_list.append(data_format[0] + data_format_type * len(temp_list))
        result_dict[start_index] = temp_list


        for key in result_dict:
            if result_dict[key]:
                i = list(result_dict.keys()).index(key)
                self.master.execute(slave=slave, function_code=md.WRITE_MULTIPLE_REGISTERS,
                                    starting_address=adr+key, output_value=result_dict[key],
                                    data_format=data_format_list[i])

        # # 之间有None值跳过
        # values_to_write = []
        # addresses_to_write = []
        # for i in range(len(value)):
        #     if value[i] is not None and (isinstance(value[i],int) or isinstance(value[i],float)):
        #         values_to_write.append(value[i])
        #         addresses_to_write.append(adr + i)
        # data_format = data_format[:len(addresses_to_write)+1]

        # if values_to_write:
        #     self.master.execute(slave=slave, function_code=md.WRITE_MULTIPLE_REGISTERS,
        #                         starting_address=addresses_to_write[0], output_value=values_to_write,
        #                         data_format=data_format)

if __name__ == '__main__':
    # master = connect_tcp('192.168.1.47')
    # new_plc = Plc(master)  # 建立一个plc对象
    # print(new_plc.set_06(10,7,9999))

    master = connect_rtu('com8',timeout=1.0)
    new_plc = Plc(master)  # 建立一个plc对象
    print(new_plc.get_03(1, 0, 10))