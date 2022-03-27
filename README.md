# hcs-python

## 기존 라이브러리 호환

기존에 있던 그 라이브러리의 코드는 [old 브랜치에 있습니다.](https://github.com/covid-hcs/hcs-python/tree/old)
하지만 그 브랜치는 유지보수가 잘 되지 않을 가능성이 높기 때문에, 대신 이 main 브랜치를 쓰시는 게 좋습니다.  
새로 바뀐 api에 맞춰 코드를 갈아엎기 힘드시다면 `covid_hcs.old` 모듈을 import하면 기존의 api와 호환되는 api를
쓸 수 있습니다. 다만 해당 모듈의 라이센스는 기존 라이브러리와 같은 GPL-3.0으로 제공됩니다.


## 예시 코드




## 다운로드

git을 통해 설치하실 수 있습니다.
> 윈도우나 리눅스의 터미널에서 다음과 같이 입력합니다.
> ```shell
> python -m pip install -U pip
> pip install git+https://github.com/covid-hcs/hcs-python.git@main
> ```


## 도움을 주신 분

[코드 일부분(transkey 부분)](https://github.com/covid-hcs/transkey-py)의 저작권은 blluv 님에게 있습니다.
