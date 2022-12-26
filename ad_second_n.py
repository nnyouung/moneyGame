import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QHBoxLayout, QWidget, QGroupBox, QPushButton, QGridLayout,
                             QVBoxLayout, QMessageBox, QLCDNumber, QDesktopWidget)
from PyQt5.QtCore import QTimer
from matplotlib import pyplot as plt
import ad_first_n
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
from musicPlayer import *

class AdSecond(QWidget):
    def __init__(self, itemnumber, myitemnumber, mission):
        super(AdSecond, self).__init__()
        self.setStyleSheet("background-color: white;")
        self.OriginItems = 'items.txt'
        self.OriginMyItems = 'myItems.txt'
        self.items = []
        self.myItems = []
        self.myItemsPriceList = []
        self.myExp = 0
        self.buy_count = 0
        self.sell_count = 0
        self.remainLife = 10   # 각각 buy와 sell이 5번씩 가능하도록 해놨으므로, 총 10번의 기회가 있음.
        self.itemnumber = itemnumber
        self.myitemnumber = myitemnumber
        self.missioning = mission
        self.money = 20000  # 보유금
        self.buyPrice = 0

        f = open("buypriceTmp.txt", 'r')
        self.myItemBoughtPrice = f.readline()
        f.close()
        
        self.music = MusicPlayer()
        self.music.playAudioFile()
        
        self.initUI()
        self.disabledBtn()
        self.moneyDB()
        self.center()
        self.show()

    def initUI(self):

        f = open("buypriceTmp.txt" ,'w')
        f.write('')
        f.close()

        grid = QGridLayout()
        grid.addWidget(self.groupGameInfo(), 0, 0)
        grid.addWidget(self.groupGraphandTimer(1061, 950, 0, 0), 1, 0)  # 그래프 파라미터 수정하기
        grid.addWidget(self.groupButtons(), 2, 0)

        self.setLayout(grid)

        self.setWindowTitle("Game")
        self.resize(600, 800)
        self.center()
        self.show()

    # 돈 관리 함수 (값 업데이트 용도)
    def moneyDB(self):
        f = open('money.txt', 'w')
        money = f.write(str(int(self.money)))
        self.money = money
        f.close()

    # 물건 목록 관리 함수
    def readDB_1(self, filename):
        self.f = open(filename, 'r')
        for line in self.f:
            dat = line.strip()
            object = dat.split(',')

            record = {}
            for attr in object:
                kv = attr.split(':')
                record[kv[0]] = kv[1]
            self.items += [record]
        self.f.close()

    # 보유 물건 목록 관리 함수
    def readDB_2(self, filename):
        self.f = open(filename, 'r')
        for line in self.f:
            dat = line.strip()
            object = dat.split(',')

            record = {}
            for attr in object:
                kv = attr.split(':')
                record[kv[0]] = kv[1]
            self.myItems += [record]
        self.f.close()

    # 상점 물건 혹은 보유 물건인지에 따라, buy/sell 버튼 활성화 혹은 비활성화
    def disabledBtn(self):
        if self.myitemnumber == -1:   # 상점 물건일 때
            self.sellButton.setEnabled(False)
            self.buyButton.setEnabled(True)
        else:   # 보유 물건일 때
            self.sellButton.setEnabled(True)
            self.buyButton.setEnabled(False)

    # 게임 정보창
    def groupGameInfo(self):
        self.readDB_1(self.OriginItems)
        self.readDB_2(self.OriginMyItems)

        groupbox = QGroupBox("게임 정보")

        if self.itemnumber != -1:
            # 상점 물건 선택
            self.object = str(self.items[self.itemnumber]['name'])
            currentItem = QLabel("물건 : %s" % self.object)
        if self.myitemnumber != -1:
            # 보유 물건 선택
            self.object = str(self.myItems[self.myitemnumber]['name'])
            currentItem = QLabel("물건 : %s" % self.object)

        # 초기 가격 연동
        if self.myitemnumber == -1:
            price = self.items[self.itemnumber]['initPrice']
        else:
            price = self.myItems[self.myitemnumber]['initPrice']

        initPrice = QLabel(f"초기 가격 : {price}")
        self.currentPrice = QLabel("현재 가격 : ")
        self.buyMoney = QLabel("구매 시 가격 : 0")
        self.sellMoney = QLabel("판매 시 가격 : 0")
        self.currentMoney = QLabel(f"현재 보유금 : {self.money}")
        self.remainNum = QLabel("남은 횟수 : 10")
        self.currentReturn = QLabel(f"현재 수익률 : 0%")
        currentMission = QLabel(
            "현재 미션: {0}의 수익률 {1}%이상 달성하면 {2} exp 지급".format(self.missioning['object'],
                                                               self.missioning['margin'], self.missioning['exp']))

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()

        vbox.addLayout(hbox)
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        vbox.addWidget(currentItem)
        vbox.addWidget(initPrice)
        vbox.addWidget(self.currentPrice)
        vbox.addWidget(self.buyMoney)
        vbox.addWidget(self.sellMoney)
        vbox.addWidget(self.currentMoney)
        vbox.addWidget(self.remainNum)
        vbox.addWidget(self.currentReturn)
        vbox.addWidget(currentMission)

        groupbox.setLayout(vbox)
        return groupbox

    def groupGraphandTimer(self, rate_max, rate_min, max_count, min_count):
        groupbox = QGroupBox()
        vbox = QVBoxLayout()

        # 타이머
        self.timerLabel = QLCDNumber()
        self.timerLabel.display(60)
        self.timerLabel.setSegmentStyle(2)
        self.timerLabel.setFixedSize(600, 70)
        self.timer()  # 타이머 자동 실행

        # 그래프
        self.fig = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.fig)

        self.line = plt.plot([], [],  # 그래프 라인 생성
                             color='red',
                             marker='o',
                             markerfacecolor='red',
                             markersize=1)[0]

        # print(self.items)   # 아이템 확인 (최종적으로 불필요)
        # print(self.itemnumber)   # 아이템 번호 확인 (최종적으로 불필요)

        # 그래프에 초기 가격 연동
        if self.myitemnumber == -1:
            price = self.items[self.itemnumber]['initPrice']
        else:
            l = open('buyprice.txt' ,'r')
            price = l.readline()
            l.close()
            print(price)

        self.price = price # 초기 가격
        self.rate_max = rate_max  # 10.6배 변화
        self.rate_min = rate_min  # 0.95배 변화
        self.max_count = max_count  # 하한선 체크 용도
        self.min_count = min_count  # 상한선 체크 용도

        # 그래프 표시 구간 설정
        plt.xlim(0, 301)  # x구간 300까지
        plt.ylim(0, 3*int(self.price))  # y구간 30000까지

        # 재료
        self.x = []
        self.y = []
        self.z = []

        self.minimum = float(self.price) * 0.8
        self.maximum = float(self.price) * 1.5

        # frames (x가 1,2,3... 순차적으로 들어가는 리스트 생성)
        for i in range(0, 301):
            self.z.append(i)

        # update 함수 반복 후 창 표시
        self.ani = FuncAnimation(fig=self.fig, func=self.update, frames=self.z, interval=200)
        self.canvas.draw()
        self.show()

        vbox.addWidget(self.timerLabel)
        vbox.addWidget(self.canvas)

        groupbox.setLayout(vbox)
        return groupbox

    # 그래프 관련 함수
    def update(self, i):
        change_rate = (np.random.randint(self.rate_min, self.rate_max)) / 1000  # 난수 생성 (0.95~1.06)
        # print(change_rate)  # 난수가 제대로 생성되었는지 확인 (최종적으로는 불필요)
        # print(self.price)   # 최종 가격 확인 (최종적으로는 불필요)

        self.price = float(self.price) * change_rate  # 가격 변동

        self.x.append(i)
        self.y.append(self.price)
        self.line.set_data(self.x, self.y)

        # 만약 가격이 8000원 미만으로 떨어지면 범위를 0.95~1.08 (또는 0.92~1.08)로 조정
        if self.max_count < 1:
            if self.price < self.minimum:
                self.rate_max += 30
                self.max_count = 1  # 한번만 할 수 있도록 하는 장치 (이걸 안하면 0.95 ~ 1.50 이런 식으로 확 뛸 수도 있습니다.)

        # 만약 가격이 15000원을 초과하면 범위를 0.92~1.06 (또는 0.92~1.08)로 조정
        if self.min_count < 1:
            if self.price > self.maximum:
                self.rate_min -= 30
                self.min_count = 1

        currentPrice = self.y[-1]
        self.currentPrice.setText(f"현재 가격 : {int(currentPrice)}")
        self.currentPrice.repaint()

    # timer, printTimer 모두 타이머 관련 함수
    def timer(self):
        self.initTime = 60  # 타이머 초기값

        self.leftTime = self.initTime  # 남은 시간

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.printTimer)
        self.timer.start(1000)

    def printTimer(self):
        self.leftTime -= 1

        if self.leftTime == -1:   # 미션 클리어 전에 시간 초과 시, 게임 오버
            self.leftTime = 0
            self.timer.stop()   # 타이머 중지
            self.ani.event_source.stop()   # 그래프 중지
            gameoverMB = QMessageBox.warning(self, "게임 종료", "Game Over", QMessageBox.Ok)
            if gameoverMB == QMessageBox.Ok:
                self.close()   # 두 번째 창 닫기

        self.timerLabel.display(self.leftTime)  # gui에 업데이트

    def groupButtons(self):
        groupbox = QGroupBox()

        self.buyButton = QPushButton("BUY")
        self.sellButton = QPushButton("SELL")
        self.buyButton.setStyleSheet(
            "QPushButton{padding:8px; color: white;background-color: rgb(58, 134, 255); border-radius: 30px;}")
        self.sellButton.setStyleSheet(
            "QPushButton{padding:8px; color: white;background-color: rgb(58, 134, 255); border-radius: 30px;}")

        font = self.buyButton.font()  # 폰트 객체생성
        font.setPointSize(font.pointSize() + 1)  # 글꼴크기+1
        self.buyButton.setFont(font)
        font2 = self.sellButton.font()  # 폰트 객체생성
        font2.setPointSize(font2.pointSize() + 1)  # 글꼴크기+1
        self.sellButton.setFont(font2)

        hbox = QHBoxLayout()
        hbox.addWidget(self.buyButton)
        hbox.addWidget(self.sellButton)

        groupbox.setLayout(hbox)
        self.buyButton.clicked.connect(self.buyItem)
        self.sellButton.clicked.connect(self.sellItem)

        return groupbox

    # 파일 관리 함수에 텍스트 파일 넣기
    def itemsInit(self):
        self.readDB_1(self.OriginItems)
        self.readDB_2(self.OriginMyItems)

    # 여러 번 사고 팔 때의 중복 제거
    def overlapRemove(self, filename):
        self.f_ = open(filename, 'r')
        data = self.f_.readlines()
        data2 = []
        for i in data:
            if data not in data2:
                data2.append(i)
        self.f_ = open(filename, 'w')
        self.f_ = open(filename, 'a')
        for i in data2:
            self.f_.write(str(i))
        self.f_.close()

    def buyItem(self):
        if self.buy_count > 4:   # 미션 클리어 전에 횟수 제한 시, 게임 오버
            self.timer.stop()  # 타이머 중지
            self.ani.event_source.stop()  # 그래프 중지
            gameoverMB = QMessageBox.warning(self, "게임 종료", "Game Over", QMessageBox.Ok)
            if gameoverMB == QMessageBox.Ok:
                self.close()  # 두 번째 창 닫기
        else:
            self.itemsInit()
            objectName = str(self.items[self.itemnumber]['name'])
            objectPrice = str(self.items[self.itemnumber]['initPrice'])
            objectInformation = f"name:{objectName},initPrice:{objectPrice}\n"

            # 구매 가격 저장 : 저장된 가격들 중 제일 마지막꺼 저장
            self.buyPrice = self.y[-1]
            
            #구매 가격 메모장에 남기기
            f = open("buyprice.txt", 'a')
            f.write(str(int(self.buyPrice))+'\n')
            f.close()

            f = open("buyprice.txt" , 'r')
            prices = f.readlines()
            f.close()

            f = open("buypriceTmp.txt" , 'w')
            f.write(prices[-1])
            f.close()

            # 구매 시 가격
            self.buyMoney.setText(f"구매 시 가격 : {int(self.buyPrice)}")
            self.buyMoney.repaint()

            # 물건 구매하고 남은 돈
            self.money -= self.buyPrice
            self.currentMoney.setText(f"현재 보유금 : {int(self.money)}")
            self.currentMoney.repaint()


            # 보유 물건(myItem)에 추가
            self.myFile = open('myItems.txt', 'a')
            self.myFile.write(objectInformation)
            self.myFile.close()

            # 상점 물건(item)에서 제거
            self.file = open('items.txt', 'r')
            data = self.file.readlines()
            self.file = open('items.txt', 'w')
            for i in data:
                if i != objectInformation:
                    self.file.write(i)
            self.file.close()

            # 이미 보유 물건에 있을 경우, 더 이상 buy 못하도록
            file = open('myItems.txt', 'r')
            data = file.readlines()
            for i in data:
                if i == objectInformation:
                    self.buyButton.setEnabled(False)
                    self.sellButton.setEnabled(True)
            file.close()

            self.overlapRemove('myItems.txt')

            self.buy_count += 1

            # 남은 횟수 구현
            self.remainLife -= 1
            self.remainNum.setText(f"남은 횟수 : {self.remainLife}")
            self.remainNum.repaint()

    def price(self):
        pass

    def sellItem(self):
        if self.sell_count > 4:   # 미션 클리어 전에 횟수 제한 시, 게임 오버
            self.timer.stop()  # 타이머 중지
            self.ani.event_source.stop()  # 그래프 중지
            gameoverMB = QMessageBox.warning(self, "게임 종료", "Game Over", QMessageBox.Ok)
            if gameoverMB == QMessageBox.Ok:
                self.close()  # 두 번째 창 닫기
        else:
            self.itemsInit()
            objectName = str(self.myItems[self.myitemnumber]['name'])
            objectPrice = str(self.myItems[self.myitemnumber]['initPrice'])
            objectInformation = f"name:{objectName},initPrice:{objectPrice}\n"

            # 판매 가격 저장 : 저장된 가격들 중 제일 마지막꺼 저장
            self.sellPrice = self.y[-1]
            self.myItemsPriceList.append(self.sellPrice)

            # 판매 시 가격
            self.sellMoney.setText(f"판매 시 가격 : {int(self.sellPrice)}")
            self.sellMoney.repaint()

            # 물건 판매하고 남은 돈
            self.money += self.sellPrice
            self.currentMoney.setText(f"현재 보유금 : {int(self.money)}")
            self.currentMoney.repaint()

            # 상점 물건(item)에 추가
            self.file2 = open('items.txt', 'a')
            self.file2.write(objectInformation)
            self.file2.close()

            # 보유 물건(myItem)에서 제거
            self.myFile2 = open('myItems.txt', 'r')
            data = self.myFile2.readlines()
            self.myFile2 = open('myItems.txt', 'w')
            for i in data:
                if i != objectInformation:
                    self.myFile2.write(i)
            self.myFile2.close()

            # 이미 상점 물건에 있을 경우, 더 이상 sell 못하도록
            f = open('items.txt', 'r')
            data = f.readlines()
            for i in data:
                if i == objectInformation:
                    self.sellButton.setEnabled(False)
                    self.buyButton.setEnabled(True)
            f.close()

            self.overlapRemove('items.txt')

            # 수익률 계산: (현재가격 / 구매시가격) * 100 - 100
            if self.buyPrice == 0:
                # 수익률 계산하기 위해 보유 물건의 구매했던 가격 불러옴
                f = open("buyprice.txt", 'r')
                f2 = open("myItems.txt", 'r')
                # for i in range(len(f2.readlines()[:])):
                #     self.myItemBoughtPrice = int(f.readlines()[i])
                f.close()
                self.Mymargin = (float(self.myItemBoughtPrice) / self.sellPrice) * 100 - 100
                self.currentReturn.setText(f'현재 수익률 : {self.Mymargin:.2f}%')
                self.currentReturn.repaint()
            else:
                self.Mymargin = (self.sellPrice / self.buyPrice) * 100 - 100
                self.currentReturn.setText(f'현재 수익률 : {self.Mymargin:.2f}%')
                self.currentReturn.repaint()

            # 미션 수행
            self.doMissions()

            self.sell_count += 1

            # 남은 횟수 구현
            self.remainLife -= 1
            self.remainNum.setText(f"남은 횟수 : {self.remainLife}")
            self.remainNum.repaint()

    def doMissions(self):
        if ((self.object == self.missioning['object']) & (int(self.Mymargin) >= int(self.missioning['margin']))):
            # 경험치 누적
            self.myExp = int(self.missioning['exp'])
            print(self.myExp)

            f = open("experience.txt", 'r')
            self.current_exp = f.readline()
            self.current_exp = int(self.current_exp) + self.myExp
            f.close()
            f = open("experience.txt", 'w')
            f.write(str(self.current_exp))
            f.close()

            # 완료된 미션 제거
            self.missionInfo = f"object:{self.missioning['object']},margin:{self.missioning['margin']},exp:{self.missioning['exp']}\n"

            self.missionFile = open('missions2.txt', 'r')
            data = self.missionFile.readlines()
            self.missionFile = open('missions2.txt', 'w')
            for i in data:
                if i != self.missionInfo:
                    self.missionFile.write(i)
            self.missionFile.close()

            # 알림창 뜨고, 메인 화면으로 돌아감
            buttonReply = QMessageBox.information(self, '미션 Clear', '미션을 완료했습니다!\n경험치 {0}exp 획득!'.format(self.missioning['exp']),QMessageBox.Yes)
            self.timer.stop()  # 타이머 중지
            self.ani.event_source.stop()  # 그래프 중지
            if buttonReply == QMessageBox.Yes:
                self.hide()
                self.firstopen = ad_first_n.AdFirst(self.myExp)
                self.firstopen.show()
        else:
            self.myExp = 0

    # 창을 끄게 되면 첫 번째 창으로 되돌아가는 함수
    def closeEvent(self, QCloseEvent):
        self.moneyDB()
        goFirstMB = QMessageBox.question(self, "메인 화면 이동", "메인화면으로 이동하시겠습니까?", QMessageBox.Yes | QMessageBox.No)

        if goFirstMB == QMessageBox.Yes:
            QCloseEvent.accept()
            self.timer.stop()   # 타이머 중지
            self.ani.event_source.stop()   # 그래프 중지
            self.music.stopAudioFile()   # 노래 중지
            self.first = ad_first_n.AdFirst(0)
            self.first.show()
        else:
            QCloseEvent.ignore()

    # 게임이 화면 중앙에 뜰 수 있도록 만드는 함수
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = AdSecond(0, 0, 0)
#     sys.exit(app.exec_())
