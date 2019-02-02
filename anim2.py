from spt import gx,gy,gw,gh,ww,wh,ts,second,h,half,q,quarter,e, eighth

from sprites_load import *
#from sprites_load import chartable
from math import ceil
import pygame


walkcycle=chartable


def reset():
	global walkcycle,turnip
	walkcycle,turnip = reload_character()
	#print("reseted")

class damagecontrol:
	value=True
	def __eq__(self,other):
		return self.value==other
	def __nonzero__(self):
		return bool(self.value)

def animation(screen,horizontal_position,vertical_position,direction):
	pd=direction
	x1,y=gx+horizontal_position*ts,gy+vertical_position*ts
	x0=x1-pd*ts
	ndir=not round((direction+1)/2) #right : 0, left : 1
	anim=1
	for step in range(half):
		if(damagecontrol()):
			screen.blit(walkcycle[ndir][int(anim%3)], (x,y))
		yield True
	yield False


def forward(screen,horizontal_position,vertical_position,direction):
	pd=direction
	x1,y=gx+horizontal_position*ts,gy+vertical_position*ts
	x0=x1-pd*ts
	ndir=not round((direction+1)/2) #right : 0, left : 1

	for step in range(half):
		if damagecontrol(): #damaged : visible or not
			if(step<=q):
				k=float(step)/q 
				x=x0+pd*k*ts #slide toward x1
				anim=step//2
			else:
				x=x1 #stand on x1
				anim=1
			screen.blit(walkcycle[ndir][int(anim%3)], (x,y))
		yield True
	yield False

def jump_up(screen,horizontal_position,vertical_position,direction):
	pd=direction
	x1,y1=gx+horizontal_position*ts,gy+vertical_position*ts
	x0,y0=x1-pd*ts,y1+ts
	ndir=not round((direction+1)/2) #right : 0, left : 1
	anim=1
	for step in range(half):
		if damagecontrol():
			if(step<q):
				k=float(step)/q
				x=x0+pd*k*ts
				anim=0
				y=y0-(ts/2.0)*(1.0-((float(step-e)/(e))**2))
			else:
				x=x1
				anim=1
				y=y0-ts*(float(step-q)/(e*3.0/2))

			screen.blit(walkcycle[ndir][int(anim%3)], (x,y))
		yield True
	yield False

def jump_down(screen,horizontal_position,vertical_position,direction):
	x1,y1=gx+horizontal_position*ts,gy+vertical_position*ts
	x0,y0=x1-direction*ts,y1-ts
	ndir=not round((direction+1)/2) #right : 0, left : 1
	anim=1
	for step in range(half):
		if damagecontrol():
			if(step<q):
				k=float(step)/q
				x=x0+direction*k*ts
				anim=0
				y=y0-(ts/2)*(1-((float(step-e)/(e))**2))
			else:
				x=x1
				anim=1
				y=y0+ts*(float(step-q)/(e*3/2))

			screen.blit(walkcycle[ndir][int(anim%3)], (x,y))
		yield True
	yield False

def turn(screen,horizontal_position,vertical_position,direction):
	pd=direction
	x1,y1=gx+horizontal_position*ts,gy+vertical_position*ts
	x0=x1-pd*ts
	ndir=not round((direction+1)/2) #right : 0, left : 1
	anim=1
	for step in range(half):
		if damagecontrol():
			if(step<q):
				y=y1-(ts/4.0)*(1-((float(step-e)/e)**2))
			else:
				y=y1
			if(step==e):
				ndir = not ndir
			screen.blit(walkcycle[ndir][int(anim%3)], (x1,y))
		yield True
	yield False

def endlevel(screen,horizontal_position,vertical_position,direction):
	dy=gy+gh
	counter=0
	xx=horizontal_position
	yy=vertical_position
	switch=direction*((xx%2)*2-1)
	#pres=[False]*11
	#pres[xx]=1
	pd=direction
	x1,y=gx+horizontal_position*ts,gy+vertical_position*ts
	x0=x1-pd*ts
	ndir=not round((direction+1)/2) #right : 0, left : 1
	anim=1
	animlist=list()
	MIN=xx
	MAX=xx+1

	for step in range(half):
		yield True
	for step in range(second*7):
		if((step%quarter)==0):
			parity=( (step%half)//quarter )^ ndir
			animlist+=[turn(screen,k,yy,((k%2)*2-1)*switch) \
			for k in range(max(0,MIN),min(11,MAX)) if k%2==parity]

			if((step//half)%2)==1:
				MAX+=(direction==1)
				MIN-=(direction==-1)
			else:
				MAX+=(direction==-1)
				MIN-=(direction==1)
			if(step%half==0):
				switch=-switch
		"""
		if(step==second):
			if(xx>0):
				pres[xx-1]=True
			if(xx<11-1):
				pres[xx+1]=True
		elif(step==second*2):
			if(xx>1):
				pres[xx-2]=True
			if(xx<11-2):
				pres[xx+2]=True
		elif(step==second*3):
			for i in range(1,11,2):
				pres[i]=True
		elif(step==second*4):
			for i in range(0,11,2):
				pres[i]=True
		if((step%half)==0):
			switch=-switch
			animlist=[turn(screen,k,yy,((k%2)*2-1)*switch) for k in range(11) if pres[k] == True]"""
		index=0
		while index<len(animlist):
			if(not next(animlist[index])):
				animlist.pop(index)
			else:
				index+=1
		yield True
	yield False

def diet(screen,horizontal_position,vertical_position,direction,decalage=0):
	pd=direction
	x,y=gx+horizontal_position*ts,gy+vertical_position*ts
	ndir=not round((direction+1)/2) #right : 0, left : 1
	anim=1
	for i in range(half-decalage):
		yield True
	for step in range(second):
		screen.blit(turnip[ndir*4+int(step/quarter)], (x,y))
		step+=1
		yield True
	yield False


def crush(screen,horizontal_position,vertical_position,step=0):
	x,y=gx+horizontal_position*ts,gy+vertical_position*ts
	while step<half:
		if(step<q/2):
			screen.blit(canim[-1], (x,y))
		elif(step<=h-q/2):
			screen.blit(canim[min(int((step-q/2.0)/q*6.0),5)], (x,y))
		step+=1
		yield True
	yield False

def bonus(screen,horizontal_position,vertical_position,step=0):
	x,y=gx+horizontal_position*ts,gy+vertical_position*ts
	while step<half:
		if(step>=0):
			screen.blit(bling[min(int(float(step)/h*7.0),6)], (x,y))
		else:
			screen.blit(bling[0], (x,y))
		step+=1
		yield True
	yield False
	"""
		if(step<q/2):
			pass
		elif(step<=h-q/2):
			screen.blit(canim[int((step-q/2)/q*6)], (x,y))
		step+=1
		yield True

pygame.draw.line(screen, (i*255/ts,i*255/ts,i*255/ts), (0,i),(ts,i))
"""
if __name__=="__main__":
	from random import randint,choice
	import pygame
	screen = pygame.display.set_mode((ww,wh))
	TIMER=half
	time=0
	
	black_square_that_is_the_size_of_the_screen = pygame.Surface(screen.get_size())
	black_square_that_is_the_size_of_the_screen.fill((128, 0, 0))
	screen.blit(black_square_that_is_the_size_of_the_screen, (0, 0))

	pygame.display.set_caption("7+3 animations generators")
	quit=False 
	clock = pygame.time.Clock()
	animslist=list()
	damagecount=0

	while not quit:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit=True
			elif event.type==pygame.KEYUP:	
				mx,my=pygame.mouse.get_pos()
				px,py=mx//ts-2,my//ts-1
				ile=randint(6,6)
				if(ile==1):
					animslist.append(forward(screen,px,py,choice((-1,1))))
					#print "forward"
				elif(ile==4):
					animslist.append(jump_up(screen,px,py,choice((-1,1))))
					#print "jump^"
				elif(ile==3):					
					animslist.append(jump_down(screen,px,py,choice((-1,1))))
					#print "jumpv"
				elif(ile==2):	
					animslist.append(turn(screen,px,py,choice((-1,1))))
					#print "turn"
				elif(ile==5):
					animslist.append(diet(screen,px,py,choice((-1,1))))
				elif(ile==6):
					animslist.append(endlevel(screen,px,py,choice((-1,1))))
				"""ele=randint(1,3)
				if(ele==1):
					damagecount=half+e+(ile>=3)*quarter
					animslist.append(crush(screen,px,py,-(ile>=3)*quarter))
					#print "damagecount is",damagecount
				elif(randint(1,4)==1):
					animslist.append(bonus(screen,px,py,-(ile>=3)*quarter))"""

		#animslist.append(crush(screen,randint(0,10),randint(0,6),choice((-1,1))))	
		animslist.append(forward(screen,randint(0,10),randint(0,6),choice((-1,1))))	
		#bonus 	crush 		 diet	turn forward
		damagecount=max(0,damagecount-1)

		#if(damagecount==1):
			#pass			
			#print "damagecount is one"
		damagecontrol=(damagecount<=0) or (damagecount>half) or ((damagecount%3)==0)					
		screen.blit(black_square_that_is_the_size_of_the_screen, (0, 0))
		
		index=0		
		while(index<len(animslist)):
			if(not next(animslist[index])):
				animslist.pop(index)
			else:
				index+=1


		clock.tick(60)

		pygame.display.flip()

	pygame.quit()



