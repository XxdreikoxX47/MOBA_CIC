import Agente
from time import time
from math import exp as e
import numpy as np
# import multiprocessing
# from threading import Thread, Event, Timer
from scipy.spatial.distance import cityblock
import copy


class AvatarSoporte(Agente.Agente):
    def __init__(self, x=0, y=0, equipo=1, ID=None):
        self.ID = ID
        self.type = "Unidad jugable"
        self.x = x
        self.y = y
        self.equipo = equipo
        self.salud = 12000
        self.salud_max = 12000
        self.experiencia = 0
        self.nivel = 20
        self.nivel_max = 20
        self.bonus_ataque = 0.3
        self.estado = "Normal"
        self.porta_llave = False
        self.multilabel = True
        self.labels = ["ast1", "ast2"]
        if equipo == 1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1]
        self.direccion = 0
        # self.move = False  Verificar linea de codigo
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
        self.tiempo_espera = 0

    def direccionMov(self, angulo):
        self.direccion = angulo

    def mover(self, objetos_frame):
        # self.move = True
        # Movimiento horizontal
        # Se mueve a la derecha
        # print("\nMoviendo agente: ", self.codificacion)
        if ((self.direccion < 90) or (self.direccion > 270)) and str(self.x+1)+","+str(self.y) in list(objetos_frame.keys()):
            if (objetos_frame[str(self.x+1)+","+str(self.y)].__dict__["codificacion"] == 'p'):
                # print("moviendose a la derecha")
                self.x += 1
        # Se mueve a la izquierda

        elif ((self.direccion > 90 and self.direccion <= 180) or (self.direccion >= 180 and self.direccion < 270)) and str(self.x-1)+","+str(self.y) in list(objetos_frame.keys()):
            if (objetos_frame[str(self.x-1)+","+str(self.y)].__dict__["codificacion"] == 'p'):
                # print("moviendose a la izquierda")
                self.x -= 1
        # movimiento vertical
        # Se mueve hacia arriba
        if (self.direccion > 0 and self.direccion < 180) and str(self.x)+","+str(self.y-1) in list(objetos_frame.keys()):
            if (objetos_frame[str(self.x)+","+str(self.y-1)].__dict__["codificacion"] == 'p'):
                # print("moviendose hacia arriba")
                self.y -= 1
        # Se mueve hacia abajo
        elif (self.direccion > 180 and self.direccion < 360) and str(self.x)+","+str(self.y+1) in list(objetos_frame.keys()):
            if (objetos_frame[str(self.x)+","+str(self.y+1)].__dict__["codificacion"] == 'p'):
                # print("moviendose hacia abajo")
                self.y += 1

    def lecturaMapa(self, mapa):
        self.mapa = mapa

    def mueveCursor(self, fila, columna):
        self.fila_cursor = fila
        self.columna_cursor = columna

    def apagaClick(self):
        self.click = False

    def hacerClick(self, event=None):
        self.click = True
        # self.click_time += 1
        self.click_time = 0
        # if event:
        #   event.set()
        # timer.start()

    def revisaBotones(self):
        if self.click:
            self.click_time += 0.25

        if self.boton1:
            self.boton1_init += 0.25

        if self.boton2:
            self.boton2_init += 0.25

        if self.boton3:
            self.boton3_init += 0.25

        if self.boton4:
            self.boton4_init += 0.25

        if self.estado == "Muerto":
            self.tiempo_muerte += 0.25

        if self.click_time >= 0.25:
            self.apagaClick

        if self.boton1_init >= 1:
            self.apagaBoton("1")

        if self.boton2_init >= 6.5:
            self.apagaBoton("2")

        if self.boton4_init >= 115:
            self.apagaBoton("4")

        if self.nivel < 10:
            if self.boton3_init >= 4:
                self.apagaBoton("3")
        else:
            if self.boton3_init >= 75:
                self.apagaBoton("3")

        # Se revive el avatar
        if self.estado == "Muerto":
            if self.tiempo_muerte >= self.tiempo_espera:
                self.reaparece()

    def apagaBoton(self, Boton):
        if Boton == "1":
            self.boton1 = False

        elif Boton == "2":
            self.boton2 = False

        elif Boton == "3":
            self.boton3 = False

        else:
            self.boton4 = False

        self.limite = 0
        self.target = None
    """
    Se debe hacer el cambio en el codigo de los ataques para ajustar al funcionamiento establecido en el "ataqueBasico", donde el 
    target se define como un cadena "fila(y), columna(x)" 
    """

    def ataqueBasico(self, objetos_frame):
        # print("Avatar:", self.codificacion, " Ataque basico")
        while not self.boton1:
            # print("primer if, activando boton 1")
            self.boton1 = True
            self.boton1_init = 0
            # while not self.target:
            i = self.x-3
            while i <= self.x+3:
                if i < 0:
                    i = 0
                j = self.y-3
                while j <= self.y+3:
                    if j < 0:
                        j = 0
                    # print("Buscando objetivo en posicion:", self.x+i, self.y+j)
                    if [i, j] != [self.x, self.y] and str(self.x+i)+","+str(self.y+j) in list(objetos_frame.keys()):
                        if (self.x+i >= 0) and (self.x+i < 9) and (self.y+j >= 0) and (self.y+j < 7):
                            if str(self.x+i)+","+str(self.y+j) in list(objetos_frame.keys()):
                                if ("Unidad" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) or \
                                    ("Torre" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) or \
                                    ("Base" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]) or \
                                        ("Estructura destructible" in objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["type"]):
                                 #               #print(objetos_frame[str(self.x+i)+","+str(self.y+j)])
                                    if (objetos_frame[str(self.x+i)+","+str(self.y+j)].__dict__["equipo"] != self.equipo):
                                        if cityblock([self.x, self.y], [self.x+i, self.y+j]) <= 3:
                                            self.target = str(
                                                self.x+i)+","+str(self.y+j)
                                            # print("Target definido: ", self.target)
                                            break
                    j += 1
                i += 1

            if self.target:
                # print("Atacando target", objetos_frame[self.target].__dict__)
                objetos_frame[self.target].__dict__[
                    "salud"] -= 150+((150/self.nivel_max)*self.bonus_ataque)
                if objetos_frame[self.target].__dict__["salud"] <= 0:
                    self.ganaExperiencia(100)
                # print("Target despues del ataque", objetos_frame[self.target].__dict__)
            # else:
                # print("No encontro target")

    def apuntar(self, Boton=None):
        while not self.click:
            if Boton == "1":
                self.boton1 = True

            elif Boton == "2":
                self.boton2 = True

            elif Boton == "3":
                self.boton3 = True

            else:
                self.boton4 = True

    def ataqueEspecialBasico1(self, objetos_frame):
        # print("\nAvatar:", self.codificacion, " Ataque Especial Basico 1")
        if not self.boton2:
            self.boton2 = True
            self.boton2_init = 0
            proyectil = [self.x, self.y]
            # multiprocessing.Process
            # t1 = Thread(target=self.apuntar, args=('2'))
            # t1.start()
            self.columna_cursor_ataque = copy.copy(self.columna_cursor)
            self.fila_cursor_ataque = copy.copy(self.fila_cursor)
            self.apuntar('2')
            modx = 0
            mody = 0
            # Se mueve a la derecha
            if self.columna_cursor_ataque > self.x:
                modx = 1
            # Se mueve a la izquierda
            elif self.columna_cursor_ataque < self.x:
                modx = -1
            # movimiento vertical
            # Se mueve hacia arriba
            if self.fila_cursor_ataque < self.y:
                mody = -1
            # Se mueve hacia abajo
            elif self.fila_cursor_ataque > self.y:
                mody = 1
            # Se espera a que se de click en algun proceso
            # while True:
                # print("Comenzando ataque")
            if self.click:
                # Movimiento horizontal
                # print("Se hizo click")
                tries = 0
                while cityblock([self.x, self.y], proyectil) <= 3 and tries < 25:
                    # print("Recorrido del proyectil:", str(proyectil[0])+','+str(proyectil[1]))
                    if [self.x, self.y] != proyectil:
                        # str(self.x+i)+","+str(self.y+j)
                        if str(proyectil[0])+','+str(proyectil[1]) in list(objetos_frame.keys()):
                            if ("Unidad" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                                ("Torre" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                                ("Base" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                                    ("Estructura destructible" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]):
                                # if "Unidad" in (objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                                # "Estructura destructible" in (objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]):
                                # print("En el camino del proyectil:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                                if (objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["equipo"] == self.equipo)\
                                        and cityblock([self.x, self.y], proyectil) <= 3:
                                    # print("Objetivo:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                                    self.target = str(
                                        proyectil[0]) + "," + str(proyectil[1])
                                    # self.target = objetos_frame[self.mapa[proyectil[0]][proyectil[1]]].__dict__["objID"]
                                    break
                    proyectil[0] += modx
                    proyectil[1] += mody
                    tries += 1
                # break

            if self.target:
                # print("Curando target", objetos_frame[self.target].__dict__)
                if objetos_frame[self.target].__dict__["salud"] < objetos_frame[self.target].__dict__["salud_max"]:
                    if objetos_frame[self.target].__dict__["salud"]+300 > objetos_frame[self.target].__dict__["salud_max"]:
                        dif = objetos_frame[self.target].__dict__[
                            "salud_max"] - objetos_frame[self.target].__dict__["salud"]
                        objetos_frame[self.target].__dict__["salud"] += dif
                    else:
                        objetos_frame[self.target].__dict__[
                            "salud"] += 300+((300/self.nivel_max)*self.bonus_ataque)

                # print("Target despues del ataque", objetos_frame[self.target].__dict__)
            # else:
                # print("No se encontró target")

        # timer = Timer(6.5, self.apagaBoton, args=("2"))
        # timer.start()

    def curacion(self, radio, objetos_frame, curacion=50, danio=50, estado="normal", cura=True, stop_time=3, refresh_time=0.5):
        t1 = time()
        curado = False
        # while True:
        i = -radio
        while i < radio:
            if i < 0:
                i = 0
            j = -radio
            while j < radio:
                if j < 0:
                    j = 0
                # ###print("Activando onda...")
                if str(self.x+i)+","+str(self.y+j) in list(objetos_frame.keys()):
                    if ("Unidad" in objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["type"]) or\
                        ("Torre" in objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["type"]) or \
                        ("Base" in objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["type"]) or \
                        ("Estructura destructible" in objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["type"])\
                            and [self.x, self.y] != [self.x+i, self.y+j]:
                        c_time2 = time()
                        if curado:
                            if c_time2-c_time >= refresh_time:
                                curado = False
                        if cura:
                            if (objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["equipo"] == self.equipo) and not curado:
                                # print("Curando compañero:",objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__ )
                                if objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["salud"] < objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["salud_max"]:
                                    if objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["salud"]+curacion > objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["salud_max"]:
                                        dif = objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__[
                                            "salud_max"] - objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["salud"]
                                        objetos_frame[str(
                                            self.x+i)+','+str(self.y+j)].__dict__["salud"] += dif
                                    else:
                                        objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__[
                                            "salud"] += curacion+((curacion/self.nivel_max)*self.bonus_ataque)
                                # else:
                                  # print("Compañero sano :D")

                                # objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["salud"]+= curacion
                                # objetos_frame[str(i)+','+str(j)].__dict__["estado"]= estado
                                curado = True
                                c_time = time()
                        else:

                            if (objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["equipo"] != self.equipo) and not curado:
                                # print("Dañando enemigo:",objetos_frame[str(self.x+i)+','+str(self.y+j)] )
                                objetos_frame[str(
                                    self.x+i)+','+str(self.y+j)].__dict__["salud"] -= danio
                                if objetos_frame[str(self.x+i)+','+str(self.y+j)].__dict__["salud"] <= 0:
                                    self.ganaExperiencia(100)
                                # objetos_frame[str(i)+','+str(j)].__dict__["estado"]= estado
                                curado = True
                                c_time = time()
                j += 1
            i += 1
            t2 = time()
            if t2-t1 >= stop_time:
                # print("Deteniendo despues de:", t2-t1, "segundos")
                # event.set()
                return 0

    def ataqueEspecialBasico2(self, objetos_frame):
        """
        En esta primera version el ataque básico 2 no considera el efecto de 'inmobilizacion' que
        debería provocar a las unidades no aliadas que alcanza. 
        """
        # print("Avatar:", self.codificacion, " Ataque Especial Basico 2")
        if not self.boton3:
            self.boton3 = True
            self.boton3_init = 0
            radio = 1
            self.apuntar('3')
            # t1 = Thread(target=self.apuntar, args=('3'))
            # t1.start()
            # Se espera a que se de click en algun proceso
            # while True:
            # El click es un proceso que sucede en paralelo
            # if self.click:# or self.boton3:
            # print("Se hizo click")
            # e = Event()
            self.curacion(radio, objetos_frame, 50)
            # cura.start()
            # print("se mando a llamar el hilo")
            # break
        # timer = Timer(4, self.apagaBoton, args=("3"))
        # timer.start()

    def ataqueEspecial11(self, objetos_frame):
        """
        En esta primera version el ataque especial 11 no considera el efecto de 'reduccion de salud maxima' que
        debería provocar a las unidades no aliadas que alcanza. 
        """
        if not self.boton2:
            self.boton2 = True
            proyectil = [self.x, self.y]
            self.apuntar('2')
            self.boton2_init = 0
            # t1 = Thread(target=self.apuntar, args=('2'))
            # t1.start()
            self.columna_cursor_ataque = copy.copy(self.columna_cursor)
            self.fila_cursor_ataque = copy.copy(self.fila_cursor)
            modx = 0
            mody = 0
            # Se mueve a la derecha
            if self.columna_cursor_ataque > self.x:
                modx = 1
            # Se mueve a la izquierda
            elif self.columna_cursor_ataque < self.x:
                modx = -1
            # movimiento vertical
            # Se mueve hacia arriba
            if self.fila_cursor_ataque < self.y:
                mody = -1
            # Se mueve hacia abajo
            elif self.fila_cursor_ataque > self.y:
                mody = 1
            # Se espera a que se de click en algun proceso
            # while True:
                # print("Comenzando ataque")
            if self.click:
                # Movimiento horizontal
                # print("Se hizo click")
                while cityblock([self.x, self.y], proyectil) <= 3:
                    # print("Recorrido del proyectil:", str(proyectil[0])+','+str(proyectil[1]))
                    if [self.x, self.y] != proyectil:
                        # str(self.x+i)+","+str(self.y+j)
                        if str(proyectil[0])+','+str(proyectil[1]) in list(objetos_frame.keys()):
                            if ("Unidad" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                                ("Torre" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                                ("Base" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                                    ("Estructura destructible" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]):
                                # if "Unidad" in (objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                                # "Estructura destructible" in (objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]):
                                # print("En el camino del proyectil:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                                if (objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["equipo"] == self.equipo)\
                                        and cityblock([self.x, self.y], proyectil) <= 3:
                                    # print("Objetivo:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                                    self.target = str(
                                        proyectil[0]) + "," + str(proyectil[1])
                                    # self.target = objetos_frame[self.mapa[proyectil[0]][proyectil[1]]].__dict__["objID"]
                                    break
                    proyectil[0] += modx
                    proyectil[1] += mody
                # break

            if self.target:
                # print("Atacando target", objetos_frame[self.target].__dict__)
                objetos_frame[self.target].__dict__[
                    "salud"] -= 200+((200/self.nivel_max)*self.bonus_ataque)
                # print("Target despues del ataque", objetos_frame[self.target].__dict__)
                if objetos_frame[self.target].__dict__["salud"] <= 0:
                    self.ganaExperiencia(100)

        # timer = Timer(6.5, self.apagaBoton, args=("2"))
        # timer.start()

    def ataqueEspecial21(self, objetos_frame):
        """
        En esta primera version el ataque básico 2 no considera los efecto de 'confusion', ni 'fortificacion' que
        debería provocar a las unidades que alcanza. 
        """
        if not self.boton3:
            self.boton3 = True
            radio = 1
            self.boton3_init = 0
            targets_notAlly = []
            targets_Ally = []
            proyectil = [self.x, self.y]

            # t1 = Thread(target=self.apuntar, args=('3'))
            # t1.start()
            self.columna_cursor_ataque = copy.copy(self.columna_cursor)
            self.fila_cursor_ataque = copy.copy(self.fila_cursor)
            self.apuntar('3')
            modx = 0
            mody = 0
            # Se mueve a la derecha
            if self.columna_cursor_ataque > self.x:
                modx = 1
            # Se mueve a la izquierda
            elif self.columna_cursor_ataque < self.x:
                modx = -1
            # movimiento vertical
            # Se mueve hacia arriba
            if self.fila_cursor_ataque < self.y:
                mody = -1
            # Se mueve hacia abajo
            elif self.fila_cursor_ataque > self.y:
                mody = 1
            # Se espera a que se de click en algun proceso
            centro = [0, 0]
            # while True:
            #   if self.click:
            # Movimiento horizontal

            while cityblock([self.x, self.y], proyectil) <= 3 and not self.target:
                if str(proyectil[0])+','+str(proyectil[1]) in list(objetos_frame.keys()):
                    if ("Unidad" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                        ("Torre" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                        ("Base" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                            ("Estructura destructible" in objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]):
                        # if "Unidad" in (objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]) or \
                        #    "Estructura destructible" in (objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["type"]):
                        # print("En el camino del proyectil:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                        if (objetos_frame[str(proyectil[0])+','+str(proyectil[1])].__dict__["equipo"] == self.equipo)\
                                and cityblock([self.x, self.y], proyectil) <= 3 and [self.x, self.y] != proyectil:
                            # print("Objetivo:", objetos_frame[str(proyectil[0])+','+str(proyectil[1])])
                            self.target = str(
                                proyectil[0]) + "," + str(proyectil[1])
                            centro = copy.copy(proyectil)
                            break

                proyectil[0] += modx
                proyectil[1] += mody
                # ###print(objetos_frame[self.mapa[proyectil[0]][proyectil[1]]])

            if (self.target):
                init_i = centro[0]-radio
                init_j = centro[1]-radio
                fin_i = centro[0]+radio
                fin_j = centro[1]+radio
            else:
                init_i = proyectil[0]-radio
                init_j = proyectil[1]-radio
                fin_i = proyectil[0]+radio
                fin_j = proyectil[1]+radio
            # print("Onda de impacto...")
            i = init_i
            while i < fin_i:
                j = init_j
                while j < fin_j:
                    # ###print("Explotando en posicion:", str(i)+','+str(j))
                    if "Unidad" in (objetos_frame[str(i)+','+str(j)].__dict__["type"]) or\
                            cityblock([self.x, self.y], proyectil) == 3:
                        if objetos_frame[str(i)+','+str(j)].__dict__["equipo"] != self.equipo:
                            # print("Agregando target no aliado:", objetos_frame[str(i)+','+str(j)].__dict__)
                            targets_notAlly.append(str(i)+','+str(j))
                        elif objetos_frame[str(i)+','+str(j)].__dict__["equipo"] == self.equipo and\
                                [i, j] != [self.x, self.y]:
                            # print("Agregando target aliado:", objetos_frame[str(i)+','+str(j)].__dict__)
                            targets_Ally.append(str(i)+','+str(j))
                    j += 1
                i += 1
                # self.target = objetos_frame[self.mapa[proyectil[0]][proyectil[1]]].__dict__["objID"]
            # break
            if len(targets_Ally) > 0:
                for tA in targets_Ally:
                    # print("Curando aliado...", objetos_frame[tA].__dict__)
                    if objetos_frame[tA].__dict__["salud"] < objetos_frame[tA].__dict__["salud_max"]:
                        if objetos_frame[tA].__dict__["salud"]+200 > objetos_frame[tA].__dict__["salud_max"]:
                            dif = objetos_frame[tA].__dict__[
                                "salud_max"] - objetos_frame[tA].__dict__["salud"]
                            objetos_frame[tA].__dict__["salud"] += dif
                        else:
                            objetos_frame[tA].__dict__[
                                "salud"] += 200+((200/self.nivel_max)*self.bonus_ataque)
                    # print("Aliado despues de curacion...", objetos_frame[tA].__dict__)
                    # objetos_frame[tA].__dict__["salud"]+= 200+((200/self.nivel_max)*self.bonus_ataque)
            if len(targets_notAlly) > 0:
                for tnA in targets_notAlly:
                   # ###print("Atacando objetivo:", objetos_frame[tnA].__dict__)
                    objetos_frame[tnA].__dict__["salud"] -= 350 + \
                        ((350/self.nivel_max)*self.bonus_ataque)
                    if objetos_frame[tnA].__dict__["salud"] <= 0:
                        self.ganaExperiencia(100)
                    # print("Target despues del ataque:", objetos_frame[tnA].__dict__)

        # timer = Timer(7.5, self.apagaBoton, args=("3"))
        # timer.start()

    def ataqueEspecialMaximo(self, objetos_frame):
        """"
        En esta version, se hizo una simplificacion de la ulti del atacante,
        para cumplir en tiempo y forma con la entrega. Se hizo un ajuste del atauqe especial 21, que genera 
        mas daño
        """
        # print("Avatar:", self.codificacion, " Ataque Especial Maximo")
        if not self.boton4:
            self.boton4 = True
            self.boton4_init = 0
            self.apuntar('4')
            # t1 = Thread(target=self.apuntar, args=('4'))
            # t1.start()
            # Se espera a que se de click en algun proceso
            # while True:
            # El click es un proceso que sucede en paralelo
            if self.click:  # or self.boton3:
                # self, event, radio, objetos_frame, curacion=50, danio=50, estado="normal", cura=True, stop_time=3, refresh_time=0.5
                time1 = 0
                time2 = 0
                i = 0
                while time2 < 18:
                    # print("Ronda:", i+1, "de ondas")
                    # print("Han pasado:", time2-time1, "segundos")
                    # e = Event()
                    self.curacion(2, objetos_frame, 200, 0,
                                  "normal", False, 0.5, 0.485)
                    # onda1 = Thread(target= self.curacion, args=(e, 2, objetos_frame, 200, 0, "normal", False, 0.5, 0.485))
                    # onda1.start()
                    self.curacion(3, objetos_frame, 500, 0,
                                  "normal", True, 0.5, 0.485)
                    # onda2 = Thread(target= self.curacion, args=(e, 3, objetos_frame, 500, 0, "normal", True, 0.5, 0.485))
                    # onda2.start()
                    self.curacion(1, objetos_frame, 150, 0,
                                  "normal", False, 0.5, 0.485)
                    # onda3 = Thread(target= self.curacion, args=(e, 1, objetos_frame, 150, 0, "normal", False, 0.5, 0.485))
                    # onda3.start()
                    self.curacion(4, objetos_frame, 300, 0,
                                  "normal", True, 0.5, 0.485)
                    # onda4 = Thread(target= self.curacion, args=(e, 4, objetos_frame, 300, 0, "normal", True, 0.5, 0.485))
                    # onda4.start()
                    time2 += 1
                    i += 1
                # print("ATAQUE ULTI DETENIDO DESPUES DE:", time2-time1, "segundos")
            #    break

        # timer = Timer(1.15, self.apagaBoton, args=("4"))
        # timer.start()
        # print("LLEGAMOS HASTA AQUI....")

    def recibeGolpe(self, danio, efecto):
        """Daño y/o efecto recibidos"""
        self.salud -= danio
        # self.estado = efecto
        if self.salud <= 0:
            self.estado = "Muerto"
            self.tiempo_muerte = 0
            self.tiempo_espera = (
                (self.nivel*100)*(0.15*e(5.15)*(self.nivel/100)))/300

    def reaparece(self):
        self.estado = "Normal"
        if self.equipo == '1':
            self.x = 0
            self.y = len(self.mapa)
        else:
            self.x = len(self.mapa[0])
            self.y = 0

    # def revive(self):
     #   self.tiempo_espera = ((self.nivel*100)*(0.15*e(5.15)*(self.nivel/100)))/300
      #  self.reaparece()
        # timer = Timer(tiempo, self.reaparece)
        # timer.start()

    def ganaExperiencia(self, exp):
        self.experiencia += exp
        topeNivel = (self.nivel*100)*(0.15*e(5.15)*(self.nivel/100))
        if self.experiencia >= (topeNivel) and self.nivel < self.nivel_max:
            self.nivel += 1
            self.bonus_ataque += 0.4
            self.salud_max = 12000*(1+(0.25*self.nivel))
