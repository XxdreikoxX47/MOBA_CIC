import Agente
import AvatarDefensivo as tank
import AvatarSoporte as support
import AvatarAtacante as atacker
import os
import fnmatch
import numpy as np
import pickle
import objetos_test as MOBAobjs
import inspect
import copy
from time import time
from math import exp as e
# import multiprocessing
# from threading import Thread, Event, Timer
from scipy.spatial.distance import cityblock
import copy


class Partida_PushLane(object):
    '''
    El ambiente propuesto es una matriz de n*m en la que
    cada casilla representa un sprite de un nivel.

    '''

    def __init__(self, filas, columnas, max_steps, objs={}, mapa={}, minReward=0.75,
                 rewardsFile="historicoR.npy", totalRFile="historicoRT.npy", promRFile="historicoRProm.npy",
                 pVal=0.5):
        self.filas = filas
        self.columnas = columnas
        self.mapa = mapa
        self.limit = max_steps
        self.reward_team1 = 0
        self.reward_team2 = 0
        self.objetos_frame = objs
        self.rewardsFile = rewardsFile
        self.totalRFile = totalRFile
        self.promRFile = promRFile
        self.minReward = minReward
        self.maxReward = -99
        self.bestLevel = []
        self.counter = 0
        self.path = "/home/cscog2080/Documents/TesisBeto/Generador/PushLane/mapas/"  # /casoBase/""
        # self.expCounter = 0
        self.bestExp = -1
        self.pVal = pVal  # Un valor de penalizacion para la recompensa si el nivel no es terminable
        # Se crean dos estructuras "gemelas", map y state
        # state y mapa contienen la misma informacion, la matriz de la rebanada que se esta creando
        # Sin embargo, state contiene informacion numerica y map es una matriz de caracteres
       # self.state = [np.zeros(self.columnas) for i in range(self.filas)]
        self.objetos = {}
        self.codigos = []
        self.agentes = []
        self.avatares = []
        self.frames_agentes = {}
        self.creeps = []
        self.torre = None
        self.metadatos = {"salud_total": {}, "nivel": [
            1, 20], "portador_llave": [0, 1], "alianza": [0, 1, 2]}
        self.historico_atackerTeamHealth = {}
        self.historico_defenderTeamHealth = {}
        self.historico_towerHealth = []
        self.historico_atackerTeamExperience = {}
        self.historico_defenderTeamExperience = {}
        self.historico_atackerTeamDistVsTorre = {}
        self.historico_defenderTeamDistVsTorre = {}
        self.historico_atackerTeamRewards = {}
        self.historico_defenderTeamRewards = {}
        self.historico_atackerTeamDecisiones = {}
        self.historico_defenderTeamDecisiones = {}
        self.historico_atackerTeamNivel = {}
        self.historico_defenderTeamNivel = {}

    # @tf.function

    def cargaObjetos(self):

        clases = []
        clasesDic = {}
        sources = [MOBAobjs, atacker, support, tank]
        for s in sources:
            for name, obj in inspect.getmembers(s):
                # print(name,type(obj))
                if inspect.isclass(obj):
                    # print(obj.codificacion)
                    # print(obj.__name__)
                    if name not in ["Event", "Thread", "Timer"]:
                        clases.append(obj)
                        clasesDic[obj.__name__] = obj
        # print("clases\n", clases)
        for c in clases:
            aux = c()
            if aux.multilabel:
                for l in aux.labels:
                    aux.codificacion = l
                    if "2" in l:
                        aux.equipo = 2
                    self.objetos[aux.codificacion] = (
                        copy.deepcopy(aux.__dict__))
                    self.objetos[aux.codificacion]["name"] = c.__name__
                    self.objetos[aux.codificacion]["constructor"] = c
            else:
                self.objetos[aux.codificacion] = (copy.deepcopy(aux.__dict__))
                self.objetos[aux.codificacion]["name"] = c.__name__
                self.objetos[aux.codificacion]["constructor"] = c
        # objetos

        for o in self.objetos:
            self.codigos.append(self.objetos[o]["codificacion"])
            if "Unidad jugable" == self.objetos[o]["type"]:
                self.avatares.append(self.objetos[o]["codificacion"])
            if "salud" in list(self.objetos[o].keys()):
                self.metadatos["salud_total"][self.objetos[o]
                                              ["codificacion"]] = self.objetos[o]["salud"]

    def loadMap(self):
        archivos = []
        for file in os.listdir(self.path):
            if fnmatch.fnmatch(file, "*.pickle"):
                archivos.append(file)
        # Seleccionamos un archivo al azar
        cual_m = np.random.randint(0, len(archivos))
        with open(self.path+archivos[cual_m], "rb") as file:
            # print(file)
            mapas = pickle.load(file)
        cual = np.random.randint(0, len(mapas))
        self.mapa = mapas[cual]

    # @tf.function
    def revisaMapa(self):
        # Se revisa que sea un buen mapa inicial y se hacen los ajustes necesarios si no lo es
        # Se agregaron las bases como parte de los avatares (labels) prohibidos para esta fase experimental
        avs_prohibidos = ["ajt1", "ajt2", "aet1", "aet2", "b1", "b2",
                          "ast1", "ast2", "cnt1", "cnt2"]  # "aat1", "aat2", "adt1", "adt2"
        # Se revisa el mapa seleccionado
        avs_vistos = []
        fila = 0
        torre = None
        team_torre = 0
        llave = None
        while fila < len(self.mapa):
            col = 0
            while col < len(self.mapa[0]):
                # print("Revisando celda: [", fila, ",", col, "]")
                # Un mapa no puede tener los avatares en la lista de prohibidos
                if self.mapa[fila][col] in avs_prohibidos:
                    # print("Eliminando avatar prohibido:", elegido[fila][col])
                    self.mapa[fila][col] = 'p'
                # un mapa no puede tener avatares repetidos, por lo tanto,
                # se mantiene la primera aparicion del avatar y cualquiera repeticion,
                # se reemplaza con pasto
                if "Avatar" in self.objetos[self.mapa[fila][col]]["name"]:
                    # print("Se encontró el avatar:", elegido[fila][col])
                    if self.mapa[fila][col] not in avs_vistos:
                        avs_vistos.append(self.mapa[fila][col])
                    else:
                        #   print("Eliminando avatar repetido...")
                        self.mapa[fila][col] = 'p'
                # No puede haber mas de una torre
                if "Torre" in self.objetos[self.mapa[fila][col]]["name"]:
                    if not torre:
                        torre = self.mapa[fila][col]
                        if '1' in torre:
                            team_torre = "1"
                        else:
                            team_torre = "2"
                    else:
                        self.mapa[fila][col] = 'p'
                if "Llave" in self.objetos[self.mapa[fila][col]]["name"]:
                    # print("Llave detectada")
                    llave = [fila, col]
                col += 1
            fila += 1
        # si no estan los 2 avatares, es un nivel no valido
        if len(avs_vistos) != 2:
            return False

        # si los avatares son de equipos contrarios, es un nivel no valido
        amigos = False
        for av1 in avs_vistos:
            team = 0
            if "1" in av1:
                team = '1'
            else:
                team = "2"

            for av2 in avs_vistos:
                if av1 != av2:
                    if team in av2:
                        amigos = True
        if not amigos:
            return False

        # si no hay avatares del equipo contrario a la torre, es un nivel no valido
        enemigos = False
        for av in avs_vistos:
            if team_torre not in av:
                enemigos = True

        if not enemigos:
            return False

        if not torre:
            # print("Este nivel no sirve, tomar otro")
            return False
        return True
        # Si la llave y la torre tienen la misma etiqueta de equipo, se cambia la etiqueta de la llave
        # esta debe ser forzosamente del equipo contrario para que la torre pueda ser destruida
       # if "1" in torre:
       #     if "1" in self.mapa[llave[0]][llave[1]]:
       #         self.mapa[llave[0]][llave[1]] = "tk2"
       #         return True
       # else:
       #     if "2" in self.mapa[llave[0]][llave[1]]:
       #         self.mapa[llave[0]][llave[1]] = "tk1"
       #         return True

    # @tf.function
    def creaObjetos(self):

        self.objetos_frame = {}
        i = 0
        cont = 0
        for fila in self.mapa:
            j = 0
            for columna in fila:
                # if columna != 'p':# and columna not in avatares:
                # print(columna)
                if "1" in columna:
                    self.objetos_frame[str(cont)] = self.objetos[columna]["constructor"](
                        x=j, y=i, equipo=1, ID=cont)
                elif "2" in columna:
                    self.objetos_frame[str(cont)] = self.objetos[columna]["constructor"](
                        x=j, y=i, equipo=2, ID=cont)
                else:
                    self.objetos_frame[str(cont)] = self.objetos[columna]["constructor"](
                        x=j, y=i, ID=cont)
                if self.objetos_frame[str(cont)].type == "Unidad jugable":
                    self.agentes.append(str(cont))
                    self.frames_agentes[str(cont)] = np.zeros([5*7*9])
                if self.objetos_frame[str(cont)].type == "Unidad NPC":
                    self.creeps.append(str(cont))
                if self.objetos_frame[str(cont)].type == "Torre":
                    self.torre = str(cont)
                cont += 1
                j += 1
            i += 1

    # @tf.function0.25
    def actualizaMapa(self, dims=[13, 15]):
        mapaNuevo = []
        # self.agentes = []
        # self.creeps = []
        # self.torre = None
        i = 0
        while i < dims[0]:
            j = 0
            mapaNuevo.append([])
            while j < dims[1]:
                mapaNuevo[i].append(-1)
                j += 1
            i += 1
       # print("mapa generado vacio")
        # for m in mapaNuevo:
         #   print(m)
        d = 0
        llaves = list(self.objetos_frame.keys())
        # print("Actualizacion...")
        while d < len(self.objetos_frame):
            x = self.objetos_frame[llaves[d]].__dict__["x"]
            y = self.objetos_frame[llaves[d]].__dict__["y"]
            # mod = False
            if self.objetos_frame[llaves[d]].__dict__["codificacion"] != 'p':
             #   print("Revisando ID:", d)
              #  print("Objeto:", self.objetos_frame[llaves[d]].__dict__["codificacion"])
               # print("En posicion:", x,y)
                # print("Colocando ID:", self.objetos_frame[llaves[d]].__dict__["ID"])
                # print("Antes de modificar...", mapaNuevo[y][x])
                mapaNuevo[y][x] = self.objetos_frame[llaves[d]].__dict__["ID"]
                # print("Ya modificado", mapaNuevo[y][x])
             #   mod = True
            # elif not mod:
                # Colocamos un ID egenrico para "no objeto" o pasto...
            #    mapaNuevo[y][x] = -1
            d += 1
        # print("mapa actualizado")
        # for m in mapaNuevo:
         #   print(m)
        self.mapa = mapaNuevo

    # @tf.function
    def reset(self):
        # self.filas = self.filas
        # self.columnas = self.columnas
        # self.limit = self.limit
        self.reward_team1 = 0
        self.reward_team2 = 0
        self.objetos_frame = []
        # self.rewardsFile = self.rewardsFile
        # self.totalRFile = self.totalRFile
        # self.promRFile = self.promRFile
        # self.minReward = self.minReward
        self.maxReward = -99
        self.bestLevel = []
        self.counter = 0
        self.path = "/home/cscog2080/Documents/TesisBeto/Generador/PushLane/mapas/"  # /casoBase/"
        # self.expCounter = 0
        self.bestExp = -1
        # Un valor de penalizacion para la recompensa si el nivel no es terminable
        self.pVal = self.pVal
        # Se crean dos estructuras "gemelas", map y state
        # state y mapa contienen la misma informacion, la matriz de la rebanada que se esta creando
        # Sin embargo, state contiene informacion numerica y map es una matriz de caracteres
       # self.state = [np.zeros(self.columnas) for i in range(self.filas)]
        # self.objetos = {}
        # self.codigos = []
        self.agentes = []
        # self.avatares = []
        self.frames_agentes = {}
        self.creeps = []
        self.torre = None
        # self.metadatos = {"salud_total":{}, "nivel":[1,20], "portador_llave":[0,1], "alianza":[0,1,2]}

        self.loadMap()
       # print("El mapa es:")
       # for m in self.mapa:
        # print(m)
        # self.cargaObjetos()
        flag_level = self.revisaMapa()
        # cont=0
        while not flag_level:
            self.mapa = None
            self.loadMap()
            flag_level = self.revisaMapa()
         #   cont+=1
        # print("Mapa valido encontrado despues de:", cont, " intentos")

        self.creaObjetos()
        self.actualizaMapa()
        # self.state = self.mapToState()
        self.max_global_Reward = -99
        self.max_ind_reward = [-99, -99, -99]
        self.counter = 0
        # self.expCounter = 0
        # self.bestExp = -1
        return self.mapa

    def dist(self, a, b):
        sum = 0
        i = 0
        while i < len(a):
            sum += (a[i]-b[i])**2
            i += 1
        return np.sqrt(sum)

    def loadResults(self):
        # Se cargan las recompensas
        with open(self.path+'/'+self.rewardsFile, 'rb') as f:
            fsz = os.fstat(f.fileno()).st_size
            outRewards = np.load(f)
            while f.tell() < fsz:
                outRewards = np.vstack((outRewards, np.load(f)))
        return outRewards

    # @tf.function
    def accionAgente(self, agente, direccion, seMueve, cursor, boton):
        if agente.nivel <= 10:
            botones = [agente.ataqueBasico, agente.ataqueEspecialBasico1,
                       agente.ataqueEspecialBasico2, agente.ataqueEspecialMaximo]
        elif agente.nivel > 10:
            botones = [agente.ataqueBasico, agente.ataqueEspecial11,
                       agente.ataqueEspecial21, agente.ataqueEspecialMaximo]
        agente.direccionMov(direccion)
        if seMueve:
            agente.mover()
        objetos_frame = agente.mueveCursor(cursor[0], cursor[1])
        agente.hacerClick()
        # t1 = Thread(target= agente.hacerClick, args=())
        # agente.hacerClick()
        # t1.start()
        botones[boton](self.objetos_frame)
        # t2 = Thread(target=botones[boton], args=([self.objetos_frame]))
        # t2.start()
        # t1.join()
        # t2.join()
        # botones[boton](self.objetos_frame)

   # @tf.function
    def step(self, team_actions, pastReward=0):
        '''
        Recibe:
        - team_actions: Es un diccionario que contiene una tupla de accion para cada agente en el mini-mapa
        Basado en funcion step usada en fuente, debe regresar:
        - observation_ : el estado despues de ejecutar la acción
        - reward : la evaluación del ambiente modificado 
                (recompensa por ejecutar la accion)
        - done : bandera que indica si es un estado final 
        - info : idk, pero voy a mandar un 0 porque no lo usa xD
        '''
        # print("Creando hilos...")
        # print("Mapa al inicio del paso")

     #   print("Los agentes detectados son:")
        enemigos = []
        reward_ind = {}
        salud_inicial_defender = {}
        salud_max_defender = {}
        distancias_support = {}
        for a in self.agentes:
            if "Defensivo" in str(self.objetos_frame[a]):
                salud_inicial_defender[a] = copy.deepcopy(
                    self.objetos_frame[a].salud)
                salud_max_defender[a] = copy.deepcopy(
                    self.objetos_frame[a].salud_max)
      #      print(self.objetos_frame[a])
            if self.objetos_frame[a].equipo != self.objetos_frame[self.torre].equipo:
                enemigos.append(copy.copy(a))
            reward_ind[a] = 0
        # for m in self.mapa:
         #   print(m)
        agents_Threads = []
        creeps_Threads = []
        i = 0
        while i < len(self.agentes):
            self.objetos_frame[self.agentes[i]].lecturaMapa(self.mapa)
            self.accionAgente(self.objetos_frame[self.agentes[i]], team_actions[self.agentes[i]]["dir"], team_actions[self.agentes[i]]
                              ["seMueve"], team_actions[self.agentes[i]]["cursor"], team_actions[self.agentes[i]]["boton"])
            self.actualizaMapa()
            # agents_Threads.append(Thread(target=self.accionAgente, \
            #                            args=([self.objetos_frame[self.agentes[i]], \
            #                                 team_actions[self.agentes[i]]["dir"],team_actions[self.agentes[i]]["seMueve"],\
            #                                team_actions[self.agentes[i]]["cursor"], team_actions[self.agentes[i]]["boton"] ])))
            i += 1
        self.objetos_frame[self.torre].leeMapa(self.mapa)
        self.objetos_frame[self.torre].Attack(self.objetos_frame)
        self.objetos_frame[self.torre].curacion()
        self.actualizaMapa()
        # t_tower = Thread(target= self.objetos_frame[self.torre].Attack, args=([self.objetos_frame, [len(self.mapa), len(self.mapa[0])]]))
        i = 0
       # while i <len(self.creeps):

        #    self.objetos_frame[self.creeps[i]].creepMovement(self.objetos_frame, [len(self.mapa), len(self.mapa[0])])
        # creeps_Threads.append(Thread(target=self.objetos_frame[self.creeps[i]].creepMovement, \
        #                            args=([self.objetos_frame, [len(self.mapa), len(self.mapa[0])]])))
        #   self.actualizaMapa()
        #   i+=1

        i = 0

        # t_tower.start()
        self.actualizaMapa()
        # for a in agents_Threads:
        #   a.start()
        #  self.actualizaMapa()
        # for c in creeps_Threads:
        #    c.start()
        #    self.actualizaMapa()
       # print("Mapa al final del paso")
        # for m in self.mapa:
        #   print(m)

        # Una vez efectuadas todas las acciones, se extraen los frames de los agentes
        # print("Agentes")

        for a in self.agentes:
            # print(a)
            # print("tipo:", self.objetos_frame[a].type)
            # print("x:", self.objetos_frame[a].x)
            # print("y:", self.objetos_frame[a].y)
            # print("Creando frame para el agente", a)
            self.frames_agentes[a] = np.zeros([5, 7, 9])

            # print("Frame del agente:", a)
            # for frame in self.frames_agentes[a]:
            #    for canal in frame:
            #        print(canal)

            i = -3
            fila = 0
            while self.objetos_frame[a].y+i <= self.objetos_frame[a].y+3:
                j = -4
                columna = 0
                while self.objetos_frame[a].x+j <= self.objetos_frame[a].x+4:
                    id_frame = str(self.objetos_frame[a].ID)
                    # print("Revisando la posicion", str(self.objetos_frame[a].x+i)+","+str(self.objetos_frame[a].y+j), "del mapa...")
                    # if punto_frame in list(self.objetos_frame.keys()):
                    # print("Escribiendo datos en el frame...")
                 #       print(self.mapa[self.objetos_frame[a].y+j][self.objetos_frame[a].x+i])
                    # Mapa de caracteres
                    self.frames_agentes[a][0, fila, columna] = float(self.codigos.index(
                        self.objetos_frame[id_frame].codificacion)/len(self.codigos))
                    # Salud
                    if "salud" in list(self.objetos_frame[id_frame].__dict__.keys()):
                        #            print("Añadiendo la salud del objeto:", punto_frame)
                        self.frames_agentes[a][1, fila, columna] = float(
                            self.objetos_frame[id_frame].salud/self.objetos_frame[id_frame].salud_max)
                    if "nivel" in list(self.objetos_frame[id_frame].__dict__.keys()):
                        #             print("Añadiendo el nivel del objeto:", punto_frame)
                        self.frames_agentes[a][2, fila, columna] = float(
                            self.objetos_frame[id_frame].nivel/self.objetos_frame[id_frame].nivel_max)
                    if "porta_llave" in list(self.objetos_frame[id_frame].__dict__.keys()):
                        #              print("Añadiendo bandera de portador de llave del objeto:", punto_frame)
                        self.frames_agentes[a][3, fila, columna] = float(
                            self.objetos_frame[id_frame].porta_llave)
                    if "equipo" in list(self.objetos_frame[id_frame].__dict__.keys()):
                        #               print("Añadiendo alianza de llave del objeto:", punto_frame)
                        self.frames_agentes[a][4, fila, columna] = float(
                            self.objetos_frame[id_frame].equipo/2)

                    j += 1
                    columna += 1
                i += 1
                fila += 1

        for a in self.agentes:
            self.objetos_frame[a].revisaBotones()
            self.frames_agentes[a] = self.frames_agentes[a].reshape([7, 9, 5])
            if "Atacante" in str(self.objetos_frame[a]):
                reward_ind[a] = self.objetos_frame[a].danio_causado
            elif "Defensivo" in str(self.objetos_frame[a]):
                reward_ind[a] = (
                    abs(salud_inicial_defender[a]-self.objetos_frame[a].salud))/salud_max_defender[a]
            elif "Soporte" in str(self.objetos_frame[a]):
                for a2 in self.agentes:
                    if self.objetos_frame[a2].equipo == self.objetos_frame[a].equipo:
                        if a not in list(distancias_support.keys()):
                            distancias_support[a] = 0
                        distancias_support[a] += (5-cityblock([self.objetos_frame[a].x, self.objetos_frame[a].y], [
                                                  self.objetos_frame[a2].x, self.objetos_frame[a2].y]))/5
                reward_ind[a] = distancias_support[a]

         #   print("Frame anotado del agente:", a)
          #  for frame in self.frames_agentes[a]:
           #     for canal in frame:
            #        print(canal)
        self.objetos_frame[self.torre].revisaBotones()
        i = 0
        while i < len(self.creeps):
            self.objetos_frame[self.creeps[i]].revisaBotones()
            i += 1

        # La situacion "empujar linea" se termina:
        done = False
        # 1.- si la torre fue destruida
        if self.objetos_frame[self.torre].salud <= 0:
            print("GANO EL EQUIPO ATACANTE")
            done = True

        # 2.- Si los enemigos a la torre son derrotados
        muertos = 0
        for e in enemigos:
           # print("Enemigo:", e)
           # print("Estado:", self.objetos_frame[e].estado)
            if self.objetos_frame[e].salud <= 0:
                muertos += 1
        if muertos == len(enemigos):
            print("GANO EL EQUIPO DEFENSOR")
            done = True
        # 3.- si se llega al numero maximo de pasos
        self.counter += 1
        if self.counter >= self.limit:
            print("SE TERMINO EL TIEMPO")
            done = True

        return copy.deepcopy(self.frames_agentes), [self.objetos_frame[self.torre].salud, self.objetos_frame[self.torre].salud_max], reward_ind, done, 0
