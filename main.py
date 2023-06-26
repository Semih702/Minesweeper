# Example file showing a circle moving on screen
import pygame
import block

# pygame setup
pygame.init()
number_colors={1:"darkslateblue",2:"orange",3:"fuchsia",4:"mediumaquamarine",5:"purple3",6:"royalblue4",7:"yellow",8:"forestgreen"}
width=1280
height=720
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
color_dark='indigo'
color_light='darkblue'
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
font=pygame.font.SysFont('Ariel',35)
number_font=pygame.font.SysFont('Ariel',55)
lose_font=pygame.font.SysFont('Ariel',50)
text=[font.render('easy',True,'ghostwhite'),font.render('normal',True,'ghostwhite'),font.render('hard',True,'ghostwhite')]
clicked_easy=False
clicked_normal=False
clicked_hard=False
clicked=False
is_started=False
is_ended=False
right_clicked=False
mid_clicked=False
win=False
remaining_bombs=0
remaining_blocks=0
first_move=False
blocks = []
current_x=0
current_y=0
texts=[]
flags=[]
ended_color=""
ended_index=0
mode=""
def start(width,height):
    screen = pygame.display.set_mode((width, height))
    return True
    
def reveal_everything(blocks):
    pass

while running:
    if is_started and not remaining_blocks:
        is_ended=True
        win=True
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1 and not is_started and width/2-60 <=mouse[0] <=width/2 + 60 and height/2-70<=mouse[1]<= height/2 - 30:
                clicked_easy=True
            elif event.button==1 and not is_started and width/2-60 <=mouse[0] <=width/2 + 60 and height/2-20<=mouse[1]<= height/2 + 20:
                clicked_normal=True
            elif event.button==1 and not is_started and width/2-60 <=mouse[0] <=width/2 + 60 and height/2+30<=mouse[1]<= height/2 + 70:
                clicked_normal=True
            elif is_started and mouse[1]>90:
                current_x=mouse[0]//40 +1
                current_y=(mouse[1]-90)//40 +1
                if (mouse[0]-1)%40 and (mouse[0]-2)%40 and (mouse[1]-91)%40 and (mouse[1]-92)%40:
                    if event.button==3:
                        right_clicked=True
                    elif event.button==1:
                        clicked=True
                    elif event.button==2:
                        mid_clicked=True
            elif is_ended:
                clicked=True
        if event.type == pygame.MOUSEBUTTONUP:
            if is_ended:
                running=False
            elif event.button==1 and not is_started:
                if clicked_easy and width/2-60 <=mouse[0] <=width/2 + 60 and height/2-70<=mouse[1]<= height/2 -30:
                    is_started=True
                    width=360
                    height=450
                    first_move=start(360,450)
                    remaining_bombs=10
                    remaining_blocks=71
                    mode="easy"
                elif clicked_normal and width/2-60 <=mouse[0] <=width/2 + 60 and height/2-20<=mouse[1]<= height/2 + 20:
                    is_started=True
                    width=640
                    height=730
                    first_move=start(640,730)
                    remaining_bombs=40
                    remaining_blocks=216
                    mode="normal"
                elif clicked_normal and width/2-60 <=mouse[0] <=width/2 + 60 and height/2+30<=mouse[1]<= height/2 + 70:
                    is_started=True
                    width=1200
                    height=730
                    first_move=start(1200,730)
                    remaining_bombs=99
                    remaining_blocks=381
                    mode="hard"
            elif is_started and (clicked or right_clicked or mid_clicked):
                if mouse[0]//40 +1 == current_x and (mouse[1]-90)//40 + 1==current_y and ((mouse[0]-1)%40 and (mouse[0]-2)%40 and (mouse[1]-91)%40 and (mouse[1]-92)%40):
                    if clicked  and event.button==1:
                        if first_move:
                            if mode=="easy":
                                blocks= block.create(9, 9, 10, blocks ,(current_y,current_x))
                            elif mode=="normal":
                                blocks= block.create(16, 16, 40, blocks ,(current_y,current_x))
                            elif mode=="hard":
                                blocks= block.create(30, 16, 99, blocks ,(current_y,current_x))


                            
                            first_move=False
                        numbers=blocks[current_y][current_x].reveal_first(blocks)
                        if numbers==False:
                            is_ended=True
                        elif numbers is not None:
                            for i in numbers:
                                remaining_blocks-=1
                                if i[0]!=0:
                                    texts.append((number_font.render(str(i[0]),True,"black"),i[1],i[2]))
                    elif right_clicked and event.button==3 and not first_move:
                        bools=blocks[current_y][current_x].flag_it()
                        if bools[0]:
                            if bools[1]:
                                flags.append((number_font.render("&",True,'black'),current_x,current_y))
                                remaining_bombs-=1
                            else:
                                for i,j in enumerate(flags):
                                    if j[1]==current_x and j[2]==current_y:
                                        flags.pop(i)
                                        remaining_bombs+=1
                                        break
                    elif mid_clicked and event.button==2 and not first_move:
                        numbers=blocks[current_y][current_x].auto_reveal(blocks)
                        if numbers==False:
                            is_ended=True
                        if numbers is not None:
                            if not numbers:
                                is_ended=True
                            else:
                                for i in numbers:
                                    remaining_blocks-=1
                                    texts.append((number_font.render(str(i[0]),True,'black'),i[1],i[2]))

            mid_clicked=False
            clicked=False
            right_clicked=False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("darkgrey")

    mouse = pygame.mouse.get_pos()
    if not is_started:
        if width/2 -60 <= mouse[0]<= width/2+60:
            if height/2 -70 <= mouse[1] <= height/2-30:
                pygame.draw.rect(screen,color_light,[width/2-60,height/2-70,120,40])
                pygame.draw.rect(screen,color_dark,[width/2-60,height/2-20,120,40])
                pygame.draw.rect(screen,color_dark,[width/2-60,height/2+30,120,40])

            elif height/2 -20 <= mouse[1] <= height/2+20:
                pygame.draw.rect(screen,color_dark,[width/2-60,height/2-70,120,40])
                pygame.draw.rect(screen,color_light,[width/2-60,height/2-20,120,40])
                pygame.draw.rect(screen,color_dark,[width/2-60,height/2+30,120,40])

            elif height/2 +30 <= mouse[1] <= height/2+70:
            
                pygame.draw.rect(screen,color_dark,[width/2-60,height/2-70,120,40])
                pygame.draw.rect(screen,color_dark,[width/2-60,height/2-20,120,40])
                pygame.draw.rect(screen,color_light,[width/2-60,height/2+30,120,40])

            else:
                pygame.draw.rect(screen,color_dark,[width/2-60,height/2-70,120,40])
                pygame.draw.rect(screen,color_dark,[width/2-60,height/2-20,120,40])
                pygame.draw.rect(screen,color_dark,[width/2-60,height/2+30,120,40])
        else:
            pygame.draw.rect(screen,color_dark,[width/2-60,height/2-70,120,40])
            pygame.draw.rect(screen,color_dark,[width/2-60,height/2-20,120,40])
            pygame.draw.rect(screen,color_dark,[width/2-60,height/2+30,120,40])
        screen.blit(text[0] , (width/2-25,height/2-60))
        screen.blit(text[1] , (width/2-25,height/2-10))
        screen.blit(text[2] , (width/2-25,height/2+40))

    else:
        for i in range(width//40):
            for j in range((height-90)//40):
                if (i+j)%2:
                    if(blocks and blocks[j+1][i+1].is_revealed()):
                        color="darkolivegreen1"
                    else:
                        color="khaki" #gold
                else:
                    if(blocks and blocks[j+1][i+1].is_revealed()):
                        color="darkolivegreen4"
                    else:
                        color="khaki3" #goldenrod1
                pygame.draw.rect(screen,color,[i*40,90+j*40,40,40])
                    

        #pygame.draw.rect(screen,"yellow",[0,90,width,height])
        pygame.draw.rect(screen,"gray23",[0,85,width,5])
        if not is_ended:
            text=lose_font.render(f"Remaining Bombs: {remaining_bombs}",True,'black')
            screen.blit(text,(20,20))
        elif win:
            text=lose_font.render("You Won The Game",True,'black')
            screen.blit(text,(20,20))
            ended_color="lime"
        elif is_ended:
            text=lose_font.render("You Lost",True,'black')
            screen.blit(text,(20,20))
            ended_color="red"
        """if is_ended:
            for i in range((ended_index//20)//(width//40)):
                for j in range((height-90)//40):
                    print(i,j)
                    pygame.draw.rect(screen,ended_color,[i*40,90+40*j,40,40])

            for j in range((ended_index//20)//(width//40)):
                for i in range((height-90)//40):
                    if not blocks[j+1][i+1].is_revealed() or blocks[(ended_index//20)//(width//40+1)][i+1].finished:
                        pygame.draw.rect(screen,ended_color,[i*40,90+40*(j),40,40])
            for i in range((ended_index//20)%(width//40)):
                if not blocks[(ended_index//20)//(width//40+1)][i+1].is_revealed() or blocks[(ended_index//20)//(width//40+1)][i+1].finished:
                    pygame.draw.rect(screen,ended_color,[i*40,90+40*((ended_index//20)//(width//40)),40,40])
            temp= blocks[(ended_index//20)//(height//40)+1][(ended_index//20)%(width//40)+1]
            if temp.is_revealed() and not temp.finished:
                ended_index+=19
            else:
                temp.revealed=True
                temp.finished=True
                if temp.number is not None:
                    texts.append((number_font.render(str(temp.number),True,'black'),temp.x,temp.y))
            print(((len(blocks)-2)*(len(blocks[0])-2)-1)*20 -1)
            if ended_index!=((len(blocks)-2)*(len(blocks[0])-2)-1)*20-1:
                ended_index+=1"""

        for i in range((height-90)//40):
            pygame.draw.rect(screen,"gray23",[0,40*i+90,width,2])
        for i in range(width//40):
            pygame.draw.rect(screen,"gray23",[40*i,90,2,height])
        for i in texts:
            text=i[0]
            screen.blit(text,((i[1]-1)*40+10,(i[2]-1)*40+90+5))
        for i in flags:
            text=i[0]
            screen.blit(text,((i[1]-1)*40+10,(i[2]-1)*40+90+5))

    # flip() the display to put your work on screen
    pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()