import pygame
from math import ceil
import os
ts=TILESIZE=12*3 #5
ww=WIDTH=TILESIZE*15
wh=HEIGHT=TILESIZE*10
gx=GAME_AREA_X=TILESIZE*2
gy=GAME_AREA_Y=TILESIZE*2
gw=GAME_AREA_WIDTH=TILESIZE*11
gh=GAME_AREA_HEIGHT=TILESIZE*7

puzzle_list=["mazetown","breaktrough","catastrophe","annoyance","delivrance2"]
levels_list=["avoid","barrage","zigzag","recueil","vial","detour","maze","delivrance1"]
puzzle_list=["avoid", "barrage","zigzag", "recueil", "vial", "detour","breaktrough", "mazetown","catastrophe","annoyance", "delivrance1","delivrance2"]
second=60

datafile=open(os.path.join("levels","test.rawdata"))
fat=(int(datafile.readline().strip())%11)
datafile.close()

def sf(value):
	datafile=open(os.path.join("levels","test.rawdata"),"r+")
	datafile.write(str(value))
	datafile.close()

def sc(value):
	datafile=open(os.path.join("levels","level0.rawdata"),"r+")
	datafile.write(str(value))
	datafile.close()

def lf():
	global fat
	datafile=open(os.path.join("levels","test.rawdata"))
	fat=(int(datafile.readline().strip()))
	datafile.close()
	return fat

def lc():
	global fat
	datafile=open(os.path.join("levels","level0.rawdata"))
	fat=(int(datafile.readline().strip())%11)
	datafile.close()
	return fat

h=half=int(ceil(second/2))
q=quarter=int(ceil(half/2))
e=eighth=int(ceil(quarter/2))

FONTSIZE=ts
pygame.font.init()
myfont=pygame.font.Font("freesansbold.ttf",24)
font2=pygame.font.Font("freesansbold.ttf",12)


colors=( (0,255,255),(0,180,0),(200,100,0),(150,100,50),(100,80,50),(80,50,20),(70,40,10) )
