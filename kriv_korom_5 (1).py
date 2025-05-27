from math import *
import PySimpleGUI as sg
import time

# Параметры графики
Wwidth=600                      # ширина окна графики
Wheight=400                     # высота окна графики
a=Wwidth/4                      # координата X центра вершины
b=Wheight/2                     # координата Y центра вершины
r1=120                          # длина кривошипа
r2=180                          # длина шатуна
r3=160                          # длина коромысла
r4=200                          # длина стойки

dots_coords=[]

def draw_coords(a,b):
    line = window['-graph-'].DrawLine((0,b), (Wwidth,b), color='black')             #чертим ось X
    line = window['-graph-'].DrawLine((a,0), (a,Wheight), color='black')            #чертим ось Y

def draw_mechanical(r1,r2,r3,r4,alfa):
    global dots_coords
    xA=0
    yA=0
    xB=r1*cos(radians(alfa))
    yB=r1*sin(radians(alfa))
    xD=r4
    yD=0
    E=(xD-xB)/yB
    F=(r4*r4+r2*r2-r3*r3-r1*r1)/(2*yB)
    D=4*(r4+E*F)*(r4+E*F)-4*(1+E*E)*(F*F+r4*r4-r3*r3)
    xC=(2*(r4+E*F)+D**0.5)/(2*(1+E*E))
    yC=xC*E-F
    temp=[]
    temp.append(xC)
    temp.append(yC)
    dots_coords.append(temp)
    window['-graph-'].erase()
    line = window['-graph-'].DrawLine((0,b), (Wwidth,b), color='black')             #чертим ось X
    line = window['-graph-'].DrawLine((a,0), (a,Wheight), color='black')            #чертим ось Y
    line = window['-graph-'].DrawLine((a+xA,b+yA), (a+xB,b+yB), color='blue')             #чертим кривошип
    line = window['-graph-'].DrawLine((a+xB,b+yB), (a+xC,b+yC), color='blue')     #чертим шатун
    line = window['-graph-'].DrawLine((a+xC,b+yC), (a+xD,b+yD), color='blue')       #чертим коромысло 

def draw_dots():
    global dots_coords
    for i in dots_coords:
        point = window['-graph-'].DrawPoint((a+i[0],b+i[1]), 5, color='red')
        window.refresh()
        time.sleep(0.01) 

# задаем расположение основных элементов на слое
message='Выберите угол и параметры механизма'
layout =    [
     [(sg.Graph((Wwidth, Wheight), (0, 0), (Wwidth, Wheight), key='-graph-', background_color='white'))],
     [sg.B('Старт', key='-calc-', border_width=5, pad=(10,10))],
     [sg.T('Длина кривошипа', size=(15, 1), key='-t1-', font='Helvetica 16'),sg.I('120', key='-r1-', size=(5,1), pad=(10,10)),sg.T('Длина шатуна', size=(15, 1), key='-t2-', font='Helvetica 16'),sg.I('180', key='-r2-', size=(5,1), pad=(10,10))],
     [sg.T('Длина коромысла', size=(15, 1), key='-t3-', font='Helvetica 16'),sg.I('160', key='-r3-', size=(5,1), pad=(10,10)),sg.T('Длина стойки', size=(15, 1), key='-t4-', font='Helvetica 16'),sg.I('200', key='-r4-', size=(5,1), pad=(10,10))],
     [sg.Text(message, size=(50, 2), key='-text-', font='Helvetica 16')],
     [sg.Slider(range=(1,179),default_value=45,expand_x=True,enable_events=True,key='-SL-',orientation='h')]
            ]
# формируем окно программы
window = sg.Window('Кинематика четвырехзвенного кривошипно-коромыслового механизма', layout, size=(700,700),finalize=True)

# чертим стартовое положение
draw_coords(a,b)
draw_mechanical(r1,r2,r3,r4,45)
window['-graph-'].DrawText('Кривошип', (a+42,b+42), color='red')
window['-graph-'].DrawText('Шатун', (a+168,b+118), color='red')
window['-graph-'].DrawText('Коромысло', (a+226,b+76), color='red')
window['-graph-'].DrawText('Стойка', (a+100,b-10), color='red')



# основной цикл программы
while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break

    if event == '-calc-':
        dots_coords=[]
        r1 = int(values['-r1-'])
        r2 = int(values['-r2-'])
        r3 = int(values['-r3-'])
        r4 = int(values['-r4-'])
        for alfa in range(1,179,5):
            if (((r1+r4)<=(r2+r3))and(abs(r2-r3)<=abs(r4-r1))and(abs(r4-r3)<=(r1+r2))and((r1+r2)<=(r4+r3))):
                message="При такой конфигурации звеньев механизм существует"
                window['-graph-'].erase()
                draw_coords(a,b)
                draw_mechanical(r1,r2,r3,r4,alfa)
                window.refresh()
                time.sleep(0.02)  
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
        if (((r1+r4)<=(r2+r3))and(abs(r2-r3)<=abs(r4-r1))and(abs(r4-r3)<=(r1+r2))and((r1+r2)<=(r4+r3))):
            message="При такой конфигурации звеньев механизм существует"
            window['-graph-'].erase()
            draw_coords(a,b)
            draw_mechanical(r1,r2,r3,r4,alfa)
        else:
            message="При такой конфигурации звеньев механизм НЕ существует"
        text_elem = window['-text-']
        text_elem.update(message)

window.close()