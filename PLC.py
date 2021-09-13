# PLC or 网络继电器控制器
# IP:192.168.0.18
# Slave ID=1
# TCP port=502
# Modbus Mapping, Coil address=0, Relay 1 (Restart button)
# Modbus Mapping, Coil address=1, Relay 2 (AC power)
# from pyModbusTCP.client import ModbusClient

import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
import time

# 远程连接到服务器端, 192.168.0.18 是Modbus TCP slave 设备（网络继电器控制器）
master = mt.TcpMaster("192.168.0.18", 502)
master.set_timeout(5.0)

# @slave=1 : identifier of the slave. from 1 to 247.  0为广播所有的slave
# @function_code=READ_HOLDING_REGISTERS：功能码
# @starting_address=1：开始地址
# @quantity_of_x=3：寄存器/线圈的数量
# @output_value：一个整数或可迭代的值：1/[1,1,1,0,0,1]/xrange(12)
# @data_format
# @expected_length

# Hold_value = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=1, quantity_of_x=3, output_value=5)
# Hold_value = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=1, quantity_of_x=3, output_value=5)
# Coils_value = master.execute(slave=6, function_code=md.READ_COILS, starting_address=1,  quantity_of_x=3, output_value=5)
# print(Hold_value)  # 取到的寄存器的值格式为元组(55, 12, 44)
# print(Coils_value)  # 取到的寄存器的值格式为元组(1, 1, 1)
# master.open() modbus_tk.modbus_tcp.TcpMaster 打开这个链接
# master.close() modbus_tk.modbus_tcp.TcpMaster 关闭这个链接

def AC_Power_off():
    master.open()
    time.sleep(2)
    master.execute(slave=1, function_code=md.WRITE_SINGLE_COIL, starting_address=0, output_value=0)
    time.sleep(1)
    master.close()


def AC_Power_on():
    master.open()
    time.sleep(2)
    master.execute(slave=1, function_code=md.WRITE_SINGLE_COIL, starting_address=0, output_value=1)
    time.sleep(1)
    master.close()


def Secondary_BIOS_off():
    master.open()
    time.sleep(2)
    master.execute(slave=1, function_code=md.WRITE_SINGLE_COIL, starting_address=1, output_value=0)
    time.sleep(1)
    master.close()


def Secondary_BIOS_on():
    master.open()
    time.sleep(2)
    master.execute(slave=1, function_code=md.WRITE_SINGLE_COIL, starting_address=1, output_value=1)
    time.sleep(1)
    master.close()


# Secondary_BIOS_off()
# AC_Power_off()
# AC_Power_on()