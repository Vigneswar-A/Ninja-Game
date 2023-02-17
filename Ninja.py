import pygame,sys,os
from pygame.constants import K_ESCAPE,K_RSHIFT, K_SPACE, TIMER_RESOLUTION,K_a, K_d, K_x
pygame.init()
resources=[]
def r(relative_path):
    
    try:
        base_path=sys._MEIPASS
    except Exception:
        base_path=os.path.abspath(".")
    resources.append(f"('{relative_path}','{base_path}')")
    return os.path.join(base_path,relative_path)

#Variables
Player="G"
Width=1500
Height=750
Jump_Power=150
Speed=5
FPS=60
APS=0.3
Tile_Size=(50,50)
Player_Scale=1/5
Gravity=15
Jump_CoolDown=1000
Kunai_Speed=30
Zombie_Speed=2
Kill_Distance=50
Detection_Range=300
Current_Map=1
Zombie_Health=100
Player_Health=500
Kunai_Damage=5
pygame.mouse.set_visible(False)
pygame.display.set_caption('Ninja Fighting Simulator!')

#Sound Effects
Jump=pygame.mixer.Sound(r("SoundEffects/Jump.wav"))
KunaiSound=pygame.mixer.Sound(r("SoundEffects/Kunai.wav"))
FightSound=pygame.mixer.Sound(r("SoundEffects/PlayerBAttack.wav"))
Zombie=pygame.mixer.Sound(r("SoundEffects/Zombie.wav"))

#Clock
Clock=pygame.time.Clock()

#Image Functions
def Load(image,size):
    Image=pygame.transform.scale(pygame.image.load(r(image)),(size[0],size[1]))
    return Image
def Load_Scale(image,size):
    Image=pygame.image.load(r(image))
    Width=Image.get_width()
    Height=Image.get_height()
    return pygame.transform.scale(Image,(int(Width*size),int(Height*size)))
def Flip(image):
    return pygame.transform.flip(image,True,False)

#Screen
Screen=pygame.display.set_mode((Width,Height))
BackGround=Load(r("BG/BG.png"),(Width,Height))

Tile_Rect_List=[]
Zombie_Spawn_List=[]
Decoration_List=[]
#Class World
class WORLD(pygame.sprite.Sprite):
    Tiles=[]
    for i in range(1,19,1):
        Tiles.append(Load(f"Tiles/{i}.png",Tile_Size))
    
    Decorations=[]
    Decorations.append(Load("Object/Bush(1).png",Tile_Size))
    Decorations.append(Load("Object/Bush(2).png",Tile_Size))
    Decorations.append(Load("Object/Bush(3).png",Tile_Size))
    Decorations.append(Load("Object/Bush(4).png",Tile_Size))
    Decorations.append(Load("Object/Crate.png",Tile_Size))
    Decorations.append(Load("Object/Mushroom_1.png",Tile_Size))
    Decorations.append(Load("Object/Mushroom_2.png",Tile_Size))
    Decorations.append(Load("Object/Sign_1.png",Tile_Size))
    Decorations.append(Load("Object/Sign_2.png",Tile_Size))
    Decorations.append(Load("Object/Stone.png",Tile_Size))
    Decorations.append(Load("Object/Tree_1.png",Tile_Size))
    Decorations.append(Load("Object/Tree_2.png",Tile_Size))
    Decorations.append(Load("Object/Tree_3.png",Tile_Size))
    
    Map_1=[
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"d1",0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,2,3,0,0,0,0,13,14,15,0,0,0,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,0,0,0,1,2,5,5,5,0,0,"z",0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,1,2,5,5,5,5,5,0,0,0,0,0,0,0,0,0,1,2,3,0,0,0,0,0],
    [5,0,0,"d11",0,0,5,5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0],
    [5,2,2,2,2,2,5,5,5,5,5,5,5,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    ]
    Map_2=[
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,"z",0,0,0,0,0,"z",0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,0,"d9",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,2,2,2,2,2,5,5,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    ]
    Map_3=[
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,6,0,0,0,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,6,6,0,0,0,0,"z",0,0,0,0,0],
    [5,0,0,0,6,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,2,2,2,2,2,2,2,2,2,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [5,5,5,5,5,5,5,5,5,5,0,0,0,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    [5,5,5,5,5,5,5,5,5,5,0,0,0,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    ]
    Map_4=[
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,0,"d9",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,2,2,2,2,2,5,5,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    ]
    Map_5=[
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,0,"d9",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,2,2,2,2,2,5,5,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    ]

    World=[Map_1,Map_2,Map_3,Map_4,Map_5]
    
    def __init__(self,index,position):
        super(WORLD,self).__init__()
        self.images=WORLD.Tiles
        self.image=self.images[index]
        self.rect=self.image.get_rect()
        self.rect.topleft=position

    def Build(map_no):
        World_Group=pygame.sprite.Group()
        World_Group.remove()
        Tile_Rect_List.clear()
        Decoration_List.clear()
        y=0
        for Column in WORLD.World[map_no-1]:
            x=0
            for Tile in Column:
                if Tile!=0 and Tile!="z" and str(Tile)[0]!="d":
                    World_Group.add(WORLD(int(Tile)-1,(x,y)))
                    Tile_Rect_List.append(pygame.Rect((x,y),Tile_Size))
                elif str(Tile)=="z":
                    Zombie_Spawn_List.append((x,y))
                elif str(Tile)[0]=="d":
                    Decoration_List.append((int(str(Tile)[1:len(Tile)]),x,y))
                x+=50
            y+=50     
        return World_Group

#Class Player
class PLAYER(pygame.sprite.Sprite):
    #Class Animations
    class ANIMATIONS():
        def __init__(self,name,list,left_list):
            self.name=name
            self.right_list=list
            self.left_list=left_list

    #Image Lists
    Attack=[]
    Dead=[]
    Glide=[]
    Idle=[]
    Jump=[]
    Jump_Attack=[]
    Run=[]
    Throw=[]
    Attack_Left=[]
    Dead_Left=[]
    Glide_Left=[]
    Idle_Left=[]
    Jump_Left=[]
    Jump_Attack_Left=[]
    Run_Left=[]
    Throw_Left=[]
    Jump_Throw=[]
    Jump_Throw_Left=[]

    #Loading Images
    Animations_List=[ANIMATIONS("Attack",Attack,Attack_Left),ANIMATIONS("Dead",Dead,Dead_Left),ANIMATIONS("Idle",Idle,Idle_Left),ANIMATIONS("Jump",Jump,Jump_Left),ANIMATIONS("Jump_Attack",Jump_Attack,Jump_Attack_Left),ANIMATIONS("Run",Run,Run_Left),ANIMATIONS("Throw",Throw,Throw_Left),ANIMATIONS("Jump_Throw",Jump_Throw,Jump_Throw_Left)]
    for Animation in Animations_List:
        for i in range(10):
            try:
                Animation.right_list.append(Load_Scale(f"Player{Player}/{Animation.name}__00{i}.png",Player_Scale))
                Animation.left_list.append(Flip(Load_Scale(f"Player{Player}/{Animation.name}__00{i}.png",Player_Scale)))
                
            except:
                Animation.right_list.append(Load_Scale(f"Player{Player}/{Animation.name}__00{i}.png",Player_Scale))
                Animation.left_list.append(Flip(Load_Scale(f"Player{Player}/{Animation.name}__00{i}.png",Player_Scale)))


    def __init__(self):
        super(PLAYER,self).__init__()
        self.images=PLAYER.Idle
        self.index=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.topleft=(300,300)
        self.velx=0
        self.vely=0
        self.accx=0
        self.accy=0
        self.Left=False
        self.Jumped=True
        self.Press_Time=pygame.time.get_ticks()
        self.Attack=False
        self.Throw=False
        self.ThrowEnded=True
        self.Kunai_CoolDown=False
        self.Health=Player_Health
        self.Damage=False
        self.Dead=False
        self.APS=APS

    def Movements(self):
        #Default
        self.velx=0
        self.vely=0
        self.Attack=False
        self.APS=APS

        if self.Jumped==False and self.ThrowEnded==True:
            self.images=PLAYER.Idle
            if self.Left==True and self.ThrowEnded==True:
                self.images=PLAYER.Idle_Left

        #Gravity:
        self.accy=Gravity
            
        if self.vely<0:
            self.images=PLAYER.Jump
            if self.Left==True:
                self.images=PLAYER.Jump_Left

        #Controls
        events=pygame.event.get()
        move=pygame.key.get_pressed()  
        for event in events:
            if event.type==pygame.QUIT:
                sys.exit()

        if move[K_d] and self.ThrowEnded==True:
            self.velx=Speed
            self.Left=False
            if self.Jumped==False:
                self.images=PLAYER.Run
        elif move[K_a] and self.ThrowEnded==True:
            self.velx=-Speed
            self.Left=True
            if self.Jumped==False:
                self.images=PLAYER.Run_Left

        if move[K_SPACE] and self.Jumped==False:
                Jump.play()
                self.images=PLAYER.Jump
                if self.Left==True:
                    self.images=self.Jump_Left
                self.vely-=Jump_Power
                self.Jumped=True
                self.Press_Time=pygame.time.get_ticks()

        if move[K_RSHIFT] and self.Jumped==True and self.ThrowEnded==True:
            self.Attack=True
            self.images=PLAYER.Jump_Attack
            if self.Left==True:
                self.images=PLAYER.Jump_Attack_Left
                self.Attack=True
        
        elif move[K_RSHIFT] and self.ThrowEnded==True:
            self.Attack=True
            self.images=PLAYER.Attack
            self.velx=0
            if self.Left==True:
                self.Attack=True
                self.images=PLAYER.Attack_Left

        if move[K_x] and self.ThrowEnded==True and self.Kunai_CoolDown==False:
            KunaiSound.play()
            self.Throw=True
            self.velx=0
            self.images=PLAYER.Throw
            if self.Left==True:
                self.images=PLAYER.Throw_Left
        
        if move[K_x] and self.ThrowEnded==True and self.Jumped==True and self.Kunai_CoolDown==False:
            KunaiSound.play()
            self.Throw=True
            self.velx=0
            self.images=PLAYER.Jump_Throw
            if self.Left==True:
                self.images=PLAYER.Jump_Throw_Left
        
        if move[K_ESCAPE]:
            exit()
        
        
        #Final Velocity
        self.vely=self.vely+0.5*self.accy
        self.velx=self.velx+0.5*self.accx

        #Collision
        for Rect in Tile_Rect_List:
            if Rect.colliderect(self.rect.x+self.velx,self.rect.y,self.rect.width,self.rect.height):
                if self.velx>=0:
                    self.velx=Rect.left-self.rect.right
                elif self.velx<0:
                    self.velx=self.rect.left-Rect.right
            if Rect.colliderect((self.rect.x,self.rect.y+self.vely),(self.rect.width,self.rect.height)):
                if self.vely<0:
                    self.vely=Rect.bottom-self.rect.top
                    self.accy=0
                elif self.vely>=0:
                    self.vely=Rect.top-self.rect.bottom
                    self.accy=0
        
        #Death
        if self.Damage==True:
            self.APS=0.1
            self.Health-=1
            self.images=[PLAYER.Dead[0],PLAYER.Dead[1]]
            if self.Left==True:
                self.Health-=1
                self.images=[PLAYER.Dead_Left[0],PLAYER.Dead_Left[1]]
                self.APS=0.01

        if self.Health==0:
            self.Dead=True
            self.image=PLAYER.Dead[9]
        if self.Dead:
            sys.exit()
                
        #Update
        if self.Dead==False:
            self.rect.topleft=(self.rect.x+self.velx,self.rect.y+self.vely)
            self.index+=self.APS
            try:
                self.image=self.images[round(self.index)]
            except:
                self.index=0
        
        #Jump CoolDown:
        if self.Jumped==True:
            if pygame.time.get_ticks()-self.Press_Time>=Jump_CoolDown:
                self.Jumped=False

Player_Sprite=PLAYER()
Player_Group=pygame.sprite.Group(Player_Sprite)

#Class Kunai:
class KUNAI(pygame.sprite.Sprite):
    Kunai_Left=Flip(Load_Scale((f"Player{Player}/Kunai.png"),1/4))
    Kunai=Load_Scale((f"Player{Player}/Kunai.png"),1/4)
    def __init__(self):
        super(KUNAI,self).__init__()
        self.image=KUNAI.Kunai
        self.rect=self.image.get_rect()
        self.rect.bottomright=(0,0)
        self.Left=False
        self.Movement=True

    def Movements(self):
        if Player_Sprite.Throw==True:
            if Player_Sprite.Left==False:
                self.image=KUNAI.Kunai
                self.rect.midleft=Player_Sprite.rect.midright
                self.Left=False
                self.Movement=True
                Player_Sprite.Throw=False
                Player_Sprite.ThrowEnded=False
                Player_Sprite.Kunai_CoolDown=True
            elif Player_Sprite.Left==True:
                self.image=KUNAI.Kunai_Left
                self.rect.midright=Player_Sprite.rect.midleft
                self.Left=True
                self.Movement=True
                Player_Sprite.Throw=False
                Player_Sprite.ThrowEnded=False
                Player_Sprite.Kunai_CoolDown=True
        
        if self.Movement==True:
            if self.Left==False:
                self.rect.x+=Kunai_Speed
            elif self.Left==True:
                self.rect.x-=Kunai_Speed
        
        if self.Left==True:
            if self.rect.x<0-self.image.get_width():
                Player_Sprite.ThrowEnded=True
            if self.rect.x<0-Kunai_Speed*100:
                self.Movement=False
                Player_Sprite.Kunai_CoolDown=False
        elif self.Left==False:
            if self.rect.x>Width+self.image.get_width():
                Player_Sprite.ThrowEnded=True
            if self.rect.x>Width+Kunai_Speed*100:
                self.Movement=False
                Player_Sprite.Kunai_CoolDown=False

        
                
Kunai_Sprite=KUNAI()
Kunai_Group=pygame.sprite.Group(Kunai_Sprite)
    
#Class Zombie:
class ZOMBIE(pygame.sprite.Sprite):

    #Class Animations
    class ANIMATIONS():
        def __init__(self,name,list,left_list,max_index):
            self.name=name
            self.right_list=list
            self.left_list=left_list
            self.max_index=max_index

    #Image Lists
    Idle=[]
    Idle_Left=[]
    Walk=[]
    Walk_Left=[]
    Attack=[]
    Attack_Left=[]
    Dead=[]
    Dead_Left=[]

    Animations_List=[ANIMATIONS("Attack",Attack,Attack_Left,9),ANIMATIONS("Dead",Dead,Dead_Left,13),ANIMATIONS("Walk",Walk,Walk_Left,11),ANIMATIONS("Idle",Idle,Idle_Left,16)]
    for Animation in Animations_List:
        for i in range(1,Animation.max_index):
                Animation.right_list.append(Load_Scale(f"Enemy{Player}/{Animation.name}({i}).png",Player_Scale))
                Animation.left_list.append(Flip(Load_Scale(f"Enemy{Player}/{Animation.name}({i}).png",Player_Scale)))

    def __init__(self,Spawn):
        super(ZOMBIE,self).__init__()
        self.images=ZOMBIE.Idle
        self.index=0
        self.image=self.images[round(self.index)]
        self.rect=self.image.get_rect()
        self.rect.topleft=Spawn
        self.Left=False
        self.velx=0
        self.vely=0
        self.accx=0
        self.accy=0
        self.Dead=False
        self.Health=Zombie_Health
    
    def Movements(self):
        self.velx=0
        self.vely=0
        self.images=ZOMBIE.Idle

        if self.Left==True:
            self.images=ZOMBIE.Idle_Left
      
        #Gravity
        self.accy=Gravity
        if self.Dead==False:
            if Player_Sprite.rect.x<self.rect.x:
                if self.rect.x-Player_Sprite.rect.x<Detection_Range and self.rect.y-Player_Sprite.rect.y<100:
                    if self.rect.x-Player_Sprite.rect.x>Kill_Distance:
                        self.images=ZOMBIE.Walk_Left
                        self.velx-=Zombie_Speed
                        self.Left=True
                    elif self.rect.x-Player_Sprite.rect.x<=Kill_Distance:
                        Zombie.play(0)
                        self.images=ZOMBIE.Attack_Left
                        self.velx==0

            if self.rect.x<Player_Sprite.rect.x:
                if Player_Sprite.rect.x-self.rect.x<Detection_Range:                 
                    if Player_Sprite.rect.x-self.rect.x>Kill_Distance:
                        self.images=ZOMBIE.Walk
                        self.velx+=Zombie_Speed
                        self.Left=False
                    elif Player_Sprite.rect.x-self.rect.x<=Kill_Distance:
                        Zombie.play(0)
                        self.images=ZOMBIE.Attack
                        self.velx=0
    
        #Final Velocity
        self.vely=self.vely+0.5*self.accy
        self.velx=self.velx+0.5*self.accx


        #Collision
        for Rect in Tile_Rect_List:
            if Rect.colliderect(self.rect.x+self.velx,self.rect.y,self.rect.width,self.rect.height):
                if self.velx>=0:
                    self.velx=Rect.left-self.rect.right
                    self.images=ZOMBIE.Idle
                elif self.velx<0:
                    self.velx=self.rect.left-Rect.right
                    self.images=ZOMBIE.Idle_Left
            if Rect.colliderect((self.rect.x,self.rect.y+self.vely),(self.rect.width,self.rect.height)):
                if self.vely<0:
                    self.vely=Rect.bottom-self.rect.top
                    self.accy=0
                elif self.vely>=0:
                    self.vely=Rect.top-self.rect.bottom
                    self.accy=0

        #Death
        for zombie in Zombies_List:
            if pygame.sprite.spritecollide(zombie,Player_Group,0):
                if Player_Sprite.Attack==True:
                    Player_Sprite.Damage=False
                    if zombie.Left==False:
                        zombie.images=[ZOMBIE.Dead[0],ZOMBIE.Dead[1],ZOMBIE.Dead[2],ZOMBIE.Dead[3]]
                        zombie.Health-=1
                        if zombie.Health==0:
                            zombie.Dead=True                 
                    elif zombie.Left==True:
                        zombie.images=[ZOMBIE.Dead_Left[0],ZOMBIE.Dead_Left[1],ZOMBIE.Dead_Left[2],ZOMBIE.Dead_Left[3]]
                        zombie.Health-=1
                        if zombie.Health==0:
                            zombie.Dead=True
                elif Player_Sprite.Attack==False and zombie.Dead==False:
                    Player_Sprite.Damage=True
            else:
                Player_Sprite.Damage=False
                    

            if pygame.sprite.spritecollide(zombie,Kunai_Group,0):
                if zombie.Left==False:
                    zombie.images=[ZOMBIE.Dead[0],ZOMBIE.Dead[1],ZOMBIE.Dead[2],ZOMBIE.Dead[3]]
                    zombie.Health-=Kunai_Damage
                    if zombie.Health==0:
                        zombie.Dead=True                   
                elif zombie.Left==True:
                    zombie.images=[ZOMBIE.Dead_Left[0],ZOMBIE.Dead_Left[1],ZOMBIE.Dead_Left[2],ZOMBIE.Dead_Left[3]]
                    zombie.Health-=Kunai_Damage
                    if zombie.Health==0:
                        zombie.Dead=True
                                    
        #Update
        self.index+=APS
        self.rect.topleft=(self.rect.x+self.velx,self.rect.y+self.vely)    
        try:
            self.image=self.images[round(self.index)]
        except:
            self.index=0
        if self.Dead==True:
            self.image=ZOMBIE.Dead[11]
            if self.Left==True:
                self.image=ZOMBIE.Dead_Left[11]
    
class DECORATIONS(pygame.sprite.Sprite):
    def __init__(self,index,position):
        super(DECORATIONS,self).__init__()
        self.images=WORLD.Decorations
        self.image=self.images[index]
        if index>10:
            self.image=pygame.image.load(r("Object/Tree_2.png"))
            self.rect=self.image.get_rect()
            self.rect.midbottom=(position[0],position[1]+50)
        else:
            self.rect=self.image.get_rect()
            self.rect.topleft=position
                     
World_Group=WORLD.Build(Current_Map)  
Decorations_Group=pygame.sprite.Group()
for Decor in Decoration_List:
    Decorations_Group.add(DECORATIONS(Decor[0],(Decor[1],Decor[2])))
Zombie_Group=pygame.sprite.Group()
Zombies_List=[]
for Zombie_Spawn in Zombie_Spawn_List:
    zombie=ZOMBIE(Zombie_Spawn)
    Zombies_List.append(zombie)
    Zombie_Group.add(zombie)
    
while 1:
    if Player_Sprite.rect.x>Width and Current_Map<len(WORLD.World):
        Player_Sprite.rect.x=200
        Player_Sprite.rect.y=500
        Zombie_Group.empty()
        Decorations_Group.empty()
        Zombies_List.clear()
        Zombie_Spawn_List.clear()
        Current_Map+=1
        World_Group=WORLD.Build(Current_Map)
        for Zombie_Spawn in Zombie_Spawn_List:
            zombie=ZOMBIE(Zombie_Spawn)
            Zombies_List.append(zombie)
            Zombie_Group.add(zombie)
        for Decor in Decoration_List:
            Decorations_Group.add(DECORATIONS(Decor[0],(Decor[1],Decor[2])))

    if Player_Sprite.rect.y>Height:
        Player_Sprite.Dead=True

    Clock.tick(FPS)
    Screen.blit(BackGround,(0,0))
    World_Group.draw(Screen)
    Decorations_Group.draw(Screen)
    Zombie_Group.draw(Screen)
    for zombie in Zombies_List:
        zombie.Movements()
    Player_Group.draw(Screen)
    Player_Sprite.Movements()
    Kunai_Group.draw(Screen)
    Kunai_Sprite.Movements()
    pygame.display.flip()
    if Player_Sprite.Dead==True:
        pygame.time.delay(500)
        exit()