import cv2
import re
import numpy as np
import pytesseract
import time
from datetime import datetime


# Remove space from string function
def remove_space(string):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', string)

def initial_camera():
    # Pre-photo recognized list
    # camera pre-config
    # camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # 使用下面的设置，会有一个 warning
    time.sleep(3)
    cv2.VideoCapture(0).release()
    time.sleep(3)
    camera = cv2.VideoCapture()
    camera.open(0, cv2.CAP_DSHOW)
    time.sleep(3)

    codec = 0x47504A4D  # MJPG
    camera.set(cv2.CAP_PROP_FPS, 15.0)  # 30 frame per second
    camera.set(cv2.CAP_PROP_FOURCC, codec)  #
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # resolution
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # resolution
    time.sleep(5)

    if camera.isOpened():
        return_temp, picture = camera.read()
        time.sleep(1)

        if picture.size == 0:
            print("Attempt 1st, initialize camera error！")
        else:
            print("Attempt 1st, initialize camera successfully!")

            image01_time = datetime.now()
            image02_time1 = image01_time.strftime("%H:%M:%S")
            image02_time2 = image02_time1.replace(':', '-')
            print(image02_time2)
            img02_name = 'Initial_camera{}.jpg'.format(image02_time2)
            cv2.imwrite(img02_name, picture)
            return camera

        return_temp1, picture1 = camera.read()
        time.sleep(1)

        if picture1.size == 0:
            print("Attempt 2ed, initialize camera error！")
        else:
            print("Attempt 2ed, initialize camera successfully!")
            return camera
    else:
        print("Camera is not open!")
        quit()


def check_united_image_bios_version(camera):

    if camera.isOpened():

        for i in range(1):
            # read camera's image, 是否已经读到。以前没有判断，会导致一个报错：cv2.cvtColor 这个函数error，因为没有捕捉到。
            time.sleep(0.1)
            return_value, img = camera.read()

            if return_value == 1:
                to_gray = img

                image401_time = datetime.now()
                image402_time1 = image401_time.strftime("%H:%M:%S")
                image402_time2 = image402_time1.replace(':', '-')
                print(image402_time2)
                img402_name = 'Check_BIOS_Version{}.jpg'.format(image402_time2)
                # cv2.imwrite(img402_name, to_gray)
            else:
                return_value1, img1 = camera.read()
                if return_value1 == 1:
                    to_gray = img1

                else:
                    print("Can't capture the photo!")
                    quit()

            time.sleep(0.1)
            # color convert
            # img = cv2.resize(img, None, fx=0.8, fy=0.8)
            # gray = cv2.cvtColor(to_gray, cv2.COLOR_BGR2GRAY)
            # t, T_threshold = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY_INV)

            to_gray_1 = to_gray[173:220, 730:1100]
            # cv2.imshow("EE1", to_gray_1)
            # cv2.waitKey()

            # cv2.imshow("EE2", gray)
            image_time = datetime.now()
            image_time1 = image_time.strftime("%H:%M:%S")
            image_time2 = image_time1.replace(':', '-')
            print(image_time2)
            img_name = 'BIOS_Version_Hydra_{}.jpg'.format(image_time2)
            print(img_name)

            # cv2.imshow("EE1", gray)
            # cv2.waitKey()
            cv2.imwrite(img_name, to_gray_1)
            # adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,1)
            # cv2.imwrite('img_name.jpg', adaptive_threshold)
            time.sleep(1)

            text = pytesseract.image_to_string(to_gray_1, lang='eng')
            print(text)
            string1 = remove_space(text)
            string2 = string1.replace('.', '')
            string3 = string2.replace(',', '')
            string4 = string3.replace('0', '')
            string = string4.replace('O', '')
            print(string)
            if "U" in string:
                BIOS_upgrade_result = True
                print(string)
                print("Upgrade UI BIOS successfully")
            else:
                BIOS_upgrade_result = False
                print(string)
                print("Error: BIOS is not correct.")
            # fullstring = string
            # substring = "过当前页面"
            #
            # if substring in fullstring:
            #     print("found this picture!")
            #     break
            # else:
            #     print("Not found!{}".format(i))
    else:
        print("camera error")

    camera.release()
    del(camera)

    cv2.destroyAllWindows()
    return BIOS_upgrade_result


def capture_EFI_Shell(camera):


    # isOpened() 用来检查 摄像头初始化是否成功
    if camera.isOpened():
        for i in range(1):
            # read camera's image
            return_value, img = camera.read()
            if return_value == 1:
                to_gray = img

            else:
                return_value1, img1 = camera.read()
                if return_value1 == 1:
                    to_gray = img1

                else:
                    print("Can't capture the photo!")
                    quit()

            time.sleep(0.1)
            # 将图像转成灰度
            # cv2.imshow("EE11", to_gray)
            # cv2.waitKey()
            # cv2.imwrite('img_name1.jpg', to_gray)

            gray = cv2.cvtColor(to_gray, cv2.COLOR_BGR2GRAY)
            # 再将灰度图片做‘反二值化 阈值处理’ （具体可参考 P133 《OpenCV 轻松入门面向Python》）
            t, T_threshold = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY_INV)
            # 抽取图像中的行、列（行从220 到500， 列从260 到700）（具体可参考 P29 《OpenCV 轻松入门面向Python》）
            T1_threshold = T_threshold[585:700, 20:600]
            # cv2.imshow("EE1", T1_threshold)
            # cv2.waitKey()

            image1_time = datetime.now()
            image2_time1 = image1_time.strftime("%H:%M:%S")
            image2_time2 = image2_time1.replace(':', '-')
            print(image2_time2)
            img2_name = 'EFI_Shell_Screen_{}.jpg'.format(image2_time2)

            cv2.imwrite(img2_name, T1_threshold)
            # 使用google pytesseract 抽取图片里的英文文字
            text = pytesseract.image_to_string(T1_threshold, lang='eng')
            # 除去字符串里的空白行（不包含有空格的行）
            string1 = text.replace('\n\n', '\n')
            # The lstrip() method removes any leading characters (space is the default leading character to remove)
            string2 = string1.lstrip()
            # The rstrip() method removes any trailing characters (characters at the end a string), space is the default trailing character to remove.
            string3 = string2.rstrip()
            print(string3)
            # 计算这个string 有几行
            Boot_device_qty = len(string3.splitlines())
            print("Boot_device_quantity:")
            print(Boot_device_qty)
            full_string = string3

            if Boot_device_qty == 3:
                # 下面for循环,得到SanDisk 这个单词在第几行
                row_number = 1
                for item in full_string.split("\n"):
                    if "Shell" in item:
                        sandisk_at_row = row_number
                        # print("U_Disk locate at {} row".format(row_sandisk))
                        break
                    row_number = row_number + 1
                print("EFI shell at row #:")
                print(row_number)
            elif Boot_device_qty == 2:
                row_number = 0
            else:
                print("USB device error!, 请在MI100端_插拔一下U盘和其他设备，确保U盘插紧_并重新测试！")
                print("视频采集卡error!, 请在电脑端插拔一下，确保插紧_并重新测试！")

            # print(row_sandisk)
            # print(Eddy_Rows)
            # print(full_string)
            # cv2.imshow("ttt", T1_threshold)
            # cv2.waitKey()
            # cv2.imwrite('tttt.jpg', T1_threshold)
    else:
        print("camera error")

    camera.release()
    del(camera)

    cv2.destroyAllWindows()
    return (row_number, Boot_device_qty)


# Zhen = initial_camera()
# Zhen3 = check_united_image_bios_version(Zhen)
# print(Zhen3)

#
# Zhen = initial_camera()
# Zhen4, Zhen5 = capture_EFI_Shell(Zhen)
# print(Zhen4, Zhen5)


# capture_usb_boot_option()
# GGTest= capture_usb_boot_option()
# print(GGTest[0])