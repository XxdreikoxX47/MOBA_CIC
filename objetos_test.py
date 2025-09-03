from time import time
from math import exp as e
#import multiprocessing
#from threading import Thread, Event, Timer
from scipy.spatial.distance import cityblock
class Base(object):
    def __init__(self, x=0, y=0, equipo=1, ID=0):
        self.ID = ID          
        self.type = "Base"        
        self.x = x
        self.y = y
        self.equipo = equipo
        self.salud = 100000 
        self.salud_max = 100000 
        self.multilabel=True    
        self.labels=["b1", "b2"]
        if equipo==1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1] 

class Torre(object):
    def __init__(self, x=0, y=0, equipo=1, ID=0):
        self.ID = ID        
        self.type = "Torre"        
        self.x = x
        self.y = y
        self.equipo = equipo 
        self.salud = 25000
        self.salud_max = 25000
        self.multilabel=True
        self.labels=["t1", "t2"]
        if equipo==1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1] 
        self.target = None
        self.limite = 0   
        self.boton1 = False
        self.attack_time = 0    
        self.esperaCuracion = 0
        self.mapa =  None 

    def revisaBotones(self):
        if self.attack_time>0:
            self.attack_time+=0.25

        if self.esperaCuracion>0:
            self.esperaCuracion+=0.25

        if self.attack_time>=1:
            self.apagaBoton('1')
            self.attack_time = 0
        
        if self.esperaCuracion>=30:
            self.esperaCuracion = 0

    def apagaBoton(self,Boton):
        if Boton=="1":
            self.boton1 = False                    
            
        self.limite = 0
        self.target = None

    def leeMapa(self, mapa):
        self.mapa= mapa
    
    def curacion(self):
        if self.salud <= int(self.salud_max*0.65):
            if not self.boton1=='1' and self.esperaCuracion==0:
                self.attack_time += 0.01
                self.esperaCuracion += 0.01
                self.boton1 = True
                self.salud+= int(self.salud_max*0.25)

    
    def Attack(self,objetos_frame):
        #La torre ataca al primer target que encuentre en su zona de vision
        #print("La torre esta en la posicion:", self.x, self.y)
        #print("La torre esta atacando...")
        radio_fils = 3
        radio_cols = 4
        detected = False
        cols = self.x-radio_cols
        while cols < self.x+radio_cols:
            fils = self.y-radio_fils
            while fils < self.y+radio_fils:
                if cols>0 and fils>0 and cols<len(self.mapa[0]) and fils<len(self.mapa):
                    ind = str(self.mapa[fils][cols]) #str(cols)+","+str(fils)
                    if ind in list(objetos_frame.keys()):
                       # #print("Revisando en ", ind)
                        if "Unidad" in objetos_frame[ind].__dict__["type"] and\
                        objetos_frame[ind].__dict__["equipo"]!= self.equipo:
                            self.target = ind 
                            detected = True
                fils+=1
            cols+=1
        if detected and not self.boton1:
            self.boton1 = True
            #print("La torre atacara al objeto",objetos_frame[self.target])
            objetos_frame[self.target].__dict__["salud"]-= 300
            self.attack_time += 1
            #print("Target despues del ataque", objetos_frame[self.target].__dict__)
            objetos_frame[self.target].recibeGolpe(300, None)
            #timer = Timer(1, self.apagaBoton, args=("1"))
            #timer.start() 
        #else:
            ###print("La torre no detecto enemigos")
            
class Arbusto(object):
    def __init__(self, x=0, y=0, ID=0):
        self.ID = ID        
        self.type = "Escondite indestructible"        
        self.x = x
        self.y = y        
        self.codificacion = "a"
        self.multilabel = False 

class Muro(object):
    def __init__(self, x=0, y=0, ID=0):
        self.ID = ID        
        self.type = "Estructura indestructible"        
        self.x = x
        self.y = y
        self.codificacion = "m" 
        self.multilabel = False

class Muro_destruible(object):
    def __init__(self, x=0, y=0, equipo=1, ID=0):
        self.ID = ID        
        self.type = "Estructura destructible"        
        self.x = x
        self.y = y
        self.salud = 5000
        self.salud_max = 5000
        self.multilabel = True
        self.labels = ["m_d1", "m_d2"]
        self.equipo = equipo
        if equipo==1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1] 

class Creep_normal(object):
    def __init__(self, x=0, y=0, equipo=1, portador=False, ID=0, linea="top"):
        self.ID = ID        
        self.type = "Unidad NPC"        
        self.x = x
        self.y = y
        self.salud = 750
        self.salud_max = 750
        self.equipo = equipo
        self.porta_llave = portador 
        self.multilabel = True
        self.labels=["cnt1", "cnt2"]
        if equipo==1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1] 
        self.target = None
        self.linea = linea
        self.boton1 = False
        self.attack_time = 0     

    def revisaBotones(self):
        
        if self.attack_time>0:
            self.attack_time+=0.25
        if self.attack_time>=1:
            self.apagaBoton('1')
            self.attack_time=0
        #if self.salud<=0:
        #    
    
    def apagaBoton(self,Boton):
        if Boton=="1":
            self.boton1 = False                    
            
        self.limite = 0
        self.target = None
    
    def creepMovement(self,objetos_frame, dims):
        #el creep se mueve bajo dos condiciones
        #
        # 1 cuando detecta a una unidad enemiga 
        # a una distancia manhattan igual o menor a 4
        ##print("Moviendo creep")
        radio =  4
        detected = False
        cols = self.x-radio
       # ##print("El agente busca un target")
        ###print("las columnas van de ", cols, "a ", self.x+radio)
        ###print("Las filas van de ", self.y-radio, "a ", self.y+radio)
        while cols < self.x+radio:
         #   ##print("cols", cols)
            fils = self.y-radio
            while fils < self.y+radio:
            #    ##print("fils", fils)
                if fils>0 and cols>0 and fils<dims[0] and cols<dims[1]:
                    ind = str(cols)+","+str(fils)
                    if ind in list(objetos_frame.keys()):
                        ###print("objetos frame:", objetos_frame)
                        if "Unidad" in objetos_frame[ind].__dict__["type"]:
                            if cityblock([objetos_frame[ind].__dict__["x"],objetos_frame[ind].__dict__["y"]],[fils,cols]) <=4 and objetos_frame[ind].__dict__["equipo"]!=self.equipo:
                                self.target = ind 
                                detected = True
                                break
                fils+=1
            cols+=1
        
        if not detected:
            #2 cuando no ha detetado un enemigo
            #se mueve sobre la linea asignada, hacia delante
            #Las lineas asignadas se identifican por medio de 
            #la siguiente lista
            # -top
            # -mid
            # -bottom
            
            ###print("Moviendo creep en linea:", self.linea)
            if self.linea=="top" and (self.y>4) and (self.y-1)>0:                        
                self.y-=1
            elif self.linea=="top" and (self.y<=4) and (self.x+1)<dims[1]:
                self.x+=1            
            elif self.linea=="mid" and (self.x+1)<dims[1]and (self.y-1)>0:
                self.x+=1
                self.y-=1
            elif self.linea=="bottom" and (self.x<dims[1]-4) and (self.x+1)<dims[1]:     
                self.x+=1
            elif self.linea=="bottom" and (self.x>=dims[1]-4) and (self.y-1)>0: 
                self.y-=1            
                    
        else:
            ##print("Se detecto un enemigo...")
            ind = self.target            
            #Se mueve hacia el target
            if self.y>objetos_frame[ind].__dict__["y"]:    
                self.y-=1            
            elif self.y<objetos_frame[ind].__dict__["y"]:
                self.y+=1            
            if self.x>objetos_frame[ind].__dict__["x"]:
                self.x-=1            
            elif self.x<objetos_frame[ind].__dict__["x"]:            
                self.x+=1            
            
            if not self.boton1 and cityblock([self.x, self.y], [objetos_frame[ind].__dict__["x"],objetos_frame[ind].__dict__["y"]]) <=2:
                ###print("Atacando target", objetos_frame[self.target].__dict__)
                objetos_frame[self.target].__dict__["salud"]-= 200
                self.boton1 = True
                self.attack_time  += 1
                ###print("Target despues del ataque", objetos_frame[self.target].__dict__)
    

class Medicina(object):
    def __init__(self, x=0, y=0, ID=0):
        self.ID = ID        
        self.type = "Objeto curativo un uso"        
        self.x = x
        self.y = y
        self.curativo = 2500
        self.codificacion = "med"
        self.multilabel = False

class Adrenalina(object):
    def __init__(self, x=0, y=0, ID=0):
        self.ID = ID        
        self.type = "Objeto acelerador un uso"        
        self.x = x
        self.y = y
        self.velocidad = 1.5
        self.codificacion = "ad"
        self.multilabel = False

class Llave_de_la_torre(object):
    def __init__(self, x=0, y=0, equipo=1, ID=0):
        self.ID = ID        
        self.type = "Llave"        
        self.x = x
        self.y = y
        self.equipo = equipo 
        self.multilabel=True
        self.labels=["tk1", "tk2"]
        if equipo==1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1] 

class A_Pasto(object):
    def __init__(self, x=0, y=0, ID=0):
        self.ID = ID        
        self.type = "Piso"        
        self.x = x
        self.y = y
        self.codificacion = "p"
        self.multilabel=False

# class Avatar_atacante1(object):
#     def __init__(self, x=0, y=0, equipo=1, ID=0):
#         self.ID = ID        
#         self.type = "Unidad jugable"        
#         self.x = x
#         self.y = y
#         self.equipo = equipo
#         self.salud = 7500
#         self.salud_max = 7500
#         self.nivel = 1 
#         self.nivel_max = 20
#         self.bonus_ataque = 0.5
#         self.porta_llave = False
#         self.multilabel=True
#         self.labels=["aat1", "aat2"]
#         if equipo==1:
#             self.codificacion = self.labels[0]
#         else:
#             self.codificacion = self.labels[1] 
                 
# class Avatar_defensivo1(object):
#     def __init__(self, x=0, y=0, equipo=1, ID=0):
#         self.ID = ID        
#         self.type = "Unidad jugable"        
#         self.x = x
#         self.y = y
#         self.equipo = equipo
#         self.salud = 14000
#         self.salud_max = 14000
#         self.nivel = 1 
#         self.nivel_max = 20
#         self.bonus_ataque = 0.3
#         self.porta_llave = False
#         self.multilabel=True
#         self.labels=["adt1", "adt2"]
#         if equipo==1:
#             self.codificacion = self.labels[0]
#         else:
#             self.codificacion = self.labels[1]                 

# class Avatar_soporte1(object):
#     def __init__(self, x=0, y=0, equipo=1, ID=0):
#         self.ID = ID        
#         self.type = "Unidad jugable"        
#         self.x = x
#         self.y = y
#         self.equipo = equipo 
#         self.salud = 12000
#         self.salud_max = 12000
#         self.nivel = 1 
#         self.nivel_max = 20
#         self.bonus_ataque = 0.3
#         self.porta_llave = False
#         self.multilabel=True
#         self.labels=["ast1", "ast2"]
#         if equipo==1:
#             self.codificacion = self.labels[0]
#         else:
#             self.codificacion = self.labels[1] 

# class Avatar_equilibrado1(object):
#     def __init__(self, x=0, y=0, equipo=1, ID=0):
#         self.ID = ID        
#         self.type = "Unidad jugable"        
#         self.x = x
#         self.y = y
#         self.equipo = equipo
#         self.salud = 10500
#         self.salud_max = 10500
#         self.nivel = 1 
#         self.nivel_max = 20
#         self.bonus_ataque = 0.35 
#         self.porta_llave = False
#         self.multilabel=True
#         self.labels=["aet1", "aet2"]
#         if equipo==1:
#             self.codificacion = self.labels[0]
#         else:
#             self.codificacion = self.labels[1] 

# class Avatar_jungla1(object):
#     def __init__(self, x=0, y=0, equipo=1, ID=0):
#         self.ID = ID
#         self.type = "Unidad jugable"        
#         self.x = x
#         self.y = y
#         self.equipo = equipo 
#         self.salud = 9500
#         self.salud_max = 9500
#         self.nivel = 1 
#         self.nivel_max = 20
#         self.bonus_ataque = 0.6
#         self.porta_llave = False
#         self.multilabel = True
#         self.labels=["ajt1", "ajt2"]
#         if equipo==1:
#             self.codificacion = self.labels[0]
#         else:
#             self.codificacion = self.labels[1] 

