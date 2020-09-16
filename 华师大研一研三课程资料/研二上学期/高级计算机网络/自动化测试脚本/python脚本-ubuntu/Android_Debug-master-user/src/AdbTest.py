import os
import time
import threading
import pexpect
import re
import subprocess
import AndroidKeyName
import copy
from adb import ADB

# android目录
ANDROID_HOME = "/home/changlf/Android/Sdk/platform-tools"
# adb路径
_adb = ""
# pyadb
_pyadb = None
_Recording = True
# 是否录制
recording = True
# 触摸精度
Event_Precision = 20
# 点击动作是否录入的标志位
Event_Enter = None

userEvent = []
class Key():
        keytime = None
        keyevent = None
        keytype = None
        keyname = None
        keycode = None
        keyend = False
# class 处理adb各种数据
class AdbService(threading.Thread):
    # 用于处理提取event事件的正则表达式
    ##print("I am in AdbService")
    keyre = re.compile(".*?([+-]?\\d*\\.\\d+)(?![-+0-9\\.]).*?((?:\\/[\\w\\.\\-]+)+).*?(\\d+).*?((?:[a-z0-9][a-z0-9]*[a-z0-9]+[a-z0-9]*)).*?((?:[a-z0-9][a-z0-9]*[a-z0-9]+[a-z0-9]*))", re.IGNORECASE | re.DOTALL)
    ##print(keyre)
    # 触摸屏的x与y的最大与最小,用于坐标转换
    xMax = None
    xMin = None
    yMax = None
    yMin = None
    ##print(xMax,xMin,yMax,yMin)
    # 屏幕的分辨率,用于坐标转换
    k_Hight = None
    k_Width = None
    # x,y坐标,若x或y不变则不会继续传值
    valX = 0
    valY = 0
    # 触摸事件head
    __teach = None
    # 触摸x
    __teach_x = None
    # 触摸y
    __teach_y = None
    ##print(__teach_x, __teach_y, "__teach_x, __teach_y")
    def __init__(self):
        super().__init__()
        # 初始化触摸屏的xy与坐标的分辨率
        self.initCoordinate()
        ##print(self.initCoordinate())
        ##print("----3----")
        self.initResolution()
        ##print(self.initResolution())
        ##print("----4----")
    # 获取屏幕的xy值的相对值
    def initCoordinate(self):
        command = os.popen("adb shell getevent -p").read().splitlines()
        ##print(command,"commeand")
        minre = re.compile('.*?(min)(.)(\\d+)', re.IGNORECASE | re.DOTALL)
        maxre = re.compile('.*?(max)(.)(\\d+)', re.IGNORECASE | re.DOTALL)
        ##print(minre,maxre,"minre,maxre")
        for d in range(0, len(command) - 1):
            n = minre.search(command[d])
            m = maxre.search(command[d])
            if(n and m):
                keyname = int(re.compile(".*? .*? .*? .*? .*? .*?( )((?:[a-z0-9][a-z0-9]*[a-z0-9]+[a-z0-9]*))(  )", re.IGNORECASE | re.DOTALL).search(command[d]).group(2), 16)
                if(AndroidKeyName.KEYNAME_TEACH_X == keyname):
                    self.xMax = int(m.group(3), 10)
                    self.xMin = int(n.group(3), 10)
                elif(AndroidKeyName.KEYNAME_TEACH_Y == keyname):
                    self.yMax = int(m.group(3), 10)
                    self.yMin = int(n.group(3), 10)
        #print(self.xMax,self.xMin,"self.xMax,self.xMin")
    # 获取屏幕的分辨率
    def initResolution(self):
        ##print('111')
        command = os.popen('''adb shell wm size''').read().splitlines()
        ##print(command,"initResolution")
        #m = re.compile(".*?\\[.*?(\\[)([+-]?\\d*\\.\\d+)(?![-+0-9\\.])(,)([+-]?\\d*\\.\\d+)(?![-+0-9\\.])(\\])", re.IGNORECASE | re.DOTALL).search(command[0])
        pattern = re.compile(r'\d+')
        m = pattern.findall(command[0])
        ##print(m,"m")
        if(m):
            self.k_Width = m[0]
            self.k_Hight = m[1]
        #print(self.k_Width,self.k_Hight,"self.k_Width self.k_Hight")
        
    # 提取事件与数值进行返回
    def eventCode(self, cmd):
        key = self.keyre.search(cmd)
        if (key):
            try:
                keyname = int(key.group(4), 16)
                keycode = int(key.group(5), 16)
                return keyname, keycode
            except ValueError:
                return None, None
        else:
            return None, None
    # 返回所有键值数据
    def eventAllCade(self, cmd):
        key = self.keyre.search(cmd)
        if(key):
            try:
                keytime = float(key.group(1))
                keyevent = key.group(2)
                keytype = int(key.group(3), 16)
                keyname = int(key.group(4), 16)
                keycode = int(key.group(5), 16)
                return keytime, keyevent, keytype, keyname, keycode
            except ValueError:
                return None, None, None, None, None
        else:
            return None, None, None, None, None
    # xy坐标转换
    def eventXY2xy(self, origin, n):
        if(n == AndroidKeyName.KEYNAME_TEACH_X):
            return format((origin - self.xMin) * self.k_Width / (self.xMax - self.xMin), '.2f')
        elif(n == AndroidKeyName.KEYNAME_TEACH_Y):
            return (format((origin - self.yMin) * self.k_Hight / (self.yMax - self.yMin), '.2f'))
    def run(self):
        #print("I am in run－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－开始运行指令")
        
        child = pexpect.spawn("adb shell getevent -t", timeout=120)
        ##print(child, "in function run child")
        ##print(_Recording,"_Recording")

        def endTouch(k):
            # 录入终点位置
            userEvent.append(k)
            #print(k,"录入终点位置")
            # 记录操作终止符
            end = copy.deepcopy(k)
            end.keytype = 0
            end.keyname = 0
            end.keycode = 0
            end.keyend = True
            userEvent.append(end)

        while _Recording:
            # 上一组指令的时间
            ##print("I am in recording")
            child.expect (["\r\n", "\r\x1b", "\r"], timeout=120)
            cmd = child.before.decode()
            ##print(cmd,"cmd")
            k = Key()
            ##print(k,"k first for Key()")
            k.keytime, k.keyevent, k.keytype, k.keyname, k.keycode = self.eventAllCade(cmd)
            #print('keyevent keytype keyname keycode: ', k.keyevent, k.keytype, k.keyname, k.keycode)

            if(k.keytime != None and _Recording):
                ##print("开始录制点击userEvent动作")
                ##print(k,"k second for Key()")  
                self.__teach = k.keytime  
                if(k.keyname == AndroidKeyName.KEYNAME_TEACH_EVENT and k.keycode == 1):
                    #print(k,"录入触摸起始位置")
                    # 录入触摸起始位置
                    userEvent.append(k)
                elif(k.keyname == AndroidKeyName.KEYNAME_TEACH_EVENT and k.keycode == 0):
                    self.__teach_x = None
                    self.__teach_y = None
                    userEvent.append(k)
                    #endTouch(k)
                elif(k.keycode == AndroidKeyName.KEYNAME_THACHEND and \
                            k.keyname == AndroidKeyName.KEYNAME_THACHEND and \
                            k.keytype == AndroidKeyName.KEYNAME_THACHEND):
                    if(userEvent[len(userEvent) - 1].keyname == AndroidKeyName.KEYNAME_TEACH_EVENT and \
                                userEvent[len(userEvent) - 1].keycode == 0):
                        userEvent.append(k)
                        k.keyend = True
                        #print ("end")
                #记录电源键的点亮与关闭
                elif(k.keyname == AndroidKeyName.KEYNAME_POWER and k.keycode == 1):
                    #print("点亮屏幕的开始动作")
                    userEvent.append(k)
                elif(k.keyname == AndroidKeyName.KEYNAME_POWER and k.keycode == 0):
                    endTouch(k)
                #音量加
                elif(k.keyname == AndroidKeyName.KEYNAME_VOLUME_UP and k.keycode == 1):
                    #print("点亮屏幕的开始动作")
                    userEvent.append(k)
                elif(k.keyname == AndroidKeyName.KEYNAME_VOLUME_UP and k.keycode == 0):
                    endTouch(k)
                #音量减
                elif(k.keyname == AndroidKeyName.KEYNAME_VOLUME_DOWN and k.keycode == 1):
                    #print("点亮屏幕的开始动作")
                    userEvent.append(k)
                elif(k.keyname == AndroidKeyName.KEYNAME_VOLUME_DOWN and k.keycode == 0):
                    endTouch(k)

                # 录制end符
                if(k.keyname == AndroidKeyName.KEYNAME_THACHEND \
                                and k.keytype == AndroidKeyName.KEYNAME_THACHEND \
                                and k.keycode == AndroidKeyName.KEYNAME_THACHEND \
                                and len(userEvent) != 0 \
                                and userEvent[len(userEvent)-1].keyname != AndroidKeyName.KEYNAME_THACHEND):
                        #print(k,"录制end符")
                        ##print('keyevent keytype keyname keycode: ', k.keyevent, k.keytype, k.keyname, k.keycode)
                        userEvent.append(k)

                # 判断属于一个触摸事件段
                if(self.__teach != None):
                    if(k.keyname == AndroidKeyName.KEYNAME_TEACH_X):
                        ##print()
                        if(self.__teach_x != None):
                            precision = k.keycode - self.__teach_x
                            precision = precision > 0 and precision or precision * -1
                            if(precision > Event_Precision or Event_Enter == 'y' or Event_Enter == None):
                                userEvent.append(k)
                                Event_Enter = 'x'
                                self.__teach_x = k.keycode
                        else:
                            userEvent.append(k)
                            Event_Enter = 'x'
                            self.__teach_x = k.keycode
                    if(k.keyname == AndroidKeyName.KEYNAME_TEACH_Y):
                        if(self.__teach_y != None):
                            precision = k.keycode - self.__teach_y
                            precision = precision > 0 and precision or precision * -1
                            if(precision > Event_Precision or Event_Enter == 'x'):
                                userEvent.append(k)
                                Event_Enter = 'y'
                                self.__teach_y = k.keycode
                        else:
                            userEvent.append(k)
                            Event_Enter = 'y'
                            self.__teach_y = k.keycode
                    #print(self.__teach_x,self.__teach_y,"self.__teach_x,self.__teach_y")
#                         userEvent[self.__teach].append("%s shell sendevent %s %d %d %d" % (_adb, keyevent, keytype, keyname, keycode))
           
            #print("I am in run－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－结束录制，并开始打印userEvent事件")
            '''#print(userEvent,"userEvent")
            counter = 0
            while counter < len(userEvent):
                var = userEvent[counter]
                #print('keyevent keytype keyname keycode: ', var.keyevent, var.keytype, var.keyname, var.keycode)
                counter = counter + 1
            #print(" ")'''

class UserPlay():
    def play(self):
        flaglenth = len(userEvent)
        #print("flaglenth", flaglenth)
        for i in range(0, len(userEvent)):
            #print("第一个位置", len(userEvent))
            #print("I am in the class UserPlay play for 循环内部")
            event = userEvent[i]
            #print("第二个位置", len(userEvent))
            ##print(userEvent,"userEvent")
            _pyadb.shell_command("sendevent %s %d %d %d" % (event.keyevent, event.keytype, event.keyname, event.keycode))
            #print("第三个位置", len(userEvent))
#             os.system("%s shell sendevent %s %d %d %d" % (_adb, event.keyevent, event.keytype, event.keyname, event.keycode))
#             #print("%s shell sendevent %s %d %d %d" % (_adb, event.keyevent, event.keytype, event.keyname, event.keycode))
            ##print("sendevent %s %d %d %d" % (event.keyevent, event.keytype, event.keyname, event.keycode),'''"sendevent %s %d %d %d" % (event.keyevent, event.keytype, event.keyname, event.keycode)''')
            if(event.keyend and i < len(userEvent) - 1):
                enext = userEvent[i + 1]
                time.sleep(0.5)
                #print(enext.keytime - event.keytime)
                '''if (i == len(userEvent) - 2):
                    time.sleep(0.5)
                    print("0.5")
                else:
                    time.sleep(enext.keytime - event.keytime)
                    print(enext.keytime)
                    print(event.keytime)
                    print(enext.keytime - event.keytime)
                '''
        del userEvent[flaglenth:len(userEvent)]
        #print(len(userEvent))

if(ANDROID_HOME != None):
    #ANDROID_HOME = os.getenv("ANDROID_HOME")
    # 找到adb路径
    _adb = ANDROID_HOME + '/adb'
    #print(_adb,"找到adb路径 1")
    _pyadb = ADB(_adb)
    #print(_pyadb,"_pyadb 2")
    _pyadb.wait_for_device()
    ##print(_pyadb.wait_for_device(),"3")
    err, dev = _pyadb.get_devices()
    print('设备名：',_pyadb.get_devices())
    _pyadb.set_target_device(dev[-1])
    #print(_pyadb.set_target_device(dev[-1]), '5')
    # 开始录制
    if(input("输入y开始录制: ") == "y"):
        ##print("---")
        adb = AdbService()
        ##print("-2--")
        adb.start()
        #print("-3--")

    # 停止录制    
    if(input("输入y停止录制: ") == "y"):
        ##print("-4--")
        _Recording = False
        #print("-5--")
    
    # 开始回放
    _Recording = False
    '''__play = True
    while __play:
        if(input("输入yes开始回放") == "y"):
            ue = UserPlay()
            ue.play()
            __play = False
        else:
            __play = False
    '''

    # 开始回放
    
    numIndex = int(input("输入回放次数: "))
    for num in range(0, numIndex):
        __play = True
        flag = input("输入y开始回放(输入其他字符或者ENTER键盘，将会结束回放): ")
        print("正在进行第 ", num+1, "次回放……")
        if(flag == "y"):
            ue = UserPlay()
            ue.play()
            __play = False
        else:
            __play = False
            break
    print("你刚刚进行了 ", numIndex, "次回放")

    '''
    #截图功能
    if(input("输入yes保存截图") == "y"):
        picturename = '/sdcard/' + str(time.time())[:10] + '.png'
        _pyadb.screenShot(picturename)
        _pyadb.get_remote_file(picturename,local = '/home/changlf/')
    
    #截log
    if(input("输入yes保存log: ") == "y"):
        logroot = '/home/changlf/logText111.txt'
        _pyadb.get_logcat(logroot)

    #获取当前页面的包名
    if(input("输入yes保存当前包名: ") == "y"):
        _pyadb.get_packagename()
    '''

    # 停止录制
    # 设置循环
else:
    #print("没有找到ANDROID_HOME")
    exit()
