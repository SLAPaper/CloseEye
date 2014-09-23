import os
import string
import random

class Game:
    #身份列表 = {} #格式为“身份:[玩家,玩家,...]”
    游戏字典 = {} #格式为"玩家名:玩家对象"
    讨论时间 = 5
    医生总针数 = 5
    狙击手子弹数 = 3

    def play():
        test = input('是否开始游戏？（y/n）').lower()
        while test == 'y':
            #os.system('cls')
            f = open("config.txt", encoding="utf_8")

            玩家名字 = f.readline().rstrip('\n').lstrip('\ufeff')
            玩家列表 = []
            while 玩家名字 != "":
                玩家列表.append(玩家名字)
                玩家名字 = f.readline().rstrip('\n')

            print("正在分配身份\n")
            print(玩家列表,end='\n\n')

            print("现在共有%s名玩家。" % len(玩家列表))
            身份 = input("\n请输入身份组成及其人数（例：警察 2），一行一个，输入空行结束，总和必须小于等于总人数\n")
            temp = 0
            玩家列表副本 = 玩家列表[:]
            while 身份 != "" and temp <= len(玩家列表):
                t = 身份.split()
                for ti in t[1:]:    #去除非法字符
                    if not ti.isnumeric():
                        t.remove(ti)

                for ti in range(int(t[1])):
                    抽出玩家 = random.choice(玩家列表副本)
                    玩家列表副本.remove(抽出玩家)
                    
                    if t[0] == "平民":
                        Game.游戏字典[抽出玩家] = 平民()
                    elif t[0] == "杀手":
                        Game.游戏字典[抽出玩家] = 杀手()
                    elif t[0] == "警察":
                        Game.游戏字典[抽出玩家] = 警察()
                    elif t[0] == "医生":
                        Game.游戏字典[抽出玩家] = 医生()
                    elif t[0] == "狙击":
                        Game.游戏字典[抽出玩家] = 狙击手()
                    else:
                        Game.游戏字典[抽出玩家] = 平民()

                temp += int(t[1])
                身份 = input()
                
            #处理剩余玩家
            if len(玩家列表副本)> 0:
                for x in 玩家列表副本:
                    Game.游戏字典[x] = 平民()

            print("身份分配完毕，身份如下：",end='\n\n')
            
            #####测试用代码#####
            #print(Game.身份列表)
            for x in Game.游戏字典.items():
                print(x[0]+'\t'+x[1].charactor)
            ####################

            警察组对象 = 警察组()
            杀手组对象 = 杀手组()
            行动字典 = {"警察组":警察组对象, "杀手组":杀手组对象}
            for x in Game.游戏列表.items():
                if x[1].charactor == "杀手":
                    杀手组对象.killers[x[0]] = x[1]
                elif x[1].charactor == "警察":
                    警察组对象.polices[x[0]] = x[1]
                else
                    行动字典[x[0]] = x[1]
            
            #游戏流程开始
            days = 1
            night = False
            while True:
                #夜晚流程开始
                night = not night
                for x in Game.游戏字典.values():
                    x.killCount = 0
                print("\n第%d天夜晚开始，请有身份的玩家开始行动。" % days)
                for x in 行动字典.values():
                    x.operate()
                
                #处理夜晚的行动结果
                print("\n第%d天夜晚结束。" % days)
                flag = True
                for x in Game.游戏字典.items():
                    if x[1].isKilled():
                        print("昨天晚上，%s被杀了，身份是%s，请留下遗言。" % (x[0],x[1].charactor))
                        flag = False
                if flag:
                    print("昨晚是个平安夜。")
                
                #白天流程开始
                days += 1
                night = not night
                print("第%d天白天开始，请各位自由讨论，时长%d分钟。" % (days, Game.讨论时间))
                #TODO：计时器和投票程序
                存活列表 = []
                for x in Game.游戏字典.items():
                    if x[1].isAlive() == True:
                        x[1].numOfVotes = 0
                        存活列表.append(x[0])
                voteCount = 0
                voteDict = {}   #格式为：{"投票人":"被票人"，...}
                voteCountDict = {}  #格式为：{"被票人":票数, ...}
                while voteCount <= len(存活列表):
                    if voteCount == len(存活列表):
                        voteInformation = print("所有存活玩家已投票，回复空行结束白天流程并进行计票，回复“投票人 被票人”进行改票").rstrip("\n").split()
                        if voteInformation[0] == "":
                            voteCount += 1
                    else:
                        voteInformation = input("请输入投票信息，格式为”投票人 被票人“一次一行，如“小V 悲喜”").split()
                    if voteInformation[0] not in 存活列表:
                        print("错误：%s不具有投票权限" % voteInformation[0])
                    else:
                        if voteInformation[0] not in voteDict.keys():
                            voteCount += 1
                        if voteInformation[1] not in 存活列表:
                            print("警告：%s投票了不能票到的%s（已死亡/输入有误），将视为自票" % voteInformation）
                            voteDict[voteInformation[0]] = voteInformation[0]
                        else:
                            voteDict[voteInformation[0]] = voteInformation[1]
                    for x in voteDict.items():
                        print("%s\t%s" % x)
                
                for x in voteDict().values():
                    if x not in voteCountDict:
                        voteCountDict[x] = 1
                    else:
                        voteCountDict[x] += 1
                
                voteCountList = list(voteCountDict).sort()
                
                for x in voteCountList:
                    print("%s\t%d" % x)
                
                maxVotes = []
                for x in Game.游戏字典.items():
                    x[1].numOfVotes = voteCountDict[x[0]]
                    if len(maxVotes) == 0 or x[1].numOfVotes >= maxVotes[0][1].numOfvotes:
                        if x[1].numOfVotes > maxVotes[0][1].numOfVotes:
                            maxVotes.clear()
                        maxVotes.append(x)
                    elif y[1].numOfVotes > maxVotes:
                out = ""
                if len(maxVotes) > 1:
                    print("现在有超过一名玩家得票并列最高，为%d票，如下所示：" % maxVotes[0][1].numOfVotes)
                    maxVotesList = []
                    for x in maxVotes:
                        print("%s\t%d票" % (x[0],x[1].numOfVotes))
                        maxVotesList.append(x[0])
                    out = input("请输入出局的玩家").rstrip("\n")
                    while out == "" or out not in maxVotesList:
                        out = input("请输入出局的玩家")
                else:
                    out = maxVotes[0][0]
                Game.游戏字典[out].alive = False
                print("玩家%s被投票出局，身份是%s，没有遗言。" % (out, Game.游戏字典[out].charactor)
                
                #TODO: 胜利条件判定
                break

            test = input('是否开始游戏？（y/n）').lower()

class 角色:
    def __init__(self):
        self.alive = True
        self.zeroPin = 0
        self.killCount = 0
        self.charactor = ''
        self.numOfVotes = 0
        self.deathNotes = ""

    def isAlive(self):
        return self.alive

    def getNumOfZeroPin(self):
        return self.zeroPin

    def killed(self):
        self.killCount += 1

    def cure(self):
        self.killCount -= 1

    def isKilled(self):
        if self.killCount>0:
            self.alive = False
            self.deathNotes = "被杀了"
            return True
        elif self.killCount<0:
            self.zero_pin += 1
            if self.zero_pin>1:
                self.alive = false
                self.deathNotes = "被扎死了"
                return True
        return False

    def vote(self, target):
        target.voted()

    def voted(self):
        self.numOfVotes += 1

    def getNumOfVotes(self):
        return self.numOfVotes

class 身份:
    def operate(self):
        return


class 平民(角色,身份):
    def __init__(self):
        super().__init__()
        self.charactor = '平民'

class 警察(角色,身份):
    def __init__(self):
        super().__init__()
        self.charactor = '警察'

class 警察组(身份):
    def __init__(self,police = {}):
        self.polices = police

    def observe(self, charactor):
        return charactor.charactor

    def operate(self):
        print("现在是警察的活动时间，请选择需要查身份的玩家。")

class 杀手(角色):
    def __init__(self):
        super().__init__()
        self.charactor = '杀手'

class 杀手组(身份):
    def __init__(self,killer = {}):
        self.killers = killer

    def kill(self, charactor):
        charactor.killed()
        
    def operate(self):
        print("现在是杀手的活动时间，请选择需要杀死的玩家。")

class 医生(角色,身份):
    def __init__(self):
        super().__init__()
        self.charactor = '医生'
        self.numOfPins = Game.医生总针数

    def cure(self, charactor):
        charactor.cure()
        
    def operate(self):
        print("现在是医生的活动时间，请选择需要扎针的玩家。")

class 狙击手(角色,身份):
    def __init__(self):
        super().__init__()
        self.charactor = '狙击'
        self.numOfShoots = Game.狙击手子弹数
    
    def shoot(self, charactor):
        #TODO:判断子弹数量和已击发子弹数量
        #TODO:判断是否射到杀手
        charactor.killed()
    
    def operate(self):
        print("现在是杀手的活动时间，请选择需要射击的玩家。")
Game.play()
