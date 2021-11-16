# 1 - Import các thư viện
import pygame
import math
import random
pygame.mixer.init()
from pygame.locals import *

# 2 - Khởi tạo game
pygame.init() #Khởi tạo tất cả các modul cho pygame
width, height = 640, 480 #tạo biến chiều dài và chiều rộng 
screen=pygame.display.set_mode((width, height)) #Khai báo màn hình với chiều rộng vàchiều dài
keys = [False, False, False, False]
playerpos=[100,100] #tọa độ người chơi ban đầu
acc=[0,0] #danh sách số mũi tên bắn trùng và đã bắn
arrows=[] #danh sách mũi tên
badtimer=100 #Khởi tạo biến thời gian
badtimer1=0
badguys=[[640,100]] #tọa độ lửng mật
healthvalue=194 #Khởi tạo giá trị thanh sức khỏe
# 3 - Chèn hình ảnh vào khung game
player = pygame.image.load("image/resources/images/dude.png") # nhân vật
grass = pygame.image.load("image/resources/images/grass.png") # nền
castle = pygame.image.load("image/resources/images/castle.png") # thành trì
arrow = pygame.image.load("image/resources/images/bullet.png") # mũi tên
badguyimg1 = pygame.image.load("image/resources/images/badguy.png") # lửng mật
badguyimg=badguyimg1
healthbar = pygame.image.load("image/resources/images/healthbar.png") # thanh sức khỏe(hp)
health = pygame.image.load("image/resources/images/health.png") # sức khỏe
gameover = pygame.image.load("image/resources/images/gameover.png") # nền thua
youwin = pygame.image.load("image/resources/images/youwin.png") # nền thắng
# 3.1 - Chèn nhạc
hit = pygame.mixer.Sound("image/resources/audio/explode.wav") # nhạc lúc bắn nhau
enemy = pygame.mixer.Sound("image/resources/audio/enemy.wav") # nhạc của lửng mật
shoot = pygame.mixer.Sound("image/resources/audio/shoot.wav") # nhạc bắn tên
hit.set_volume(0.05) # đặt âm lượng cho nhạc
enemy.set_volume(0.05) # đặt âm lượng cho nhạc
shoot.set_volume(0.05) # đặt âm lượng cho nhạc
pygame.mixer.music.load('image/resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0) # bật nhạc mọi lúc
pygame.mixer.music.set_volume(0.25)
# 4 - Qua trình lặp lại trong game
running = 1
exitcode = 0
while running: #Trong khi chạy
    badtimer-=1
    # 5 - làm mới màn hình trước khi chơi
    screen.fill(0)
    # 6 - vẽ/chèn các phần tử vào màn hình
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100)) # chèn hình nền vào màn hình ở các tọa độ
    screen.blit(castle,(0,30)) # chèn thành trì vào màn hình 
    screen.blit(castle,(0,135)) # chèn thành trì vào màn hình
    screen.blit(castle,(0,240)) # chèn thành trì vào màn hình
    screen.blit(castle,(0,345 )) # chèn thành trì vào màn hình
    # 6.1 - Đặt vị trí cho người chơi
    position = pygame.mouse.get_pos() # Lấy vị trí con trỏ chuột
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26)) #trả về giá trị tan của tọa độ y/ tọa độ x
    playerrot = pygame.transform.rotate(player, 360-angle*57.29) # Xoay hình ảnh người chơi với góc quay dựa vào con trỏ chuột
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2) #Tọa độ sau khi xoay và chuyển động
    screen.blit(playerrot, playerpos1) #Cập nhật tọa độ mới
    # 6.2 - Vẽ mũi tên
    for bullet in arrows:
        index=0
        velx=math.cos(bullet[0])*10 #trả về giá trị cos tọa độ của mũi tên
        vely=math.sin(bullet[0])*10 #trả về giá trị sin tọa độ của mũi tên
        bullet[1]+=velx #tạo chuyển động cho mũi tên bằng cách thay đổi tọa độ
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480: #xét điều kiện nếu chạm khung hình sẽ biến mất
            arrows.pop(index)
        index+=1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29) # đường mũi tên bay theo hướng chỉ định của con trỏ chuột
            screen.blit(arrow1, (projectile[1], projectile[2])) # Chèn mũi tên sau khi thay đổi vào màn hình
    # 6.3 - Vẽ con lửng mật
    if badtimer==0:
        badguys.append([640, random.randint(50,430)]) #Thêm một con lửng mật vào danh sách 
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index=0
    for badguy in badguys:
        if badguy[0]<-64: # điều kiện nếu lửng mật đi đến thành trì thì xóa bỏ
            badguys.pop(index)
        badguy[0]-=7
        # 6.3.1 - Tấn công thành trì
        badrect=pygame.Rect(badguyimg.get_rect()) #Khởi tạo biến về tọa độ lửng mật
        badrect.top=badguy[1] 
        badrect.left=badguy[0]
        if badrect.left<64: #điều kiện nếu con lửng đến thành trì
            
            hit.play() # nhạc hoạt động
            healthvalue -= random.randint(5,20) # thanh sức khỏe trừ giá trị random từ 5-20
            badguys.pop(index) # xóa con lửng
        #6.3.2 - Kiểm Tra va chạm của mũi tên
        index1=0
        for bullet in arrows:
            bullrect=pygame.Rect(arrow.get_rect()) # Khởi tạo về tọa độ của mũi tên
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            if badrect.colliderect(bullrect): #điều kiện mũi tên va chạm với lửng mật
                enemy.play() # nhạc hoạt động
                acc[0]+=1
                badguys.pop(index) #xóa lửng mâth
                arrows.pop(index1) #xóa mũi tên
            index1+=1
        index+=1
    for badguy in badguys:
        screen.blit(badguyimg, badguy) #chèn lại lửng mật vào màn hình
    # 7 - Cập nhật màn hình
    # 6.4 - vẽ đồng hồ
    font = pygame.font.Font(None, 24) #Khởi tạo phông chữ với cỡ chứ
    survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0)) #Văn bản in ra
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5] #tọa độ văn bản
    screen.blit(survivedtext, textRect) #chèn văn bản vào màn hình
    # 6.5 - Vẽ thanh sức khỏe
    screen.blit(healthbar, (5,5)) #chèn thanh sức khỏe vào màn hình
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8)) # in thanh sức khỏe(cập nhật thanh sức khỏe)
    pygame.display.flip() 
    # 8 - Lặp lại sự kiện
    for event in pygame.event.get():
        # Kiểm tra sự xuất hiện của nút
        if event.type==pygame.QUIT:
            # nếu kết thúc trò chơi
            pygame.quit() 
            exit(0) 
        if event.type == pygame.KEYDOWN: #điều kiện xuất hiện các nút
            if event.key==K_w:
                keys[0]=True
            elif event.key==K_a:
                keys[1]=True
            elif event.key==K_s:
                keys[2]=True
            elif event.key==K_d:
                keys[3]=True
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            elif event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False
    if event.type==pygame.MOUSEBUTTONDOWN: #điều kiện xuất hiện nháy chuột
            shoot.play() # nhạc hoạt động
            position=pygame.mouse.get_pos()
            acc[1]+=1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32]) #thêm mũi tên vào danh sách
    # 9 - Di chuyển người chơi
    if keys[0]:
        playerpos[1]-=5
    elif keys[2]:
        playerpos[1]+=5
    if keys[1]:
        playerpos[0]-=5
    elif keys[3]:
        playerpos[0]+=5
    #10 - Kiểm tra thắng thua
    if pygame.time.get_ticks()>=90000: #điều kiện thời gian thỏa mãn dừng chương trình. Để dễ thắng hơn thì chỉnh xuống 10000
        running=0 
        exitcode=1
    if healthvalue<=0: #điều kiện thanh sức khỏe về 0 dừng chương trình
        running=0
        exitcode=0
    if acc[1]!=0: #điều kiện số mũi tên bắn trúng lớn hơn 0
        accuracy=acc[0]*1.0/acc[1]*100 # khởi tạo biến chính xác(tỷ lệ %)
    else:
        accuracy=0
# 11 - hiển thị thắng thua    
if exitcode==0: #điều kiện dừng game nếu thua
    pygame.font.init()
    font = pygame.font.Font(None, 24) #phông chữ
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0)) #văn bản in ra
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0)) #in ra kết thúc trò chơi
    screen.blit(text, textRect) #in ra văn bản
else: #điều kiện dừng game nếu thắng
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1: #vòng lặp sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
