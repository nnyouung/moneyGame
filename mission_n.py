import random

class Word:
    def __init__(self, filename):
        self.fH = open(filename, 'r')
        self.scdb = []
        self.count = 0
        self.exps=50 #사용자 누적 경험치 (추후 변수수정가능)
        for line in self.fH:
            dat = line.strip()
            object = dat.split(',')
            self.count += 1
            record = {}
            for attr in object:
                kv = attr.split(':')
                record[kv[0]] = kv[1]
            self.scdb += [record]
        self.fH.close()

    def test(self):
        return 'default'

    def randFromDB(self):
        r = random.randrange(self.count)
        onemission=self.scdb[r]
        return onemission #딕셔너리형태

    def doMission(self): #미션 수행했는지 확인
        for p in self.scdb:  # scdb에 저장된 애들 한줄씩 살피기
            #미션 완료했을 경우
            if (p['object'] == 'NikeShoes') & (p['action']=='buy') & (p['margin']=='20'):#오른쪽 값들은 물건파트의 각 값들과 추후연결필요
                self.exps+=int(p['exp']) #미션완료됐을 때, 경험치 누적하고 .
                self.scdb.remove(p) #완료미션을 미션리스트에서 없앤후,
                return self.randFromDB() #다시 랜덤으로 미션 생성




word=Word('missions2.txt')
word.randFromDB()

