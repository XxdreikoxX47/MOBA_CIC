import Agente
import objetos_test as MOBAobjs
import inspect
from time import time
from math import exp as e
from threading import Thread, Event, Timer
from scipy.spatial.distance import cityblock
import numpy as np
import copy

class AvatarEquilibrado(Agente.Agente):
    def __init__(self,x=0,y=0, equipo=1, ID=None):
        self.ID = ID
        self.type = "Unidad jugable"        
        self.x = x
        self.y = y
        self.equipo = equipo
        self.salud = 10500
        self.salud_max = 10500
        self.experiencia = 0
        self.nivel = 1
        self.nivel_max = 20
        self.bonus_ataque = 0.35
        self.estado = "Normal"
        self.porta_llave = False
        self.multilabel = True
        self.labels = ["aet1", "aet2"]
        if equipo ==1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1]
        self.direccion = 0
        self.direccion_ataque = 0
        self.angulo_giro = 0 #Se usa para los ataques giratorios
        #self.move = False
        self.fila_cursor = 0
        self.columna_cursor = 0
        self.fila_cursor_ataque = 0
        self.columna_cursor_ataque = 0
        self.click = False
        #self.click_time = 0
        self.boton1 = False
        self.boton2 = False
        self.boton3 = False
        self.boton4 = False
        self.target = None
        self.limite = 0
        self.mapa = None
        
        self.p = 0 #Es un indicador del punto actual donde esta atacando el avatar, esto permite cambiarlo en metodos que se a¿ejutan en paralelo

    def direccionMov(self, angulo):
        self.direccion = angulo
    
    def mover(self):
        if self.estado!="inmovil":
            #self.move = True        
            #Movimiento horizontal
            #Se mueve a la derecha
            if (self.direccion<90) or (self.direccion>270):
                self.y+= 1
            #Se mueve a la izquierda
            elif (self.direccion>90 and self.direccion>180) or (self.direccion>180 and self.direccion<270):
                self.y-= 1
            #movimiento vertical
            #Se mueve hacia arriba
            if (self.direccion>0 and self.direccion<180):
                self.x-= 1
            #Se mueve hacia abajo
            elif (self.direccion>180 and self.direccion<360):
                self.x+= 1

    def mueveCursor(self, fila, columna):
        self.fila_cursor = fila
        self.columna_cursor = columna        
    
    def apagaClick(self):
        self.click = False            

    def hacerClick(self, event=None):
        self.click = True
        #self.click_time = time()       
        if event:
            event.set()
        timer = Timer(0.25, self.apagaClick)
        timer.start() 
    
    def apagaBoton(self,Boton):
        if Boton=="1":
            self.boton1 = False            
        
        elif Boton=="2":
            self.boton2 = False
        
        elif Boton=="3":
            self.boton3 = False            

        else:
            self.boton4 = False
            
        self.limite = 0
        self.target = None

    def ataqueBasico(self, objetos_frame):
        #print("Atacando")
        targets = []        
        while not self.boton1:                
            #print("primer if, activando boton 1")
            self.boton1 = True
               #Se mueve a la derecha
            if self.columna_cursor>self.y:                
                minCol = self.x
                maxCol = self.x+1
                minFil = self.y-1
                maxFil = self.y+1                                
                
            #Se mueve a la izquierda
            elif self.columna_cursor<self.y:                
                minCol = self.x-1
                maxCol = self.x
                minFil = self.y-1
                maxFil = self.y+1              

            #movimiento vertical
            #Se mueve hacia arriba
            if self.fila_cursor<self.x:                
                minCol = self.x-1
                maxCol = self.x+1
                minFil = self.y
                maxFil = self.y-1

            #Se mueve hacia abajo
            elif self.fila_cursor>self.x:                
                minCol = self.x-1
                maxCol = self.x+1
                minFil = self.y
                maxFil = self.y+1      


            while not self.target:
               # print("Buscando objetivo...")
                i = minCol
                while i <=maxCol:
                    j = minFil
                    while j<=maxFil:
                        if [i,j]!=[self.x,self.y]:                            
                            if ("Unidad" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) or \
                                ("destructible" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) and \
                                    "indestructible" not in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]:
                                #print(objetos_frame[str(self.x+i)+","+str(self.y+j)])
                                if (objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["equipo"]!=self.equipo):                                    
                                    if cityblock([self.x,self.y],[self.x+i,self.y+j])<=1:
                                        targets.append(str(self.x+i)+","+str(self.y+j))
                                 #       print("Target definido: ", self.target)
                                        break
                        j+=1
                    i+=1
        
            if len(targets>0):
                for t in targets:
                    print("Atacando target", objetos_frame[t].__dict__)
                    objetos_frame[t].__dict__["salud"]-= 125+((125/self.nivel_max)*self.bonus_ataque)
                    print("Target despues del ataque", objetos_frame[t].__dict__)
        
        timer = Timer(0.75, self.apagaBoton, args=("1"))
        timer.start() 
    
    def apuntar(self, Boton=None):
        while not self.click:
            if Boton=="1":
                self.boton1 = True            
            
            elif Boton=="2":
                self.boton2 = True
            
            elif Boton=="3":
                self.boton3 = True

            else:
                self.boton4 = True
                                    
    def ataqueEspecialBasico1(self, objetos_frame):
        targets= []
        if not self.boton2:                
            self.boton2 = True
            radio = 2
            t1 = Thread(target=self.apuntar, args=(self, '2'))
            t1.start()
            #Se define la direccion en X y en Y
            addX = np.sign(np.cos(self.direccion))
            addY = np.sign(np.sin(self.direccion))
            #Si esta en una posicion completamente vertical, se duplica en Y
            if (self.direccion*(np.pi/180))%(np.pi)==np.pi/2:
                addY*=2
                addX=0
            #Si esta en una posicion completamente horizontal, se duplica en X
            if (self.direccion*(np.pi/180))%(np.pi)==0:
                addX*=2
                addY=0

            #Se espera a que se de click en algun proceso                
            while True: 
                if self.click:
                    #Movimiento horizontal
                    while cityblock([self.x,self.y],[self.x+radio, self.y+radio])<=1:                                           
                        if "Unidad" in (objetos_frame[self.mapa[self.x+addX][self.y+addY]].__dict__["type"]) or \
                         "destructible" in (objetos_frame[self.mapa[self.x+addX][self.y+addY]].__dict__["type"]): 
                                print(objetos_frame[self.mapa[self.x+addX][self.y+addY]])
                                if (objetos_frame[self.mapa[self.x+addX][self.y+addY]].__dict__["equipo"]!=self.equipo):
                                    targets.append(str(self.y+addY)+","+str(self.x+addX))
                                                        
                self.limite+=1
                if self.limite>=20:
                    break
            
        else:
            #El avatar se desplaza
            self.x+=addX
            self.y+=addY
            if len(targets)>0:
                for t in targets:
                    objetos_frame[t].__dict__["salud"]-= 275+((275/self.nivel_max)*self.bonus_ataque)                   
        
        timer = Timer(3.5, self.apagaBoton, args=("2"))
        timer.start() 
    
    def girarAtaque(self):
        """
        Hace un giro en sentido contrario de las manecillas del reloj, avanzando 1 bloque
        en la direccion indicada, desplazando el punto anterior donde atacó
        Esta funcion requiere de un llamado en paralelo cada t segundos, donde t=0.25s
        
        p se codifica en [x,y]
        """
        #Se mueve a la derecha
        if (self.angulo_giro<90) or (self.angulo_giro>270):
            self.p[1]+=1
        #Se mueve a la izquierda
        elif (self.angulo_giro>90 and self.angulo_giro>180) or (self.angulo_giro>180 and self.angulo_giro<270):
            self.p[1]-= 1
        #movimiento vertical
        #Se mueve hacia arriba
        if (self.angulo_giro>0 and self.angulo_giro<180):
            self.p[0]-= 1
        #Se mueve hacia abajo
        elif (self.angulo_giro>180 and self.angulo_giro<360):
            self.p[0]+= 1

        self.angulo_giro+=45
        if(self.angulo_giro>=360):
            self.angulo_giro=0        


    def ataqueEspecialBasico2(self, objetos_frame):        
        if not self.boton3:                
            self.boton3 = True  
            i=0
            while True: 
                if self.click:         
                    self.direccion_ataque = copy.copy(self.direccion)
                    self.angulo_giro = copy.copy(self.direccion)
                    self.estado = "inmovil"
                    addX = np.sign(np.cos(self.direccion_ataque))
                    addY = np.sign(np.sin(self.direccion_ataque))
                    if (self.direccion_ataque*(np.pi/180))%(np.pi)==np.pi/2:                
                        addX=0
                    #Si esta en una posicion completamente horizontal, se duplica en X
                    if (self.direccion_ataque*(np.pi/180))%(np.pi)==0:                        
                        addY=0
                    
                    while i<9:                                            
                        if i>7:
                            #Si esta en una posicion completamente vertical, se duplica en Y
                            if (self.direccion_ataque*(np.pi/180))%(np.pi)==np.pi/2:                
                                addY*=2
                            #Si esta en una posicion completamente horizontal, se duplica en X
                            if (self.direccion_ataque*(np.pi/180))%(np.pi)==0:                        
                                addX*=2
                        self.p = [(self.x+addX),(self.y+addY)]
                        punto = str(self.p[0])+","+str(self.p[1])
                        if (objetos_frame[self.mapa[self.p[1]][self.p[0]]].__dict__["equipo"]!=self.equipo):
                            objetos_frame[punto].__dict__["salud"]-= 350+((350/self.nivel_max)*self.bonus_ataque)                   
                        timerGiro = Timer(0.25, self.girarAtaque)                 
                        timerGiro.start()
                        i+=1

                self.limite+=1
                if self.limite>=20:
                    break
                
        self.estado = "normal"
        timer = Timer(4.5, self.apagaBoton, args=("3"))
        timer.start()
    
    def ataqueEspecial11(self, objetos_frame):
        """
        En esta primera version el ataque especial 11 no considera el efecto de 'aceleracion' que
        debería provocar al avatar usuario
        """
        targets= []
        if not self.boton2:                
            self.boton2 = True
            radio = 3
            t1 = Thread(target=self.apuntar, args=(self, '2'))
            t1.start()
            #Se define la direccion en X y en Y
            addX = np.sign(np.cos(self.direccion))
            addY = np.sign(np.sin(self.direccion))
            #Si esta en una posicion completamente vertical, se duplica en Y
            if (self.direccion*(np.pi/180))%(np.pi)==np.pi/2:
                addY*=3
                addX=0
            #Si esta en una posicion completamente horizontal, se duplica en X
            if (self.direccion*(np.pi/180))%(np.pi)==0:
                addX*=3
                addY=0

            #Se espera a que se de click en algun proceso                
            while True: 
                if self.click:
                    #Movimiento horizontal
                    while cityblock([self.x,self.y],[self.x+radio, self.y+radio])<=3:                                           
                        if "Unidad" in (objetos_frame[self.mapa[self.x+addX][self.y+addY]].__dict__["type"]) or \
                         "destructible" in (objetos_frame[self.mapa[self.x+addX][self.y+addY]].__dict__["type"]): 
                                print(objetos_frame[self.mapa[self.x+addX][self.y+addY]])
                                if (objetos_frame[self.mapa[self.x+addX][self.y+addY]].__dict__["equipo"]!=self.equipo):
                                    targets.append(str(self.y+addY)+","+str(self.x+addX))
                                                        
                self.limite+=1
                if self.limite>=20:
                    break
            
        else:
            #El avatar se desplaza
            self.x+=addX
            self.y+=addY
            if len(targets)>0:
                for t in targets:
                    objetos_frame[t].__dict__["salud"]-= 400+((400/self.nivel_max)*self.bonus_ataque)                   
        
        timer = Timer(4.5, self.apagaBoton, args=("2"))
        timer.start() 

    def succion(self, event, radio, objetos_frame, daño=0):
        t1 = time.time()
        while True:
            i=self.x-radio
            while i< self.x+radio:
                j=self.y-radio
                while j< self.y+radio:
                    if (objetos_frame[str(i)+','+str(j)].__dict__["equipo"]!=self.equipo):
                        objetos_frame[str(i)+','+str(j)].__dict__["x"]+= 1*np.sign(self.x-i)
                        objetos_frame[str(i)+','+str(j)].__dict__["y"]+= 1*np.sign(self.y-j)
                        objetos_frame[str(i)+','+str(j)].__dict__["salud"]-= daño
                    j+=1
                i+=1
            t2 = time.time()
            if t2-t1>=5:
                event.set()
                return 0


    def ataqueEspecial21(self, objetos_frame):
        """
        En esta primera version el ataque especial 21 no considera el efecto de 'congelamiento' que
        debería provocar a las unidades no aliadas que alcanza. 
        """
        if not self.boton3:                
            self.boton3 = True  
            while True: 
                if self.click:         
                    self.direccion_ataque = copy.copy(self.direccion)
                    self.angulo_giro = copy.copy(self.direccion)                    
                    addX = np.sign(np.cos(self.direccion_ataque))
                    addY = np.sign(np.sin(self.direccion_ataque))
                    e = Event()
                    succiona = Thread(target= self.succion, args=(e, 3, objetos_frame))
                    succiona.start()
                    if (self.direccion_ataque*(np.pi/180))%(np.pi)==np.pi/2:                
                        addX=0                    
                    if (self.direccion_ataque*(np.pi/180))%(np.pi)==0:                        
                        addY=0
                    start = time.time()
                    
                    while end-start<=5:                                                                    
                        self.p = [(self.x+addX),(self.y+addY)]
                        punto = str(self.p[0])+","+str(self.p[1])
                        if (objetos_frame[self.mapa[self.p[1]][self.p[0]]].__dict__["equipo"]!=self.equipo):
                            objetos_frame[punto].__dict__["salud"]-= 200+((200/self.nivel_max)*self.bonus_ataque)                                           
                        timerGiro = Timer(0.25, self.girarAtaque)                 
                        timerGiro.start()
                        end = time.time()

                self.limite+=1
                if self.limite>=20:
                    break
        
        timer = Timer(7.5, self.apagaBoton, args=("3"))
        timer.start()
    
    def ataqueEspecialMaximo(self, objetos_frame):
        """"
        En esta version, se hizo una simplificacion de la ulti del atacante,
        para cumplir en tiempo y forma con la entrega. Se hizo un ajuste del atauqe especial 21, que genera 
        mas daño
        """
        if not self.boton4:                
            self.boton4 = True            
            t1 = Thread(target=self.apuntar, args=(self, '4'))
            t1.start()
            while True: 
                if self.click:         
                    self.direccion_ataque = copy.copy(self.direccion)
                    self.angulo_giro = copy.copy(self.direccion)      
                    self.estado = "inmovil"              
                    e = Event()
                    succiona = Thread(target= self.succion, args=(e, 1.5, objetos_frame, 100))
                    succiona.start()
                    if not succiona.is_alive():
                        radio = 2
                        i = self.x-radio
                        while i<self.x+radio:
                            j = self.y-radio
                            while j<self.y+radio:
                                punto = str(i)+","+str(j)
                                if (objetos_frame[punto].__dict__["equipo"]!=self.equipo):
                                    objetos_frame[punto].__dict__["salud"]-= 650+((650/self.nivel_max)*self.bonus_ataque) 
                                j+=1
                            i+=1

                self.limite+=1
                if self.limite>=20:
                    break
            
        self.estado = "normal"
        timer = Timer(135, self.apagaBoton, args=("4"))
        timer.start() 

    def recibeGolpe(self, danio, efecto):
        """Daño y/o efecto recibidos"""
        self.salud-=danio
        #self.estado = efecto
        if self.salud<=0:
            self.estado = "Muerto"

    def reaparece(self):
        self.estado = "Normal"
        if self.equipo=='1':
            self.x = 0
            self.y = len(self.mapa)
        else:
            self.x = len(self.mapa[0])
            self.y = 0

    def revive(self):
        tiempo = ((self.nivel*100)*(0.15*e(5.15)*(self.nivel/100)))/300
        timer = Timer(tiempo, self.reaparece)
        timer.start() 
    
    def ganaExperiencia(self, exp):
        self.experiencia += exp
        topeNivel = (self.nivel*100)*(0.15*e(5.15)*(self.nivel/100))
        if self.experiencia >= (topeNivel) and self.nivel<self.nivel_max:
            self.nivel+=1
            self.bonus_ataque+=0.45
            self.salud_max = 10500*(1+(0.25*self.nivel))