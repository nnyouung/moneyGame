# 💸 moneyGame 💸
## 주어진 물건들을 사고파는 시뮬레이션을 통해 수익을 내어, 그 수익을 통해 주어진 미션을 클리어하는 게임.

- - -

### ▶︎ 사용된 라이브러리
- pyQt5: QtWidgets, QtCore, QtGui
- matplotlib: animation, backends.backend_qt5agg
- musicPlayer
- numpy

- - -

### ▶︎ 설명
<img width="1440" alt="1" src="https://user-images.githubusercontent.com/104901660/209536318-ea482c9c-8d32-4790-8f5e-fb3f184c70eb.png">
<img width="1440" alt="2" src="https://user-images.githubusercontent.com/104901660/209536323-0c6d8b9e-0848-4866-971b-f465b98667df.png">
<img width="1440" alt="3" src="https://user-images.githubusercontent.com/104901660/209536330-204d3c40-7bad-48f9-bbe5-9cd1d46b6955.png">

- - -

### ▶︎ 게임 실행 동영상

- - -

### ▶︎ 소스파일 설명
- ad_first_n : 게임의 Home 창을 관리합니다.
- ad_second_n.py : 게임의 Game 창을 관리합니다.
- mission_n.py : 미션 관련 데이터를 관리합니다.
- musicPlayer.py : 게임 음악을 관리합니다.
- buyprice.txt : 구매 가격을 저장합니다. 초기에는 아무 내용도 없어야 합니다.
- buypriceTmp.txt : 가장 최근의 구매 가격 하나만 저장합니다. 초기에는 아무 내용도 없어야 합니다.
- items.txt : 초기 아이템들 목록입니다. 초기 내용은 다음과 같아야 합니다.
> name:IPhone11,initPrice:9000  
> name:Ipad,initPrice:9000  
  name:NikeShoes,initPrice:7000
  name:AppleWatch,initPrice:8000
  name:LogitechMouse,initPrice:7000
  name:Egg,initPrice:9450
  name:IPhone11ProMax,initPrice:10300
  name:LgGram,initPrice:12000
  name:Apple,initPrice:8500
  name:GalaxyS22,initPrice:9000
- myItems.txt : 구매한 아이템들의 목록이 들어갑니다. 초기에는 아무 내용도 없어야 합니다.
- missions2.txt : 미션 목록이 들어갑니다. 여기서 랜덤으로 미션을 가져와 게임을 실행하는 것입니다.
- money : 가지고 있는 금액의 정보를 담고 있습니다. 초기값은 20000 입니다.
- experience.txt : 가지고 있는 경험치의 정보를 담고 있습니다. 초기값은 0 입니다.
- bgm.mp3 : 게임 음악 파일입니다.
- 1.jpg / 2.jpg / 3.jpg : 프로필 이미지 파일입니다.
