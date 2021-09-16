import os
import sys
import json
import time
from typing import final
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

class PlayVideo():
    def __init__(self):
        self.config_dict = self._get_data()

        self.week = self.config_dict['week']
        self.class_link = self.config_dict['class_link']
        self.id = self.config_dict['id']
        self.pw = self.config_dict['password']

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=self.options)

        #self.driver = webdriver.Chrome('chromedriver.exe')
        self.url = "http://cyber.inu.ac.kr/"
        self.driver.get(self.url)
    
    def _get_data(self):
        try:
            with open("config.json","r", encoding="utf8") as f:
                contents = f.read()
                json_data = json.loads(contents)
            return json_data
        except:
            print("config.json file not found.")
    
    def login(self):
        """크롬 창 로딩 후 로그인 시도"""
        driver_id = self.driver.find_element_by_id("input-username").send_keys(self.id)
        driver_pw = self.driver.find_element_by_id("input-password").send_keys(self.pw)
        self.driver.find_element_by_class_name("btn-success").click()


    def play(self):
        max_class_index = 1
        section_now = self.week
        
        # for each subject
        for i in range(len(self.class_link)):
            time.sleep(3)
            self.driver.get(self.class_link[i])

            # for week
            video_index=0
            while video_index < 10:
                video_index += 1
                print('find video -> ', video_index)
                
                # find video
                try:
                    timeline = self.driver.find_element_by_xpath('//*[@id="section-' + str(section_now) + '"]/div[3]/ul/li[' + str(video_index) + ']/div/div/div[2]/div/span/span[2]').text
                    timeline = timeline.replace(", ", "")
                    print('video time : ', timeline)
                except:
                    print("video time : no video")
                    continue

                # click and change tab to open video
                self.driver.find_element_by_xpath('//*[@id="section-' + str(section_now) + '"]/div[3]/ul/li[' + str(video_index) + ']/div/div/div[2]/div/a').click()
                self.driver.switch_to.window(self.driver.window_handles[1])

                try:
                    # pass alert and played
                    da = Alert(self.driver)
                    da.accept()
                except:
                    # click play video
                    self.driver.find_element_by_xpath('//*[@id="vod_viewer"]').click()
                
                # wait playing video
                print('----- waiting video -----')
                times = reversed(list(map(int, timeline.split(':'))))
                video_time = [t * (60**i) for i, t in enumerate(times)]
                time.sleep(sum(video_time) + 20)
    
                # close and change tab
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                time.sleep(3)

        print('Done! Program terminated.')
        self.driver.quit()


if __name__=="__main__":
    playVideo = PlayVideo()
    playVideo.login()
    playVideo.play()
    