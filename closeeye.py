#20131212
import os
import string
import random

class Game:
    def play():
        test = input('是否开始游戏？（是/否）')
        while test == '是':
            os.system('cls')
            f = open("config.txt")
            #人数 = int(input("请输入游戏人数："))
            人数 = int(f.readline())
            i = 0
            玩家 = {}
            while i < 人数:
                #name = input("请输入玩家%s名字：" % str(i+1))
                name = f.readline()
                玩家[name] = [i]
                i += 1 

            print("正在分配身份\n")

            玩家列表 = list(玩家.keys())
            身份列表 = {} #格式为“身份:[玩家,玩家,...]”
            
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
            test = input('是否开始游戏？（是/否）')

class 角色:
    def __init__(self):
        self.alive = true
        self.zeroPin = 0
        self.kill = 0
        self.charactor = ''
        self.numOfVotes = 0

    def isAlive(self):
        return self.alive
    
    def getNumOfZeroPin(self):
        return self.zeroPin
    
    def kill(self):
        self.kill += 1

    def cure(self):
        self.kill -= 1

    def isKilled(self):
        if self.kill>0:
            self.alive = false
        elif self.kill<0:
            self.zero_pin += 1
            if self.zero_pin>1:
                self.alive = false

    def vote(self,target):
        target.voted()

    def voted(self):
        self.numOfVotes += 1

    def getNumOfVotes(self):
        return self.numOfVotes

    alive = property(isAlive)
    zero_pin = property(getNumOfZeroPin)
    numOfVotes = property(getNumOfVotes)

class 平民(角色):
    def __init__(self):
        super(角色,self).__init__()
        self.charactor = '平民'

class 警察(角色):
    def __init__(self):
        super(角色,self).__init__()
        self.charactor = '警察'
    
    def observe(self,charactor):
        return charactor.charactor

class 杀手(角色):
    def __init__(self):
        super(角色,self).__init__()
        self.charactor = '杀手'

    def killSb(self,charactor):
        charactor.kill()

class 医生(角色):
    def __init__(self):
        super(角色,self).__init__()
        self.charactor = '医生'

    def cureSb(self,charactor):
        charactor.cure()

        
Game.play()
