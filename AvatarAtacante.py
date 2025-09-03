import Agente
import pygame
from Textos import DamageText
import constante_1
from time import time
from math import exp as e
#import multiprocessing
#from threading import Thread, Event, Timer
from scipy.spatial.distance import cityblock
import copy

class AvatarAtacante(Agente.Agente):
    def __init__(self, x=0, y=0, equipo=1, ID=None):
        self.ID = ID
        self.type = "Unidad jugable"        
        self.x = x
        self.y = y
        self.equipo = equipo
        self.nivel = 10
        self.nivel_max = 20
        self.salud = 7500 * (1 + (0.25 * self.nivel))
        self.salud_max = 7500 * (1 + (0.25 * self.nivel))
        self.experiencia = 0        
        self.bonus_ataque = 0.5 + (0.5 * self.nivel)
        self.estado = "Normal"
        self.dist_basico = 3
        self.porta_llave = False
        self.multilabel = True
        self.labels = ["aat1", "aat2"]
        if equipo == 1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1]
        self.direccion = 0
        self.fila_cursor = 0
        self.columna_cursor = 0
        self.fila_cursor_ataque = 0
        self.columna_cursor_ataque = 0
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
        self.danio_causado = 0
        self.danio_causado_Torre = 0
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
         #   event.set()
        #timer = Timer(0.25, self.apagaClick)
        #timer.start() 

    def revisaBotones(self):
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
        
        if self.boton4_init>=125:
            self.apagaBoton("4")

        if self.nivel<10:  
            if self.boton2_init>=4:
                self.apagaBoton("2")
            
        else:
            if self.boton2_init>=5.5:
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
        self.danio_causado = 0
    """
    Se debe hacer el cambio en el codigo de los ataques para ajustar al funcionamiento establecido en el "ataqueBasico", donde el 
    target se define como un cadena "fila(y), columna(x)" 
    """
    def ataqueBasico(self, objetos_frame):
       # #print("\nAvatar:", self.codificacion, " Ataque basico")
        ##print("El avatar esta en la posicion:", self.x, self.y)
        if self.estado!="Muerto":
            while not self.boton1:                
                ##print("primer if, activando boton 1")
                self.boton1 = True
                self.boton1_init = 0
                #while not self.target:
            #   #print("Buscando objetivo...")
                i = -self.dist_basico
                while i <= self.dist_basico:
                    j=-self.dist_basico
                    while j<=self.dist_basico:
                        if self.x+i>=0 and self.y+j>=0 and self.x+i<len(self.mapa[0]) and self.y+j<len(self.mapa):
            #              #print("Buscando objetivo en posicion:", self.x+i, self.y+j)
                            if [self.x+i,self.y+j]!=[self.x,self.y]:
                                if str(self.mapa[self.y+j][self.x+i]) in list(objetos_frame.keys()):                            
                                    #if str(self.x+i)+","+str(self.y+j) in list(objetos_frame.keys()):
            #                     #print("ID: ", str(self.mapa[self.y+j][self.x+i]))
                #                    #print("Objeto:", objetos_frame[str(self.mapa[self.y+j][self.x+i])])
                                    if ("Unidad" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Torre" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Base" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]) or \
                                        ("Estructura destructible" in objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["type"]):
                                    #if ("Unidad" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) or \
                                    #   ("Estructura destructible" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) and \
                                    #      "indestructible" not in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]:
                            #           ####print("objeto:",str(self.x+i),",",str(self.y+j),":",objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__)
                                        if (objetos_frame[str(self.mapa[self.y+j][self.x+i])].__dict__["equipo"]!=self.equipo):     
                                        # ####print("Si es del equipo contrario")                              
                                            #####print("La distancia es:", cityblock([self.x,self.y],[self.x+i,self.y+j]))
                                            if cityblock([self.x,self.y],[self.x+i,self.y+j])<=self.dist_basico:
                                                self.target = str(self.mapa[self.y+j][self.x+i])
                #                           #print("Target definido: ", self.target)
                                            break
                                        #else:
                                            #   ####print("No esta dentro del rango :(")
                        j+=1
                    i+=1
            # if not self.target:
            #     #print("No se encontro objetivo")
            #     break
            
                if self.target:
                #    #print("Atacando target", objetos_frame[self.target].__dict__)
                    if ("Torre" in objetos_frame[self.target].__dict__["type"]):
                        self.danio_causado_Torre += (125+((125/self.nivel_max)*self.bonus_ataque))/objetos_frame[self.target].__dict__["salud_max"]
                    objetos_frame[self.target].__dict__["salud"]-= 125+((125/self.nivel_max)*self.bonus_ataque)
                    self.danio_causado += (125+((125/self.nivel_max)*self.bonus_ataque))/objetos_frame[self.target].__dict__["salud_max"]
                #   #print("Target despues del ataque", objetos_frame[self.target].__dict__)
            
            #timer = Timer(1, self.apagaBoton, args=("1"))
            #timer.start() 
    
    def apuntar(self, Boton=None):
        print("Apuntando con botón:", Boton)
        if self.estado != "Muerto":
            while not self.click:
                if Boton == "1":
                    self.boton1 = True
                elif Boton == "2":
                    self.boton2 = True
                elif Boton == "3":
                    self.boton3 = True
                else:
                    self.boton4 = True
                self.click = True  # Asegurar que se haga click para no esperar indefinidamente
                print(f"Botón {Boton} presionado, click establecido.")
                                    
    def ataqueEspecialBasico1(self, objetos_frame):
        print("\nAvatar:", self.codificacion, "realizando ataque especial básico 1")
        if self.estado != "Muerto":
            while not self.boton2:
                self.boton2 = True
                self.boton2_init = 0
                proyectil = [self.x, self.y]
                self.apuntar('2')
                self.columna_cursor_ataque = copy.copy(self.columna_cursor)
                self.fila_cursor_ataque = copy.copy(self.fila_cursor)
                modx = 0
                mody = 0
                if self.columna_cursor_ataque > self.x:
                    modx = 1
                elif self.columna_cursor_ataque <= self.x:
                    modx = -1
                if self.fila_cursor_ataque <= self.y:
                    mody = -1
                elif self.fila_cursor_ataque > self.y:
                    mody = 1

                print("Esperando a que se haga click para el ataque especial...")
                while True:
                    if self.click:
                        print("Se hizo click, procediendo con el ataque especial.")
                        tries = 0
                        while cityblock([self.x, self.y], proyectil) <= 3 and tries < 25:
                            print(f"Proyectil en posición: {proyectil}, Intentos: {tries}")
                            if 0 <= proyectil[1] < len(self.mapa) and 0 <= proyectil[0] < len(self.mapa[0]):  # Verificar los límites
                                if str(self.mapa[proyectil[1]][proyectil[0]]) in list(objetos_frame.keys()):
                                    if ("Unidad" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]) or \
                                       ("Torre" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]) or \
                                       ("Base" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]) or \
                                       ("Estructura destructible" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]):
                                        if (objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["equipo"] != self.equipo) and cityblock([self.x, self.y], proyectil) <= 3:
                                            print("Objetivo encontrado en:", proyectil)
                                            self.target = str(self.mapa[proyectil[1]][proyectil[0]])
                                            break
                            else:
                                print(f"Proyectil fuera de los límites en posición: {proyectil}")
                                break
                            proyectil[0] += modx
                            proyectil[1] += mody
                            tries += 1
                        break

                if self.target:
                    if ("Torre" in objetos_frame[self.target].__dict__["type"]):
                        self.danio_causado_Torre += (375 + ((375 / self.nivel_max) * self.bonus_ataque)) / objetos_frame[self.target].__dict__["salud_max"]
                    objetos_frame[self.target].__dict__["salud"] -= 375 + ((375 / self.nivel_max) * self.bonus_ataque)
                    self.danio_causado += (375 + ((375 / self.nivel_max) * self.bonus_ataque)) / objetos_frame[self.target].__dict__["salud_max"]
                    print("Target después del ataque", objetos_frame[self.target].__dict__)
                else:
                    print("No se encontró objetivo")


    
    def ataqueEspecialBasico2(self, objetos_frame):
        """
        En esta primera version el ataque básico 2 no considera el efecto de 'inmobilizacion' que
        debería provocar a las unidades no aliadas que alcanza. 
        """
        ##print("\nAvatar:", self.codificacion, " Ataque Especial Basico 2")
        if not self.boton3:                
            self.boton3 = True
            self.boton3_init = 0
            proyectil = [self.x,self.y]
            self.apuntar('3')
            #t1 = Thread(target=self.apuntar, args=('3'))
            #t1.start()
            self.columna_cursor_ataque = copy.copy(self.columna_cursor) 
            self.fila_cursor_ataque = copy.copy(self.fila_cursor) 
             #Se mueve a la derecha
            modx = 0
            mody = 0
            if self.columna_cursor_ataque>self.y:
                mody = 1
            #Se mueve a la izquierda
            elif self.columna_cursor_ataque<self.y:
                mody = -1
            #movimiento vertical
            #Se mueve hacia arriba
            if self.fila_cursor_ataque<self.x:
                modx = -1
            #Se mueve hacia abajo
            elif self.fila_cursor_ataque>self.x:
                modx = 1
            #Se espera a que se de click en algun proceso                
          #  while True: 
                ####print("Comenzando ataque")
            if self.click:
                #Movimiento horizontal
                ####print("Se hizo click")
                tries = 0
                while cityblock([self.x,self.y],proyectil)<=3 and tries<25 and proyectil[0]>=0 and proyectil[1]>=0 and proyectil[0]<len(self.mapa[0]) and proyectil[1]<len(self.mapa):     
                    if str(self.mapa[proyectil[1]][proyectil[0]]) in list(objetos_frame.keys()):
                        if ("Unidad" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]) or \
                            ("Torre" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]) or \
                            ("Base" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]) or \
                            ("Estructura destructible" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]):
                    ####print("Recorrido del proyectil:", str(proyectil[0])+','+str(proyectil[1]))                                          
                    #if "Unidad" in (objetos_frame[str(proyectil[0]) + "," + str(proyectil[1])].__dict__["type"]) or \
                        #"Estructura destructible" in (objetos_frame[str(proyectil[0]) + "," + str(proyectil[1])].__dict__["type"]): 
                            ####print("En el camino del proyectil:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                            #  ####print(objetos_frame[str(proyectil[0]) + "," + str(proyectil[1])])
                            if (objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["equipo"]!=self.equipo)\
                                and cityblock([self.x,self.y],proyectil)<=3:
                                ####print("Objetivo:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                                self.target = str(self.mapa[proyectil[1]][proyectil[0]])
                                #self.target = objetos_frame[self.mapa[proyectil[0]][proyectil[1]]].__dict__["objID"]
                                break
                    proyectil[0]+=modx; proyectil[1]+=mody
                    tries+=1
               # break
               # self.limite+=1
                #if self.limite>=20:
                 #   break
      
            if self.target:
                ##print("Atacando target", objetos_frame[self.target].__dict__)
                if ("Torre" in objetos_frame[self.target].__dict__["type"]):
                    self.danio_causado_Torre += (375+((375/self.nivel_max)*self.bonus_ataque))/objetos_frame[self.target].__dict__["salud_max"]
                objetos_frame[self.target].__dict__["salud"]-= 250+((250/self.nivel_max)*self.bonus_ataque)
                self.danio_causado += (375+((375/self.nivel_max)*self.bonus_ataque))/objetos_frame[self.target].__dict__["salud_max"]
                ##print("Target despues del ataque", objetos_frame[self.target].__dict__)

            #else:
                ##print("No target") 

        #timer = Timer(6, self.apagaBoton, args=("3"))
        #timer.start()
    
    def ataqueEspecial11(self, objetos_frame):
        """
        En esta primera version el ataque básico 2 no considera el efecto de 'ralentizacion' que
        debería provocar a las unidades no aliadas que alcanza. 
        """
        #print("\nAvatar:", self.codificacion, " Ataque Especial 11")
        if self.estado!="Muerto":
            if not self.boton2:                
                self.boton2 = True
                self.boton2_init = 0
                proyectil = [self.x,self.y]
                self.apuntar('2')
                #t1 = Thread(target=self.apuntar, args=('2'))
                #t1.start()
                self.columna_cursor_ataque = copy.copy(self.columna_cursor) 
                self.fila_cursor_ataque = copy.copy(self.fila_cursor) 
                #Se mueve a la derecha
                modx = 0
                mody = 0
                if self.columna_cursor_ataque>=self.y:
                    mody = 1
                #Se mueve a la izquierda
                elif self.columna_cursor_ataque<self.y:
                    mody = -1
                #movimiento vertical
                #Se mueve hacia arriba
                if self.fila_cursor_ataque<self.x:
                    modx = -1
                #Se mueve hacia abajo
                elif self.fila_cursor_ataque>=self.x:
                    modx = 1
                #Se espera a que se de click en algun proceso                
                #while True: 
                    #####print("Comenzando ataque")
                if self.click:
                    ####print("Se hizo click")
                    #Movimiento horizontal
                    while cityblock([self.x,self.y],proyectil)<=3:
                        if proyectil[0]>=0 and proyectil[1]>=0 and proyectil[0]<len(self.mapa[0]) and proyectil[1]<len(self.mapa):     
                            if str(self.mapa[proyectil[1]][proyectil[0]]) in list(objetos_frame.keys()):
                                ####print("Recorrido del proyectil:", str(proyectil[0])+','+str(proyectil[1]))
                                if ("Unidad" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]) or \
                                    ("Torre" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]) or \
                                    ("Base" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]) or \
                                    ("Estructura destructible" in objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["type"]):
                                #if "Unidad" in (objetos_frame[str(proyectil[0]) + "," + str(proyectil[1])].__dict__["type"]) or \
                                #"Estructura destructible" in (objetos_frame[str(proyectil[0]) + "," + str(proyectil[1])].__dict__["type"]): 
                                        ####print("En el camino del proyectil:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                                    if (objetos_frame[str(self.mapa[proyectil[1]][proyectil[0]])].__dict__["equipo"]!=self.equipo)\
                                        and cityblock([self.x,self.y],proyectil)<=3:
                                        ####print("Objetivo:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                                        self.target = str(self.mapa[proyectil[1]][proyectil[0]])
                                        #self.target = objetos_frame[self.mapa[proyectil[0]][proyectil[1]]].__dict__["objID"]
                                        break
                        proyectil[0]+=modx; proyectil[1]+=mody                        
                        #break
                    #self.limite+=1
                    #if self.limite>=20:
                    #   break
                

    ###           HAY QUE ADAPTAR TODOS LOS ATAQUES PARA QUE FUNCIONEN CON LA LECTURA EN PARALELO DEL MAPA, MISMO QUE SE GUARDARA EN
    ###           SELF.MAPA O SELF.OBJETOS_FRAME, PERO NO PUEDE SER UNA ENTRADA A LA FUNCIÓN, O SERÍA ESTATICO, ES DECIR, NO DETECTARÍA
    ###           LAS ACTUALIZACIONES CADA 0.25S DEL FRAME 

    ###            NO ES NECESARIO HACERLO A MANO, EN PYTHON EL APUNTADOR A LA LISTA DE OBJETOS HACE QUE LA MODIFICACIÓN DESDE LAS FUNCIONES DEL 
    ###            OBJETO MODIFIQUE TAMBIÉN LA LISTA ORIGINAL

    ###           Hay que sincronizar bien el "while True" para que espere unicamente

                if self.target:
                    #print("Atacando target", objetos_frame[self.target].__dict__)
                    if ("Torre" in objetos_frame[self.target].__dict__["type"]):
                        self.danio_causado_Torre += (400+((400/self.nivel_max)*self.bonus_ataque))/objetos_frame[self.target].__dict__["salud_max"]
                    objetos_frame[self.target].__dict__["salud"]-= 400+((400/self.nivel_max)*self.bonus_ataque)
                    self.danio_causado += (400+((400/self.nivel_max)*self.bonus_ataque))/objetos_frame[self.target].__dict__["salud_max"]
                    #print("Target despues del ataque", objetos_frame[self.target].__dict__)
                #else:
                    ####print("No target")
            
            #timer = Timer(5.5, self.apagaBoton, args=("2"))
            #timer.start()

    def ataqueEspecial21(self, objetos_frame, damage_text_group, font):
        """
        Ataque especial en área con explosión.
        """
        if self.estado != "Muerto":
            targets = []
            if not self.boton3:
                self.boton3 = True
                self.boton3_init = 0
                radio = 2
                self.apuntar('3')
                
                if self.click:
                    fila = -radio
                    while fila <= radio:
                        col = -radio
                        while col <= radio:
                            if cityblock([self.x, self.y], [self.x + col, self.y + fila]) <= 2:
                                if (0 <= self.y + fila < len(self.mapa) and
                                    0 <= self.x + col < len(self.mapa[0])):
                                    
                                    obj_key = str(self.mapa[self.y + fila][self.x + col])
                                    if obj_key in objetos_frame:
                                        obj = objetos_frame[obj_key]
                                        if any(tipo in obj.type for tipo in ["Unidad", "Torre", "Base", "Estructura destructible"]):
                                            if obj.equipo != self.equipo:
                                                targets.append(obj)
                            col += 1
                        fila += 1
                
                if targets:
                    for obj in targets:
                        daño = 250 + ((250 / 20) * self.bonus_ataque)
                        obj.salud -= daño
                        self.danio_causado += daño / obj.salud_max
                        
                        # Crear texto flotante del daño
                        damage_text = DamageText(obj.forma.centerx, obj.forma.top, str(int(daño)), font, constante_1.ROJO)
                        damage_text_group.add(damage_text)
                
                # Reset del botón después de unos segundos
                pygame.time.set_timer(pygame.USEREVENT + 1, 6000, True)
        
    
    def ataqueEspecialMaximo(self, objetos_frame):
        """"
        En esta version, se hizo una simplificacion de la ulti del atacante,
        para cumplir en tiempo y forma con la entrega. Se hizo un ajuste del atauqe especial 21, que genera 
        mas daño 750 y se amplia el radio a 5
        """
        #print("Avatar:", self.codificacion, " Ataque Especial Maximo")
        if self.estado!="Muerto":
            targets = []
            if not self.boton4:                
                self.boton4 = True
                self.boton4_init = 0
                radio = 5
                self.apuntar('4')
                #t1 = Thread(target=self.apuntar, args=('4'))
                #t1.start()
                #Se espera a que se de click en algun proceso                
                #while True:                 
                    #El click es un proceso que sucede en paralelo
                if self.click:# or self.boton3:
                    ####print("Se hizo click")
                    fila = -radio
                    while fila <=+radio:                    
                        col = -radio
                        while col<=radio:
                            #####print("fila:", fila, "columna:", col)
                            if cityblock([self.x,self.y],[self.x+col, self.y+fila])<=5\
                                and self.x+col>=0 and self.x+col<15 and self.y+fila>=0 and self.y+fila<13:
                                #####print("Recorrido de la onda:", str(self.x+col) +","+ str(self.y+fila))
                                if str(self.mapa[self.y+fila][self.x+col]) in list(objetos_frame.keys()):
                                    if ("Unidad" in objetos_frame[str(self.mapa[self.y+fila][self.x+col])].__dict__["type"]) or \
                                        ("Torre" in objetos_frame[str(self.mapa[self.y+fila][self.x+col])].__dict__["type"]) or \
                                        ("Base" in objetos_frame[str(self.mapa[self.y+fila][self.x+col])].__dict__["type"]) or \
                                        ("Estructura destructible" in objetos_frame[str(self.mapa[self.y+fila][self.x+col])].__dict__["type"]):
                                #if "Unidad" in (objetos_frame[str(self.x+col) + "," + str(self.y+fila)].__dict__["type"]) or \
                                    #   "Estructura destructible" in (objetos_frame[str(self.x+col) + "," + str(self.y+fila)].__dict__["type"]):                                       
                                        if (objetos_frame[str(self.mapa[self.y+fila][self.x+col])].__dict__["equipo"]!=self.equipo):
                                    #           ####print("Agregando objetivo:", objetos_frame[str(self.x+col) + "," + str(self.y+fila)])
                                            targets.append(str(self.mapa[self.y+fila][self.x+col]))
                                            #self.target = objetos_frame[self.mapa[self.x+fila][self.y+col]].__dict__["objID"]                                            
                            col+=1
                        fila+=1
                        #break
                    #self.limite+=1
                    #if self.limite>=20:
                    #   break
                    
                if len(targets)>0:
                    for t in targets:
                        #print("Atacando target", objetos_frame[t].__dict__)
                        if ("Torre" in objetos_frame[t].__dict__["type"]):
                            self.danio_causado_Torre += (750+((750/self.nivel_max)*self.bonus_ataque)) /objetos_frame[t].__dict__["salud_max"]
                        objetos_frame[t].__dict__["salud"]-= 750+((750/20)*self.bonus_ataque)
                        self.danio_causado += (750+((750/self.nivel_max)*self.bonus_ataque)) /objetos_frame[t].__dict__["salud_max"]
                        #print("Target despues del ataque", objetos_frame[t].__dict__)
                    self.danio_causado/=len(targets)
                #else:
                    ##print("No target")
            #timer = Timer(1.25, self.apagaBoton, args=("4"))
            #timer.start() 

    def recibeGolpe(self, danio, efecto):
        """Daño y/o efecto recibidos"""
        self.salud-=danio
        #self.estado = efecto
        if self.salud<=0:
            print("El avatar atacante murio")
            self.x = 0
            self.y = 0
            self.estado = "Muerto"
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
     #   tiempo = ((self.nivel*100)*(0.15*e(5.15)*(self.nivel/100)))/300
      #  timer = Timer(tiempo, self.reaparece)
       # timer.start() 
    
    def ganaExperiencia(self, exp):
        self.experiencia += exp
        topeNivel = (self.nivel*100)*(0.15*e(5.15)*(self.nivel/100))
        if self.experiencia >= (topeNivel) and self.nivel<self.nivel_max:
            self.nivel+=1
            self.bonus_ataque+=0.5
            self.salud_max = 7500*(1+(0.25*self.nivel))