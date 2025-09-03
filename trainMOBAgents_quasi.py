
import numpy as np
import time
import copy
import Partida_PushLane as PL
# import MOBAgent_quasi as agent
# import MOBAgent_quasi_politicaItems as agent
import json
from pickle import dump, dumps, load, loads
from scipy.spatial.distance import cityblock
from npy_append_array import NpyAppendArray

path = "/home/cscog2080/Documents/TesisBeto/Agentes/Experimentos/"


def redondea(num):
    if num >= 0.5:
        return 1.0
    else:
        return 0


def trainModel(env, agentes_creados, n_games, lim, load=False, epocTrain=5, epocSave=10, extraString=''):
    """
    Esta funcion ejecuta un entrenamiento de un agente basado en RL para la generación automática de niveles.
    Recibe:
    - env.- El ambiente, un objeto de la clase Environment. Debe estar inicializado de acuerdo al problema a resolver
    - agentes.- Los agentes, es un de la clase Agent. Debe estar inicializado de acuerdo al problema a resolver
    - actions.- La lista de acciones que puede ejecutar el agente.
    - filas.- El número de filas del nivel.
    - columnas.- El número de columnas del nivel.
    - n_games.- El número de experimentos a realizar, cada experimento significa un nivel creado desde cero. 
    - lim.- El número de acciones a ejecutar en cada experimento.
    - load=False.- Un indicador para saber si el modelo ha sido entrenado previamente y se desea sobreescribir o 
                   si se desea construir desde cero. 
    - epocTrain=5.- El número de pasos para entrenar la red neuronal.
                    Por defecto, es cada 5 epocas
    - epocSave=1000.- El número de pasos para actualizar el archivo de la red neuronal, debe ser un numero entre 1 y c.
                      Por defecto es 1000
    - gameLevel=100.- El número de pasos para almacenar un nivel con evaluación superior a minReward.
                      Por defecto es 100 
    - minReward=0.75.- El valor de la recompensa mínima para almacenar un nivel.
    - exp="Salto".- La experiencia de juego que se intenta aprender.
    Entrega:
    No entrega nada, pero genera archivos de:
          - Arquitectura de la RNA entrenada en un archivo *.h5
          - Historico de recompensas del agente en un archivo *.npy
          - Proceso(s) de creacion de nivel(es) en archivo(s) *.npy
          - Información sobre evaluación de nivel(es) creado(s) en archivo(s) *.json
          - Nivel(es) creado(s) en archivo(s) *.json
    """
    scores_atacker = []
    scores_defender = []
    danioTorre = []
    historic_Atk_score = []
    historic_def_score = []
    # eps_history= []
    init = time.time()
    print("Iniciando en:", time.ctime(init))
    for i in range(n_games):
        print("Comenzando episodio:", i+1)
        agentes = {}
        done = False
        score_atacker = 0
        score_defender = 0
        # env.reset()
        # observation = env.reset()
        obs = []
        dt = []
        print("En la partida hay:", len(env.agentes),
              "agentes y ", len(env.frames_agentes), "frames")
        for e in env.frames_agentes:
            dt.append((e, list))
            obs.append(copy.deepcopy(
                np.array(env.frames_agentes[e]).reshape(7, 9, 5)))
        # observations = np.array((obs), dtype=np.dtype(dt))
        observations = np.asarray(obs)  # , dtype=np.dtype(dt))
        # print("observations", observations)

        # print(observations.shape)
        for a in env.agentes:

            if env.objetos_frame[a].equipo != env.objetos_frame[env.torre].equipo:
                # Se crean los avatares atacantes
                if "Atacante" in str(env.objetos_frame[a]):
                    agentes[a] = agentes_creados["AtackerTeam_atacker"+extraString]
                    agentes[a].asignaAvatar(env.objetos_frame[a])
                elif "Defensivo" in str(env.objetos_frame[a]):
                    agentes[a] = agentes_creados["AtackerTeam_defender"+extraString]
                    agentes[a].asignaAvatar(env.objetos_frame[a])
                elif "Soporte" in str(env.objetos_frame[a]):
                    agentes[a] = agentes_creados["AtackerTeam_support"+extraString]
                    agentes[a].asignaAvatar(env.objetos_frame[a])
            else:
                # Se crean los avatres defensores
                if "Atacante" in str(env.objetos_frame[a]):
                    agentes[a] = agentes_creados["DefenderTeam_atacker"+extraString]
                    agentes[a].asignaAvatar(env.objetos_frame[a])
                elif "Defensivo" in str(env.objetos_frame[a]):
                    agentes[a] = agentes_creados["DefenderTeam_defender"+extraString]
                    agentes[a].asignaAvatar(env.objetos_frame[a])
                elif "Soporte" in str(env.objetos_frame[a]):
                    agentes[a] = agentes_creados["DefenderTeam_support"+extraString]
                    agentes[a].asignaAvatar(env.objetos_frame[a])
            # inpot_dims = 1*1*48-> segun las dimensiones del frame embedding producido por el AE

         # print("Estado inicial:\n")
         # fila = 0
         # while fila<len(env.mapa):
         #   col=0
         #   while col<len(env.mapa[fila]):
         #       if env.mapa[fila][col]!=-1:
         #           print(env.objetos_frame[str(env.mapa[fila][col])].codificacion, end="\t")
         #       else:
         #           print('p', end="\t")
         #       col+=1
         #   print()
         #   fila+=1
        # for n in env.mapa:
        #  print(n)
        c = 0
        pastReward = 0
        # print("La torre esta en la posicion:", env.torre)
        infoH = {}
        frames = []
        # infoH["objetivo"]= copy.deepcopy(env.caracteristicas)
        # env.historico_towerHealth = []
        # bitacora = {}

        while c < lim:
            bitacoraInteresante = False
            # print("paso:", c)
            # print("observations.shape", observations.shape)
            actions = {}

            if c == 0:
                env.historico_towerHealth = []
                env.historico_towerHealth.append(
                    env.objetos_frame[env.torre].salud)

            for a in agentes:
             # print("Accediendo al agente:", a, "contador - ", cont)
             # print("frames_array[:,cont].shape",frames_array[:,cont].shape)
                # print("frames_array.shape",frames_array.shape)
                if c == 0:
                    # Se crean los arreglos historicos de los agentes
                    # env.historico_towerHealth.append(env.objetos_frame[env.torre].salud)
                    env.historico_atackerTeamHealth[agentes[a].avatar.codificacion] = [
                    ]
                    env.historico_atackerTeamHealth[agentes[a].avatar.codificacion].append(
                        copy.copy(agentes[a].avatar.salud))
                    # env.historico_defenderTeamHealth = {}
                    env.historico_atackerTeamExperience[agentes[a].avatar.codificacion] = [
                    ]
                    env.historico_atackerTeamExperience[agentes[a].avatar.codificacion].append(
                        copy.copy(agentes[a].avatar.experiencia))
                    # env.historico_defenderTeamExperience = {}
                    env.historico_atackerTeamDistVsTorre[agentes[a].avatar.codificacion] = [
                    ]
                    env.historico_atackerTeamDistVsTorre[agentes[a].avatar.codificacion].append(copy.copy(cityblock(
                        [agentes[a].avatar.x, agentes[a].avatar.y], [env.objetos_frame[env.torre].x, env.objetos_frame[env.torre].y])))
                    # env.historico_defenderTeamDistVsTorre = {}
                    # env.historico_atackerTeamRewards[a] = []
                    # env.historico_defenderTeamRewards = {}
                    env.historico_atackerTeamDecisiones[agentes[a].avatar.codificacion] = [
                    ]
                    # env.historico_defenderTeamDecisiones = {}
                    env.historico_atackerTeamNivel[agentes[a].avatar.codificacion] = [
                    ]
                    env.historico_atackerTeamNivel[agentes[a].avatar.codificacion].append(
                        copy.copy(agentes[a].avatar.nivel))
                    # env.historico_defenderTeamNivel = {}

                agent_signals = agentes[a].choose_action(
                    ([env.objetos_frame[env.torre].x, env.objetos_frame[env.torre].y], env.objetos_frame[env.torre].salud, env.med, env.accel))
                # agent_signals = agent_signals[0]

                # print("a", a)

                actions[a] = {"dir": agent_signals[0], "seMueve": agent_signals[1],
                              "cursor": [agent_signals[2], agent_signals[3]], "boton": agent_signals[4]}
                env.historico_atackerTeamDecisiones[agentes[a].avatar.codificacion].append(
                    copy.deepcopy(actions[a]))

             # print("actions:", actions)

            # action  = agent.choose_action(observation)
             # print("Ejecutando acciones")
            observations_, reward, reward_ind, done, info = env.step(actions)
            env.historico_towerHealth.append(
                env.objetos_frame[env.torre].salud)
            for a in agentes:
                env.historico_atackerTeamHealth[agentes[a].avatar.codificacion].append(
                    copy.copy(agentes[a].avatar.salud))
                env.historico_atackerTeamExperience[agentes[a].avatar.codificacion].append(
                    copy.copy(agentes[a].avatar.experiencia))
                env.historico_atackerTeamDistVsTorre[agentes[a].avatar.codificacion].append(copy.copy(cityblock(
                    [agentes[a].avatar.x, agentes[a].avatar.y], [env.objetos_frame[env.torre].x, env.objetos_frame[env.torre].y])))
                env.historico_atackerTeamNivel[agentes[a].avatar.codificacion].append(
                    copy.copy(agentes[a].avatar.nivel))
            # Se calcula el siguiente estado, su recompensa, si ya se legó a un estado terminal, etc
             # print("Acciones ejecutadas en el ambiente")

            # print("Obteniendo observaciones del estado nuevo")
            # obs_ = []
            # for e in observations_:
            #  obs_.append(([env.objetos_frame[env.torre].x,env.objetos_frame[env.torre].y],env.objetos_frame[env.torre].salud))
            # obs_ = np.array(obs_)
            # print("obs_.shape", obs_.shape)
             # print("Estado nuevo:\n")
            # fila = 0
            # while fila<len(env.mapa):
            #  col=0
            #  while col<len(env.mapa[fila]):
            #      if env.mapa[fila][col]!=-1:
            #          print(env.objetos_frame[str(env.mapa[fila][col])].codificacion, end="\t")
            #      else:
            #          print('p', end="\t")
            #      col+=1
            #  print()
            #  fila+=1
            #  for n in env.mapa:
             # print(n)

            # La recompensa viene en el formato [salud actual torre, salud maxima de la torre]

            # historic_Atk_score.append((abs((reward[1]-reward[0])))/reward[1])
            # historic_def_score.append(1-(abs((reward[1]-reward[0])))/reward[1])
            score_atacker += (abs((reward[1]-reward[0])))/reward[1]
            score_defender += 1-(abs((reward[1]-reward[0])))/reward[1]
            # score_atacker+= (abs((reward[1]-reward[0])))/reward[1]
            # score_defender+=  ((reward[0]-abs(reward[1]-reward[0]))/reward[1])/100

            # print("Calculando estimaciones de valores Q nuevos")
            # output_ = AE_model(obs_)

            # print("informacion almacenada...")
            # else:
            #   for a in agentes:
            #       output = np.array(AE_model(np.array([observations[a]]))[0]).reshape([48])
            #       output_ = np.array(AE_model(np.array([observations_[a]]))[0]).reshape([48])
            #       if env.objetos_frame[a].equipo!=env.objetos_frame[env.torre].equipo:
            #           agentes[a].remember(output, actions[a], score_atacker+reward_ind[a], output_, float(done), actions=actions[a])
            #       else:
            #           agentes[a].remember(output, actions[a], score_defender+reward_ind[a], output_, float(done), actions=actions[a])

            # observations = copy.copy(obs_)
            for a in agentes:
                agentes[a].avatar.revisaBotones()
            infoH[str(c)] = info
            pastReward = copy.copy(reward)
            # print("State modified...\n", observation)
            # print("Episodio: ",i+1,", Accion: ",c+1 ,", Accion elegida:", actions[action])

            c += 1

            # print("\nGuardando progreso de entrenamiento")

            if (c == lim):
                print("\nLímite de tiempo alcanzado")
            if done:
                c = lim

        # Guardamos la salud final de la torre en cada episodio, como un indicador del desempeño final de los agentes
        # env.historico_towerHealth.append(env.objetos_frame[env.torre].salud)
        danioTorre.append(reward[0])
        endCiclo = time.time()
        print("Experimento:", i+1, "terminado en:", time.ctime(endCiclo))
        # eps_history.append(agent.epsilon)
        scores_atacker.append(score_atacker)
        scores_defender.append(score_defender)
        avg_score_atk = np.mean(np.array(scores_atacker))
        avg_score_def = np.mean(np.array(scores_defender))
        # avg_score_atk = np.mean(scores_atacker[max(0, i-100):(i+1)])
        # avg_score_def = np.mean(scores_defender[max(0, i-100):(i+1)])
        print('Episodio', i+1)
        print("Los puntos de salud finales de la torre son: ",
              reward[0], "/", reward[1])
        print("Desempeño por equipos:\n", 'recompensa acumulada atacantes %.2f' % score_atacker, '/', lim, 'promedio de recompensa de atacantes %2.f' % avg_score_atk, "\n"
              'recompensa acumulada de los defensores %.2f' % score_defender, "/", lim, 'promedio de recompensa de defensores %2.f' % avg_score_def)

        with NpyAppendArray(path+"Tower_FinalHealthPoints"+extraString+".npy") as npaa:
            npaa.append(np.array([reward[0]]))

        with NpyAppendArray(path+"AccumulatedReward_AttackerTeam"+extraString+".npy") as npaa:
            npaa.append(np.array([score_atacker]))

        with NpyAppendArray(path+"AccumulatedReward_DefenderTeam"+extraString+".npy") as npaa:
            npaa.append(np.array([score_defender]))

        # with NpyAppendArray(path+"HistoricalReward_AttackerTeam"+extraString+".npy") as npaa:
           # npaa.append(np.array([historic_Atk_score]))

        # with NpyAppendArray(path+"HistoricalReward_DefenderTeam"+extraString+".npy") as npaa:
           # npaa.append(np.array([historic_def_score]))

        print("Desempeño por agente:")
        for a in reward_ind:

            if env.objetos_frame[a].equipo != env.objetos_frame[env.torre].equipo:
                # Se crean los avatares atacantes
                print("Recompensa del agente: Equipo Atacante", a,
                      str(env.objetos_frame[a]), "-> ", reward_ind[a])

                if "Atacante" in str(env.objetos_frame[a]):
                    filename = "AttackerTeam_Attacker"+extraString+".npy"
                    with NpyAppendArray(path+filename) as npaa:
                        npaa.append(np.array([reward_ind[a]]))
                    with NpyAppendArray(path+"timeCounters_"+filename) as npaa:
                        npaa.append(np.array(
                            [agentes[a].counter_rand, agentes[a].timecounter_rand, agentes[a].counter_qn, agentes[a].timecounter_qn]))

                elif "Defensivo" in str(env.objetos_frame[a]):
                    filename = "AttackerTeam_Defender"+extraString+".npy"
                    with NpyAppendArray(path+filename) as npaa:
                        npaa.append(np.array([reward_ind[a]]))
                    with NpyAppendArray(path+"timeCounters_"+filename) as npaa:
                        npaa.append(np.array(
                            [agentes[a].counter_rand, agentes[a].timecounter_rand, agentes[a].counter_qn, agentes[a].timecounter_qn]))

                elif "Soporte" in str(env.objetos_frame[a]):
                    filename = "AttackerTeam_Support"+extraString+".npy"
                    with NpyAppendArray(path+filename) as npaa:
                        npaa.append(np.array([reward_ind[a]]))
                    with NpyAppendArray(path+"timeCounters_"+filename) as npaa:
                        npaa.append(np.array(
                            [agentes[a].counter_rand, agentes[a].timecounter_rand, agentes[a].counter_qn, agentes[a].timecounter_qn]))

            else:
                print("Recompensa del agente: Equipo Defensor", a,
                      str(env.objetos_frame[a]), "-> ", reward_ind[a])
                # Se crean los avatres defensores
                if "Atacante" in str(env.objetos_frame[a]):
                    filename = "DefenderTeam_Attacker"+extraString+".npy"
                    with NpyAppendArray(path+filename) as npaa:
                        npaa.append(np.array([reward_ind[a]]))
                    with NpyAppendArray(path+"timeCounters_"+filename) as npaa:
                        npaa.append(np.array(
                            [agentes[a].counter_rand, agentes[a].timecounter_rand, agentes[a].counter_qn, agentes[a].timecounter_qn]))

                elif "Defensivo" in str(env.objetos_frame[a]):
                    filename = "DefenderTeam_Defender"+extraString+".npy"
                    with NpyAppendArray(path+filename) as npaa:
                        npaa.append(np.array([reward_ind[a]]))
                    with NpyAppendArray(path+"timeCounters_"+filename) as npaa:
                        npaa.append(np.array(
                            [agentes[a].counter_rand, agentes[a].timecounter_rand, agentes[a].counter_qn, agentes[a].timecounter_qn]))

                elif "Soporte" in str(env.objetos_frame[a]):
                    filename = "DefenderTeam_Support"+extraString+".npy"
                    with NpyAppendArray(path+filename) as npaa:
                        npaa.append(np.array([reward_ind[a]]))
                    with NpyAppendArray(path+"timeCounters_"+filename) as npaa:
                        npaa.append(np.array(
                            [agentes[a].counter_rand, agentes[a].timecounter_rand, agentes[a].counter_qn, agentes[a].timecounter_qn]))

            # print("Recompensa del agente:", a, str(env.objetos_frame[a]), "-> ", reward_ind[a])
            print("El agente uso la red neuronal en: ",
                  agentes[a].counter_qn, "/", lim, "pasos. ")
            if agentes[a].counter_qn > 0:
                print("En promedio requirio de:",
                      agentes[a].timecounter_qn/agentes[a].counter_qn, "s, para dichos pasos")
            else:
                print("En promedio requirio de: 0s, para dichos pasos")
            print("El agente tomo decisiones aleatorias en: ",
                  agentes[a].counter_rand, "/", lim, "pasos. ")
            if agentes[a].counter_rand > 0:
                print("En promedio requirio de:",
                      agentes[a].timecounter_rand/agentes[a].counter_rand, "s, para dichos pasos")
            else:
                print("En promedio requirio de: 0s, para dichos pasos")
            agentes[a].resetCounters()
        # env.expCounter+=1

        # if done:
        # Se llego a un estado terminal al final del entrenamiento, donde env.maxRewad>= minReward
           # print("*******************************************************************************************************")
           # print("                                           FIN DE LA PARTIDA")
           # print("*******************************************************************************************************")

        # Se almacena el historico de mejores recompensas
         # with open(drivePath+''+env.rewardsFile,'ab') as f:
           # np.save(f, np.array([env.maxReward]))

        # Se almacena el historico de recompensas total
         # with open(path+''+env.totalRFile,'ab') as f:
        #  np.save(f, np.array([score]))

        # Se almacena el historico de recompensas promedio
       #  with open(drivePath+''+env.promRFile,'ab') as f:
    #     np.save(f, np.array([avg_score]))
    #     if i+1%2==0:
    #      print("Guardando progreso de entrenamiento")
#        agent.save_model()

    end = time.time()
    print("Terminando en:", time.ctime(end))
    return {"salud_torre": env.historico_towerHealth, "salud_atacantes": env.historico_atackerTeamHealth, "experiencia_atacantes": env.historico_atackerTeamExperience, "distanciasVsTorre_atacantes": env.historico_atackerTeamDistVsTorre, "recompensas_atacantes": env.historico_atackerTeamRewards, "decisiones_atacantes": env.historico_atackerTeamDecisiones, "nivel_atacantes": env.historico_atackerTeamNivel}

    # print("Epsilon: ", agent.epsilon)

    # with open(drivePath+'/'+"bestlevel"+exp+"_train"+str(i)+"."+str(env.bestMove)+".npy", 'wb') as f:
    # np.save(f, np.array(proceso[:env.bestMove+1]), allow_pickle=True)
