import pygame
import os
from constants import myfont, font2,ts

chartable=list()	
canim=tuple()
for i in range(6):
	canim+=(pygame.image.load(os.path.join("graphics","cr"+str(i)+".png")),)
canim+=(pygame.image.load(os.path.join("graphics","cr.png")),)
bling=tuple()
for i in range(7):
	bling+=(
	pygame.image.load(os.path.join("graphics","bl"+str(i)+".png")),
	)

turnip=tuple() #0 : droite. #1 : gauche


cbnasurf = pygame.image.load(os.path.join('graphics', 'cbna.png'))
#cbnasurf.convert(screen)

boostup =  pygame.image.load(os.path.join('graphics', 'boostup.png'))
#boostup.convert_alpha(screen)
boostdown=pygame.transform.flip(boostup,False,True)
boostingsurf= pygame.image.load(os.path.join('graphics', 'boosting.png'))
#boostingsurf.convert_alpha(screen)
heartsurf= pygame.image.load(os.path.join("graphics", "heart.png"))
#heartsurf.convert_alpha(screen)
lifevial=pygame.image.load(os.path.join("graphics","bonus.png"))
#lifevial.convert_alpha(screen)
starsurf=pygame.image.load(os.path.join("graphics", "star.png"))
#starsurf.convert_alpha(screen)
infinity=pygame.image.load(os.path.join("graphics", "infinity.png"))
#infinity.convert_alpha(screen)
boostnote=pygame.image.load(os.path.join("graphics", "boostnote.png"))
#boostnote.convert_alpha(screen)

marker=pygame.image.load(os.path.join("graphics","marker.png"))
#marker.convert_alpha(screen)
#from spt import FONTSIZE,myfont,font2
leveltitle=myfont.render("Level :", False, (255,255,255))
scoretitle=myfont.render("Score :", False, (255,255,255))
boosttitle=font2.render("Boost",False,(255,255,255))

gradtile=pygame.Surface((ts,ts))
for i in range(ts):
	pygame.draw.line(gradtile, (128-i*128/ts,128-i*128/ts,128-i*128/ts), (0,i),(ts,i))

def reload_character():
	datafile=open(os.path.join("levels","level0.rawdata"))
	fat=(int(datafile.readline().strip())*(ts%11))
	#print("fat=",fat)
	datafile.close()
	global chartable
	global turnip
	chartable=list()	
	for i in range(3):
		chartable.append(pygame.image.load(os.path.join("graphics","character"+str(i+fat)+".png"))) #load character images
	chartable=list((tuple(chartable),tuple()))
	for img in chartable[0]: #flipped images
		chartable[1]+=(pygame.transform.flip(img,True,False),)
	turnip=tuple() #0 : droite. #1 : gauche
	for d in range(2):
		turnip+=(chartable[d][0],)
		for i in range(3):
			turnip+=(pygame.transform.rotate(turnip[-1],(d*2-1)*90),)
	return chartable,turnip

reload_character()
"""
sprites["chartable"]=chartable
sprites["canim"]=canim
sprites["bling"]=bling
sprites["cbnasurf"]=cbnasurf
sprites["boostup"]=boostup
sprites["boostdown"]=boostdown
sprites["boostingsurf"]=boostingsurf
sprites["heartsurf"]=heartsurf
sprites["lifevial"]=lifevial
sprites["starsurf"]=starsurf
sprites["infinity"]=infinity"""
