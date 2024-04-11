import pygame,sys,random
import tkinter

#initializing python
pygame.init()

#creating the game window
screen=pygame.display.set_mode((1152,500))
#setting a clock for frame rate
clock=pygame.time.Clock()

#bird movement
gravity=0.18
bird_move=0
run_game=True
score=0
high_score=0
#continuous base function
def move_base():
	screen.blit(base_surf,(base_pos,430))
	screen.blit(base_surf,(base_pos+576,430))
	screen.blit(base_surf,(base_pos+1152,430))
	
def create_pipe():
	hd=random.choice(difference)
	pipe_pos=random.choice(pipe_height)
	bottom_pipe=pipe_surf.get_rect(midtop=(1200,pipe_pos))
	top_pipe=pipe_surf.get_rect(midbottom=(1200,pipe_pos - hd))
	return bottom_pipe,top_pipe

def move_pipe(pipes):
	for pipe in pipes :
		pipe.centerx-=4.5
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom>=500:
			screen.blit(pipe_surf,pipe)
		else:
			flip_pipe=pygame.transform.flip(pipe_surf,False,True)
			screen.blit(flip_pipe,pipe)
			
def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			return False
	if bird_rect.top<=0 or bird_rect.bottom>=430:
		return False

	return True	

def rotate_bird(bird):
	new_bird=pygame.transform.rotozoom(bird,-bird_move*5,1)
	return new_bird

def bird_animation():
	new_bird=bird_frames[bird_index]
	new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
	return new_bird,new_bird_rect

def display_score(game_state):
	if game_state=='active':
		score_surf=game_font.render(f'Score: {int(score)}',True,(255,255,255))
		score_rect=score_surf.get_rect(center=(576,50))
		screen.blit(score_surf,score_rect)
	if game_state=='over':
		score_surf=game_font.render(f'Score: {int(score)}',True,(255,255,255))
		score_rect=score_surf.get_rect(center=(576,50))
		screen.blit(score_surf,score_rect)

		highscore_surf=game_font.render(f'High Score: {int(high_score)}',True,(255,0,0))
		highscore_rect=highscore_surf.get_rect(center=(576,380))
		screen.blit(highscore_surf,highscore_rect)

def update_score(score,high_score):
	if score>high_score :
		high_score=score
	return high_score	

def remove_pipes(pipes):
	for pipe in pipes:
		if pipe.centerx<=-35:
			pipes.remove(pipe)
			
#window title
pygame.display.set_caption('Flappy Bird')
bg_surf=pygame.image.load('D:/Chinmay/pics/bg3.png').convert()
bg_surf=pygame.transform.scale2x(bg_surf)

base_surf=pygame.image.load('D:/Chinmay/pics/base.png').convert()
base_surf=pygame.transform.scale2x(base_surf)
base_pos=0

bird_mid_surf=pygame.image.load('D:/Chinmay/pics/yellowbirdmid.png').convert_alpha()
bird_down_surf=pygame.image.load('D:/Chinmay/pics/yellowbirddown.png').convert_alpha()
bird_up_surf=pygame.image.load('D:/Chinmay/pics/yellowbirdup.png').convert_alpha()
bird_frames=[bird_down_surf,bird_mid_surf,bird_up_surf]
bird_index=0
bird_surf=bird_frames[bird_index]
bird_rect=bird_surf.get_rect(center=(100,250))

game_font=pygame.font.Font('04B_19.ttf',40)
BIRDFLAP=pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,200)

#bird_surf=pygame.image.load('D:/Chinmay/pics/yellowbirdmid.png').convert_alpha()
#bird_rect=bird_surf.get_rect(center=(100,250))
pipe_surf=pygame.image.load('D:/Chinmay/pics/redpipe.png').convert()
pipe_surf=pygame.transform.scale2x(pipe_surf)
pipe_list=[]

CREATEPIPE=pygame.USEREVENT
pygame.time.set_timer(CREATEPIPE,750)
pipe_height=[180,250,275,350]

msg_surf=pygame.image.load('D:/Chinmay/pics/message.png').convert_alpha()
msg_rect=msg_surf.get_rect(center=(576,210))
difference=[130,140,150]

#Game Loop
while True:
	for event in pygame.event.get():
		if event.type==pygame.QUIT :
			pygame.quit()
			sys.exit()
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_SPACE and run_game :
				bird_move=0
				bird_move-=4.8
			if event.key==pygame.K_RETURN and run_game==False :
				run_game=True
				pipe_list.clear()
				bird_rect.center=(100,180)
				bird_move=0
				score=0
		if event.type==CREATEPIPE:
			pipe_list.extend(create_pipe())
		if event.type==BIRDFLAP:
			if bird_index<2:
				bird_index+=1
			else:
				bird_index=0

			bird_surf,bird_rect=bird_animation()	
	screen.blit(bg_surf,(0,0))		
	base_pos-=3
	if run_game:
		bird_move+=gravity
		bird_rect.centery+=bird_move
		rotated_bird=rotate_bird(bird_surf)
		screen.blit(rotated_bird,bird_rect)
		pipe_list=move_pipe(pipe_list)
		draw_pipes(pipe_list)
		remove_pipes(pipe_list)
		run_game=check_collision(pipe_list)
		score+=0.1
		display_score('active')
	else:
		screen.blit(rotated_bird,bird_rect)
		bird_move=0
		draw_pipes(pipe_list)
		screen.blit(msg_surf,msg_rect)
		high_score=update_score(score,high_score)
		display_score('over')
	move_base()
	if base_pos-576<=-576:
		base_pos=0
	pygame.display.update()
	clock.tick(125)
