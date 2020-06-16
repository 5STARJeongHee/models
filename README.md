![Logo](https://storage.googleapis.com/model_garden_artifacts/TF_Model_Garden.png)

# Welcome to the Model Garden for TensorFlow

The TensorFlow Model Garden is a repository with a number of different implementations of state-of-the-art (SOTA) models and modeling solutions for TensorFlow users. We aim to demonstrate the best practices for modeling so that TensorFlow users can take full advantage of TensorFlow for their research and product development.

| Directory | Description |
|-----------|-------------|
| [official](official) | • A collection of example implementations for SOTA models using the latest TensorFlow 2's high-level APIs<br />• Officially maintained, supported, and kept up to date with the latest TensorFlow 2 APIs by TensorFlow<br />• Reasonably optimized for fast performance while still being easy to read |
| [research](research) | • A collection of research model implementations in TensorFlow 1 or 2 by researchers<br />• Maintained and supported by researchers |
| [community](community) | • A curated list of the GitHub repositories with machine learning models and implementations powered by TensorFlow 2 |

## [Announcements](../../wiki/Announcements)

| Date | News |
|------|------|
| May 21, 2020 | [Unifying Deep Local and Global Features for Image Search (DELG)](https://github.com/tensorflow/models/tree/master/research/delf#delg) code released
| May 7, 2020 | [MnasFPN with MobileNet-V2 backbone](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md#mobile-models) released for object detection
| May 1, 2020 | [DELF: DEep Local Features](https://github.com/tensorflow/models/tree/master/research/delf) updated to support TensorFlow 2.1
| March 31, 2020 | [Introducing the Model Garden for TensorFlow 2](https://blog.tensorflow.org/2020/03/introducing-model-garden-for-tensorflow-2.html) ([Tweet](https://twitter.com/TensorFlow/status/1245029834633297921)) |

## Contributions

[![help wanted:paper implementation](https://img.shields.io/github/issues/tensorflow/models/help%20wanted%3Apaper%20implementation)](https://github.com/tensorflow/models/labels/help%20wanted%3Apaper%20implementation)

If you want to contribute, please review the [contribution guidelines](../../wiki/How-to-contribute).

## License

[Apache License 2.0](LICENSE)

## bing_crawler.py
-----------------------------
Bing 웹사이트에서 이미지를 긁어모으는 파이썬 스크립트 코드로
아래와 같은 설정들을 변경해주어야 사용 가능합니다.

0. 설치 해야할 것: 
1)크롬

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "sudo deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update
sudo apt-get install google-chrome-stable

2)크롬드라이버

wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
unzip chromedriver_linux64.zip


3)xvfb, python, python-pip
sudo apt-get install xvfb python3.6
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6

4)selenium, bs4, pyvirtualdisplay (드라이버를 팬텀으로 써도 브라우저 동작하는 모습을 안보이게 할수 있다.)

pip install seleium bs4 pyvirtualdisplay

1. 리눅스 전용 라이브러리가 있어서 윈도우에서 사용하려면 

from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024,768))
display.start()

위의 코드를 지워야 됩니다.

2. 크롬드라이버의 위치에 따라 경로명을 바꾸셔야 합니다.

drv = webdriver.Chrome('/home/ubuntu/Downloads/chromedriver') #현제 크롬 버전과 맞는 크롬 드라이버 위치

위의 코드에서 '/home/ubuntu/Downloads/chromedriver' 부분을 변경 

3. 긁어 모을 이미지의 검색어들을 변경

keyword_list =["시각장애인 블럭","시각장애인 도로","시각장애인 길","점자 도로","Tiles For Disable Blind People"]

위의 코드의 리스트에 있는 검색어들을 지우고 검색하실 검색어들을 넣어주세요

4. url 

search_engine_url = "https://www.bing.com/images/search?q="+keyword+"&qs=n&form=QBIR&qft=%20filterui%3Aimagesize-custom_512_512"

위와 같이 url의 keyword 뒷 부분에 512x512 이상의 이미지만 검색하도록 되어 있으므로 keword 뒷 부분을 없애시면 512x512 크기 보다 작은 이미지도 검색 가능합니다.

5. 크기 512x512 이상인 이미지만 저장되는 부분

 if width>=512 and height>=512: # 크기가 512 x 512 이상인 경우만

            count= count+1
            print(count)
            try:

                params.append(img_src.get('src'))

            except KeyError:

                params.append(img_src.get('data-src'))

        drv.close()

        drv.switch_to.window(tabs[0])
        
위의 코드의 512x512 이상의 이미지만 골라 내기 위해 사용했었음 512를 다른 숫자로 변경하면 다른 크기의 이미지도 저장되게 할 수 있습니다.

6. 이미지 저장 경로 변경

store_loc=r"/home/ubuntu/Crawling/BrailleBlock/"

위의 변수의 경로를 변경하시면 됩니다. 

7. 타임스탬프 찍기
from datetime import datetime 이렇게 임포트해서 
print(str(datetime.now())) 이 코드로 timestamp 찍는거 참고하려고 여기에 잠시 썼습니다.
