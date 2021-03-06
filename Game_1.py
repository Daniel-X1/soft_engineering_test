#
#   游戏类
#

from define import *
import extern
import Player
import Item

import pygame
import json
from pygame.locals import *

class Single_player_game():
    def __init__(self):
        self.single_player=Player.Player()
    # 调用初始化函数,加载关卡信息,敌人数量与类型,地图资源
        self.enemy_list=[]
        self.background="背景地图的图片对象"
        self.enemypic='敌人的图片'
        self.playerpic='人物的图片'
        self.world='整个游戏地图'
        self.worldsize='整个游戏地图大小'
        self.gameover='游戏是否结束'
        self.load_from_json()
    # 技能列表
        self.skill_list=[]
    # 信号列表,用于暂存未处理的信号
        self.signal_list=[]
    # 键盘状态
        self.keyboardevent=pygame.key.get_pressed()

# 初始化函数,从json文件读入信息
    def load_from_json(self):
        with open (gametestjson,'r') as checkpointinfo:
            checkpoint1=json.load(checkpointinfo)
            for enemysite in checkpoint1[6]:
                self.enemy_list.append(Item.Enemy())
            for count in list(range(1,len(self.enemy_list)+1)):
                self.enemy_list[count].site=checkpoint1[6][count]
                self.enemy_list[count].size=checkpoint1[4]
            self.worldsize=checkpoint1[1]
            self.playerpic=pygame.image.load(checkpoint1[3]).convert()
            self.enemypic=pygame.image.load(checkpoint1[5]).convert()
            self.background=pygame.image.load(checkpoint1[0]).convert()
            self.single_player.size=checkpoint1[2]
            self.gameover=0


# 攻击判定方法,根据技能列表里的技能判断是否向message_list写入信号
    def attack_judge(self):
        tempplayerskill=[]
        if (len(self.skill_list)==0):
            pass
        else:
            for skill in self.skill_list:
                if (skill.caster==self.single_player):
                    tempplayerskill.append(skill)
                else:
                    # 技能打到了人物而且人物之前没有被这个技能打到
                    if (skill.attack_judge(self.single_player) & \
                    (skill not in self.single_player.attacked_skill_list)):
                        self.single_player.signal=SIGNALATTACKED
                        self.single_player.life_value=self.single_player.life_value-skill.damage
                        if (skill.last==0):
                            del skill
                        else:
                            #被哪些技能攻击到的列表
                            self.single_player.attacked_skill_list.append(skill)
            if (len(tempplayerskill)==0):
                pass
            else:
                for skill in tempplayerskill:
                    for enemy in self.enemylist:
                        if (skill.attack_judge(enemy)):
                            enemy.signal=SIGNALATTACKED
                            enemy.life_value=enemy.life_value-skill.damage
                            if (skill.last==0):
                                del skill

# 移动判定方法,判定对象是否可以移动,将结果写入成员对象的movable属性
    def move_judge(self,tempsignal):
        tempsite=tempsignal.receiver.site
        tempsize=tempsignal.receiver.size
        tempsignal.receiver.movable=True
        tempsignal.receiver.signal=SIGNALMOVE
        tempmoveflag=[True,True]
        for enemy in self.enemy_list:
            umovalbe=((abs(enemy.site[1]-tempsite[1]-(enemy.size[1]+tempsize[1])/2)<COLLISIONTHRESHOLD) &  \
                    (abs(enemy.site[0]-tempsite[0])<(enemy.size[0]+tempsize[0])/2))
            dmovable=((abs(-enemy.site[1]+tempsite[1]-(enemy.size[1]+tempsize[1])/2)<COLLISIONTHRESHOLD) &  \
                    (abs(enemy.site[0]-tempsite[0])<(enemy.size[0]+tempsize[0])/2))
            lmovable=((abs(enemy.site[0]-tempsite[0]-(enemy.size[0]+tempsize[0])/2)<COLLISIONTHRESHOLD) &  \
                    (abs(enemy.site[1]-tempsite[1])<(enemy.size[1]+tempsize[1])/2))
            rmovable=((abs(-enemy.site[0]+tempsite[0]-(enemy.size[0]+tempsize[0])/2)<COLLISIONTHRESHOLD) &  \
                    (abs(enemy.site[1]-tempsite[1])<(enemy.size[1]+tempsize[1])/2))
            if (tempsignal.type==MOVEUP):
                if (umovalbe):
                    tempsignal.receiver.movable=False
                    break
            elif (tempsignal.type==MOVEDOWN):
                if (dmovable):
                    tempsignal.receiver.movable=False
                    break
            elif (tempsignal.type==MOVELEFT):
                if (lmovable):
                    tempsignal.receiver.movable=False
                    break
            elif (tempsignal.type==MOVERIGHT):
                if (rmovable):
                    tempsignal.receiver.movable=False
                    break
            elif (tempsignal.type==MOVEUPLEFT):
                if (umovalbe):
                    tempmoveflag[1]=False
                if (lmovalbe):
                    tempmoveflag[0]=False
                if (tempmoveflag[1]==False & tempmoveflag[0]==False):
                    break
            elif (tempsignal.type==MOVEUPRIGHT):
                if (umovalbe):
                    tempmoveflag[1]=False
                if (rmovalbe):
                    tempmoveflag[0]=False
                if (tempmoveflag[1]==False & tempmoveflag[0]==False):
                    break
            elif (tempsignal.type==MOVEDOWNLEFT):
                if (dmovable):
                    tempmoveflag[1]=False
                if (lmovable):
                    tempmoveflag[0]=False
                if (tempmoveflag[1]==False & tempmoveflag[0]==False):
                    break
            elif (tempsignal.type==MOVEDOWNRIGHT):
                if (dmovable):
                    tempmoveflag[1]=False
                if (rmovable):
                    tempmoveflag[1]=False
                if (tempmoveflag[1]==False & tempmoveflag[0]==False):
                    break
        if (tempsignal.type==MOVEUPLEFT):
            if (tempmoveflag[1]==False & tempmoveflag[0]==False):
                tempsignal.type=False
            elif (tempmoveflag[1]==False):
                tempsignal.type==MOVELEFT
            elif (tempmoveflag[0]==False):
                tempsignal.type==MOVEUP
        elif (tempsignal.type==MOVEUPRIGHT):
            if (tempmoveflag[1]==False & tempmoveflag[0]==False):
                tempsignal.receiver.movable=False
            elif (tempmoveflag[1]==False):
                tempsignal.type==MOVERIGHT
            elif (tempmoveflag[0]==False):
                tempsignal.type==MOVEUP
        elif (tempsignal.type==MOVEDOWNLEFT):
            if (tempmoveflag[1]==False & tempmoveflag[0]==False):
                tempsignal.receiver.movable=False
            elif (tempmoveflag[1]==False):
                tempsignal.type==MOVELEFT
            elif (tempmoveflag[0]==False):
                tempsignal.type==MOVEDOWN
        elif (tempsignal.type==MOVEDOWNRIGHT):
            if (tempmoveflag[1]==False & tempmoveflag[0]==False):
                tempsignal.receiver.movable=False
            elif (tempmoveflag[1]==False):
                tempsignal.type==MOVERIGHT
            elif (tempmoveflag[0]==False):
                tempsignal.type==MOVEDOWN
        if (tempmoveflag[1]==True | tempmoveflag[0]==True):
            tempsignal.receiver.movable=True


# 信号处理函数,解决信号冲突,向每个对象发送信号
    def message_translate(self):
        move_state = self.keyboardevent[K_w]<<3 | self.keyboardevent[K_s]<<2 | \
                    self.keyboardevent[K_a]<<1 | self.keyboardevent[K_d]
        move_switch = [None,3,2,None,1,7,6,None,0,5,4,None,None,None,None,None]
        if (not move_switch[move_state] is None):
            tempsignal=Signal(move_switch[move_state],self.single_player)
        skill_state = self.keyboardevent[K_j]<<2 | self.keyboardevent[K_k]<<1 | self.keyboardevent[K_l]
        skill_switch = [None,10,9,None,8,None,None,None]
        #J      SKILL1=8
        #K      SKILL2=9
        #L      SKILL3=10
        #可改变skill_switch定义组合技
        if (not skill_switch[skill_state] is None):
            self.single_player.signal=skill_switch[skill_state]
        #先考虑移动
        move_judge(tempsignal)
        #在考虑攻击判定，这样被打到就会取消之前的移动信号
        attack_judge()
        
# 游戏画面与状态更新
    def game_update(self):
        for skill in skill_list:
            if ():#skill寿命到了的话
                del skill
        for enemy in enemylist:
            if (enemy.state==ENEMYDEAD):
                del enemy
        if (self.single_player.state==PLAYERDEAD):
            self.gameover=1
        if (len(self.enemylist)==0):
            self.gameover=1

# 信号类
class Signal():
    def __init__(self,type,receiver):
        self.type=type
        self.receiver=receiver
