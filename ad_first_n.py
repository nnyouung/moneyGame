import sys
from PyQt5.QtWidgets import (QApplication, QComboBox, QProgressBar, QListWidget, QDesktopWidget, QSpacerItem)
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QRect
from ad_second_n import *
from mission_n import Word

class AdFirst(QWidget):
    def __init__(self, exp):
        super().__init__()
        self.OriginItems = 'items.txt'
        self.OriginMyItems = 'myItems.txt'
        self.items = []
        self.myItems = []
        self.totalExps = 0
        self.gotExps = exp
        self.current_exp = 0
        self.my_level = 0
        self.level_value = 0
        self.lv_value = 0
        self.setStyleSheet("background-color: white;")
        self.initUI()
        self.show()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.groupMyInfo(), 0, 0, 1, 2)
        grid.addWidget(self.groupMyMission(), 1, 0, 1, 2)
        grid.addWidget(self.groupListOfThings1(), 2, 0, 1, 1)
        grid.addWidget(self.groupListOfThings2(), 2, 1, 1, 1)
        grid.addWidget(self.groupButtons(), 3, 0, 1, 2)

        self.setLayout(grid)

        self.setWindowTitle("Main Window")
        self.resize(50, 600)
        self.center()

    # 돈 관리 함수 (저장된 값 읽어오는 용도)
    def moneyDB(self):
        f = open('money.txt', 'r')
        self.money = f.readline()
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

    def groupMyInfo(self):
        groupbox = QGroupBox("MY PAGE")

        # 프로필 콤보박스
        self.combo = QComboBox()
        self.combo.addItems(["1번", "2번", "3번"])
        self.combo.setStyleSheet(
            "QComboBox{background-color: rgb(231, 230, 234); border-radius: 10px;border:1px solid gray;padding: 1px 18px 1px 3px;min-width: 6em;")

        # 기본 프로필 이미지
        self.image = QLabel()
        self.image.setPixmap(QPixmap("1.jpg").scaled(70, 70))

        # 이미지 바꾸는 기능
        self.combo.currentIndexChanged.connect(self.imageCombo)

        # 경험치와 레벨
        f = open("experience.txt", 'r')
        self.current_exp = f.readline()
        f.close()

        if int(self.current_exp) < 20:
            self.my_level = 1
        elif int(self.current_exp) < 40:
            self.my_level = 2
        elif int(self.current_exp) < 60:
            self.my_level = 3
        elif int(self.current_exp) < 80:
            self.my_level = 4
        elif int(self.current_exp) < 100:
            self.my_level = 5
        elif int(self.current_exp) < 120:
            self.my_level = 6
        else:
            self.my_level = 7

        # 레벨
        if self.my_level < 7:
            level = QLabel("레벨: {}".format(self.my_level))
        else:
            level = QLabel("레벨: MAX")

        # 현재 보유금
        self.moneyDB()
        self.currentMoney = QLabel(f"현재 보유금 : {self.money}")

        # 경험치
        f = open("experience.txt", 'r')
        self.current_exp = f.readline()
        f.close()
        self.lv_value = 5 * int(self.current_exp)
        self.level_value = ((self.lv_value) % 20) * 5

        self.experience = QProgressBar()
        self.experience.setStyleSheet(
            "QProgressBar{border:1.5px solid grey;border-radius:4px;} "
            "QProgressBar::chunk {background-color:#FFC5D6; width:15px;  }")
        self.experience.setGeometry(30, 40, 200, 25)
        self.experience.setValue(self.level_value)  # 경험치 값
        self.experience.setAlignment(Qt.AlignCenter)  # 경험치 숫자의 위치

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox1 = QVBoxLayout()   # 콤보박스, 이미지 칸
        vbox2 = QVBoxLayout()   # 수익률, 레벨, 경험치, 미션 칸

        vbox.addLayout(hbox)
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        vbox1.addWidget(self.combo)
        vbox1.addWidget(self.image)
        vbox2.addWidget(self.currentMoney)
        vbox2.addWidget(level)
        vbox2.addWidget(self.experience)

        groupbox.setLayout(vbox)
        return groupbox

    def groupMyMission(self):
        groupbox = QGroupBox("MISSION")
        # 현재 미션
        word = Word('missions2.txt')
        self.a = word.randFromDB()
        self.mission = QLabel(
            "현재 미션: {0}의 수익률 {1}%이상 달성하면 {2} exp 지급".format(self.a['object'], self.a['margin'], self.a['exp']))

        hbox = QHBoxLayout()
        hbox.addWidget(self.mission)
        groupbox.setLayout(hbox)

        return groupbox

    def groupListOfThings1(self):
        self.readDB_1(self.OriginItems)
        groupbox = QGroupBox("SHOP")

        self.listWidget = QListWidget()
        for i in range(len(self.items)):
            self.listWidget.insertItem(i, str(self.items[i]['name']))

        vbox = QVBoxLayout()
        vbox.addWidget(self.listWidget)

        groupbox.setLayout(vbox)

        return groupbox

    def groupListOfThings2(self):
        self.readDB_2(self.OriginMyItems)
        groupbox = QGroupBox("MY BAG")

        f = open("buyprice.txt", 'r')
        self.buyPrice = f.readlines()
        f.close()

        self.listWidget2 = QListWidget()
        for i in range(len(self.myItems)):
            try:
                self.listWidget2.insertItem(i, f"{self.myItems[i]['name']}, {self.buyPrice[i].rstrip()}원")
            except IndexError:
                self.listWidget2.insertItem(i, self.myItems[i]['name'])

        vbox = QVBoxLayout()
        vbox.addWidget(self.listWidget2)

        groupbox.setLayout(vbox)

        return groupbox

    def groupButtons(self):
        groupbox = QGroupBox()

        startButton = QPushButton("Game Start")
        startButton.setStyleSheet(
            "QPushButton{padding:8px; color: white;background-color: rgb(58, 134, 255); border-radius: 30px;}")

        hbox = QHBoxLayout()
        hbox.addWidget(startButton)

        groupbox.setLayout(hbox)
        startButton.clicked.connect(self.buttonToSecond)

        return groupbox

    # Game 창과 연동
    def buttonToSecond(self):
        self.currentMoney.setText(f"현재 보유금 : {self.money}")
        self.currentMoney.repaint()

        self.itemNumber = -1
        self.myItemNumber = -1

        item = self.listWidget.currentItem()
        if (item == None):
            self.itemNumber = -1
        else:
            for i in range(len(self.items)):
                if item.text() == self.items[i]['name']:
                    self.itemNumber = i

        item2 = self.listWidget2.currentItem()
        if (item2 == None):
            self.myItemNumber = -1
        else:
            for i in range(len(self.myItems)):
                target = self.myItems[i]['name']
                s = item2.text().find(target)
                if s >= 0:
                    self.myItemNumber = i

        if (self.itemNumber == -1) and (self.myItemNumber == -1):   # 물건 선택 안 했을 때 경고창
            QMessageBox.warning(self, "Warning", "하나의 물건을 선택해야 합니다.")
        else:   # 물건 선택하고 게임 스타트했을 때, 두 번째 창 연동
            # self.hide()   
            self.second = AdSecond(self.itemNumber, self.myItemNumber, self.a)
            self.close()

    # 프로필 이미지 바꾸는 함수
    def imageCombo(self):
        if self.combo.currentText() == "2번":
            self.image.setPixmap(QPixmap("2.jpg").scaled(70, 70))
        elif self.combo.currentText() == "3번":
            self.image.setPixmap(QPixmap("3.jpg").scaled(70, 70))

    # 게임이 화면 중앙에 뜰 수 있도록 만드는 함수
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./AppleSDGothicNeoUL00.ttf')
    app.setFont(QFont('AppleSDGothicNeoUL00', 9))
    ex = AdFirst(0)
    sys.exit(app.exec_())
