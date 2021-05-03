game_name = 'Flappy Bird'
if game_name == 'Flappy Bird':
    import random 
    import pygame as pg 
    import sys

    pg.init()
    pg.font.init()

    screen_width =300
    screen_height =600

    screen = pg.display.set_mode((screen_width, 560))
    pg.display.set_caption(' Flappy Bird ')
    pg.display.set_icon(pg.image.load('bird1.png').convert_alpha())

    background = pg.image.load('background.png').convert()
    bird1 = pg.image.load('bird1.png').convert_alpha()
    bird2 = pg.image.load('bird2.png').convert_alpha()
    bird3 = pg.image.load('bird3.png').convert_alpha()
    bird = [bird1, bird1,  bird2, bird2, bird3, bird3]
    fall_bird = pg.transform.rotate(pg.image.load('falling_bird.png').convert_alpha(), -90)
    pipe = pg.image.load('pipe.png').convert_alpha()
    invert_pipe = pg.transform.flip(pipe, False, True)
    ground = pg.image.load('base.png').convert()
    message = pg.image.load('message.png').convert_alpha()

    hit = pg.mixer.Sound('hit.wav')
    wing = pg.mixer.Sound('wing.wav')
    point = pg.mixer.Sound('point.wav')
    die = pg.mixer.Sound('die.wav')
    swoosh = pg.mixer.Sound('swoosh.wav')

    GROUNDX = 0
    GROUNDY = int(screen_height - ground.get_height())

    clock = pg.time.Clock()

    joysticks = []
    for i in range(pg.joystick.get_count()):
        joysticks.append(pg.joystick.Joystick(i))
        joysticks[-1].init()

    def welcome():
        messagex = (screen_width - message.get_width())/2
        messagey = (screen_height - message.get_height())/2 

        PLAYERX = int(screen_width/3)
        PLAYERY = int((screen_height - bird[0].get_height())/2)

        while True:
            for event in pg.event.get():
                if (event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)):
                    pg.quit()
                    sys.exit()
                if event.type == pg.JOYBUTTONDOWN and event.button ==5:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN  or event.type == pg.MOUSEBUTTONDOWN:
                    return
                if event.type == pg.JOYBUTTONDOWN and event.button == 0 :
                    return
                
            screen.blit(background, [-5, 0])
            screen.blit(ground, [GROUNDX, GROUNDY])
            screen.blit(message, [messagex , messagey])
            screen.blit(bird[0], [PLAYERX, PLAYERY])
        
            pg.display.update()
            clock.tick(30)

    def game(bird):
        PLAYERX = int(screen_width/3)
        PLAYERY = int((screen_height - bird[0].get_height())/2) 

        SCORE = 0

        try:
            highscore = int(get_highscore())
        except:
            highscore = 0

        pipe1 = get_pipe()
        pipe2 = get_pipe()

        u_pipes = [
            {'x': screen_width+200, 'y':pipe1[0]['y']},
            {'x': screen_width+200+screen_width/2, 'y':pipe2[0]['y']}
        ]

        l_pipes = [
            {'x': screen_width+200, 'y':pipe1[1]['y']},
            {'x': screen_width+200+screen_width/2, 'y':pipe2[1]['y']}
        ]

        base1 = get_ground()
        base2 = get_ground()

        bases = [
            {'x': 0 , 'y': base1[0]['y']},
            {'x':ground.get_width(), 'y': base2[0]['y']}
        ]

        basevelx = -4
        pipevelx = -4

        playerFlapped = False
        playerVelY = -9
        playerMaxVelY = 10
        playerFlappVelY = -8
        playerAcc = 1

        swoosh.play()

        i = 0
    
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if event.type == pg.JOYBUTTONDOWN and event.button ==5 :
                    pg.quit()
                    sys.exit()
                if (event.type == pg.KEYDOWN and (event.key == pg.K_UP or event.key == pg.K_SPACE)) or event.type == pg.MOUSEBUTTONDOWN:
                    playerFlapped = True
                if event.type == pg.JOYBUTTONDOWN and( event.button == 0 or event.button == 1):
                    playerFlapped = True
                
            if playerFlapped:
                playerVelY = playerFlappVelY
                playerFlapped = False
                wing.play()

            if playerVelY < playerMaxVelY and not playerFlapped  :
                playerVelY += playerAcc
            
            PLAYERY += playerVelY

            for u_pipe in u_pipes:
                u_pipe['x'] += pipevelx

            for l_pipe in l_pipes:
                l_pipe['x'] += pipevelx
            
            if 0< u_pipes[0]['x']<5:
                pipe_new = get_pipe()
                u_pipes.append(pipe_new[0])
                l_pipes.append(pipe_new[1])

            if -pipe.get_width() >= u_pipes[0]['x']:
                u_pipes.pop(0)
                l_pipes.pop(0)

            for base in bases:
                base['x'] += basevelx
            
            if bases[0]['x'] <= -ground.get_width():
                new_base = get_ground()
                bases.append(new_base[0])

            if bases[0]['x'] <= -ground.get_width():
                bases.pop(0)

            crashed = bird_crash(PLAYERX , PLAYERY, u_pipes, l_pipes)
            if crashed:
                hit.play()
                break 
                    
            PlayerMidpos = PLAYERX + bird[0].get_width()/2
            for u_pipe in u_pipes:
                pipeMidPos = u_pipe['x'] + pipe.get_width()/2
                if pipeMidPos<= PlayerMidpos < pipeMidPos +4:
                    SCORE += 1
                    point.play()
                    
            screen.blit(background, [0,0])

            for u_pipe in u_pipes:
                screen.blit(invert_pipe, [u_pipe['x'], u_pipe['y']] )
            
            for l_pipe in l_pipes:
                screen.blit(pipe, [l_pipe['x'], l_pipe['y']] )
            
            screen.blit(bird[i], [PLAYERX, PLAYERY])
            for base in bases:
                screen.blit(ground, [base['x'], base['y']-5])
            
            if SCORE > highscore:
                highscore = SCORE
            
            show_score(SCORE , highscore)

            with open("score.txt", 'w') as f:
                f.write(str(highscore))

            i += 1
            if i > 5:
                i = 0
            pg.display.update()
            clock.tick(30)

        die.play()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if event.type == pg.JOYBUTTONDOWN and event.button ==5 :
                    pg.quit()
                    sys.exit()
                
            pipevelx = 0

            basevelx = 0
            
            playerVelY = 5
            
            if PLAYERY >= GROUNDY - bird[0].get_height():
                return SCORE
            
            PLAYERY += playerVelY

            screen.blit(background, [0,0])
            
            for u_pipe in u_pipes:
                screen.blit(invert_pipe, [u_pipe['x'], u_pipe['y']] )
            
            for l_pipe in l_pipes:
                screen.blit(pipe, [l_pipe['x'], l_pipe['y']] )
            
            screen.blit(fall_bird, [PLAYERX, PLAYERY])
            for base in bases:
                screen.blit(ground, [base['x'], base['y']-5])

            pg.display.update()
            clock.tick(30)

    def game_Over():
        score = game(bird)
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if event.type == pg.JOYBUTTONDOWN and event.button ==5 :
                    pg.quit()
                    sys.exit()
                if (event.type == pg.KEYDOWN and (event.key == pg.K_UP or event.key == pg.K_SPACE)) or event.type == pg.MOUSEBUTTONDOWN:
                    return
                if event.type == pg.JOYBUTTONDOWN and event.button == 0 :
                    return
                
            screen.blit(background, [-5, 0])
            screen.blit(ground, [GROUNDX, GROUNDY])

            show_gameOver(score)

            pg.display.update() 
            clock.tick(30)

    def show_gameOver(score):
        font = pg.font.SysFont('Comic Sans MS', 40)
        text1 = font.render(" GAME OVER ", True, (0, 0, 0))
        screen.blit(text1, [25, 250]) 
        text2 = font.render(" SCORE : "+str(score), True, (0, 0, 0))
        screen.blit(text2, [25, 300]) 

    def show_score(SCORE, highscore):
        font = pg.font.SysFont('Comic Sans MS', 30)
        font1 = pg.font.SysFont('Comic Sans MS', 20)
        
        score_text1 = 'Score: ' + str(SCORE)
        score_text2 = 'High Score: ' + str(highscore)
        
        text_img1 = font.render(score_text1, True, (0, 0, 0))
        text_img2 = font1.render(score_text2, True, (0, 0, 0))
        
        screen.blit(text_img1, [20, 40])
        screen.blit(text_img2, [20, 10])

    def get_ground():
        basex = ground.get_width()
        basey = GROUNDY
        groundxy = [{'x': basex, 'y':basey}]
        return groundxy

    def get_pipe():
        space = 150
        pipe_x = screen_width + 10
        y2 = random.randrange(space + 40, int(GROUNDY-100))
        y1 = y2 - space - pipe.get_height()
        upper_lower_pipe = [
            {'x': pipe_x , 'y': y1 },
            {'x': pipe_x , 'y': y2 }
        ]
        return upper_lower_pipe

    def bird_crash(PLAYERX , PLAYERY, u_pipes, l_pipes):
        if PLAYERY <= 0  :
            return True 
        
        if PLAYERY >= GROUNDY - bird[0].get_height():
            return True
        
        for u_pipe in u_pipes :
            if PLAYERY < (u_pipe['y'] + pipe.get_height()) and (PLAYERX + bird[0].get_width()) > u_pipe['x'] and PLAYERX < (u_pipe['x'] + pipe.get_width()):
                return True 
        
        for l_pipe in l_pipes :
            if (PLAYERY + bird[0].get_height()) > l_pipe['y'] and (PLAYERX + bird[0].get_width()) > l_pipe['x'] and PLAYERX < (l_pipe['x'] + pipe.get_width()):
                return True

    def get_highscore():
        with open("score.txt", 'r') as f:
            return f.read() 


    welcome()
    while True:
        game_Over()