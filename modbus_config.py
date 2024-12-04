from Function.ModbusCommunication import ModbusServer

modbus_server = ModbusServer()
server = modbus_server.connect_tcp_server(ip='0.0.0.0', port=502)