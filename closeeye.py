import os
import string
import random

class Game:
    玩家 = {}
    身份列表 = {} #格式为“身份:[玩家,玩家,...]”
    SetTime = 5

    def play():
        test = input('是否开始游戏？（y/n）').lower()
        while test == 'y':
            os.system('cls')
            f = open("config.txt")

            name = f.readline()
            i = 0
            while name != "":
                name = f.readline()
                玩家[name] = [i]
                i += 1

            print("正在分配身份\n")

            玩家列表 = list(玩家.keys())

            print("现在共有%s名玩家" % 人数)
            身份 = input("请输入身份组成及其人数（例：警察 2），一行一个，输入空行停止，总和必须小于等于总人数\n")
            temp = 0
            玩家列表temp = 玩家列表[:]
            while 身份 != "" and temp <= 人数:
                t = 身份.split()
                for ti in t[1:]:    #去除非法字符
                    if not ti.isnumeric():
                        t.remove(ti)

                for ti in range(int(t[1])):
                    玩家temp = random.choice(玩家列表temp)
                    玩家列表temp.remove(玩家temp)
                    if t[0] in 身份列表:
                        身份列表[t[0]].append(玩家temp)
                    else:
                        身份列表[t[0]] = [玩家temp]

                temp += int(t[1])
                身份 = input()

            if len(玩家列表temp)> 0:
                if "平民" in 身份列表:
                    身份列表["平民"] += 玩家列表temp
                else:
                    身份列表["平民"] = 玩家列表temp

            print("身份分配完毕，身份如下：\n")
            print(身份列表)

            for x in 身份列表:
                if x[1] == "平民":
                    身份列表[1] = 平民()
                elif x[1] == "杀手":
                    身份列表[1] = 杀手()
                elif x[1] == "警察":
                    身份列表[1] = 警察()
                elif x[1] == "医生":
                    身份列表[1] = 医生()
                else:
                    身份列表[1] = 平民()

            polices = 警察组()
            killers = 杀手组()
            游戏列表 = [polices, killers]
            for x in 身份列表:
                if x[1].charactor == "杀手":
                    killers.killers.append(x)
                elif x[1].charactor == "警察":
                    polices.polices.append(x)
                else:
                    游戏列表.append(x)

            #游戏流程开始
            days = 1
            night = False
            while True:
                #夜晚流程开始
                night = not night
                print("第%d天夜晚开始，请有身份的玩家开始行动。" % days)
                for x in 游戏列表:
                    #处理每个身份类型
                    x.operate()
                
                #处理夜晚的行动结果
                print("第%d天夜晚结束。" % days)
                flag = True
                for x in 身份列表:
                    if x[1].isKilled():
                        print("昨天晚上，%s。" % (x[0]+"被杀了，身份是"+x[1].charactor))
                        flag = False
                if flag:
                    print("昨晚是个平安夜。")
                
                #白天流程开始
                days += 1
                night = not night
                print("第%d天白天开始，请各位自由讨论，时长%d分钟。" % (days, SetTime))
                
                break

            test = input('是否开始游戏？（是/否）').lower()

class 角色:
    def __init__(self):
        self.alive = True
        self.zeroPin = 0
        self.kill = 0
        self.charactor = ''
        self.numOfVotes = 0
        self.deathNotes = ""

    def isAlive(self):
        return self.alive

    def getNumOfZeroPin(self):
        return self.zeroPin

    def killed(self):
        self.kill += 1

    def cure(self):
        self.kill -= 1

    def isKilled(self):
        if self.kill>0:
            self.alive = False
            self.deathNotes = "被杀了"
            return True
        elif self.kill<0:
            self.zero_pin += 1
            return False
            if self.zero_pin>1:
                self.alive = false
                self.deathNotes = "被扎死了"
                return True

    def vote(self, target):
        target.voted()

    def voted(self):
        self.numOfVotes += 1

    def getNumOfVotes(self):
        return self.numOfVotes

    alive = property(isAlive)
    zero_pin = property(getNumOfZeroPin)
    numOfVotes = property(getNumOfVotes)

class 身份:
    def operate(self):
        return


class 平民(角色,身份):
    def __init__(self):
        super(角色,self).__init__()
        self.charactor = '平民'

class 警察(角色,身份):
    def __init__(self):
        super(角色,self).__init__()
        self.charactor = '警察'

class 警察组(身份):
    def __init__(self,police = []):
        self.polices = police

    def observe(self, charactor):
        return charactor.charactor

    def operate(self):
        print("现在是警察的活动时间，请选择需要查身份的玩家。")

class 杀手(角色):
    def __init__(self):
        super(角色,self).__init__()
        self.charactor = '杀手'

class 杀手组(身份):
    def __init__(self,killer = []):
        self.killers = killer

    def kill(self, charactor):
        charactor.killed()
        
    def operate(self):
        print("现在是杀手的活动时间，请选择需要杀死的玩家。")

class 医生(角色,身份):
    def __init__(self):
        super(角色,self).__init__()
        self.charactor = '医生'

    def cure(self, charactor):
        charactor.cure()
        
    def operate(self):
        print("现在是医生的活动时间，请选择需要扎针的玩家。")


Game.play()
