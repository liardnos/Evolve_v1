import random
import copy
import math
import learning2
import pygame
import time
from pygame.locals import *

window_x = 1000
window_y = 800

pygame.init()
window = pygame.display.set_mode((window_x, window_y))

#reseau = [5,8,6,4,2]
reseau = [5,4,3,2]
#reseau = [5,2]
size = 50
pos = (window_x-len(reseau)*(size+1), 10)

graph_draw = 4
frame_skip = 1 #2000
start_fact = 0.01
fact_stack = 1
ais_nb = 100
grav = 1
AIs = []

myfont = pygame.font.SysFont("monospace", 15)
class graph_flox(object):
    #create a graph
    def __init__(self, point=[[0,0],[300,100]], color=(255,0,0), rail=False, window = False):
        self.point = point
        self.color = color
        self.rail = rail
        self.window = window
        self.size_x = point[1][0] - point[0][0]
        self.size_y = point[1][1] - point[0][1]
        self.values = []
        self.m = 1

    def draw(self):
        max, min = self.values[0], self.values[0]
        for v in self.values:
            if v > max:
                max = v
            if v < min:
                min = v

        self.p1 = self.point[0]
        self.p2 = [self.point[1][0], self.point[0][1]]
        self.p3 = self.point[1]
        self.p4 = [self.point[0][0], self.point[1][1]]
        if self.window:
            pygame.draw.lines(window, self.color,True ,[self.p1, self.p2, self.p3, self.p4], 1)

        size = max - min
        if size == 0:
            size = 1
        mult = (self.size_y)/size

        n = len(self.values)
        for v in self.values:
            p = [
            self.point[1][0] - n,
             self.point[0][1] + self.size_y-(v-min)*mult ,
            ]
            pygame.draw.lines(window, self.color, False, [p,p],1)
            n -=1

        if len(self.values)> self.size_x:
            self.values.pop(0)

        label = myfont.render(str(max), 1, (255,255,255))
        window.blit(label, (self.point[0][0],self.point[0][1]))
        label = myfont.render(str(min), 1, (255,255,255))
        window.blit(label, (self.point[0][0],self.point[1][1]-15))

    def add(self, value):
        self.values.append(value)


def draw_reseau(reseau, size=50, pos=(50,50)):
    add = reseau.tableau_bias
    mult = reseau.tableau_weight
    l_nb = 0
    for l in mult:
        neuron_nb = 0
        for neuron in l:
            neuron_nb2 = 0
            for line in neuron:
                if line >=0:
                    R = 0
                    V = min(255,line*255)
                else:
                    R = min(255,-line*255)
                    V = 0
                color = (R,V,0)
                pygame.draw.line(window, color, [l_nb*size+pos[0],neuron_nb*size+pos[1]], [(l_nb+1)*size+pos[0],neuron_nb2*size+pos[1]], 1)
                neuron_nb2 += 1

            neuron_nb += 1
        l_nb += 1
    l_nb = 0
    for l in add:
        neuron_nb = 0
        for neuron in l:
            neur = (1/(1+math.e**(-neuron*30))-0.5)*2
            if neuron >=0:
                R = 0
                V = min(255,neur*255)
            else:
                R = min(255,-neur*255)
                V = 0
            color = (R,V,0)
            pygame.draw.circle(window, color, [l_nb*size+pos[0],neuron_nb*size+pos[1]], 5)
            neuron_nb += 1
        l_nb += 1

def find(a,x):
    n = 0
    for t in a:
        if t == x:
            return [1,n]
        n+=1
    return [0,n]

def redraw():
    pass


graph_bach = graph_flox(color = (25, 25, 220), point = [[0,10],[400,210]])
graph_bach.add(0)
graph_best = graph_flox(color = (220, 25, 25), point = [[0,10],[400,210]])#, point = [[0,10],[400,210]]
graph_best.add(0)
graph_pourcent = graph_flox(color = (25, 220, 25), point = [[0,10],[400,210]])
graph_pourcent.add(0)

fact = start_fact
go = 1
evole_nb = 0
m2 = 0
x_max2 = 0
bach = 0
p_angle = 0

t = fact
n = 0
while n < ais_nb:
    AIs.append([learning2.learning(copy.deepcopy(reseau)), [window_x/2,window_y/2], [0,0], 0, 0, 0])
    #leaning, (x,y), (vx,vy), angle, score, dead
    #    0        1     2       3     4       5
    AIs[n][0].evolve(fact)
    n+=1

best_ia = AIs[0][0]
x_max = -100000000
x_max2 = x_max
v_angle = 0
last_bach_score = -30
bach_score = 1


#x y vx vy gx gy
#0 1 2  3  4  5

while go:
    print("bach : " + str(bach))
    bach +=1

    result = []
    frame = 0
    simu_go = 1
    window_size = window_x/2
    grav_angle = 0

    #random objectif
    objectif = [[0, 0],[0, 0],[0, 0]]

    while simu_go:
        if frame > 2000:
            simu_go = 0
        for event in pygame.event.get():
            if (event.type == QUIT):
                AIs[0][0].save_network()
                quit()

        mouse_x = objectif[0][0]
        mouse_y = objectif[0][1]
        objectif[0][0] += objectif[1][0]
        objectif[0][1] += objectif[1][1]
        objectif[1][0] += objectif[2][0]
        objectif[1][1] += objectif[2][1]

        objectif[0][0] =  (objectif[0][0]-window_x/2) * 0.85 + window_x/2
        objectif[0][1] =  (objectif[0][1]-window_y/2) * 0.85 + window_y/2
        objectif[1][0] *= 0.9
        objectif[1][1] *= 0.9
        objectif[2][0] *= 0.999
        objectif[2][1] *= 0.999

        objectif[2][0] += (random.random()-0.5)*1
        objectif[2][1] += (random.random()-0.5)*1

        ia_num = 0
        for ai in AIs:
            if (ai[5] == 0):

                #if (frame+1)%3000 == 0:
                #    ai[2][0] += (random.random()-0.5)*1
                #    ai[2][1] += (random.random()-0.5)*1


                ai[1] = ai[1][0]+ai[2][0], ai[1][1]+ai[2][1]
                ai[2][0] += math.sin(grav_angle)*0.1
                ai[2][1] += math.cos(grav_angle)*0.1


                """if frame < 3000:
                    pos_x = ai[1][0]/window_x*2-1
                    pos_y = ai[1][1]/window_y*2-1
                else:"""
                pos_x = (ai[1][0]-mouse_x)/window_x*2
                pos_y = (ai[1][1]-mouse_y)/window_y*2
                #pos_x = pos_x > 0 if pos_x**0.5 else -(-pos_x)**0.5

                v_angle += 1/((pos_x**2+pos_y**2+1))/100000/ais_nb
                #v_angle = v_angle**0.5 * v_angle

                #print((pos_x**2 + pos_y**2)**0.5)
                if ( (pos_x**2 + pos_y**2)**0.5 > 2 ):
                    ai[5] = 1

                if (ai[4] < x_max*2):
                    ai[5] = 1

                if (ai[5] == 1):
                    ai[4] -= 10000000-frame*10
                    ai[5] = 1

                angle = ai[3]/math.pi
                if angle > 1:
                    angle = 1
                elif angle < -1:
                    angle = -1


                v_x = ai[2][0]/10
                v_y = ai[2][1]/10

                if v_x > 1:
                    v_x = 1
                elif v_x < -1:
                    v_x = -1
                if v_y > 1:
                    v_y = 1
                elif v_y < -1:
                    v_y = -1


                r = [pos_x, pos_y, angle, v_x, v_y]
                # y, x, angle, vx, vy
                r = ai[0].run(r)
                #power, v_angle
                ai[2][0] += -r[0]*math.sin(ai[3])
                ai[2][1] += -r[0]*math.cos(ai[3])

                ai[3] += r[1]

                x, y = ai[1]
                ai[4] += -(pos_x**2+pos_y**2)**0.5
                """
                if y > p2 or y < p1 or x < p1 or x > p2:
                    result.append([AIs[ia_num],ai[4]-100000000])
                    #ai score"""


                if ((frame+1)%frame_skip == 0):
                    pygame.draw.line(window, [255,255,255], [x, y], [x-math.sin(ai[3])*10, y-math.cos(ai[3])*10], 2)

            ia_num += 1
        if ((frame+1)%frame_skip == 0):
            pygame.draw.line(window, [0,255,0], [window_x/2, window_y/2], [window_x/2+math.sin(grav_angle)*10, window_y/2+math.cos(grav_angle)*10], 2)

            draw_reseau(best_ia, pos=pos, size=size)

            pygame.draw.circle(window, [0,255,0], [int(mouse_x), int(mouse_y)], 3)

            graph_bach.draw()
            graph_best.draw()
            graph_pourcent.draw()

            pygame.display.flip()
            #time.sleep(0.0)
            window.fill((0,0,0))

        if len(AIs) == 0:
            simu_go = 0
        frame +=1

    bach_score = 1
    bash_score_divide = 0
    for ai in AIs:
        if (ai[5] == 0):
            bach_score += ai[4]
            bash_score_divide += 1
        result.append([ai,ai[4]])
        #if ai[1][0] > window_x or ai[1][0] < 0 or ai[1][1] > window_y or ai[1][1] < 0:
        ai[1] = [window_x/2,window_y/2]
        #ai[1] = [mouse_x, mouse_y]
        ai[3] = 0
        ai[2] = [0,0]
        ai[5] = 0

    if bash_score_divide > 0:
        bach_score /= bash_score_divide
    else:
        bash_score = -50

    x_max2 = x_max
    nb = 0
    x_max = -5000000000000000000
    for r in result:
        if r[1] >= x_max:
            x_max = r[1]
            best = [r[0][0].tableau_bias, r[0][0].tableau_weight]
            best_ia = r[0][0]
            c = nb
        nb +=1
    bach_score /= ais_nb
    if x_max <= x_max2:
        fact *= fact_stack

    pourcent = (bach_score-last_bach_score)/(last_bach_score)*100

    i = 0
    while (i < graph_draw):
        graph_bach.add(bach_score)
        if (pourcent < 200 and pourcent > -200):
            graph_pourcent.add(pourcent)
        else:
            graph_pourcent.add(0)
        if x_max > -10000:
            graph_best.add(x_max)
        else:
            graph_best.add(0)
        i += 1

    print("best is :"+str(c)+" with d = "+str(x_max))
    print("bach score is " + str(bach_score) + " | " + str(pourcent))
    print("evolve fact : "+str(fact))
    last_bach_score = bach_score
    #n = 0
    #while n<ais_nb:
    #    AIs.append([learning2.learning(copy.deepcopy(reseau)),[window_x/2,window_y/2],[0,0],0,0])
    #    n+=1


    n = 0
    for ai in AIs:
        AIs[n][0].tableau_bias = copy.deepcopy(best[0])
        AIs[n][0].tableau_weight = copy.deepcopy(best[1])
        AIs[n][0].evolve((n*t)**2)
        #ai[1] = [window_x/2, window_y/2]
        ai[4] = 0
        n+=1



    """
    redraw()
    #draw_reseau(best_ia, pos=pos, size=size)
    pygame.display.flip()
    time.sleep(0.1)
    window.fill((0,0,0))
    if m == 1:
        print(best[0])
        print()
        print(best[1])
        quit()
    """
