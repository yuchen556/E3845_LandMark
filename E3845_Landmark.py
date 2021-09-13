# https://datatofish.com/entry-box-tkinter/
import tkinter as tk
# import PLC
import Camera_Hydra_ZQ
import Keyboard_Function
import os
from os import path
import logging
import smtplib
import ssl
import PLC
from Camera_Hydra_ZQ import remove_space
import cv2
import re
import numpy as np
import pytesseract
import time
from datetime import datetime


# 调用图形界面
root = tk.Tk()
# 图形界面的大小 400*300
canvas1 = tk.Canvas(root, width=1100, height=700, relief='raised')
canvas1.pack()
# 图形界面里显示的文字、及位置
label1 = tk.Label(root, text='E3845_蓝马-LandMark Test Platform')
label1.config(font=('helvetica', 20))
canvas1.create_window(400, 45, window=label1)
# 图形界面里显示的文字、及位置
label2 = tk.Label(root, text='请扫描条形码:')
label2.config(font=('helvetica', 15))
canvas1.create_window(400, 100, window=label2)
# 图形界面里SN 的输入框、及位置
entry1 = tk.Entry(root)
canvas1.create_window(400, 140, window=entry1)


# 点击button，运行get_spinel_sn()函数:
def get_spinel_sn():
    global spinel_sn
    spinel_sn = entry1.get()

    # check the previous broken log file existed or not.
    if path.exists(r'D:\LandMark_E3845_Log\20212021.log'):
        print("Delete the previous file.")
        os.remove(r'D:\LandMark_E3845_Log\20212021.log')
    else:
        print("No file existed!")

    time.sleep(2)
    ui_temp_name = "20212021" + ".log"
    logging.basicConfig(filename=r'D:\LandMark_E3845_Log\{:s}'.format(ui_temp_name), filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d, %H:%M:%S',
                        level=logging.DEBUG)

    logging.debug(':Start testing')

    # 若sn 是13位的，则使输入框disable.
    if (len(spinel_sn) == 13):
        # 图形界面里显示的文字
        t1 = time.time()
        label3 = tk.Label(root, text='SN of this board is:', font=('helvetica', 10))
        canvas1.create_window(200, 210, window=label3)

        label4 = tk.Label(root, text=spinel_sn, font=('helvetica', 20, 'bold'))
        canvas1.create_window(200, 250, window=label4)
        # 图形界面里button 变为绿色，输入框变为不能输入
        button1.configure(background="green")
        entry1.config(state='disabled')

        # 01________上电进入DOS系统
        PLC.Secondary_BIOS_off()
        # 给系统上电
        PLC.AC_Power_off()
        time.sleep(1)
        PLC.AC_Power_on()

        # Session_01更新BIOS, BIOS 在DOS盘里
        # Session_01更新BIOS, BIOS 在DOS盘里
        # 启动后直接进入DOS 盘去更新BIOS
        logging.debug(':_Power_On_go_to_DOS!')

        print("Power_On_go_to_DOS!")
        for xx11 in range(30):
            print("Power_on_wait" + "_" + str(xx11))
            time.sleep(1)

        # 02_________check whether in DOS page:
        time.sleep(2)
        UI_Camera = Camera_Hydra_ZQ.initial_camera()
        R111= Camera_Hydra_ZQ.capture_dos(UI_Camera)

        if R111 == "FreeDOS kernel":
            R11=True
            print("Already_in_DOS_OS.")
        else:
            R11 = False
            print('_error_NOT_IN_DOS!!')
            print('_error_NOT_IN_DOS!!')
            print('_error_NOT_IN_DOS!!')
            PLC.AC_Power_off()
            quit()

        time.sleep(2)
        Keyboard_Function.Keyboard_send("1")
        print("Keyboard_send_1")
        time.sleep(1)
        Keyboard_Function.Keyboard_send("Send_Enter")
        print("Keyboard_Send_Enter")
        time.sleep(1)

        # 03_________Upgrading LandMark 蓝马 BIOS
        for xxx11 in range(200):
            print("Upgrading_LandMark_BIOS" + "_" + str(xxx11))
            time.sleep(1)

        # Reboot system to check BIOS version
        time.sleep(4)
        Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
        print("Restart_OS_Del+Ctrl+Alt_1")
        time.sleep(1)
        Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
        print("Restart_OS_Del+Ctrl+Alt_2")

        # Send Delete Key, go into BIOS interface to check BIOS version
        for tt11 in range(30):
            Keyboard_Function.Keyboard_send("Send_Delete")
            print("Send_Delete_go_to_BIOS_interface" + "_" + str(tt11))
            time.sleep(1)


        time.sleep(2)
        Keyboard_Function.Keyboard_send("Send_Enter")
        print("Keyboard_Send_Enter")
        time.sleep(1)

        # Check BIOS version

        time.sleep(1)
        UI_Camera = Camera_Hydra_ZQ.initial_camera()
        LM_BIOS= Camera_Hydra_ZQ.check_landmark_bios_version(UI_Camera)


        if LM_BIOS == True:
            logging.debug('BIOS is upgraded Successfully!')
            t2 = time.time()
            duration = t2 - t1
            logging.critical(': test duration:_' + str(duration))
            print(duration)
            print("BIOS_is_Successful")
            print("BIOS_is_Successful")
            print("BIOS_is_Successful")
            print("BIOS_is_Successful")
            print("BIOS_is_Successful")

            test_time = datetime.now()
            test_time1 = test_time.strftime("%c")
            test_time2 = test_time1.replace(':', '-')

            logging.shutdown()
            os.rename(r'D:\LandMark_E3845_Log\20212021.log', r'D:\LandMark_E3845_Log\SN_{}.log'.format(spinel_sn + '_' + test_time2 + '_' + 'Passed'))

            time.sleep(4)
            # Mail result
            # smtp_server = 'smtp.163.com'
            # port = 465
            # sender = 'joinus_tech_hydra@163.com'
            # receiver1 = "556wangzhen@163.com"
            # receiver2 = "jiandong_bao@163.com"
            # message = "Subject:Passed_LandMark_{}!\r\nThis message was sent from Python!\r\nFrom:{}\r\nTo: {}\r\n".format(spinel_sn, sender, receiver1)
            #
            # context = ssl.create_default_context()
            # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            #     server.login(sender, 'WVZOVFAHYMLFDNUL')
            #     time.sleep(1)
            #     server.sendmail(sender, receiver1, message)
            #     print('Mail_sent')
            #
            # time.sleep(2)
            # message = "Subject:Passed_LandMark_{}!\r\nThis message was sent from Python!\r\nFrom:{}\r\nTo: {}\r\n".format(spinel_sn, sender, receiver2)
            #
            # context = ssl.create_default_context()
            # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            #     server.login(sender, 'WVZOVFAHYMLFDNUL')
            #     time.sleep(1)
            #     server.sendmail(sender, receiver2, message)
            #     print('Mail_sent')

        else:
            logging.critical('BIOS_Error_!!!')
            t2 = time.time()
            duration = t2 - t1
            logging.critical(': test duration:_' + str(duration))
            print(duration)
            print("BIOS_Error_!")
            print("BIOS_Error_!")
            print("BIOS_Error_!")
            print("BIOS_Error_!")
            print("BIOS_Error_!")

            test_time = datetime.now()
            test_time1 = test_time.strftime("%c")
            test_time2 = test_time1.replace(':', '-')

            logging.shutdown()
            os.rename(r'D:\LandMark_E3845_Log\20212021.log', r'D:\LandMark_E3845_Log\SN_{}.log'.format(spinel_sn + '_' + test_time2 + '_' + 'Failed'))

            time.sleep(4)
            # Mail result
            smtp_server = 'smtp.163.com'
            port = 465
            sender = 'joinus_tech_hydra@163.com'
            receiver1 = "556wangzhen@163.com"
            receiver2 ="jiandong_bao@163.com"
            message = "Subject:Failed_LandMark_{}!\r\nThis message was sent from Python!\r\nFrom:{}\r\nTo: {}\r\n".format(spinel_sn, sender, receiver1)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender, 'WVZOVFAHYMLFDNUL')
                server.sendmail(sender, receiver1, message)
                print('Mail_sent')

            time.sleep(2)
            message = "Subject:Failed_LandMark_{}!\r\nThis message was sent from Python!\r\nFrom:{}\r\nTo: {}\r\n".format(spinel_sn, sender, receiver2)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender, 'WVZOVFAHYMLFDNUL')
                server.sendmail(sender, receiver2, message)
                print('Mail_sent')



        # J8，J9 都设置成断开状态，将PLC（网络继电器控制器）的Realy—2 设置为常开。
        PLC.AC_Power_off()
        quit()

    # 若sn 不是13位的，则提示sn is incorrect；
    else:
        label3 = tk.Label(root, text='SN is incorrect', fg='red', font=('helvetica', 10,))
        canvas1.create_window(200, 210, window=label3)

        label4 = tk.Label(root, text=spinel_sn, font=('helvetica', 10, 'bold'))
        canvas1.create_window(200, 230, window=label4)

        button1.configure(background="black")


# 点击button，运行get_spinel_sn() 函数:
button1 = tk.Button(text='Testing', command=get_spinel_sn, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(400, 190, window=button1)

root.mainloop()
