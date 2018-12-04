#
#   游戏成分类
#

from define import *
import extern
import pygame
import Game
from pygame.locals import *

# Item基类,作为敌人类,障碍物类等的父类
class Item():
    def __init__(self):
        self.site='物体位置'
        self.size='物体大小'
        self.movable='可否移动'
        self.direction='朝向'
        self.game='当前游戏指针'
        self.state='状态'
    
    def item_blit(self):
        pass

# 敌人类
class Enemy(Item):
    def __init__(self):
        super(Enemy,self).__init__()
        self.life_value='生命值'
        self.signal='接收到的信号'
        self.load()

# 敌人类的状态更新
    def update(self):
        pass

# 敌人类的初始化函数
    def load(self):
        self.size=extern.singleplayer_enemysize

# 敌人的贴图函数
    def item_blit(self):
        extern.singleplayer_background_pic_temp.blit(extern.singleplayer_enemy_pic_static,
        (int(self.site[0]-self.size[0]/2),int(self.site[1]-self.size[1]/2)))

# 障碍物类
class Obstacle(Item):
    def __init__(self):
        super(Obstacle,self).__init__()
        self.life_value='生命值'
        self.signal='接收到的信号'
        self.load()

    # 障碍物类的状态更新
    def update(self):
        pass

    # 障碍物类的初始化函数
    def load(self):
        pass

# 技能类
class Skill(Item):
    def __init__(self):
        super(Skill,self).__init__()
        self.damage='伤害值'
        self.duration='技能持续时间'
        self.inittime='初始化时间'
        self.signal='接收到的信号'
        self.caster='技能释放者'
        self.last='击中后是否消失'
        self.delflag='技能是否应该被删除'
        self.kind='技能类型'
        self.velocity='技能速度'
        self.load()

    # 技能类的状态更新
    def update(self):
        if extern.last_fresh_time-self.inittime>self.duration:
            self.delflag=True
        else:
            self.skill_move()
            self.item_blit()
    
    def skill_move(self):
        self.site[0]=self.site[0]+self.movex[self.direction]
        if self.site[0]>(extern.singleplayer_background_size[0]-int(self.size[0]/2)):
            self.delflag=True
        if self.site[0]<int(self.size[0]/2):
            self.delflag=True
        self.site[1]=self.site[1]+self.movey[self.direction]
        if self.site[1]>(extern.singleplayer_background_size[1]-int(self.size[1]/2)):
            self.delflag=True
        if self.site[1]<int(self.size[1]/2):
            self.delflag=True
        print(self)

    def load(self):
        self.delflag=0
        self.duration=extern.skill_1_duration
        self.velocity=extern.skill_1_velocity
        self.movex=[self.velocity*x for x in movex]
        self.movey=[self.velocity*y for y in movey]
        self.size=extern.skill_1_size

    def item_blit(self):
        print('item_blit')
        extern.singleplayer_background_pic_temp.blit(extern.skill_1_pic,
        (int(self.site[0]-self.size[0]/2),int(self.site[1]-self.size[1]/2)))