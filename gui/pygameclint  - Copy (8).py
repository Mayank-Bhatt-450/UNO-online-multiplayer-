import pygame,random,time
import _pickle as pickle
import threading,json
import requests
########################################################################
import random

def prn(*a,**k):
    colors=['red','green','yellow','blue','pink','light_blue','white']
    try:
        color=k['color']
        for i in range(7):
            if color==colors[i]:
                print(f"\x1b[{0};{30};{41+i}m",a,'\x1b[0m')
                break
    except:
        #print('\x1b[6;35;42m' + 'except!' + '\x1b[0m')
        print(f"\x1b[{0};{30};{random.randint(43,48)}m",a ,'\x1b[0m')
#########################################################################################
#username='bhatt1'
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
a=['black','+4']
deck={
'red':["['red','0'].png","['red','1'].png","['red','2'].png","['red','3'].png","['red','4'].png","['red','5'].png","['red','6'].png","['red','7'].png","['red','8'].png","['red','9'].png","['red','o'].png","['red','r'].png","['red','+2'].png","['red','+4'].png","['red','c'].png"]
,'yellow':["['yellow','0'].png","['yellow','1'].png","['yellow','2'].png","['yellow','3'].png","['yellow','4'].png","['yellow','5'].png","['yellow','6'].png","['yellow','7'].png","['yellow','8'].png","['yellow','9'].png","['yellow','o'].png","['yellow','r'].png","['yellow','+2'].png","['yellow','+4'].png","['yellow','c'].png"]
,'green':["['green','0'].png","['green','1'].png","['green','2'].png","['green','3'].png","['green','4'].png","['green','5'].png","['green','6'].png","['green','7'].png","['green','8'].png","['green','9'].png","['green','o'].png","['green','r'].png","['green','+2'].png","['green','+4'].png","['green','c'].png"]
,'blue':["['blue','0'].png","['blue','1'].png","['blue','2'].png","['blue','3'].png","['blue','4'].png","['blue','5'].png","['blue','6'].png","['blue','7'].png","['blue','8'].png","['blue','9'].png","['blue','o'].png","['blue','r'].png","['blue','+2'].png","['blue','+4'].png","['blue','c'].png"]
,'black':["['black','+4'].png","['black','c'].png"]}
ldeck={'red':[]
       ,'yellow':[]
       ,'green':[]
       ,'blue':[]
       ,'black':[]
       }
for c in ['red','yellow','green','black','blue']:
    for i in range(len(deck[c])):
        ldeck[c].append(pygame.image.load(deck[c][i]))

##########################################################################
# create the screen##########################

screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE)#,pygame.FULLSCREEN)#(1024,768))
print(pygame.display.Info())
pygame.display.set_caption("GU NO")
tital_icon=pygame.image.load('guno tokken.png')
pygame.display.set_icon(tital_icon)
pygame.init()
######################################################################
################REQUEST VARIABLES###################################
def login_view(username,password):
    global answer
    if username=='':
        return 'username'
    if password=='':
        return 'password'
    login_request=f"http://127.0.0.1:8000/{username},{password}_login"
    try:
        op=json.loads( requests.get(login_request).text)
    except:
        network(login_request)
        op=answer
    prn(login_request)
    return op
def waiting_view(host):
    global answer
    login_request=f"http://127.0.0.1:8000/{host}_wating_room"
    try:
        a=requests.get(login_request).text
    except:
        network(login_request)
        a=answer
    #prn(a)
    return json.loads( a)
def start_game(username):
    global answer
    login_request=f"http://127.0.0.1:8000/{username}_start_game"
    try:
        requests.get(login_request)
    except:
        network(f"http://127.0.0.1:8000/{username}_start_game")
def create_room_view(username):
    global answer
    login_request=f"http://127.0.0.1:8000/{username}_create_room"
    try:
        requests.get(login_request)
    except:
        prn('erroe in create view')
        network(f"http://127.0.0.1:8000/{username}_create_room")
def join_room_view(username,host):
    global answer
    if host=='':
        return {'text':'host is empty'}
    login_request=f"http://127.0.0.1:8000/{username},{host}_join_room"
    #print(login_request)
    try:
        l=requests.get(login_request).text
    except:
        network(login_request)
        l=answer
    #prn(l)
    return json.loads(l )
def leave_waiting_view(username,host):
    global answer
    login_request=f"http://127.0.0.1:8000/{username},{host}_leave_waiting"
    try:
        requests.get(login_request)
    except:
        prn('erroe in create view')
        network(f"http://127.0.0.1:8000/{username}_create_room")
def leave_game_view(username,host):
    global answer
    login_request=f"http://127.0.0.1:8000/{username},{host}_leave_game"
    try:
        requests.get(login_request)
    except:
        prn('erroe in create view')
        network(f"http://127.0.0.1:8000/{username}_create_room")
#################################################################
#########GAME VARIABLES#################################################
host=''
username=''
winner=''
gameloop_flag=False
hand_cards_list=[]
bg=[pygame.image.load('bg 0.png'),
    pygame.image.load('bg 1.png'),
    pygame.image.load('bg 1t.png'),
    pygame.image.load('bg 0t.png')
    ]
answer=''
game_states={}
turnflag=0
num_of_players=0
TURN=False
back_img=pygame.image.load('BACK.png')
turn_img=pygame.image.load('turn.png')
kick_img=pygame.image.load('kick.png')
network_view=pygame.image.load('network.png')
guno=pygame.image.load('GUNO.png')
gunot=pygame.image.load('GUNOt.png')
guno_flag=False
deckpile=pygame.image.load('draw.png')
deckpilecards=pygame.image.load('drawdeckcards.png')
num_deck_card=64
pile_cards=pygame.image.load('pilecards.png')
color_selector=pygame.image.load('color.png')
pile_cards_number=64
current=['green', '1']
clickedcard=[-1,[]]
clickflag=0
action=[]
draw_break=False
choose_color_flag=False
color_pt=(0,0)
tags_for_players=['0.png','1.png','3.png','4.png','5.png']
players_tag={}
tem_name=[]
for ii in [(175,78),(605,78),(1046,78),(175,507),(1046,507)]:
    while True:
        ss=random.randint(0,4)
        if ss not in tem_name:
            players_tag[str(ii)]=pygame.image.load(tags_for_players[ss])
            tem_name.append(ss)
            break
player_places={ '2':[(430,78)],
                '3':[(0,78),(871,78)],
                '4':[(0,78),(430,78),(871,78)],
                '5':[(0,78),(871,78),(0,507),(867,507)],
                '6':[(0,78),(430,78),(871,78),(0,507),(867,507)]}
player_name_tag_pos={   '2':[(605,78)],
                        '3':[(175,78),(1046,78)],
                        '4':[(175,78),(605,78),(1046,78)],
                        '5':[(175,78),(1046,78),(175,507),(1046,507)],
                        '6':[(175,78),(605,78),(1046,78),(175,507),(1046,507)]}
##################################################################################
username='bhatt1'
def uno():
    global TURN,current,action,hand_cards_list,draw_break,username,host
    global guno_flag,turnflag,pile_cards_number,num_deck_card,num_of_players,game_states
    global gameloop_flag,winner
    #pos=username
    while True:
        try:
            source =json.loads( requests.get(f'http://127.0.0.1:8000/{host}_game_state_view').text)#.replace("\\",'')
        except:
            network(f'http://127.0.0.1:8000/{host}_game_state_view')
            #prn(requests.get(f'http://127.0.0.1:8000/{host}_game_state_view').text)
        if source['text'].replace("\\",'')=='room close':
            gameloop_flag=True
            break
        if source['winner'].replace("\\",'')!='':
            winner=source['winner'].replace("\\",'')
            prn(winner)
            break
        game_state=json.loads(source['text'].replace("\\",''))
        #prn(game_state)
        game_states=game_state
        #print(yo)
        current=game_state['current']
        #print('current=',current,'}}___UNO')
        try:
            hand_cards_list=game_state[str(username)]['hand_cards']
        except:
            prn(f'uno break can"t find{username}',color='red')
            gameloop_flag=True
            break
        #prn(hand_cards_list,color='pink')
        draw_break=game_state['draw_break']
        guno_flag=game_state[username]['guno']
        turnflag=game_state['turnflag']
        num_deck_card=game_state['num_deck_card']
        pile_cards_number=game_state['pile']
        num_of_players=game_state['num_of_players']

        #print(pos,game_state[str(username)]['turn'])
        if game_state[str(username)]['turn']=='true':
            #prn("\n\n in \n\n")
            post={'action':('',''),'color':'','uno':False,'username':host}
            TURN=True
            #print("post['action']=",action)
            while True:
                if action!=[]:
                    prn('action',color='green')
                    #'''
                    #if action[1][1]=='+4':
                        #input("post['action']=",action[1])#'''
                    post['action']=action[1]
                    #print("uno_post['action']=",action)
                    post['color']=action[1][0]
                    post['uno']=guno_flag
                    action=[]
                    TURN=False
                    #guno_flag=False
                    prn(f'post={post}',color='light_blue')
                    break
                #time.sleep(0.2)


            #send(post)
            #prn(post)
            try:
                requests.get('''http://127.0.0.1:8000/'''+json.dumps(post)+"_myturn")
            except:
                network('''http://127.0.0.1:8000/'''+json.dumps(post)+"_myturn")

            #requests.get('''http://127.0.0.1:8000/'''+json.dumps(post)+"_myturn")#.replace("\\",'')

            #a=int(client.recv(5).decode(str_format))
            #print(pickle.loads(client.recv(2048)))
def sleep():
    time.sleep(5)
    print('uthgya')
def socket():
    thread=threading.Thread(target=uno)
    thread.daemon=True
    thread.start()

##########################################################
def clickcheck(c=''):
    global clickflag
    x=pygame.mouse.get_pressed()
    '''
    if c!='':
        print(x)'''
    if (x==(1,0,0)) and clickflag==0:
        clickflag=2
        #print(c)
        return True
    elif clickflag>0 and clickflag<=2:
        if (x==(1,0,0)) :
            clickflag=2
        clickflag-=1

def clickchecks(c=''):
    #print('in')
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
def hand_cards(events):
    global hand_cards_list,clickedcard,choose_color_flag
    xalpha=0
    if hand_cards_list!=[]:
        a=hand_cards_list

        l=len(a)
        spacing=round(1200/l)
        if spacing>110:
            spacing=110
            xalpha=int(600-(l/2)*110)
        for i in range(l):
            x0=(spacing*i)+xalpha
            if i==clickedcard[0]:#clicked card logic
                y0=651-90
            else:
                y0=651


            x1=x0+110
            y1=y0+143
            color=a[i][0]
            actn=a[i][1]
            if actn=='o':
                actn=10
            elif actn=='r':
                actn=11
            elif actn=='+2':
                actn=12
            elif actn=='+4':
                actn=0
            elif actn=='c':
                actn=1
            else:
                try:
                    actn=int(actn)
                except:
                    print('hands_cards__hands_cards_list=',a)

            screen.blit(ldeck[color][actn],(x0,y0))
            if events!=():
                x,y=events
                '''
                if clickcheck('i')==True:
                    print(clickedcard[1])
                    print((x>x0 and y>y0) , (x<x1 and y<y1) , (x<spacing*(i+1)))
                    print(('x>x0',x>x0 ,'y>y0', y>y0) , ('\nx<x1',x<x1 ,'y<y1', y<y1) )
                    print(x0,y0)
                    print(x,y)
                    print(x1,y1)#'''


                if (x>x0 and y>y0) and (x<x1 and y<y1) and (x<(spacing*(i+1))+xalpha) :

                    #if clickcheck()==True:

                        #print('lol')
                        if clickedcard[0]==i:
                            if a[i][1]=='+4':
                                choose_color_flag=False
                            if a[i][1]=='c':
                                choose_color_flag=False
                                print('hand_cards__yo',a[i])
                            clickedcard=[-1,[]]
                        else:
                            clickedcard[0]=i
                            clickedcard[1]=a[i]
def choose_color(events):
    global color_pt,choose_color_flag,clickedcard,action
    selected_color=''
    if choose_color_flag==True:
        #print('\n\n\n oo bhaimaaro')
        screen.blit(color_selector,color_pt)
        if events!=():
            x,y=events#pygame.mouse.get_pos()
            x0,y0=color_pt
            x1,y1=color_pt[0]+110,color_pt[1]+143
            xp,yp=color_pt[0]+53,color_pt[1]+69
            if (x>x0 and y>y0) and (x<x1 and y<y1):
                if x<xp and y<yp:
                    selected_color='red'
                if x>xp and y<yp:
                    selected_color='yellow'
                if x>xp and y>yp:
                    selected_color='blue'
                if x<xp and y>yp:
                    selected_color='green'
                action=[-1,[selected_color,clickedcard[1][1]]]
                choose_color_flag=False
                clickedcard=[-1,[]]
                #print('\n\n\n\n\naction sent\n\n',action)
                '''
                else:
                    print("\n\n\n\n\clickcheck('choose')=False \n\n")'''

def pile(events):
    global action,pile_cards_number,current,clickedcard,color_pt,choose_color_flag
    x0=552
    y0=530
    xm=0
    ym=0
    if current!=['',''] :
        for i in range(pile_cards_number):
            screen.blit(pile_cards,(x0+xm,y0+ym))
            ym-=2

        actn=current[1]
        if actn=='o':
            actn=10
        elif actn=='r':
            actn=11
        elif actn=='+2':
            actn=12
        elif actn=='+4':
            actn=13
        elif actn=='c':
            actn=14
        else:
            try:
                actn=int(actn)
            except Exception as e:
                print('1)pile_error=',actn,current,str(e))

        try:

            screen.blit(ldeck[current[0]][actn],(x0+xm,y0+ym-143))
        except Exception as e:
            print('pile_error=',actn,current,str(e))
        color_pt=(x0+xm+110,y0+ym-143)##############################


        x1=x0+110
        y1=y0
        y0=y0+ym-147
    else:
        x0,y0=548,376
        x1,y1=674,524

    if events!=():
        x,y=events
        '''
        if clickcheck()==True:
            print(x0,y0)
            print(x,y)
            print(x1,y1)'''
        if (x>x0 and y>y0) and (x<x1 and y<y1) and TURN==True and clickedcard!=[-1, []]:
            print('pile=',clickedcard)
            try:
                if draw_break==False:
                    if current[1]=='+4'and ((current[1]==clickedcard[1][1])):
                        choose_color_flag=True

                        print('action=',action)
                    if current[1]=='+2' and ((current[1]==clickedcard[1][1])):
                        action=clickedcard
                        print('action=',action)

                elif clickedcard[1][1]=='+4':
                    choose_color_flag=True
                elif clickedcard[1][1]=='c':
                    choose_color_flag=True

                    print('\n\n\n\ninnnnnnnn\n\n\n\n')

                elif clickedcard!=[-1,[]] and ((clickedcard[1][0]==current[0] or clickedcard[1][1]==current[1] or current==['',''])) :
                        action=clickedcard
                        print('action=',action)
                        clickedcard=[-1,[]]
                else:
                    print(clickedcard)
            except Exception as e:
                print('pile__clickedcard=',clickedcard,e)

def drawer(events):
    global num_deck_card,action
    x0=400
    y0=390

    xm=0
    ym=0

    for i in range(num_deck_card):
        if i%3==0:
            screen.blit(deckpilecards,(x0+xm,y0+ym))
            xm+=1
            ym-=1

    screen.blit(deckpile,(x0+xm,y0+ym))
    x1=x0+xm+110
    y1=y0+ym+119
    if events!=():
        x,y=events
        if (x>x0 and y>y0) and (x<x1 and y<y1) and TURN==True :
            action=[-1,['draw']]
            print('draw=',clickedcard)



def gunoset(events):
    global guno_flag
    x0=772
    y0=421
    x1,y1=x0+47,y0+47
    if guno_flag==False:
        screen.blit(guno,(x0,y0))
    else:
        screen.blit(gunot,(x0,y0))
    if events!=():
        x,y=events
        if (x>x0 and y>y0) and (x<x1 and y<y1):
            #who_say_gu_no()
            print('guno button')
            if guno_flag==False:
                guno_flag=True
            else:
                guno_flag=False
class guno_back_cover:
    def __init__(self,screen,img,x,y):
        self.img=img
        self.x=x
        self.y=y
        self.screen=screen
        self.screen.blit(self.img,(self.x,self.y))


def kick_from_game(plr):
    global screen,host
    prn('',color='pink')
    cancle_button=button(screen,100,300,text='cancle',h=50,w=200)
    kick_button=button(screen,400,300,text='kick',h=50,w=200)
    running=True
    while running:
        #print('-')
        screen.blit(kick_img,(00,0))
        cancle_button.place()
        kick_button.place()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if cancle_button.event(event):
                break
            if kick_button.event(event):
                leave_game_view(plr,host)
                break
            if event.type == pygame.KEYDOWN:
                if event.key==27:
                    break
            #input('--------')
        else:
            pygame.display.update()
            continue
        break

def leave_from_game():
    global screen,host,username
    prn('',color='pink')
    cancle_button=button(screen,100,300,text='Cancle',h=50,w=200)
    kick_button=button(screen,400,300,text='Leave Game',h=50,w=200)
    running=True
    flg=''
    while running:
        #print('-')
        screen.blit(kick_img,(00,0))
        cancle_button.place()
        kick_button.place()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if cancle_button.event(event):
                break
            if kick_button.event(event):
                leave_game_view(username,host)
                flg='-'
                break
            if event.type == pygame.KEYDOWN:
                if event.key==27:
                    break
            #input('--------')
        else:
            pygame.display.update()
            continue
        break
    if flg=='':
        return False
    else:
        return True

def gunoturn(events):
    global game_states,num_of_players,username,screen,back_img,host
    #prn(game_states)
    if game_states!={}:
        num_of_players=len(game_states['players'])
        a=[]
        x=0
        if num_of_players!=1:
            for i in range(num_of_players):
                if len(game_states['players'])==1:
                    break
                plr=game_states['players'][i]
                #prn(str(num_of_players),player_places[str(num_of_players)],[x])
                if  plr!=username:
                    placeholder_cards=player_places[str(num_of_players)][x]
                    placeholder_name=player_name_tag_pos[str(num_of_players)][x]
                    placeholder_name_img=players_tag[str(placeholder_name)]
                    #prn(f'placeholder_cards={placeholder_cards},placeholder_name={placeholder_name},placeholder_name_img={placeholder_name_img}',color='yellow')
                    l=len(game_states[plr]['hand_cards'])
                    xalpha=0
                    spacing=round(239/l)
                    if spacing >110:
                        spacing=110
                        xalpha=int((placeholder_cards[0]+119)-((l/2)*110))
                    #prn(f'spacing={spacing},xalpha={xalpha}',color='red')
                    pos_is=()
                    for i in range(l):
                        x0=placeholder_cards[0]+(spacing*i)+xalpha
                        y0=placeholder_cards[1]
                        #prn(f"x0={x0},y0={y0}",color='light_blue')
                        if i==l-1:
                            pos_is=(x0+110-(placeholder_cards[0]+xalpha),y0)
                        tema=guno_back_cover(screen,back_img,x0,y0)
                    #prn(f'placeholder_cards[0]={placeholder_cards[0]},xalpha={xalpha},pos_is[0]/2={pos_is[0]/2}')
                    name_tag_pos=(((placeholder_cards[0]+xalpha)+(pos_is[0]/2))-131,placeholder_name[1]-75)
                    #prn(f'pos_is={pos_is}name_tag_pos={name_tag_pos}',color='green')
                    if game_states[plr]['turn']=='true':
                        screen.blit(turn_img,(name_tag_pos[0]-30,name_tag_pos[1]-40))
                    screen.blit(placeholder_name_img,name_tag_pos)
                    #print_text(screen,plr,placeholder_name[0]-100,placeholder_name[1]-50,size=90)
                    size=0
                    #plr='OOOOOOOO'
                    plr_len=len(plr)
                    if plr_len<=4:
                        size=90
                    elif plr_len<=6:
                        size=63
                    else:
                        size=50
                    fontx=pygame.font.Font(None,size)
                    places=fontx.render(plr,True,(0,0,0,150))
                    w=places.get_width()
                    h=places.get_height()
                    screen.blit(places,(
                    name_tag_pos[0]+42+89-(w/2)
                    ,
                    name_tag_pos[1]+14+28-(h/2)))
                    if username==host:
                        if events!=():
                            x,y=events#pygame.mouse.get_pos()

                            x0,y0=name_tag_pos[0]+42,name_tag_pos[1]+14
                            x1,y1=x0+178,y0+54
                            if (x>x0 and y>y0) and (x<x1 and y<y1):
                                kick_from_game(plr)
                    x+=1





def backgroung():
    global bg,turnflag,TURN,username
    #print(turnflag, TURN)
    if turnflag==0 and TURN==True:
        screen.blit(bg[3],(0,0))
    if turnflag==1 and TURN==True:
        screen.blit(bg[2],(0,0))
    if turnflag==0 and TURN==False:
        screen.blit(bg[0],(0,0))
    if turnflag==1 and TURN==False:
        screen.blit(bg[1],(0,0))
def who_say_gu_no():
    #print('inside')
    global game_states,num_of_players,username
    #print(pos,type(pos))
    a=[]
    b=[]#[['turn','no of cards']]
    #print(pos,num_of_players)
    for i in range(num_of_players):
        if str(i) !=username:
            #print('inside --')
            a.append(game_states['players'][i])
    for i in a:
        s=[]
        #print(i)
        s.append(game_states[str(i)]['turn'])
        s.append(len(game_states[str(i)]['hand_cards']))
        s.append(game_states[str(i)]['guno'])
        b.append(s)
    print(b)

def link_thread(link):
    global answer
    while True:
        try:
            a=requests.get(link).text
            prn(a,color='yellow')
            answer=a
            break
        except:
            prn('can not connect to',link,color='blue')
            pass

def network(link):
    global screen,answer
    prn('',color='pink')
    answer=''
    thread=threading.Thread(target=link_thread, args=(link,))
    thread.daemon=True
    thread.start()
    network_v=True
    while network_v:
        #print('-')
        screen.blit(network_view,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                network_v = False
                pygame.quit()
        if answer!='':
            prn('answer=',answer)
            network_v=False
            break
            #input('--------')
        pygame.display.update()



#username='bhatt'
###################################################################################
def gameloop():
    global game_states,turnflag,num_of_players,TURN,guno,gunot,guno_flag,deckpile
    global deckpilecards,num_deck_card,pile_cards,color_selector,pile_cards_number
    global current,clickedcard,clickflag,action,draw_break,choose_color_flag,color_pt,username
    global deck,ldeck,screen,hand_cards_list,bg,gameloop_flag,winner
    socket()
    gameloop_flag=False
    running=True
    winner=''
    flg=''
    while running:#main loop
        event_is=()
        if gameloop_flag:
            flg='you have been kicked'
            break
        if winner!='':
            flg=winner
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key==27:
                    if leave_from_game():
                        running = False
                        break
            if event.type == pygame.MOUSEBUTTONDOWN:
                 event_is=(event.pos)


        screen.fill((100,100,0))#it is leare one
        backgroung()
        #screen.blit(ldeck['black'][1],(random.randint(0,1000),random.randint(100,1000)))
        #yo()
        hand_cards(event_is)
        gunoset(event_is)


        pile(event_is)
        drawer(event_is)
        choose_color(event_is)
        gunoturn(event_is)
        pygame.display.update()

    if flg=='you have been kicked' or flg=='':
        intro_screen(flg)
    else:
        waiting(flg)

        #print(pygame.mouse.get_pos())#give mouse position
        #print(pygame.mouse.get_pressed())#show clicks
        #time.sleep(.03)
        #print(clickedcard[1])


class entry:
    def __init__(self,screen,x,y,w=100,h=10,text='',
                 color=(0,0,0),bg_color=(200,200,200),
                 font=None,boder=1,password=False,outline=(0,0,0)):
        self.screen=screen

        self.text=text
        self.x=x
        self.y=y
        self.active=True
        #self.event=event
        self.w=int(len(self.text)*(h/2))#w
        self.h=h
        self.color=color
        self.bg_color=bg_color
        self.font=font
        self.boder=boder
        self.w=100
        self.password=password
        self.outline=outline
        #self.places()
    def place(self):

        self.box=pygame.draw.rect(self.screen,(0,0,0),(self.x-(self.boder),self.y-(self.boder),self.w+(self.boder*2),self.h+(self.boder*2)),)
        #print('self.bg_color=',self.bg_color)
        pygame.draw.rect(self.screen,self.bg_color,
                         (self.x,self.y,self.w,self.h)
                         )
        self.fontx=pygame.font.Font(self.font,self.h)
        if self.password==True:
            self.places=self.fontx.render('*'*len(self.text),True,self.color)
        else:
            self.places=self.fontx.render(self.text,True,self.color)
        self.screen.blit(self.places,(self.x,self.y))
        self.w=max(300,self.places.get_width()+25)
    def event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if event.pos[0]>self.x and event.pos[1]>self.y and event.pos[0]<self.x+self.w and event.pos[1]<self.y+self.h:
                self.active = True
            else:
                self.active = False
            if self.active==False:
                #print('in')
                self.bg_color=(200,200,200)
            else:
                self.bg_color=(255,255,255)
            self.place()
            #print('lol',self.bg_color)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.place()


    def get(self):
        return str(self.text)
class button:
    def __init__(self,screen,x,y,text='button',color=(255,255,255),

                 w=50,h=10,text_color=(0,0,0),
                 ):
        self.screen=screen
        self.text=text
        self.x=x
        self.y=y
        self.active=False
        self.w=w#w
        self.given_w=w
        self.h=h
        self.color=color
        self.temcolor=color
        self.text_color=text_color

    def place(self):
        pygame.draw.rect(self.screen,
                         (0,0,0),
                         (self.x+2,self.y+2
                          ,self.w,self.h))
        pygame.draw.rect(self.screen,
                         self.color,
                         (self.x,self.y
                          ,self.w,self.h))
        self.fontx=pygame.font.Font(None,self.h)
        self.places=self.fontx.render(self.text,True,self.text_color)
        self.screen.blit(self.places,(self.x+((self.w/2)-(self.places.get_width()/2)),
                                      self.y+((self.h/2)-(self.places.get_height()/2))))
        self.w=max(self.places.get_width()+25,self.given_w)



    def event(self,event):
        pos=pygame.mouse.get_pos()
        if (pos[0]>self.x and
        pos[1]>self.y and
        pos[0]<self.x+self.w and
        pos[1]<self.y+self.h):
            if self.active:
                self.color=(min(self.color[0]+20,255),min(self.color[1]+20,255),min(self.color[2]+20,255),)
                #(max(self.color[0]-self.presscolor),)
                #print('self.color=',self.color)
                self.active=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.color=(max(self.color[0]-40,0),max(self.color[1]-40,0),max(self.color[2]-40,0))
                return True
        else:
            self.active=True
            self.color=self.temcolor

        self.place()
class print_button:
    def __init__(self,screen,x,y,text='button',color=(255,255,255),

                 w=50,h=10,text_color=(0,0,0),
                 ):
        self.screen=screen
        self.text=text
        self.x=x
        self.y=y
        self.active=False
        self.w=w#w
        self.given_w=w
        self.h=h
        self.color=color
        self.temcolor=color
        self.text_color=text_color
        pygame.draw.rect(self.screen,
                         (0,0,0),
                         (self.x+2,self.y+2
                          ,self.w,self.h))
        pygame.draw.rect(self.screen,
                         self.color,
                         (self.x,self.y
                          ,self.w,self.h))
        self.fontx=pygame.font.Font(None,self.h)
        self.places=self.fontx.render(self.text,True,self.text_color)
        self.screen.blit(self.places,(self.x+((self.w/2)-(self.places.get_width()/2)),
                                      self.y+((self.h/2)-(self.places.get_height()/2))))
        self.w=max(self.places.get_width()+25,self.given_w)



    def event(self,event):
        pos=pygame.mouse.get_pos()
        if (pos[0]>self.x and
        pos[1]>self.y and
        pos[0]<self.x+self.w and
        pos[1]<self.y+self.h):
            if self.active:
                self.color=(min(self.color[0]+20,255),min(self.color[1]+20,255),min(self.color[2]+20,255),)
                #(max(self.color[0]-self.presscolor),)
                #print('self.color=',self.color)
                self.active=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.color=(max(self.color[0]-40,0),max(self.color[1]-40,0),max(self.color[2]-40,0))
                return True
        else:
            self.active=True
            self.color=self.temcolor
class text:
    def __init__(self,screen,text,x,y,font=None,size=10,color=(0,0,0)):
        self.screen=screen
        self.text=text
        self.x=x
        self.y=y
        self.size=size
        self.color=color
        self.font=font
    def place(self):
        self.fontx=pygame.font.Font(None,self.size)
        self.places=self.fontx.render(self.text,True,self.color)
        self.screen.blit(self.places,(self.x,self.y))
class print_text:
    def __init__(self,screen,text,x,y,font=None,size=10,color=(0,0,0)):
        self.screen=screen
        self.text=text
        self.x=x
        self.y=y
        self.size=size
        self.color=color
        self.font=font
        self.fontx=pygame.font.Font(None,self.size)
        self.places=self.fontx.render(self.text,True,self.color)
        self.screen.blit(self.places,(self.x,self.y))
def login():
    global screen,username
    username_entry=entry(screen,100,100,h=50)
    password_entry=entry(screen,100,200,h=50,password=True)
    login_button=button(screen,100,300,text='LOGIN',h=50,w=200)
    running=True
    while running:#main loop
        screen.fill((255,255,255))
        username_entry.place()
        password_entry.place()
        login_button.place()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            username_entry.event(event)
            password_entry.event(event)
            if login_button.event(event):
                #print('login',username_entry.get(),password_entry.get())
                responce=login_view(username_entry.get(),password_entry.get())
                #print(responce,type(responce))
                prn(responce,color='light_blue')
                if responce=='username':
                    username_entry.bg_color=(181,119,119)
                if responce=='password':
                    password_entry.bg_color=(181,119,119)
                if responce['text']!='':
                    username=username_entry.get()
                    break
                if responce['text']=='':
                    username_entry.bg_color=(181,119,119)
                    password_entry.bg_color=(181,119,119)
            #username='bhatt'
            break
                #quit()
        else:
            pygame.display.update()
            continue
        break

    #gameloop()
    intro_screen()
def intro_screen(msg=''):
    global screen,username,host
    #prn('in')

    create_room_button=button(screen,10,10,text='Create Room',h=50)
    join_room_button=button(screen,100,100,text='Join Room',h=50)
    room_name_entry=entry(screen,100,300,h=50)
    heading=text(screen,f'WELCOM {username}',00,00,size=100)
    error_text=text(screen,'--',300,400,size=50,color=(255,0,0))
    running=True
    flag=''

    while running:#main loop
        screen.fill((255,255,150))
        heading.place()
        error_text.place()
        create_room_button.place()
        join_room_button.place()
        room_name_entry.place()
        if msg!='':
            #prn(msg)
            print_text(screen,msg,300,400,size=100,color=(0,255,50))



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            room_name_entry.event(event)
            if create_room_button.event(event):
                #prn('create_room')
                flag='create_room'
                break
            if join_room_button.event(event):
                #prn('join_room')
                tem_host=room_name_entry.get()
                a=join_room_view(username,tem_host)['text']
                print(a)

                if a=='join done':
                    flag='join_room'
                    host=tem_host
                    break
                else:
                    room_name_entry.bg_color=(181,119,119)
                    error_text.text=a
        else:
            pygame.display.update()
            continue
        break
    if flag=='create_room':
        create_room_view(username)
        host=username
        waiting()
    if flag=='join_room':
        waiting()


def waiting(win=''):
    global screen,username,host
    #prn(username,host)
    start_game_button=button(screen,300,300,text='START',h=50)
    leave_button=button(screen,430,300,text='leave',h=50)
    running=True
    flag=''
    msg=''
    while running:#main loop
        list_button=[]
        screen.fill((255,255,255))
        print_text(screen,'waiting for players...',0,0,size=100)
        main_responce=waiting_view(host)
        if main_responce['text']=='game start':
            gameloop()
            prn('start')

        responce=main_responce['players']
        #prn(responce)
        if responce==[]:
            leave_waiting_view(username,host)
            flag='leave'
            msg=f"host {username} cancle the room"
            break
        #prn(responce)
        if host==username:
            start_game_button.place()

            for i in range(len(responce)):
                list_button.append(
                print_button(screen,350,100+(100*i),text='kick',w=100,h=50,color=(255,0,0))
                )
        leave_button.place()
        for i in range(len(responce)):
            print_text(screen,f"{i+1}){responce[i]}",100,100+(100*i),size=70)


        if win!='':
            print_text(screen,f"Last game winner is {win}",400,400+(100*i),size=70)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if leave_button.event(event):
                leave_waiting_view(username,host)
                flag='leave'
                break

            if  host==username:
                if start_game_button.event(event):
                    start_game(username)
                    flag='start_game'
                    break
                for i in range(len(list_button)):
                    if list_button[i].event(event):
                        leave_waiting_view(responce[i],host)


        else:
            pygame.display.update()
            continue
        break
    if flag=='leave':
        intro_screen(msg)
    if flag=='start_game':
        gameloop()

#username='bhatt'
intro_screen()
#waiting()
#login()
#gameloop()
