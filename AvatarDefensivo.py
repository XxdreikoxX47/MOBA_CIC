import Agente
import objetos_test as MOBAobjs
import inspect
import copy
from time import time
from math import exp as e
#import multiprocessing
#from threading import Thread, Event, Timer
from scipy.spatial.distance import cityblock

class AvatarDefensivo(Agente.Agente):
    def __init__(self,x=0,y=0, equipo=1, ID=None):
        self.ID = ID
        self.type = "Unidad jugable"        
        self.x = x
        self.y = y
        self.equipo = equipo
        self.nivel = 10
        self.nivel_max = 20
        self.salud = 14000*(1+(0.25*self.nivel))
        self.salud_max = 14000*(1+(0.25*self.nivel))
        self.experiencia = 0        
        self.bonus_ataque = 0.3+(0.45*self.nivel)
        self.dist_basico = 2
        #self.dist_Torre_ant = 0
        self.estado = "Normal"
        self.porta_llave = False
        self.multilabel = True
        self.labels = ["adt1", "adt2"]
        if equipo ==1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1]
        self.direccion = 0
        #self.move = False
        self.fila_cursor = 0
        self.columna_cursor = 0
        self.fila_cursor_ataque = 0
        self.columna_cursor_ataque = 0
        self.danio_causado_Torre = 0
        self.click = False
        self.click_time = 0
        self.boton1 = False
        self.boton1_init = 0
        self.boton2 = False
        self.boton2_init = 0
        self.boton3 = False
        self.boton3_init = 0
        self.boton4 = False
        self.boton4_init = 0
        self.target = None
        self.limite = 0
        self.mapa = None
        self.tiempo_muerte = 0
        self.tiempo_espera = 0


    def direccionMov(self, angulo):
        self.direccion = angulo
    
    def mover(self):        
        #self.move = True        
        #Movimiento horizontal
        #Se mueve a la derecha
       # #print("\nMoviendo agente: ", self.codificacion)
        if self.estado!="Muerto":
            #self.move = True        
            #Movimiento horizontal
            #Se mueve a la derecha
            #print("\nMoviendo agente: ", self.codificacion)
            if ((self.direccion<90) or (self.direccion>270)) and self.x+1< len(self.mapa[0]):
                #if (objetos_frame[str(self.x+1)+","+str(self.y)].__dict__["codificacion"]=='p'):
                    #print("moviendose a la derecha")
                    self.x+= 1
            #Se mueve a la izquierda
            
            elif ((self.direccion>90 and self.direccion<=180) or (self.direccion>=180 and self.direccion<270)) and self.x-1>=0:
                #if (objetos_frame[str(self.x-1)+","+str(self.y)].__dict__["codificacion"]=='p'):
                    #print("moviendose a la izquierda")
                    self.x-= 1
            #movimiento vertical
            #Se mueve hacia arriba
            if (self.direccion>0 and self.direccion<180) and self.y-1 >=0:
                #if (objetos_frame[str(self.x)+","+str(self.y-1)].__dict__["codificacion"]=='p'):
                    #print("moviendose hacia arriba")
                    self.y-= 1
            #Se mueve hacia abajo
            elif (self.direccion>180 and self.direccion<360) and self.y+1<len(self.mapa):
                #if (objetos_frame[str(self.x)+","+str(self.y+1)].__dict__["codificacion"]=='p'):
                    #print("moviendose hacia abajo")
                    self.y+= 1


    def lecturaMapa(self, mapa):
        self.mapa = mapa

    def mueveCursor(self, fila, columna):
        self.fila_cursor = fila
        self.columna_cursor = columna        
    
    def apagaClick(self):
        self.click = False            

    def hacerClick(self, event=None):
        self.click = True
        self.click_time = 0
        #if event:
        #    event.set()
        #timer = Timer(0.25, self.apagaClick)
        #timer.start() 
    
    def revisaBotones(self):
        #now = time()
        self.danio_causado_Torre = 0 
        self.danio_causado = 0
        if self.click:
            self.click_time+=0.25
        
        if self.boton1:
            self.boton1_init+=0.25
        
        if self.boton2:
            self.boton2_init+=0.25
        
        if self.boton3:
            self.boton3_init+=0.25

        if self.boton4:
            self.boton4_init+=0.25
        
        if self.estado=="Muerto":
            self.tiempo_muerte+=0.25

        if self.click_time>=0.25:
            self.apagaClick        
        
        if self.boton1_init>=1:
            self.apagaBoton("1")

        if self.boton3_init>=6:
            self.apagaBoton("3")
        
        if self.boton4_init>=150:
            self.apagaBoton("4")

        if self.nivel<10:  
            if self.boton2_init>=4:
                self.apagaBoton("2")
            
        else:
            if self.boton2_init>=6.5:
                self.apagaBoton("2")            
        
        #Se revive el avatar                
        if self.estado == "Muerto":
            if self.tiempo_muerte>=self.tiempo_espera:
                self.reaparece()
    
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
        ##print("\nAvatar:", self.codificacion, " Ataque basico")
        if self.estado!="Muerto":
            while not self.boton1:                
                ####print("primer if, activando boton 1")
                self.boton1 = True
                self.boton1_init = 0
                #while True:
            #    #print("Buscando objetivo...")
                i = -self.dist_basico
                while i <= self.dist_basico:
                    j = -self.dist_basico
                    while j<= self.dist_basico:
            #            #print("Buscando objetivo en posicion:", self.y+j, self.x+i)
                        if self.x+i>=0 and self.y+j>=0 and self.x+i<len(self.mapa[0]) and self.y+j<len(self.mapa):                        
                            if [self.x+i,self.y+j]!=[self.x,self.y] and str(self.mapa[self.y+j][self.x+i]) in list(objetos_frame.keys()):      
            #                    #print("ID: ", str(self.mapa[self.y+j][self.x+i]))
            #                    #print("Objeto:", objetos_frame[str(self.mapa[self.y+j][self.x+i])])
                                if ("Unidad" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                    ("Torre" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                    ("Base" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                    ("Estructura destructible" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]):
                                #if ("Unidad" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) or \
                                #    ("destructible" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) and \
                                #        "indestructible" not in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]:
                                    ####print(objetos_frame[str(self.x+i)+","+str(self.y+j)])
                                    if (objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["equipo"]!=self.equipo):                                    
                                        if cityblock([self.x,self.y],[self.x+i,self.y+j])<=1:
                                            #self.target = str(self.x+i)+","+str(self.y+j)
                                            self.target = str(self.mapa[self.y+j][self.x+i])
            #                               #print("Target definido: ", self.target)
                                            break
                        j+=1
                    i+=1
                    #break
            
                if self.target:
            #       #print("Atacando target", objetos_frame[self.target].__dict__)
                    if ("Torre" in objetos_frame[self.target].__dict__["type"]):
                        self.danio_causado_Torre += (150+((150/self.nivel_max)*self.bonus_ataque)) /objetos_frame[self.target].__dict__["salud_max"]
                    objetos_frame[self.target].__dict__["salud"]-= 150+((150/self.nivel_max)*self.bonus_ataque)
            #       #print("Target despues del ataque", objetos_frame[self.target].__dict__)
            #   else:
            #        #print("No target")
            
            #timer = Timer(1, self.apagaBoton, args=("1"))
            #timer.start() 
    
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
        ##print("\nAvatar:", self.codificacion, " Ataque Especial Basico 1")
        if self.estado!="Muerto":
            if not self.boton2:                
                self.boton2 = True            
                self.boton2_init = 0            
                #t1 = Thread(target=self.apuntar, args=('2'))
                #t1.start()
                self.columna_cursor_ataque = copy.copy(self.columna_cursor) 
                self.fila_cursor_ataque = copy.copy(self.fila_cursor) 
                self.apuntar('2')
                #Se espera a que se de click en algun proceso                
                #Se mueve a la derecha        
                if self.columna_cursor_ataque>=self.x:
                    dir_empuje = "derecha"
                    minX = 0
                    maxX = 1
                    minY = -1
                    maxY = 1
                #Se mueve a la izquierda
                elif self.columna_cursor_ataque<self.x:
                    dir_empuje = "izquierda"
                    minX = -1
                    maxX = 0
                    minY = -1
                    maxY = 1              
                #movimiento vertical
                #Se mueve hacia arriba
                if self.fila_cursor_ataque<=self.y:
                    dir_empuje = "arriba"                
                    minX = -1
                    maxX = 1
                    minY = -1
                    maxY = 0
                #Se mueve hacia abajo
                elif self.fila_cursor_ataque>self.y:
                    dir_empuje = "abajo"                
                    minX = -1
                    maxX = 1
                    minY = 0
                    maxY = 1

            # while True: 
                    ####print("comenzando ataque")
                if self.click:
                    ####print("Se hizo click")
                    #Movimiento horizontal        
                    i = minX
                    while i<=maxX:                                                                       
                        j = minY
                        while j<=maxY:                         
                            if self.x+i>=0 and self.y+j>=0 and self.x+i<len(self.mapa[0]) and self.y+j<len(self.mapa):                        
                                if str(self.mapa[self.y+j][self.x+i]) in list(objetos_frame.keys()):   
                                ####print("Buscando target en posicion: ", str(self.x+i)+","+str(self.y+j))
                                    if ("Unidad" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Torre" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Base" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Estructura destructible" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]):
                                    #if "Unidad" in (objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) or \
                                    #"Estructura destructible" == (objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]): 
                                            ####print(objetos_frame[str(self.x+i)+","+str(self.y+j)])
                                        if (objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["equipo"]!=self.equipo)\
                                            and cityblock([self.x, self.y], [self.x+i,self.y+j])<=1:
                                            ####print("Añadiendo target: ",objetos_frame[str(self.x+i)+","+str(self.y+j)])
                                            targets.append(str(self.mapa[self.y+j][self.x+i]))
                                            #targets.append(objetos_frame[self.mapa[self.x+addX][self.y+addY]].__dict__["objID"])
                            j+=1
                        i+=1
                #    break                                               
                        
                if len(targets)>0:
                    for t in targets:
                        ##print("Atacando target", objetos_frame[t].__dict__)
                        objetos_frame[t].__dict__["salud"]-= 250+((250/self.nivel_max)*self.bonus_ataque)
                        ##print("Moviendo target a la direccion:", dir_empuje)
                        if "Torre" not in objetos_frame[t].__dict__["type"] and "Base" not in objetos_frame[t].__dict__["type"]:
                            if dir_empuje == "derecha":
                                objetos_frame[t].__dict__["x"]+=2                        
                            if dir_empuje == "izquierda":
                                objetos_frame[t].__dict__["x"]-=2
                            if dir_empuje == "arriba":
                                objetos_frame[t].__dict__["y"]-=2
                            if dir_empuje == "abajo":
                                objetos_frame[t].__dict__["y"]+=2
                        elif "Torre" in objetos_frame[t].__dict__["type"]:
                            self.danio_causado_Torre += (250+((250/self.nivel_max)*self.bonus_ataque)) /objetos_frame[t].__dict__["salud_max"]
                        ##print("Target despues del ataque", objetos_frame[t].__dict__)
        #        else:
                    ##print("No target")
            
            #timer = Timer(4, self.apagaBoton, args=("2"))
            #timer.start() 
    
    def stopHPBoost(self, boost):
        self.salud/=boost
        #self.salud_max/=boost


    def ataqueEspecialBasico2(self,objetos_frame):   
        ##print("\nAvatar:", self.codificacion, " Ataque Especial Basico 2")     
        if self.estado!="Muerto":
            if not self.boton3:
                if self.salud < self.salud_max*1.85:                
                    self.boton3 = True  
                    self.boton3_init = 0
                    self.salud*=1.15          
            ##print("El avatar se ha sanado")
            #self.salud_max*=1.15
         #   t1 = Timer(3, self.stopHPBoost, args=(1.15))
          #  t1.start()                                
        
        #timer = Timer(6, self.apagaBoton, args=("3"))
        #timer.start()
    
    def ataqueEspecial11(self, objetos_frame):
        """
        En esta primera version el ataque básico 2 no considera el efecto de 'ralentizacion' que
        debería provocar a las unidades no aliadas que alcanza. 
        """
        #print("\nAvatar:", self.codificacion, " Ataque Especial 11")     
        if self.estado!="Muerto":
            targets= []
            if not self.boton2:                
                self.boton2 = True  
                self.boton2_init = 0          
                self.apuntar('2')
                #t1 = Thread(target=self.apuntar, args=('2'))
                #t1.start()
                self.columna_cursor_ataque = copy.copy(self.columna_cursor) 
                self.fila_cursor_ataque = copy.copy(self.fila_cursor) 
                if self.columna_cursor_ataque>=self.x:
                    dir_empuje = "derecha"
                    minX = 0
                    maxX = 1
                    minY = -1
                    maxY = 1
                #Se mueve a la izquierda
                elif self.columna_cursor_ataque<self.x:
                    dir_empuje = "izquierda"
                    minX = -1
                    maxX = 0
                    minY = -1
                    maxY = 1              
                #movimiento vertical
                #Se mueve hacia arriba
                if self.fila_cursor_ataque<self.y:
                    dir_empuje = "arriba"                
                    minX = -1
                    maxX = 1
                    minY = -1
                    maxY = 0
                #Se mueve hacia abajo
                elif self.fila_cursor_ataque>=self.y:
                    dir_empuje = "abajo"                
                    minX = -1
                    maxX = 1
                    minY = 0
                    maxY = 1
                #Se espera a que se de click en algun proceso                
                #while True: 
                    ####print("comenzando ataque")
                if self.click:
                    ####print("Se hizo click")
                    #Movimiento horizontal        
                    i = minX
                    while i<=maxX:                                                                       
                        j = minY
                        while j<=maxY:
                            if self.x+i>=0 and self.y+j>=0 and self.x+i<len(self.mapa[0]) and self.y+j<len(self.mapa):                        
                                if str(self.mapa[self.y+j][self.x+i]) in list(objetos_frame.keys()):                     
                                    ####print("Buscando target en posicion: ", str(self.x+i)+","+str(self.y+j))
                                    if ("Unidad" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Torre" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Base" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Estructura destructible" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]):
                                #if "Unidad" in (objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) or \
                                #"Estructura destructible" in (objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]): 
                                        ####print(objetos_frame[str(self.x+i)+","+str(self.y+j)])
                                        if (objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["equipo"]!=self.equipo)\
                                            and cityblock([self.x, self.y], [self.x+i,self.y+j])<=1:
                                            ####print("Añadiendo target: ",objetos_frame[str(self.x+i)+","+str(self.y+j)])
                                            targets.append(str(self.mapa[self.y+j][self.x+i]))
                                            #targets.append(objetos_frame[self.mapa[self.x+addX][self.y+addY]].__dict__["objID"])
                            j+=1
                        i+=1
                        #break                                                                        
                
            
                if len(targets)>0:
                    for t in targets:
                        #print("Atacando target", objetos_frame[t].__dict__)
                        objetos_frame[t].__dict__["salud"]-= 350+((350/self.nivel_max)*self.bonus_ataque)
                        #print("Moviendo target a la direccion:", dir_empuje)
                        if "Torre" not in objetos_frame[t].__dict__["type"] and "Base" not in objetos_frame[t].__dict__["type"]:
                            if dir_empuje == "derecha":
                                i=0
                                while i <4 and objetos_frame[t].__dict__["x"]+1<15:
                                    objetos_frame[t].__dict__["x"]+=1
                                    i+=1
                            if dir_empuje == "izquierda":
                                i=0
                                while i <4 and objetos_frame[t].__dict__["x"]-1>0:
                                    objetos_frame[t].__dict__["x"]-=1
                                    i+=1
                            if dir_empuje == "arriba":
                                i=0
                                while i <4 and objetos_frame[t].__dict__["y"]-1>0:
                                    objetos_frame[t].__dict__["y"]-=1
                                    i+=1
                            if dir_empuje == "abajo":
                                i=0
                                while i <4 and objetos_frame[t].__dict__["y"]+1<13:
                                    objetos_frame[t].__dict__["y"]+=1
                                    i+=1
                        elif "Torre" in objetos_frame[t].__dict__["type"]:
                            self.danio_causado_Torre += (350+((350/self.nivel_max)*self.bonus_ataque)) /objetos_frame[t].__dict__["salud_max"]
                        ####print("Target despues del ataque", objetos_frame[t].__dict__)
            
            #timer = Timer(6.5, self.apagaBoton, args=("2"))
            #timer.start() 

    def ataqueEspecial21(self, objetos_frame):
        """
        En esta primera version el ataque especial 21 no considera el efecto de 'congelamiento' que
        debería provocar a las unidades no aliadas que alcanza. 
        """
        #print("\nAvatar:", self.codificacion, " Ataque Especial 21")     
        tries = 0
        while not self.boton3:                            
            self.boton3 = True
            self.boton3_init = 0
            while not self.target and tries<25:                
                i = -1
                while self.x+i <=self.x+1:
                    j=-1
                    while self.y+j<=self.y+1:
                        if self.x+i>=0 and self.y+j>=0 and self.x+i<len(self.mapa[0]) and self.y+j<len(self.mapa):                        
                            if [self.x+i,self.y+j]!=[self.x,self.y]:
                                if str(self.mapa[self.y+j][self.x+i]) in list(objetos_frame.keys()):                            
                                    if ("Unidad" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Torre" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Base" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Estructura destructible" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]):
                                # if ("Unidad" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) or \
                                    #    ("Estructura destructible" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) and \
                                    #       "indestructible" not in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]:
                                        
                                        if (objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["equipo"]!=self.equipo):                                    
                                            if cityblock([self.x,self.y],[self.x+i,self.y+j])<=1:
                                                self.target = str(self.mapa[self.y+j][self.x+i])
                                                #self.target = str(self.x+i)+","+str(self.y+j)                                        
                                                break
                        j+=1
                    i+=1
                tries+=1
        
            if self.target:
                #print("Atacando target", objetos_frame[self.target].__dict__)
                objetos_frame[self.target].__dict__["salud"]-= 350+((350/self.nivel_max)*self.bonus_ataque)
                if "Torre" in objetos_frame[self.target].__dict__["type"]:
                    self.danio_causado_Torre += (250+((250/self.nivel_max)*self.bonus_ataque)) /objetos_frame[self.target].__dict__["salud_max"]
                #print("Target despues del ataque", objetos_frame[self.target].__dict__)
        #timer = Timer(4.5, self.apagaBoton, args=("3"))
        #timer.start() 
    
    def ataqueEspecialMaximo(self, objetos_frame):
        """"
        En esta version, se hizo una simplificacion de la ulti del atacante,
        para cumplir en tiempo y forma con la entrega. Se hizo un ajuste del atauqe especial 21, que genera 
        mas daño
        """
        #print("Avatar:", self.codificacion, " Ataque Especial Maximo")
        clases = []
        for name,obj in inspect.getmembers(MOBAobjs):
            #####print(name,type(obj))
            if inspect.isclass(obj) :
                clases.append(obj)
        i=0
        while i<len(clases):
            if clases[i]== MOBAobjs.Muro_destruible:
                constructor_muro = clases[i]
                muro = clases[i](equipo=self.equipo)
            i+=1
        
        minCol = 0
        maxCol = 8
        minFil = 0
        maxFil = 8

        if not self.boton4:                
            self.boton4 = True            
            self.boton4_init = 0
            self.apuntar('4')
            #t1 = Thread(target=self.apuntar, args=('4'))
            #t1.start()
             #Se mueve a la derecha
            if self.columna_cursor>self.y:
                dir = [0,1]                
                minCol = self.x+1
                maxCol = self.x+1
                minFil = self.y-3
                maxFil = self.y+3                                
                
            #Se mueve a la izquierda
            elif self.columna_cursor<self.y:                
                dir = [0,-1]               
                minCol = self.x-1
                maxCol = self.x-1
                minFil = self.y-3
                maxFil = self.y+3              

            #movimiento vertical
            #Se mueve hacia arriba
            if self.fila_cursor<self.x:
                dir = [-1,0]                                
                minCol = self.x-3
                maxCol = self.x+3
                minFil = self.y-1
                maxFil = self.y-1

            #Se mueve hacia abajo
            elif self.fila_cursor>self.x:                
                dir = [1,0]            
                minCol = self.x-3
                maxCol = self.x+3
                minFil = self.y+1
                maxFil = self.y+1        
            ##print("Construyendo muro...")
            i=minFil
            while i <=maxFil:
                j=minCol
                while j<= maxCol:
                    if i>=0 and j>=0 and i<len(self.mapa) and j<len(self.mapa[0]):                    
                        if(self.mapa[i][j]=='p' and objetos_frame[str(self.mapa[i][j])].type=="Piso"):                        
                            #label = copy.copy(self.mapa[i][j])
                            #obj = copy.copy(objetos_frame[str(j)+","+str(i)])
                            #changed = False
                        # ####print("Moviendo objeto:", obj)
                            #k=1
                            #while not changed:
                                #if(self.mapa[i+(dir[0]*k)][j+(dir[1]*k)]=='p'):
                                    #obj.__dict__["x"] = j+(dir[1]*k)
                                    #obj.__dict__["y"] = i+(dir[0]*k)
                                    #####print("")
                                    #objetos_frame[str(j+(dir[1]*k))+","+str(i+(dir[0]*k))] = obj                                    
                                    #self.mapa[i+(dir[0]*k)][j+(dir[1]*k)] = label               
                                    #if self.objetos_frame[str(y)+","+str(x)].type == "Unidad jugable":
                                     #   self.agentes.append(str(y)+","+str(x))
                                     #   self.frames_agentes[str(y)+","+str(x)] = np.zeros([5*7*9])
                                    #if self.objetos_frame[str(y)+","+str(x)].type == "Unidad NPC":
                                     #   self.creeps.append(str(y)+","+str(x))
                                    #if self.objetos_frame[str(y)+","+str(x)].type == "Torre":
                                     #   self.torre = str(y)+","+str(x)          
                                    #changed = True
                                #k+=1
             #       ####print("Agregando muro en la posicion", str(j)+","+str(i))
                            objetos_frame[str(self.mapa[i][j])] = constructor_muro(x=j, y=i, equipo= self.equipo)
                            self.mapa[i][j] = muro.codificacion
                    j+=1
                i+=1
        #   ESTA FUNCION NO CONSIDERA COSAS COMO ESTRUCTURAS INAMOVIBLES, DEBE SER REFINADA EN FUTURAS VERSIONES
        
     #   ##print("Mapa modificado...")
     #   for m in self.mapa:
     #       ##print(m)
        #timer = Timer(150, self.apagaBoton, args=("4"))
        #timer.start() 

    def recibeGolpe(self, danio, efecto):
        """Daño y/o efecto recibidos"""
        self.salud-=danio
        #self.estado = efecto
        if self.salud<=0:
            print("El avatar defensivo murio")
            self.estado = "Muerto"
            self.x = 0
            self.y = 0
            self.tiempo_muerte = 0
            self.tiempo_espera = ((self.nivel*100)*(0.15*e(5.15)*(self.nivel/100)))/300

    def reaparece(self):
        self.estado = "Normal"
        if self.equipo=='1':
            self.x = 0
            self.y = len(self.mapa)-1
        else:
            self.x = len(self.mapa[0])-1
            self.y = 0

    #def revive(self):
    #    tiempo = ((self.nivel*100)*(0.15*e(5.15)*(self.nivel/100)))/300
     #   timer = Timer(tiempo, self.reaparece)
     #   timer.start() 
    
    def ganaExperiencia(self, exp):
        self.experiencia += exp
        topeNivel = (self.nivel*100)*(0.15*e(5.15)*(self.nivel/100))
        if self.experiencia >= (topeNivel) and self.nivel<self.nivel_max:
            self.nivel+=1
            self.bonus_ataque+=0.45
            self.salud_max = 14000*(1+(0.25*self.nivel))