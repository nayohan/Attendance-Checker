import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtTest
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

###############################################
# 틀고 싶은 과목명 일부
CLASS_NAME = ['', '', '', '']
# 틀고싶은 영상 주차 범위
START_SECTION = 1
END_SECTION = 15
STD_SECTION = 0
# 한 주차내에 영상 파일 위에 몇개의 파일이 있는가(최대)
OTHERS_CNT = 10
ID = ''
PW = ''
###############################################
# 기본 변수
video_index = 1
###############################################


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 459)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.name = QtWidgets.QLabel(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(40, 20, 121, 31))
        self.name.setObjectName("name")
        self.notice = QtWidgets.QLabel(self.centralwidget)
        self.notice.setGeometry(QtCore.QRect(390, 50, 261, 31))
        self.notice.setObjectName("notice")
        self.start = QtWidgets.QLabel(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(20, 290, 211, 21))
        self.start.setObjectName("start")
        self.end = QtWidgets.QLabel(self.centralwidget)
        self.end.setGeometry(QtCore.QRect(20, 360, 211, 21))
        self.end.setObjectName("end")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(390, 20, 251, 31))
        self.label_6.setObjectName("label_6")
        self.btn_go = QtWidgets.QPushButton(self.centralwidget)
        self.btn_go.setGeometry(QtCore.QRect(520, 300, 121, 81))
        self.btn_go.setObjectName("btn_go")
        self.txt_name_1 = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_name_1.setGeometry(QtCore.QRect(240, 20, 131, 31))
        self.txt_name_1.setDocumentTitle("")
        self.txt_name_1.setObjectName("txt_name_1")
        self.txt_end = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_end.setGeometry(QtCore.QRect(240, 350, 131, 31))
        self.txt_end.setObjectName("txt_end")
        self.txt_start = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_start.setGeometry(QtCore.QRect(240, 280, 131, 31))
        self.txt_start.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.txt_start.setObjectName("txt_start")
        self.txt_id = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_id.setGeometry(QtCore.QRect(510, 190, 131, 31))
        self.txt_id.setDocumentTitle("")
        self.txt_id.setObjectName("txt_id")
        self.name_2 = QtWidgets.QLabel(self.centralwidget)
        self.name_2.setGeometry(QtCore.QRect(470, 190, 31, 31))
        self.name_2.setObjectName("name_2")
        self.name_3 = QtWidgets.QLabel(self.centralwidget)
        self.name_3.setGeometry(QtCore.QRect(460, 230, 31, 31))
        self.name_3.setObjectName("name_3")
        self.txt_name_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_name_2.setGeometry(QtCore.QRect(240, 60, 131, 31))
        self.txt_name_2.setDocumentTitle("")
        self.txt_name_2.setObjectName("txt_name_2")
        self.txt_name_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_name_3.setGeometry(QtCore.QRect(240, 100, 131, 31))
        self.txt_name_3.setDocumentTitle("")
        self.txt_name_3.setObjectName("txt_name_3")
        self.txt_name_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_name_4.setGeometry(QtCore.QRect(240, 140, 131, 31))
        self.txt_name_4.setDocumentTitle("")
        self.txt_name_4.setObjectName("txt_name_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 30, 16, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 70, 16, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 110, 16, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(210, 150, 16, 17))
        self.label_4.setObjectName("label_4")
        self.txt_pw = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_pw.setGeometry(QtCore.QRect(510, 230, 131, 31))
        self.txt_pw.setObjectName("txt_pw")
        self.txt_pw.setEchoMode(QLineEdit.Password)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # load id file
        try:
            file = open('save_prev_data.txt', 'r')
            # 아이디, 비밀번호
            self.txt_id.setText(file.readline().strip('\n'))
            self.txt_pw.setText(file.readline().strip('\n'))
            # 과목명
            try:
                self.txt_name_1.setText(file.readline().strip('\n'))
            except:
                print('empty txt_name_1')
            try:
                self.txt_name_2.setText(file.readline().strip('\n'))
            except:
                print('empty txt_name_2')
            try:
                self.txt_name_3.setText(file.readline().strip('\n'))
            except:
                print('empty txt_name_3')
            try:
                self.txt_name_4.setText(file.readline().strip('\n'))
            except:
                print('empty txt_name_4')
            # 주차 설정
            #self.txt_start.setText("1")
            #self.txt_end.setText("1")
        except:
            print('Hello, First client!')

        self.btn_go.clicked.connect(self.go)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.name.setText(_translate("MainWindow", "과목명  :"))
        self.notice.setText(_translate("MainWindow", "(우상단의 Englich(en)로  확인)"))
        self.start.setText(_translate("MainWindow", "틀고싶은 영상 주차 시작 :"))
        self.end.setText(_translate("MainWindow", "틀고싶은 영상 주차 끝 :"))
        self.label_6.setText(_translate("MainWindow", "사이트가 영어면"))
        self.btn_go.setText(_translate("MainWindow", "play video"))
        self.name_2.setText(_translate("MainWindow", "ID :"))
        self.name_3.setText(_translate("MainWindow", "PW :"))
        self.label.setText(_translate("MainWindow", "1)"))
        self.label_2.setText(_translate("MainWindow", "2)"))
        self.label_3.setText(_translate("MainWindow", "3)"))
        self.label_4.setText(_translate("MainWindow", "4)"))

    def go(self):
        global CLASS_NAME
        global OTHERS_CNT
        global START_SECTION
        global END_SECTION
        global STD_SECTION
        global video_index
        global ID
        global PW

        CLASS_NAME[0] = str(self.txt_name_1.toPlainText())
        CLASS_NAME[1] = str(self.txt_name_2.toPlainText())
        CLASS_NAME[2] = str(self.txt_name_3.toPlainText())
        CLASS_NAME[3] = str(self.txt_name_4.toPlainText())
        START_SECTION = int(self.txt_start.toPlainText())
        END_SECTION = int(self.txt_end.toPlainText())
        ID = str(self.txt_id.toPlainText())
        PW = str(self.txt_pw.text())
        section_now = START_SECTION
        STD_SECTION = section_now

        # save id file
        file = open('save_prev_data.txt', 'w')
        file.write(ID + "\n")
        file.write(PW + "\n")
        for i in range(4):
            data = CLASS_NAME[i]
            file.write(data + "\n")
        file.close()

        # driver import
        driver = webdriver.Chrome('chromedriver.exe')
        # url 로딩
        url = "http://cyber.inu.ac.kr/"
        driver.get(url)

        # 로그인 정보
        driver_id = driver.find_element_by_id("input-username").send_keys(ID)  # 문자열 형식으로 아이디 입력
        driver_pw = driver.find_element_by_id('input-password').send_keys(PW)  # 문자열 형식으로 비밀번호 입력

        # 로그인 버튼 클릭
        driver.find_element_by_class_name("btn-success").click()
        # enter
        # driver_pw.send_keys(Keys.ENTER)

        try:
            # pop up # 팝업창 추가 # 맨앞부터
            driver.find_element_by_xpath('//*[@id="notice_popup_1_376594"]/div[3]/span').click()
            driver.find_element_by_xpath('//*[@id="notice_popup_1_354316"]/div[3]/span').click()

        except:
            print('non popup')

        # count CLASS
        max_class_index = 1
        while 1:
            try:
                just_cnt = driver.find_element_by_xpath(
                    '//*[@id="region-main"]/div/div[1]/div[2]/ul/li[' + str(max_class_index) + ']/div/a/div[2]/div[2]')
                max_class_index += 1
            except:
                break

        for i in range(4):
            if not CLASS_NAME[i] == '':
                try:
                    for j in range(1, max_class_index):
                        class_str = driver.find_element_by_xpath(
                            '//*[@id="region-main"]/div/div[1]/div[2]/ul/li[' + str(
                                j) + ']/div/a/div[2]/div[2]/h3').text
                        if not class_str.find(CLASS_NAME[i]) == -1:
                            print('find class')
                            driver.find_element_by_xpath(
                                '//*[@id="region-main"]/div/div[1]/div[2]/ul/li[' + str(j) + ']/div/a').click()
                            break
                except:
                    print('ERROR! can not find class name!')
                    driver.quit()
                    return

                while 1:
                    # Clear CLASS == back to home
                    if section_now > END_SECTION:
                        print('reach END_SECTION')
                        try:
                            driver.find_element_by_xpath('//*[@id="back-top"]').click()
                            time.sleep(3)
                            driver.find_element_by_xpath('//*[@id="page-header"]/nav/div/div[1]/a').click()
                            CLASS_NAME[i] = ''
                            section_now = START_SECTION
                            video_index = 1
                            print('TOP - BACK')
                            break
                        except:
                            driver.find_element_by_xpath('//*[@id="page-header"]/nav/div/div[1]/a').click()
                            CLASS_NAME[i] = ''
                            section_now = START_SECTION
                            video_index = 1
                            print('BACK')
                            break
                    else:
                        try:
                            # set time
                            print('start - ', video_index)
                            timeline = driver.find_element_by_xpath(
                                '//*[@id="section-' + str(section_now) + '"]/div[3]/ul/li[' + str(
                                    video_index) + ']/div/div/div[2]/div/span/span[2]').text
                            timeline = timeline.replace(", ", "")
                            print('time : ', timeline)

                            # click and open video
                            driver.find_element_by_xpath('//*[@id="section-' + str(section_now) + '"]/div[3]/ul/li[' + str(
                                    video_index) + ']/div/div/div[2]/div/a').click()
                            print('open video')

                            # change tab
                            driver.switch_to.window(driver.window_handles[1])

                            # play video
                            try:
                                # not yet played video
                                time.sleep(3)
                                driver.find_element_by_xpath('//*[@id="vod_viewer"]').click()
                                time.sleep(1)
                                # 전체화면으로 녹화하고싶을 때
                                # driver.find_element_by_xpath('//*[@id="vod_player"]/div[8]/div[4]/div[3]/div[10]').click()
                            except:
                                # already played
                                ######## 이미 재생된 영상 에러...############
                                print('already played video!')
                                driver.quit()
                                return
                            ##########################################

                            # wait playing video
                            time.sleep(5)

                            time.sleep(int(timeline[:2]) * 60 + int(timeline[3:]))
                            time.sleep(5)

                            # close and change tab
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            time.sleep(2)

                            # set var
                            video_index += 1

                        except:
                            if video_index > OTHERS_CNT:
                                section_now += 1
                                video_index = 1
                            else:
                                video_index += 1

        print('Done! thanks')
        driver.quit()
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

