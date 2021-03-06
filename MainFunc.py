#
#	Main文件的函数实现
#

import pygame
from pygame.locals import *
import os
import time
import json
import socket

import Extern as Et
import Resource as Rs
import Input as Ip
import Game as Gm
import Player as Pl
import threading
from Define import *

HOST, PORT = "localhost", 20000

#   游戏程序初始化函数
def init():
    pygame.init()	#pygame初始化
    pygame.mouse.set_visible(False)	#隐藏鼠标
    Et.game_state = GAMEINIT #初始化游戏状态
    Et.R_if = Rs.RInterface("Resource/json/interface") #加载界面资源
    Et.I_ctr = Ip.Control()     #初始化键盘控制
    Et.t_net = threading.Thread(target = host,args = ())
    t =threading.Thread(target=music,args=())
    t.setDaemon(True)
    t.start()

def music():
    filename='Resource\Musictest.mp3'
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(loops=0, start=0.0)


#   游戏退出函数
def gameQuit(event):
    if event.type==QUIT:
        pygame.quit()
        os._exit(0)

#   时间更新函数
def timeUpdate():
    temptime = time.time()
    if (temptime - Et.fresh_time) > 1/fps:
        Et.fresh_time = temptime
        return True
    else:
        return False 

def gameStateManager():
    if Et.game_state == GAMELOAD:
        Et.S_game = Gm.SingleGame()
    elif Et.game_state == GAMESTART:
        Et.S_game.update()
        #pass
    elif Et.game_state == GAMEONLINEINIT2:
        onlineInit()
        Et.t_net.setDaemon(True)
        Et.t_net.start()
    elif Et.game_state == GAMEONLINE:
        pass
        # Et.I_ctr.update()
        # for key,value in Et.I_ctr.p1_key.items():
        #         if value:
        #                 print(key)


def onlineInit():
    Et.Pr_info[0] = Pl.PlayerInfo()
    Et.Pr_info[1] = Pl.PlayerInfo()
    Et.Pr_info[1].site = [300,400]


def host():
    temptime = 0
    while True:
        if (Et.fresh_time - temptime)>1/fps:
            temptime = time.time()
            client(pack())
            if Et.online_over:
                break


def client(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    try:
        sock.sendall(message.encode("utf-8"))
        response = sock.recv(1024)
        jresp = json.loads(response.decode('utf-8'))
        Et.Pr_info[0].site = jresp[0]["site"]

    finally:
        sock.close()

def pack():
    msg = [Et.I_ctr.p1_key]
    jmsg = json.dumps(msg)
    return jmsg