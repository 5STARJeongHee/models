#!/bin/bash/python3.7
# -*- coding:utf-8 -*-

from selenium import webdriver

from bs4 import BeautifulSoup as bs

import urllib.request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

import re

from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024,768))
display.start()

#############################브라우저를 테스트하는 인스턴스 생성############

drv = webdriver.Chrome('/home/ubuntu/Downloads/chromedriver') #현제 크롬 버전과 맞는 크롬 드라이버 위치

keyword_list =["시각장애인 블럭","시각장애인 도로","시각장애인 길","점자 도로","Tiles For Disable Blind People"]





####### 키워드와 구글 이미지 검색 url을 결합하고 해당 검색 창을 띄움###

for keyword in keyword_list:

    search_engine_url = "https://www.bing.com/images/search?q="+keyword+"&qs=n&form=QBIR&qft=%20filterui%3Aimagesize-custom_512_512"

    print(search_engine_url)
    try:
        drv.get(search_engine_url)
        time.sleep(3)
    except TimeoutException as e:
        print("time out")
        print(e)


    #search_box = drv.find_element_by_name('q') #검색창 선택

    #search_box.send_keys(keyword)# 키워드 입력

    #search_box.submit()#엔터 -> 이미지 검색화면으로 옮기기엔 위의 방법이 더 빨라서 잠시 주석걸어둠



    #search_page = drv.page_source #



    #soup=bs(second_page, 'html.parser') # 검색창에서 이미지 검색창으로 옮기기 위한 url을 받아오기 위한거지만 주석걸어둠



    ###############################  스크롤 끝까지 내려서 문서 완성시키기 ###########



    for i in range(1,30):

        drv.find_element_by_xpath("//body").send_keys(Keys.END) #스크롤을 밑바닥까지

        time.sleep(0.5)



    #######################################################################

    #menu_list = soup.select("#hdtb-msb-vis > div:nth-child(2) > a")





    #이미지 소스 정보 리스트 작성

    params = [] #이미지 원본 주소 넣을 빈 리스트

    search_page_html = drv.page_source

    pattern = "[>|\s]\d{2,7}"#>나 공백이 숫자(1자리~5자리) 바로 앞에 있는 패턴만 가져오기

    #옆의 것에서 숫자 2개만 뽑아오게됨 <a id="msz" target="_blank" href="/images/search?q=%25ec%2597%25ac%25ec%259e%2590&amp;cbir=ms&amp;rxc=12&amp;sbirxc=30&amp;mid=DBF16767D97D177C71611A37854C459EB4FA96FE&amp;simid=0&amp;vw=e6be4%20e6bdb%20c06d1%20860de%2014729%2087d49%206756a%20c0994%20181b8%206d161%207339d%20c6be4%2037497%208fc2f%2044de8%20c6c1f%20dfc14%20cbd79%2080e83%2084952%20850a45f8eb1e8a3d70d5dc71255730af70ed580dca955061668550b3522cd711d354e98d399dad875abcb32e52f0114dd384&amp;FORM=IMSFRD" data-tooltip="크기 더 보기">1000 × 1500 jpeg</a>

    soup = bs(search_page_html, "html.parser") #현제 페이지 파서 가져오기(검색창)

    img_links = soup.find_all("a",class_='iusc')# 이미지 링크 다 가져오기

    print(len(img_links))

    count = 0;

    for list in img_links:

        drv.execute_script('window.open("about:blank","_blank");')#빈 탭 열기
        time.sleep(1)
        tabs = drv.window_handles#탭 핸들러가져오기

        drv.switch_to.window(tabs[1])#두번째 탭으로 핸들러 옮김

        try:
            drv.get("https://bing.com"+list.get('href'))#두번 째 탭에서 앞의 이미지
            time.sleep(1)
            element = WebDriverWait(drv, 10).until(
            EC.presence_of_element_located((By.ID, "msz"))
            )
        except TimeoutException as e:
            print(e)
            drv.get("https://bing.com"+list.get('href'))#두번 째 탭에서 앞의 이미지
            time.sleep(5)
        
        new_tab = drv.page_source #이미지 링크로 열린 페이지 가져오기
        time.sleep(2)
        new_soup = bs(new_tab,"html.parser") #새로운 탭의 파서 가져오기

        img_src = new_soup.find("img",class_="nofocus")#원본 이미지 url 가져오기
    
        print(img_src)
        
        size_info = new_soup.find('a',id="msz")#이미지 크기 정보 가져오기
        time.sleep(1)        
        size_list = re.findall(pattern, str(size_info)) #이미지 사이즈 정보만 추출(문자열 좀더 가다듬어야됨)
        print(size_list)

        if len(size_list) !=0:
            size_list[0] = size_list[0].replace('>','')#아직 정리 안된 >문자 제거

            size_list[1] = size_list[1].strip()#아직 제거 안된 공백문자 제거

            width = int(size_list[0]) #너비 정보 정수로 변환

            height = int(size_list[1])#높이 정보 정수로 변환
        else :
            width = 1
            height =1 
            print("not found..")
        #print("width: " + str(width), "height: " + str(height))

        if width>=512 and height>=512: # 크기가 512 x 512 이상인 경우만

            count= count+1
            print(count)
            try:

                params.append(img_src.get('src'))

            except KeyError:

                params.append(img_src.get('data-src'))

        drv.close()

        drv.switch_to.window(tabs[0])



        #if count==5:
            #break

    #r을 문자열 앞에 붙이면 raw로 공백이든 뭐든 다 문자열로 받아주나 봄

    store_loc=r"/home/ubuntu/Crawling/BrailleBlock/"

    file_name=keyword

    #이미지 저장하기

    for id, loc in enumerate(params,1):# id 는 1부터, loc에는 차례대로 이미지 주소가 들어감

        try:

            name, header = urllib.request.urlretrieve(loc,store_loc + file_name + str(id)+".png")
            time.sleep(1)
        except Exception as e:#에러 처리 http 403 forbidden 같은 예외 처리

            print("------------------------------------")

            print(f"{id+1}번째 이미지 Download failed!")

            print(e)

        else:

            # 성공 시 response 상태정보 확인

            print("----------------------------------------------------")

            print(f"{id+1}번째 file dowload path: {name}")

            print("----------------------------------------------------")

            print(f"{id+1}번째 Header Info :")

            print(header)







drv.close()

