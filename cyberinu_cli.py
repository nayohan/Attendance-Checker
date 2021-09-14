import os
import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

class PlayVideo():
    def __init__(self):
        self.config_dict = self._get_data()

        self.week = self.config_dict['week']
        self.subject = self.config_dict['subject']
        self.id = self.config_dict['id']
        self.pw = self.config_dict['password']

        self.driver = webdriver.Chrome('chromedriver.exe')
        self.url = "http://cyber.inu.ac.kr/"
        self.driver.get(self.url)
    
    def _get_data(self):
        try:
            with open("config.json","r", encoding="utf8") as f:
                contents = f.read()
                json_data = json.loads(contents)
            return json_data
        except:
            print("Config.json file not found.")
    
    def login(self):
        """크롬 창 로딩 후 로그인 시도"""
        driver_id = self.driver.find_element_by_id("input-username").send_keys(self.id)
        driver_pw = self.driver.find_element_by_id("input-password").send_keys(self.pw)
        self.driver.find_element_by_class_name("btn-success").click()

    def delete_popup(self):
        try:
            # pop up # 팝업창 추가 #
            self.driver.find_element_by_xpath('//*[@id="notice_popup_1_429948"]/div[3]/span').click()
            self.driver.find_element_by_xpath('//*[@id="notice_popup_1_425577"]/div[3]/span').click()
            self.driver.find_element_by_xpath('//*[@id="notice_popup_1_421319"]/div[3]/span').click()
            self.driver.find_element_by_xpath('//*[@id="notice_popup_1_421317"]/div[3]/span').click()
            self.driver.find_element_by_xpath('//*[@id="notice_popup_1_420954"]/div[3]/span').click()
            self.driver.find_element_by_xpath('//*[@id="notice_popup_1_420953"]/div[3]/span').click()
        except:
            print('popup delete error -> update new version.')

    def play(self):
        max_class_index = 1
        section_now = self.week
        video_index=1

        # count number of class
        while 1:
            try:
                just_cnt = self.driver.find_element_by_xpath('//*[@id="region-main"]/div/div[1]/div[2]/ul/li[' + str(max_class_index) + ']/div/a/div[2]/div[2]')
                max_class_index += 1
            except:
                break
        
        # for each subject
        for i in range(len(self.subject)):
            try:
                for j in range(1, max_class_index):
                    class_str = self.driver.find_element_by_xpath('//*[@id="region-main"]/div/div[1]/div[2]/ul/li[' + str(j) + ']/div/a/div[2]/div[2]/h3').text
                    # find matched class name
                    if not class_str.find(self.subject[i]) == -1:
                        print('class:', class_str)
                        self.driver.find_element_by_xpath('//*[@id="region-main"]/div/div[1]/div[2]/ul/li[' + str(j) + ']/div/a').click()
                        break
            except:
                print('ERROR! can not find class name!')
                self.driver.quit()
                return

            # for each video
            while 1:
                # reach end of video
                if section_now > self.week:
                    print('Reach end of video num')
                    try:
                        self.driver.find_element_by_xpath('//*[@id="back-top"]').click()
                        time.sleep(3)
                        self.driver.find_element_by_xpath('//*[@id="page-header"]/nav/div/div[1]/a').click()
                        self.subject[i] = ''
                        section_now = self.week
                        video_index = 1
                        print('TOP - BACK')
                        break
                    except:
                        self.driver.find_element_by_xpath('//*[@id="page-header"]/nav/div/div[1]/a').click()
                        self.subject[i] = ''
                        section_now = self.week
                        video_index = 1
                        print('BACK')
                        break
                else:
                    try:
                        # get time
                        print('find video -> ', video_index)
                        timeline = self.driver.find_element_by_xpath('//*[@id="section-' + str(section_now) + '"]/div[3]/ul/li[' + str(video_index) + ']/div/div/div[2]/div/span/span[2]').text
                        timeline = timeline.replace(", ", "")
                        print('video time : ', timeline)

                        # click and open video
                        self.driver.find_element_by_xpath('//*[@id="section-' + str(section_now) + '"]/div[3]/ul/li[' + str(video_index) + ']/div/div/div[2]/div/a').click()
                        #print('----- open video -----')

                        # change tab
                        self.driver.switch_to.window(self.driver.window_handles[1])

                        # click play video
                        try:
                            # if not yet played video
                            self.driver.find_element_by_xpath('//*[@id="vod_viewer"]').click()
                        except:
                            # if video already clicked -> pass alert
                            da = Alert(self.driver)
                            da.accept()

                        # wait playing video
                        print('----- waiting video -----')
                        #time.sleep(int(timeline[:2]) * 60 + int(timeline[3:]) + 15)
                        time.sleep(10)
                        # close and change tab
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(2)

                        # go to next video
                        video_index += 1
                    except:
                        if video_index >= 10: # max video num for each week
                            section_now += 1
                            video_index = 1
                        else:
                            video_index += 1

        print('Done! Program terminated.')
        self.driver.quit()


if __name__=="__main__":
    playVideo = PlayVideo()
    playVideo.login()
    playVideo.delete_popup()
    playVideo.play()