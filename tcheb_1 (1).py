from math import *
import PySimpleGUI as sg
import time

# Параметры графики
Wwidth=600                      # ширина окна графики
Wheight=400                     # высота окна графики
a=Wwidth/4                      # координата X центра вершины
b=Wheight/3                     # координата Y центра вершины
r1=60                          # длина кривошипа
r2=170                          # длина шатуна
r3=170                          # длина коромысла
r4=130                          # длина стойки
rDop=170                        # длина дополительного плеча

dots_coords=[]

def draw_coords(a,b):
    line = window['-graph-'].DrawLine((0,b), (Wwidth,b), color='black')             #чертим ось X
    line = window['-graph-'].DrawLine((a,0), (a,Wheight), color='black')            #чертим ось Y

def draw_mechanical(r1,r2,r3,r4,alfa,rDop):
    global dots_coords
    xA=0
    yA=0
    xB=r1*cos(radians(alfa))
    yB=r1*sin(radians(alfa))
    xD=r4
    yD=0
    Q=(r1*r1+r4*r4-2*r1*r4*cos(radians(alfa)))**0.5
    P=(r2*r2-r3*r3)/Q
    betta=atan(r1*sin(radians(alfa))/(r1*cos(radians(alfa))-r4))+acos((P+Q)/(2*r2))
    xC=xB+r2*cos(betta)
    yC=yB+r2*sin(betta)
    xE=xC+(xC-xB)*rDop/r2
    yE=yC+(yC-yB)*rDop/r2
    # E=(xD-xB)/yB
    # F=(r4*r4+r2*r2-r3*r3-r1*r1)/(2*yB)
    # D=4*(r4+E*F)*(r4+E*F)-4*(1+E*E)*(F*F+r4*r4-r3*r3)
    # xC=(2*(r4+E*F)+D**0.5)/(2*(1+E*E))
    # yC=xC*E-F
    temp=[]
    temp.append(xC)
    temp.append(yC)
    temp.append(xE)
    temp.append(yE)
    dots_coords.append(temp)
    window['-graph-'].erase()
    line = window['-graph-'].DrawLine((0,b), (Wwidth,b), color='black')             #чертим ось X
    line = window['-graph-'].DrawLine((a,0), (a,Wheight), color='black')            #чертим ось Y
    line = window['-graph-'].DrawLine((a+xA,b+yA), (a+xB,b+yB), color='blue')       #чертим кривошип
    line = window['-graph-'].DrawLine((a+xB,b+yB), (a+xC,b+yC), color='blue')       #чертим шатун
    line = window['-graph-'].DrawLine((a+xC,b+yC), (a+xD,b+yD), color='blue')       #чертим коромысло 
    line = window['-graph-'].DrawLine((a+xC,b+yC), (a+xE,b+yE), color='green')      #чертим коромысло 

def draw_dots():
    global dots_coords
    for i in dots_coords:
        point = window['-graph-'].DrawPoint((a+i[0],b+i[1]), 5, color='red')
        point = window['-graph-'].DrawPoint((a+i[2],b+i[3]), 5, color='green')
        window.refresh()
        time.sleep(0.01) 

# задаем расположение основных элементов на слое
message='Выберите угол и параметры механизма'
layout =    [
     [(sg.Graph((Wwidth, Wheight), (0, 0), (Wwidth, Wheight), key='-graph-', background_color='white'))],
     [sg.B('Старт', key='-calc-', border_width=5, pad=(10,10)),sg.T('Длина плеча', size=(10, 1), key='-tdop-', font='Helvetica 16'),sg.I('170', key='-rDop-', size=(5,1), pad=(10,10))],
     [sg.T('Длина кривошипа', size=(15, 1), key='-t1-', font='Helvetica 16'),sg.I('60', key='-r1-', size=(5,1), pad=(10,10)),sg.T('Длина шатуна', size=(15, 1), key='-t2-', font='Helvetica 16'),sg.I('170', key='-r2-', size=(5,1), pad=(10,10))],
     [sg.T('Длина коромысла', size=(15, 1), key='-t3-', font='Helvetica 16'),sg.I('170', key='-r3-', size=(5,1), pad=(10,10)),sg.T('Длина стойки', size=(15, 1), key='-t4-', font='Helvetica 16'),sg.I('130', key='-r4-', size=(5,1), pad=(10,10))],
     [sg.Text(message, size=(50, 2), key='-text-', font='Helvetica 16')],
     [sg.Slider(range=(0,720),default_value=45,expand_x=True,enable_events=True,key='-SL-',orientation='h')]
            ]
# формируем окно программы
window = sg.Window('Кинематика стопоходящей машины П.Л.Чебышева', layout, size=(700,700),finalize=True)

# чертим стартовое положение
draw_coords(a,b)
draw_mechanical(r1,r2,r3,r4,45,rDop)
window['-graph-'].DrawText('Кривошип', (a+42,b+42), color='red')
window['-graph-'].DrawText('Шатун', (a+168,b+118), color='red')
window['-graph-'].DrawText('Коромысло', (a+226,b+76), color='red')
window['-graph-'].DrawText('Стойка', (a+100,b-10), color='red')
window['-graph-'].DrawText('Плечо', (a+270,b+200), color='red')



# основной цикл программы
while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break

    if event == '-calc-':
        r1 = int(values['-r1-'])
        r2 = int(values['-r2-'])
        r3 = int(values['-r3-'])
        r4 = int(values['-r4-'])
        rDop=int(values['-rDop-'])
        dots_coords=[]
        for alfa in range(0,361,5):
            if (((r1+r4)<=(r2+r3))and(abs(r2-r3)<=abs(r4-r1))and(abs(r4-r3)<=(r1+r2))and((r1+r2)<=(r4+r3))):
                message="При такой конфигурации звеньев механизм существует"
                window['-graph-'].erase()
                #k=min((Wwidth-20)/(1.5*r1+r3+r4),(Wheight-20)/(max(r1,r3+rDop)))
                k=(Wheight/2-20)/max(r1,r3+rDop)
                draw_coords(k*a,k*b)
                draw_mechanical(k*r1,k*r2,k*r3,k*r4,alfa,k*rDop)
                window.refresh()
                time.sleep(0.1)  
            else:
                message="При такой конфигурации звеньев механизм НЕ существует"
                text_elem = window['-text-']
                text_elem.update(message)
        draw_dots()
    if event == '-SL-':
        r1 = int(values['-r1-'])
        r2 = int(values['-r2-'])
        r3 = int(values['-r3-'])
        r4 = int(values['-r4-'])
        alfa=int(values['-SL-'])
        rDop=int(values['-rDop-'])
        if (((r1+r4)<=(r2+r3))and(abs(r2-r3)<=abs(r4-r1))and(abs(r4-r3)<=(r1+r2))and((r1+r2)<=(r4+r3))):
            message="При такой конфигурации звеньев механизм существует"
            window['-graph-'].erase()
            #k=min((Wwidth-20)/(1.5*r1+r3+r4),(Wheight-20)/(max(r1,r3+rDop)))
            k=(Wheight/2-20)/max(r1,r3+rDop)
            draw_coords(k*a,k*b)
            draw_mechanical(k*r1,k*r2,k*r3,k*r4,alfa,k*rDop)
        else:
            message="При такой конфигурации звеньев механизм НЕ существует"
        text_elem = window['-text-']
        text_elem.update(message)

window.close()