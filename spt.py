#! python
import pygame
import os
import game_system as game_loader
from constants import *
unlocked=True


def menu_loop(screen,clock):
	quit=False
	game=False
	current=0
	loader=game_loader.game_map(1,screen)
	loader._load("menu")
	loader.init_level()
	loader.jumpers=0
	loader.life=3
	loader.continues=0
	loader.show=False
	#print("Is this it?")
	loader.r()
	step=0
	title="Ups and downs"
	title=myfont.render(title,False,(255,255,255))
	mark=pygame.image.load(os.path.join("graphics","marker.png"))
	mark=pygame.transform.flip(mark,True,False)
	names="Tutorial","Rush mode","Quit","Characters"
	secret=myfont.render("Puzzle",False,(255,255,255))
	messages=[myfont.render(txt,False,(255,255,255)) for txt in names]
	while not quit and not game:
		loader.draw(screen)
		screen.blit(mark,(gx,current*ts+gy+4*ts))
		screen.blit(title,(ts*2.5,ts/2*1.8))
		if(unlocked):
			screen.blit(secret,(gx+ts,gy+3*ts))
		for i,msg in enumerate(messages):
			screen.blit(msg,(gx+ts,gy+4*ts+i*ts))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit=True
			elif event.type==pygame.KEYDOWN:
				if event.key==pygame.K_DOWN:
					current=min(3,current+1)
				elif event.key==pygame.K_UP:
					current=max(-bool(unlocked),current-1)
				elif event.key==pygame.K_RIGHT or event.key==pygame.K_SPACE or event.key==pygame.K_KP_ENTER  or event.key==pygame.K_RETURN:
					if(current==2):
						quit=True
					else:
						game=True
			elif event.type==pygame.KEYUP:
				pass #TODO
		step+=1
		if(step%half==0):
			loader.step()

		pygame.display.flip()
		clock.tick(60)

	return quit,current


def game_over_loop(screen,clock):
	screen.fill((0,0,0))
	screen.blit(myfont.render("Game Over",False,(255,255,255)),(gw/2,gh-gy))
	
	pygame.display.flip()
	for i in range(second*6):
		clock.tick(second)

def game_win_loop(screen,clock):
	global unlocked
	unlocked=True
	screen.fill((0,0,0))
	screen.blit(myfont.render("You win!",False,(255,255,255)),(gw/2,gh-gy))
	screen.blit(myfont.render("You unlocked a secret character..!",False,(255,255,255)),(gx/2,gh-gy+ts))
	screen.blit(myfont.render("(Change it in the character menu)",False,(255,255,255)),(gx/2,gh-gy+ts*2))
	#screen.blit(myfont.render("You unlocked puzzle mode!",False,(255,255,255)),(gx/2,gh-gy+ts))
	sf(lf()|1)
	"""
	datafile=open(os.path.join("levels","level0.rawdata"),"r+")
	datafile.write("1")
	datafile.close()	"""

	pygame.display.flip()
	for i in range(second*6):
		clock.tick(second)
	
def character_loop(screen,clock):
	fat=lf()
	cn=("M. Bump","Potato","Radstar","Head")
	cc=("Default character","Complete the game","Complete the puzzles","Collect all life vials")
	screen.fill((0,0,0))
	quit=False
	ret=False
	current=lc()
	MAXCHOICE=2
	for i in range(MAXCHOICE):
		screen.blit(
		myfont.render(cc[i],False,(255,255,255)), (gx,gy+i*ts))
		if(i!=0 and fat!=1):
			msg="???"
		else:
			msg=cn[i]
		screen.blit(
		myfont.render(msg,False,(255,255,255)), (gx+gw-ts*3,gy+i*ts))
	fsurf=myfont.render(">",False,(255,255,255))
	screen.blit(myfont.render("Back",False,(255,255,255)),((gx,gy+ts*MAXCHOICE)))
	cursor=current
	while not quit and not ret:
		pygame.draw.rect(screen,(0,0,0),((0,0),(gx,wh)))
		pygame.draw.rect(screen,(0,0,0),((0,0),(ww,ts)))
		screen.blit(fsurf,(ts,gy+cursor*ts))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit=True
			elif event.type==pygame.KEYDOWN:
				if event.key==pygame.K_DOWN:
					cursor=min(MAXCHOICE,cursor+1)
				elif event.key==pygame.K_UP:
					cursor=max(0,cursor-1)
				elif event.key==pygame.K_RIGHT or event.key==pygame.K_SPACE or event.key==pygame.K_KP_ENTER  or event.key==pygame.K_RETURN:
					if(cursor==2):
						ret=True
					else:
						#print(cursor)
						#print(fat)
						#print((2**cursor)&fat)
						if((cursor == fat) or cursor==0):
							sc(cursor)
							current=cursor
				elif event.key == pygame.K_q or event.key==pygame.K_LEFT or event.key == pygame.K_ESCAPE :
					ret=True
		screen.blit(font2.render("Current character : "+cn[current],False,(255,255,255)),(ts/2,ts/2))
		pygame.display.flip()
		clock.tick(60)
	return quit

def puzzle_loop(screen,clock):
	quit=False
	game=False
	loader=game_loader.game_map(0,screen)
	completion=[0]*len(puzzle_list)
	current=0
	mode="Menu"
	starsurf=pygame.image.load(os.path.join("graphics", "star.png"))
	mark=pygame.image.load(os.path.join("graphics","marker.png"))
	mark=pygame.transform.flip(mark,True,False)

	names=["Back"]+[x.capitalize() for x in puzzle_list]
	names=[myfont.render(msg,False,(255,255,255)) for msg in names]
	quitmessage=font2.render("Press Q/ESC to return",False,(255,255,255))
	startmessage=font2.render("Press SPACE to start",False,(255,255,255))
	step=0
	while not quit and not game:
		if mode=="Menu":
			screen.fill((0,0,0))
			for i,msg in enumerate(names):
				screen.blit(msg,(ts*4,ts*2+i*ts))
			for i,star in enumerate(completion):
				if star:
					screen.blit(starsurf,(ts*3,ts*3+i*ts))
			screen.blit(mark,(ts*2,ts*2+current*ts))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit=True
				elif event.type==pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						current=max(0,current-1)
					elif event.key == pygame.K_DOWN:
						current=min(len(names)-1,current+1)
					elif event.key == pygame.K_q or event.key==pygame.K_LEFT\
						or event.key == pygame.K_ESCAPE :
						game=True
					
					elif event.key==pygame.K_RIGHT or event.key==pygame.K_SPACE or event.key==pygame.K_KP_ENTER or event.key==pygame.K_RETURN:
						if(current==0):
							game=True
						else:
							mode="Puzzle"
							loader._load(puzzle_list[current-1])
							loader.init_level()
							loader.jumpers=-1 #for the initial frame
							step=0
		elif mode=="Puzzle":
			loader.draw(screen)
			loader.jumpers=-1
			loader.life=3
			screen.blit(quitmessage,(0,0))
			screen.blit(startmessage,(0,ts/2))

			if((step//half)%2==0):
				loader.draw_char(screen)

			step+=1

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit=True
				elif event.type==pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						#if(loader.jumpers>0):
						loader.put_jumper(True)
					elif event.key == pygame.K_DOWN:
						#if(loader.jumpers>0):
						loader.put_jumper(False)
					elif event.key == pygame.K_r :
						loader.init_level()
					elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE :
						mode="Menu"
					elif event.key==pygame.K_SPACE or event.key==pygame.K_KP_ENTER  or event.key==pygame.K_RETURN:
						mode="Play"
						loader.jumpers=0
						step=0
				elif event.type==pygame.KEYUP:
					pass #TODO
			
		elif mode=="Play":
			loader.draw(screen)
			if(loader.level_end):
				if(len(loader.animslist)==0):
					if(loader.has_lost()):
						loader.init_level()
						mode="Puzzle"
						step=0
					else:
						completion[current-1]=True
						mode="Menu"
			else:
				if(step%half==0):
					loader.step()
				step+=1
			

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						quit=True
					elif event.type==pygame.KEYDOWN:
						if event.key == pygame.K_UP:
							if(loader.jumpers>0):
								if(loader.put_jumper(True)):
									loader.jumpers-=1
						elif event.key == pygame.K_DOWN:
							if(loader.jumpers>0):
								if(loader.put_jumper(False)):
									loader.jumpers-=1
						elif event.key == pygame.K_r:
							loader.kill()
						elif event.key==pygame.K_SPACE:
							loader.init_level()
							mode="Puzzle"
							step=0
					elif event.type==pygame.KEYUP:
						pass #TODO
		

		pygame.display.flip()
		clock.tick(60)
	return quit

def tutorial_loop(screen,clock):
	def move_mouse_in(x0,y0,x1,y1,steps):
		for i in range(int(steps)):
			yield (  (x0+float(x1-x0)*i/steps),(y0+float(y1-y0)*i/steps)  )
		while True:
			yield (x1,y1)

	def put_a_tile(x,y,mx,my,up=True,timer=1):
		move=move_mouse_in(mx,my,gx+x*ts+ts/2,gy+y*ts+ts/2,int((timer-0.5)*second))
		up,down=up,not up
		for i in range(int((timer-0.5)*second)):
			yield move.__next__(), 0, 0
		for i in range(int(second/2)):
			yield move.__next__(), up, down
			if i==int(second/4):
				loader.put(x,y,up)
				loader.jumpers-=1
		while True:
			yield move.__next__(), 0,0
	quit=False
	loader=game_loader.game_map(1,screen)
	loader._load("tutorial")
	loader.init_level()
	loader.jumpers=2
	step=0
	act=0
	skip=font2.render("Press ESC or any key to skip",False,(255,255,255))
	mouse=pygame.image.load(os.path.join("graphics","mouse.png"))
	keyup,keydown=(tuple( \
		pygame.image.load(os.path.join("graphics",name+str(i)+".png")) \
		for i in (0,1)) for name in ("keyup","keydown"))
	uparrow,downarrow=False,False
	mx,my=-ts,gy+ts*4
	#xp,yp=mx,my
	#xs,ys=gx+ts*8.5,gy+ts/2
	message=myfont.render("",False,(255,255,255))
	action=put_a_tile(8,0,mx,my,False,3)
	decal=2
	done=False
	usual_time=second
	while not quit and not done:
		loader.draw(screen)
		
		if(act==0):
			loader.draw_char(screen)
			pygame.draw.rect(screen, (0,0,0), ((gx,gy+ts*decal),(gx+gw,gy+gh)))
			if(step==1*second):
				message=myfont.render(\
				"Press UP/DOWN to put a JUMP TILE",False,(255,255,255))
			if(step<3.5*second):
				(mx,my),uparrow,downarrow=action.__next__()
			if(step==4*second):
				action=put_a_tile(8,1,mx,my,False,1)
			if(4*second<step<second*5.5):
				(mx,my),uparrow,downarrow=action.__next__()
			step+=1
			if(step==6*second):
				act=1
				action=move_mouse_in(mx,my,ww+ts,my+ts*4,second)
				step=0

		if(act==1):			
			if(step==half*4):
				message=myfont.render(\
				"You can't JUMP twice in a row!",False,(255,255,255))
			if(step<half*12):
				mx,my=action.__next__()
				if(step%half==0):
					loader.step()						
				step+=1
			else:
				decal=4
				act=2
				step=0

		if(act==2):
			if(step==0):
				action=put_a_tile(0,2,mx,my,False,2)
			if(step==half):
				message=myfont.render(\
				"Avoid coliding with BLOCKS",False,(255,255,255)) #collect life vials
			if(step==second*10):
				message=myfont.render(\
				"You have limited JUMP TILES during play",False,(255,255,255))
			if(step==second*2):
				action=put_a_tile(2,3,mx,my,False,1)
			if(step==second*4):
				decal=6
				action=put_a_tile(3,4,mx,my,False,1)
			if(step==second*5):
				action=put_a_tile(6,5,mx,my,True,1)
			if(step==second*7):
				action=put_a_tile(7,4,mx,my,True,1)
			if(step==second*8):
				action=move_mouse_in(mx,my,mx*2,my-ts,second)
			if(step==second*9):
				decal=7
			if(step==second*14):
				message=myfont.render(\
				"But before the LEVEL STARTS",False,(255,255,255))
			if(step==second*18):
				message=myfont.render(\
				"you will have INFINITE TILES",False,(255,255,255))
				loader.jumpers=-1
			#if(step==second*18):
			#	message=myfont.render(\
			#	"You will have UNLIMITED jumper tiles!",False,(255,255,255))
			if(step==second*22):
				message=myfont.render(\
				"If you ever get stuck, press R",False,(255,255,255))

			if(step%half==0):
				loader.step()
			if(step<8.5*second):
				data=action.__next__()
			data=action.__next__()
			if(len(data)==3):
				(mx,my),uparrow,downarrow=data
			else:
                                (mx,my)=data
		
			if(step==second*24):
				loader.kill()
				loader.continues=0
			if(step>second*24 and step%half==0):
				act=3
				step=0
			step+=1

		if(act==3):
			if(step==second*4):
				message=myfont.render(\
				"You have to reach the very bottom",False,(255,255,255))
			if(step==second*7):
				message=myfont.render(\
				"of the 7 floors to pass a level",False,(255,255,255))
			if(step==second*11):
				message=myfont.render(\
				"Good luck!",False,(255,255,255))
				#message=myfont.render(\
				#"You have 7 continues and 3 lives",False,(255,255,255))
				loader.life=3
				loader.continues=7
			if(step==second*15):
				message=myfont.render(\
				"Good luck!",False,(255,255,255))
			if(step==second*16):
				done=True
			step+=1
		pygame.draw.rect(screen, (0,0,0), ((gx,gy+ts*decal),(gx+gw,gy+gh)))
		if(decal<7):
			screen.blit(keyup[uparrow],(gx+ts/2,gy+gh-ts*2.5))
			screen.blit(keydown[downarrow],(gx+ts/2,gy+gh-ts*1.5))
			screen.blit(mouse,(mx,my))
		screen.blit(message,(gx-24,gy+gh))
		if(act<3):
			screen.blit(skip,(ts,0))
			

		pygame.display.flip()
		clock.tick(usual_time)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit=True
			elif event.type==pygame.KEYDOWN:
				usual_time=second*4
				if event.key == pygame.K_ESCAPE:
					done=True
			elif event.type==pygame.KEYUP:
				usual_time=second
	return quit
	
def game_loop(screen,clock):
	quit=False
	game=False
	continues=7
	score=0
	loader=game_loader.game_map(continues,screen)
	animlist=list()
	mode="Next"
	current_level=0
	step=0
	
	while not quit and not game:
		if(mode=="Next"): ###################LOADING NEXT LEVEL
			if(current_level>=len(levels_list)):
				game=True #game over : no more levels to load
			else:
				if(step==0):
					loader._load(levels_list[current_level])
					screen.fill((0,0,0))
					screen.blit(myfont.render("Get ready", False, (255,255,255)	),(gw/2,gh/2))
					screen.blit(myfont.render("You have 7+3 seconds with",False, (255,255,255)),(gw/2-ts*2,gh/2+ts))
					screen.blit(myfont.render("unlimited jumpers",False, (255,255,255)),(gw/2-ts,gh/2+ts*2))
					pygame.display.flip()
				if(step<second*4):
					clock.tick(second)
					step+=1
				else:
					mode="Start"
					step=0


		elif(mode=="Start"): ################UNLIMITED BOOSTERS PART
			if(step==0):
				loader.init_level()
				loader.jumpers=-1
				loader.life=0
				curc=10
				curter=myfont.render("G.0",False,(255,255,255))
				#curc=10-step//60
			if(step%second==0 and step!=0):
				curc=10-(step//second)
				if(curc>=0):
					curter=myfont.render(str(curc),False,(255,255,255))
				else:
					curter=myfont.render("Game",False,(255,255,255))

			yy=min(gy+gh,gy+gh-(ts*curc)+ts*3)
			loader.life=min(3,max(0,3-curc))
			loader.draw(screen)
			if((step//half)%2==0):
				loader.draw_char(screen)
			pygame.draw.rect(screen,(0,0,0),(gx,yy,gx+gw,gy+gh+ts))
			screen.blit(curter,(ts*7,min(gy+gh,max(ts*5,yy))))
			
			pygame.display.flip()
			clock.tick(second)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit=True
				elif event.type==pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						#if(loader.jumpers>0):
						loader.put_jumper(True,10-curc)
					elif event.key == pygame.K_DOWN:
						#if(loader.jumpers>0):
						loader.put_jumper(False,10-curc)
					elif event.key == pygame.K_ESCAPE:
						game=True
						loader.continues=0
						loader.level_end=True
						loader.life=0
				elif event.type==pygame.KEYUP:
					pass #TODO

			
			step+=1

			if(step==second*11):
				mode="Game"
				loader.jumpers=0
				step=0

			
		if(mode=="Game"): #################AUTO-GAME PART
			loader.draw(screen)
			step+=1
			if(step==second//2):
				step=0
				loader.step()
				if(loader.level_end):
					if(loader.has_lost()):
						continues-=1
						loader.continues-=1
						if(continues==0):
							game=True #game over
						else:
							mode="Dying"
					else:
						current_level+=1
						mode="Ending"

			pygame.display.flip()
			clock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit=True
				elif event.type==pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						if(loader.jumpers>0):
							if(loader.put_jumper(True)):
								loader.jumpers-=1
					elif event.key == pygame.K_DOWN:
						if(loader.jumpers>0):
							if(loader.put_jumper(False)):
								loader.jumpers-=1
					elif event.key == pygame.K_r:
							loader.kill()
					elif event.key == pygame.K_ESCAPE:
						game=True
						loader.continues=0
						loader.level_end=True
						loader.life=0
				elif event.type==pygame.KEYUP:
					pass #TODO

		elif(mode=="Dying"): ###########ONE DEATH
			for i in range(60*3):
				loader.draw(screen)
				pygame.display.flip()
				clock.tick(60)
			mode="Start"

		elif(mode=="Ending"): #############LEVEL END, YAY
			for i in range(60*8):
				loader.draw(screen)
				pygame.display.flip()
				clock.tick(60)
			mode="Next"


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit=True

		#pygame.display.flip()
	return quit,not loader.has_lost()

if __name__=="__main__":
	pygame.init()
	size= (WIDTH,HEIGHT)
	screen = pygame.display.set_mode(size)
	back = pygame.Surface(screen.get_size())
	back.fill((0, 0, 0))
	screen.blit(back, (0, 0))
	pygame.display.set_caption("7+3")

	clock = pygame.time.Clock()
	quit=False
	while not quit:
		quit,choice=menu_loop(screen,clock)
		if not quit:
			if(choice==0):
				quit=tutorial_loop(screen,clock)
			elif(choice==1):
				quit,win=game_loop(screen,clock)
				if not quit:
					if win:
						game_win_loop(screen,clock)
					else:
						game_over_loop(screen,clock)
			elif(choice==3):
				quit=character_loop(screen,clock)
			elif(choice==-1):
				quit=puzzle_loop(screen,clock)
	pygame.quit()
