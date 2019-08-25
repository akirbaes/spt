import os
import pygame
from copy import deepcopy
import anim2 as anim
from constants import *
from sprites_load import *

def to_dodec(number):
	chars="0123456789GH"
	ans=""
	while(number>0):
		ans=chars[number%12]+ans
		number=number//12
	return ans or "0"


class game_map:
	data=list()
	width=0
	height=0
	def __init__(self,continues,screen,width=11,height=7):
		self.r()
		self.show=True
		self.animations=list()
		self.screen=screen
		self.animslist=list()
		self.width=width
		self.height=height
		self.data=[[None]*width for i in range(height)]
		self.level=list()
		self.name=None
		self.spritesheet=dict()
		self.level_end=False
		self.next_step=30
		self.damagecount=0
		self.can_step=True
		self.continues=continues
		self.life=3
		self.level_name=None
		self.score=0
		self.init_level()
		#print("data[0][0] to data[%s][%s]"%(len(self.data),len(self.data[0])))
	def has_lost(self):	
		return self.level_end and self.life<=0

	def kill(self):
		self.life=0
	
	def r(self):
		global chartable, turnip
		chartable,turnip=reload_character()
		anim.reset()
			

	def put_jumper(self,up=True,curtain=7):
		mp=pygame.mouse.get_pos()
		mx,my=((mp[0]-gx)//ts,(mp[1]-gy)//ts)
		if(0<=mx<11 and 0<=my<7 and my<curtain):
			#print("Trying to jump the",mx,my)
			a= self.put(mx,my,up)
			#print a
			return a
		return False

	def put(self,x,y,up=True):
		#print("Direct tile",up,"in",self.level[y][x])
		if(self.level[y][x]=="0" or self.level[y][x]==None):
			if(up):
				self.level[y][x]="U"
			else:
				self.level[y][x]="D"
			return True
		return False

	def can_put(self,x,y):
		return (self.level[y][x]=="0")

	def _load(self,levelname):
		try:
			datafile=open(os.path.join("levels",str(levelname)+".rawdata")	)
		except Exception as e: 
			print("Cannot load level!",levelname,e)
			return False
		line=datafile.readline().strip()
		if(line=="This is a map"):
			self.level_name=datafile.readline().strip()
			line=datafile.readline().split()
			self.width,self.height=int(line[0]),int(line[1])
			self.data=[[None]*self.width for i in range(self.height)]
			for i in range(self.height):
				line=datafile.readline().strip()
				#print("Line",i,line)
				for j,elem in enumerate(line):
					#print elem,
					self.data[i][j]=elem
		else:
			print("Tried to open",levelname)
			print("This is not a map")
			return False

		return True

	def show(self):
		print("")
		print(self.name)
		for i,line in enumerate(self.level):
			for j,element in enumerate(line):
				print(str(element),)
			print()
		print()

	def show_level(self):
		print("")
		print(self.name)
		for i,line in enumerate(self.data):
			for j,element in enumerate(line):
				print(str(element),)
			print()
		print()

	def init_level(self):
		self.animslist=list()
		self.px=0
		self.py=0
		self.level=deepcopy(self.data)
		self.level_end=False
		self.pd=1
		self.life=3
		self.maxdepth=0
		self.jumpers=0
		self.namesurf=myfont.render(self.level_name, False, (255,255,255))

	def endofline(self):
		return(self.px+self.pd>=self.width)or(self.px+self.pd<0)

	def next_collision(self,letter="B"):
		return(self.level[self.py][self.px+self.pd]==letter)
	
	def draw(self,screen):
		screen.fill((0,0,0))
		data=self.level
		mp=pygame.mouse.get_pos()
		mx,my=((mp[0]-gx)//ts*ts,(mp[1]-gy)//ts*ts)
		#screen.blit(cbnasurf, (0,0))
		for i in range(7):
			for j in range(11):
				if(data[i][j]=="B"):
					color=(0,0,0)
					pygame.draw.rect(screen, color,        (gx+ts*j,  gy+ts*i,   ts, ts))
				else:
					color=tuple(a*(j+3)/14 for a in colors[i]) 
					pygame.draw.rect(screen, color,        (gx+ts*j,  gy+ts*i,   ts, ts))
					if(i==6):
						screen.blit(gradtile, (gx+j*ts, gy+i*ts))
				if(data[i][j]=="D"):
					screen.blit(boostdown, (gx+j*ts, gy+i*ts))
				elif(data[i][j]=="U"):
					screen.blit(boostup, (gx+j*ts, gy+i*ts))
				elif(data[i][j]=="V"):
					screen.blit(lifevial, (gx+j*ts, gy+i*ts))

		pygame.draw.lines(screen, (255,255,255), False, ((gx,gy+gh-1),(gx,gy),(gx+gw,gy),(gx+gw,gy+gh-1)))
		if(mx>=0 and my>=0 and mx <gw and my<gh):
			pygame.draw.lines(screen, (255,255,255), True, ((gx+mx,gy+my),(gx+mx+ts,gy+my),(gx+mx+ts,gy+my+ts-1),(gx+mx,gy+my+ts-1)))
			if(pygame.mouse.get_pressed()[0]==True):
				#screen.blit(boostingsurf,(gx+mx,gy+my))
				pass
		self.damagecount=max(0,self.damagecount-1)
		#print("Damage is",anim.damagecontrol)
		dc=(self.damagecount<=0) or (self.damagecount>half) or ((self.damagecount%3)==0)	
		"""
		if not anim.damagecontrol:
			print("Damage control set to",anim.damagecontrol)"""
		anim.damagecontrol=dc
		"""
		for anim in self.animslist:
			anim.damagecontrol=dc"""
		index=0		
		while(index<len(self.animslist)):
			if(not next(self.animslist[index])):
				self.animslist.pop(index)
			else:
				index+=1





		#pygame.draw.rect(screen, (0,0,0), ((1+gx+gw,gy+self.maxdepth*ts+ts),(gx+gw+ts,gy+gh)))
		if(self.maxdepth<7 and self.maxdepth>=0 and self.show):
			screen.blit(marker, (gx+gw,gy+ts*self.maxdepth))
		
		#pygame.draw.rect(screen, (0,0,0), ((0,0),(ts*7,gy-1)))
		for i in range(self.continues):
			screen.blit(starsurf, (ts*i,0))


		
		#pygame.draw.rect(screen, (0,0,0), ((0,gy+ts*2.5),(ts*1.5,gy+gh)))

		if(self.show):
			if(self.jumpers>=0):
				for i in range(3):
					if(i<self.jumpers):
						screen.blit(boostnote,(ts/2,wh+i*ts*1-5.5*ts))
					else:
						screen.blit(boost_socket,(ts/2,wh+i*ts*1-5.5*ts))
						
			elif(self.jumpers==-1):
				screen.blit(infinity,(ts/2,wh-5.5*ts))

			for v in range(3):
				if(v<self.life):
					screen.blit(heartsurf, (ts*v,ts))
				else:
					screen.blit(emptyheartsurf, (ts*v,ts))
			screen.blit(leveltitle,(ww/2,0))
			screen.blit(scoretitle,(ww/2,ts))
			screen.blit(boosttitle,(ts/2,4*ts))
		
			screen.blit(myfont.render(to_dodec(self.score), False, (255,255,255)),(ww-ts*5,gy-ts))
			screen.blit(self.namesurf,(ww-ts*5,0))





	def draw_char(self,screen):
		screen.blit(chartable[0][0],(gx,gy))


	def step(self):
		#print self.px,self.py,
		l=self.level
		if(self.life==0):
				self.animslist.append(anim.diet(self.screen,self.px,self.py,self.pd,half))		
				self.level_end=True
		elif self.endofline(): #next step is end of line
			#TODO turnanimation
			#self.animations.append(turnanimation(self.px,self.py,self.pd))
			self.animslist.append(anim.turn(self.screen,self.px,self.py,self.pd))
			self.pd=-self.pd
		elif self.next_collision("B"): #block

			self.px+=self.pd
			if(self.can_step):
				self.animslist.append(anim.forward(self.screen,self.px,self.py,self.pd))
			self.life-=1
			if(self.life>0): #following interpretatino, >0 or >=0
				#print "DAMAGE!"
				self.score-=1
				self.animslist.append(anim.crush(self.screen,self.px,self.py,-(not self.can_step)*quarter))
				#TODO damageanimation
				#self.animations.append(damageanimation(self.px,self.py,self.pd)
				l[self.py][self.px]="0"	#remove the wall marker
				self.damagecount=half+e+(not self.can_step)*quarter
			else:
				#print "DEAD!"
				self.score-=5
				self.animslist.append(anim.diet(self.screen,self.px,self.py,self.pd))
				#TODO deadanimation
				#self.animations.append(deadanimation(self.px,self.py,self.pd)				
				self.level_end=True
				#self.next_step=30 #???? not using this?
		elif self.next_collision("V"): #vial of vitality (vie)
			#print "REGEN"
			self.score+=2
			self.px+=self.pd
			if(self.can_step):
				self.animslist.append(anim.forward(self.screen,self.px,self.py,self.pd))
			self.animslist.append(anim.bonus(self.screen,self.px,self.py,-(not self.can_step)*quarter))
			l[self.py][self.px]="0"
			self.life=min(self.life+1,3) #3 is max, gotta write this one down
			#TODO bonusanimation
			#self.animations.append(bonusanimation
		elif self.next_collision("U"):
			if(self.can_step):
				if(self.py==0):
					self.px+=self.pd
					self.animslist.append(anim.forward(self.screen,self.px,self.py,self.pd))
					#TODO up edge animation
					#up edge sound bump
					pass
				else:
					#print "JUMP UP"
					self.py-=1
					self.can_step=False

					self.animslist.append(anim.jump_up(self.screen,self.px+self.pd,self.py,self.pd))
					self.step()
					self.can_step=True
			else:
				self.px+=self.pd
				#sound can't step
			
		elif self.next_collision("D"):
			if(self.can_step):
				if(self.py==self.height-1):
					self.level_end=True
					#print "* >>WIN<< *"
					self.py+=1					
					self.animslist.append(anim.jump_down(self.screen,self.px+self.pd,self.py,self.pd))
					self.animslist.append(anim.endlevel(self.screen,self.px+self.pd,self.py,self.pd))
					self.score+=self.life*3
					self.score+=self.jumpers
					#TODO win animation
					#win sound
				else:
					#print "JUMP DOWN"

					self.py+=1
					self.animslist.append(anim.jump_down(self.screen,self.px+self.pd,self.py,self.pd))
					self.can_step=False
					self.step()
					self.can_step=True
					if(self.py>self.maxdepth):
						self.maxdepth+=1
						self.jumpers=min(self.jumpers+1,3) #3 is max apparently
						#print ">>JUMPER BONUS!"
						#jumpbonus sound
						
			else:
				self.px+=self.pd
				#sound can't step
		else:
			self.px+=self.pd
			if(self.can_step):
				self.animslist.append(anim.forward(self.screen,self.px,self.py,self.pd))
		#print ""

	#def draw(self,screen):
		
	
if __name__=="__main__":
	level=game_map()
	level._load("test")
	level.show_level()
	level.init_level()
	
	while not level.level_end:
		#for i in range(10):	
		level.step()
		level.show()

