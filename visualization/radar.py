import pygame
import math
import serial

com = 'COM4'
baud = 9600

W = 1560  # Screen width = 1560 px
H_ = 1000  # Screen height = 1000 px
H = H_ - 60
# pygame setup
pygame.init()
screen = pygame.display.set_mode((W, H_))
clock = pygame.time.Clock()

running = True  # event state variable

# background surface
# semi circle grid with dark lines every 30 deg and lines every 10 deg
background = pygame.Surface((W, H_))
background.fill((0, 0, 0))

Max_radius = int((W - 60) / 2)  # 60px - 30px each side padding
px_per_cm = int(Max_radius / 30)

for i in range(px_per_cm, Max_radius + 1, px_per_cm):
    if i == 10*px_per_cm or i == 20*px_per_cm or i == 30*px_per_cm :
        pygame.draw.circle(background, (0, 255, 0), (W / 2, H), i, width=5)
    pygame.draw.circle(background, (0, 255, 0), (W / 2, H), i, width=1)
# angles at 30 degrees
for i in range(30, 180, 30):
    pygame.draw.line(background, (0, 255, 0), (W / 2, H),
                     (W / 2 + (W / 2 * math.cos(math.radians(i))), H - (W / 2 * math.sin(math.radians(i)))), width=5)
# angles at 10 degrees
for i in range(10, 180, 10):
    pygame.draw.line(background, (0, 255, 0), (W / 2, H),
                     (W / 2 + (Max_radius * math.cos(math.radians(i))), H - (Max_radius * math.sin(math.radians(i)))),
                     width=2)
pygame.draw.line(background, (0, 255, 0),
                     (30 , H - 1),
                     (W - 30, H - 1),width = 5)
pygame.draw
# surface for the fade sweep effect
dynamic = pygame.Surface((W, H), pygame.SRCALPHA)  # pygame.SRCALPHA is constant for surface transparency
trail = []  # list of recent angles


# Serial init and function
ser = serial.Serial(com, baud)
def Readserial():
    data = ser.readline().decode().strip()
    data_aslist = data.split(',')
    if len(data_aslist) == 2 and data_aslist[0] and data_aslist[1]:
        return data_aslist
    return None

def draw_sweep_line(a,d,brightness):
    # distance from outermost semicircle at which the green line should end and red line should start
    if d != 0 :
        distance_greenred = d * px_per_cm
    else:
        distance_greenred = Max_radius

    pygame.draw.line(dynamic, (0, brightness, 0, brightness),
                     (W / 2, H),
                     (W / 2 + (distance_greenred * math.cos(math.radians(a))), H - (distance_greenred * math.sin(math.radians(a)))))

    pygame.draw.line(dynamic, (brightness, 0, 0, brightness),
                     (W / 2 + (distance_greenred * math.cos(math.radians(a))), H - (distance_greenred * math.sin(math.radians(a)))),
                     (W / 2 + (Max_radius * math.cos(math.radians(a))), H - (Max_radius * math.sin(math.radians(a)))))

def draw_current_line(a,d):
    # distance from outermost semicircle at which the green line should end and red line should start
    if d != 0:
        distance_greenred = d * px_per_cm
    else:
        distance_greenred = Max_radius

    pygame.draw.line(dynamic, (0, 255, 0),
                     (W / 2, H),
                     (W / 2 + (distance_greenred * math.cos(math.radians(a))),H - (distance_greenred * math.sin(math.radians(a)))))

    pygame.draw.line(dynamic, (255, 0, 0),
                     (W / 2 + (distance_greenred * math.cos(math.radians(a))),H - (distance_greenred * math.sin(math.radians(a)))),
                     (W / 2 + (Max_radius * math.cos(math.radians(a))), H - (Max_radius * math.sin(math.radians(a)))))

font = pygame.font.SysFont('Arial', 20)



while running:
    # events
    # pygame.QUIT is executed when user presses X or ends task
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # piece render
    # Sweep Angle
    dynamic.fill((0, 0, 0, 0))
    data_aslist = Readserial()
    if data_aslist is None:
        continue

    angle = int(data_aslist[0])
    distance = float(data_aslist[1])


    # fade trail effect array
    trail.append([angle,distance])  # add current angle,distance pair as a new list of integers at each tick
    if len(trail) > 50:  # keep last 50 angles
        trail.pop(0)  # keep removing data at 0th index, basically the first one, which is the earliest angle,distance pair in the sequence since list.append() adds element at the last index

    # to draw the lines in the fading effect
    for i in range(len(trail)):
        brightness = int(255 * (i / len(trail)))  # 0 = dim, 255 = bright , brightness scales in reverse with recency of the angles
        draw_sweep_line(trail[i][0],trail[i][1],brightness)

    # draw the current line every iteration in dynamic
    draw_current_line(angle,distance)

    screen.blit(background, (0, 0))
    screen.blit(dynamic, (0, 0))

    pygame.draw.rect(screen, (0, 0, 0), (0, H, W, 60))  # black bar
    text = font.render(f'Angle: {angle}°   Distance: {distance}cm', True, (0, 255, 0))
    text2 = font.render(f'10 cm', True, (0, 255, 0))
    text3 = font.render(f'20 cm', True, (0, 255, 0))
    text4 = font.render(f'30 cm', True, (0, 255, 0))
    text5 = font.render(f'30°', True, (0, 255, 0))
    text6 = font.render(f'60°', True, (0, 255, 0))
    text7 = font.render(f'90°', True, (0, 255, 0))
    text8 = font.render(f'120°', True, (0, 255, 0))
    text9 = font.render(f'150°', True, (0, 255, 0))

    screen.blit(text, (W // 2 - text.get_width() // 2, H + 35))
    screen.blit(text2, (W // 2 + 10*px_per_cm - text2.get_width() // 2, H + 10))
    screen.blit(text3, (W // 2 + 20*px_per_cm - text3.get_width() // 2, H + 10))
    screen.blit(text4, (W // 2 + 30*px_per_cm - text4.get_width() // 2, H + 10))

    screen.blit(text5, (W / 2 + (W / 2 * math.cos(math.radians(30))) + text5.get_width() // 2, H - (W / 2 * math.sin(math.radians(30))) - text5.get_height()//2 - 15 ))
    screen.blit(text6, (W / 2 + (W / 2 * math.cos(math.radians(60))) + text6.get_width() // 2 - 5, H - (W / 2 * math.sin(math.radians(60))) - text6.get_height()//2 - 15 ))
    screen.blit(text7, (W / 2 + (W / 2 * math.cos(math.radians(90))) - text7.get_width() // 2 + 5, H - (W / 2 * math.sin(math.radians(90))) - text7.get_height()//2 - 15 ))
    screen.blit(text8, (W / 2 + (W / 2 * math.cos(math.radians(120))) - text8.get_width(), H - (W / 2 * math.sin(math.radians(120))) - text8.get_height() // 2 - 15 ))
    screen.blit(text9, (W / 2 + (W / 2 * math.cos(math.radians(150))) - text9.get_width() , H - (W / 2 * math.sin(math.radians(150))) - text9.get_height()//2 - 15 ))


    # flip() the display to put the work on the screen
    pygame.display.flip()

    # limits processes to 60 iterations per sec / 60 fps
    clock.tick(60)
pygame.quit()
