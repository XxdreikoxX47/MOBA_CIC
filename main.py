import pygame
import csv
import constante_1
from Personaje import Personaje
import objetos_test
import trainMOBAgents_quasi
from weapon import Weapon
from weapon import Explosion
from weapon import AtaEsp22
from weapon import AtaEspMAX
from Menus import MenuCargaUsuario, MenuCargar, MenuRegistro, MenuDificultad, MenuPausa
# Importar la función de carga de pantalla
from PantallaCarga import pantalla_de_carga
import os
from Textos import DamageText
import time
import AvatarAtacante
import random
import math
import Menus

# ------------------------- Pasar a constantes ---------------------------


# Dimensiones del mapa
MAP_WIDTH = 5000
MAP_HEIGHT = 5000

# Variables del ataque especial
ataque_especial = False
tiempo_ultimo_ataque_especial = 0
TIEMPO_ENFIRAMIENTO = 90  # 1 minuto y 30 segundos
DURACION_ATAQUE_ESPECIAL = 5  # Duración del ataque especial en segundos


ataque_explosion_activo = False
ataque_explosion_timer = 0
DURACION_ATAQUE_EXPLOSION = 3  # Duración del ataque de explosión en segundos
# Tiempo de enfriamiento para el ataque de explosión en segundos
TIEMPO_ENFRIAMIENTO_EXPLOSION = 5
tiempo_ultimo_ataque_explosion = 0


ataque_especial_cargando = False  # Indica si se está cargando el ataque
direccion_ataque = None  # Almacena la dirección del proyectil


# ----------------------------------------------------------------------

# Inicialización del avatar
avatar = AvatarAtacante.AvatarAtacante(
    x=constante_1.ANCHO_VENTANA // 2, y=constante_1.ALTO_VENTANA // 2)

# Inicializar objetos_frame
objetos_frame = {}

# Definir un mapa sencillo
tu_mapa = [
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0]
    #  [['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'aat1' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'cnt1' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 't2' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'cnt1' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
    # ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']]
]

# Asignar el mapa al avatar
avatar.lecturaMapa(tu_mapa)

# Funciones:


def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(
        image, (int(w * scale), int(h * scale)))
    return nueva_imagen


def contar_elementos(directorio):
    return len(os.listdir(directorio))


def nombre_carpetas(directorio):
    return os.listdir(directorio)


pygame.init()

ventana = pygame.display.set_mode(
    (constante_1.ANCHO_VENTANA, constante_1.ALTO_VENTANA))
pygame.display.set_caption("Proyecto CIC_MOBA")

font = pygame.font.Font("assets//Fonts//mago2.ttf", 80)

background_image = pygame.image.load(
    'assets//images//Escenarios//Fondo_pasto.png')
bg_width, bg_height = background_image.get_size()

animaciones = []
for i in range(7):
    img = pygame.image.load(
        f"assets//images//characters/Player/player_{i}.png").convert_alpha()
    img = escalar_img(img, constante_1.SCALA_PERSONAJE)
    animaciones.append(img)

directorio_enemigos = "assets//images//characters//Enemigos"
tipo_enemigos = nombre_carpetas(directorio_enemigos)

enemigos = []  # Lista para almacenar los enemigos

for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets//images//characters//Enemigos//{eni}"
    num_animaciones = contar_elementos(ruta_temp)

    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(
            f"{ruta_temp}//{eni}_{i + 1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constante_1.SCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)

    # Crear objeto Personaje para el enemigo
    enemigo_obj = Personaje(random.randint(0, constante_1.ANCHO_VENTANA),
                            random.randint(0, constante_1.ALTO_VENTANA),
                            lista_temp,  # Animaciones del enemigo
                            100,  # Vida del enemigo
                            1)    # Velocidad o nivel del enemigo

    enemigos.append(enemigo_obj)  # Agregar enemigo a la lista


imagen_Baculo = pygame.image.load(
    f"assets//images//Weaponds//Magico_0.png").convert_alpha()
imagen_Baculo = escalar_img(imagen_Baculo, constante_1.SCALA_BACULO)

imagen_BLuz = pygame.image.load(
    f"assets//images//Weaponds//BLuz.png").convert_alpha()
imagen_BLuz = escalar_img(imagen_BLuz, constante_1.SACALA_BLUZ)

tile_list = []
for x in range(constante_1.TILE_TYPES):
    tile_image = pygame.image.load(f"assets//images//Tiles//tile_{x + 1}.png")
    tile_image = pygame.transform.scale(
        tile_image, (constante_1.TILE_SIZE, constante_1.TILE_SIZE))
    tile_list.append(tile_image)

# Cargar las imágenes de los árboles
arbol_image = pygame.image.load(
    f"assets//images//Plantas//Arbol_1.png").convert_alpha()
arbol_image = escalar_img(arbol_image, 0.6)

# Definir las posiciones de los árboles en el mapa
posiciones_arboles = [(500, 300), (1000, 800),
                      (1500, 1200), (2000, 500), (2500, 1500)]

# Crear rectángulos de colisión para los árboles
rectangulos_arboles = [arbol_image.get_rect(
    topleft=pos) for pos in posiciones_arboles]

# Dibuja cuadricula en pantalla para mediciones


def dibujar_grid():
    tile_width = constante_1.ANCHO_VENTANA // constante_1.COLUMNAS
    tile_height = constante_1.ALTO_VENTANA // constante_1.FILAS

    for x in range(constante_1.COLUMNAS + 1):
        pygame.draw.line(ventana, constante_1.BLANCO,
                         (x * tile_width, 0),
                         (x * tile_width, constante_1.ALTO_VENTANA))

        for y in range(constante_1.FILAS + 1):
            pygame.draw.line(ventana, constante_1.BLANCO,
                             (0, y * tile_height),
                             (constante_1.ANCHO_VENTANA, y * tile_height))

        # pygame.draw.line(ventana, constante_1.BLANCO, (x * constante_1.TILE_SIZE, 0), (x * constante_1.TILE_SIZE, constante_1.ALTO_VENTANA))
        # pygame.draw.line(ventana, constante_1.BLANCO, (0, x * constante_1.TILE_SIZE), (constante_1.ANCHO_VENTANA, x * constante_1.TILE_SIZE))


jugador = Personaje(constante_1.ANCHO_VENTANA // 2,
                    constante_1.ALTO_VENTANA // 2, animaciones, 100, 1)

# Configurar la posición fija de la torre en el mapa
torre_posicion_fija = (1500, 400)
torre_imagen = pygame.image.load(
    f"assets//images//characters//Enemigos//{tipo_enemigos[1]}//{tipo_enemigos[1]}_1.png").convert_alpha()
torre_imagen = escalar_img(torre_imagen, constante_1.SCALA_PERSONAJET)

# Crear objeto Torre
Torre = Personaje(torre_posicion_fija[0], torre_posicion_fija[1], [
                  torre_imagen], 2000, 2)

# Añadir Torre a objetos_frame
objetos_frame["torre"] = Torre

Baculo = Weapon(imagen_Baculo, imagen_BLuz)
grupo_damage_text = pygame.sprite.Group()
grupo_BLuz = pygame.sprite.Group()
grupo_ata_esp22 = pygame.sprite.Group()
grupo_explosiones = pygame.sprite.Group()
grupo_ata_espMAX = pygame.sprite.Group()

Mover_arriba = False
Mover_abajo = False
Mover_derecha = False
Mover_izquierda = False
Basico_1 = 25
reloj = pygame.time.Clock()
run = True

# Variables de desplazamiento del fondo
bg_scroll_x = 0
bg_scroll_y = 0

area_ataque_rect = pygame.Rect(0, 0, 0, 0)

ajuste_x = 50
ajuste_y = 30

# Cargar la imagen del ataque básico (proporciona la ruta correcta)
ataqueEspecial21_img = pygame.image.load(
    "assets/images/Weaponds/FireBool_2_1.png").convert_alpha()
ataqueEspecial21_img = escalar_img(
    ataqueEspecial21_img, constante_1.SCALA_ATAQUE_ESPECIAL21)

# Cargar la imagen del ataque especial básico (proporciona la ruta correcta)
ataqueEspecial11_img = pygame.image.load(
    "assets/images/Weaponds/BolaMorada.png").convert_alpha()
ataqueEspecial11_img = escalar_img(
    ataqueEspecial11_img, constante_1.SCALA_ATAQUE_ESPECIAL11)

# Cargar la imagen del ataque especial básico (proporciona la ruta correcta)
ataqueEspecialMAX_img = pygame.image.load(
    "assets/images/Weaponds/FireboolRed.png").convert_alpha()
ataqueEspecialMAX_img = escalar_img(
    ataqueEspecialMAX_img, constante_1.SCALA_ATAQUE_ESPECIALMAX)

# Cargar la imagen del nuevo ataque (explosión)
ataqueExplosion_img = pygame.image.load(
    "assets/images/Weaponds/FireBool_2_1.png").convert_alpha()
ataqueExplosion_img = escalar_img(
    ataqueExplosion_img, constante_1.SCALA_ATAQUE_EXPLOSION)


en_area_ataque = False

# --------Pasar a contantes-------------

# Una bandera para indicar cuando el ataque está activo
ataque_basico_activo = False
ataque_especial_basico1_activo = False
# Agregar temporizador para el ataque especial básico
ataque_especial_basico1_timer = 0

# Variables de control de ataques
ataque_basico_activo = False
ataque_especial_basico1_activo = False
ataque_basico_timer = 0
ataque_especial_basico1_timer = 0

DURACION_ATAQUE_BASICO = 0.5  # Duración del ataque básico en segundos
# -----------------------------------------------------------
enemigos = []


# Crear menús
menu_principal = Menus.MenuPrin(ventana)
menu_carga_usuario = Menus.MenuCargaUsuario(ventana)
menu_cargar = Menus.MenuCargar(ventana)
menu_registro = Menus.MenuRegistro(ventana)
menu_dificultad = Menus.MenuDificultad(ventana)
menu_pausa = Menus.MenuPausa(ventana)

# --- Variables de Control ---
jugando = True
pausado = False
ejecutando_menu = True
salir_al_menu_carga = False

# --- Bucle Principal del Menú ---
while ejecutando_menu:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                menu_principal.mover_seleccion("arriba")
            elif evento.key == pygame.K_DOWN:
                menu_principal.mover_seleccion("abajo")
            elif evento.key == pygame.K_RETURN:
                opcion = menu_principal.seleccionar_opcion()

                if opcion == "Iniciar Juego":
                    ejecutando_menu_cargar = True

                    while ejecutando_menu_cargar:
                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                            elif evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_UP:
                                    menu_cargar.mover_seleccion("arriba")
                                elif evento.key == pygame.K_DOWN:
                                    menu_cargar.mover_seleccion("abajo")
                                elif evento.key == pygame.K_RETURN:
                                    opcion_cargar = menu_cargar.seleccionar_opcion()

                                    # --- REGISTRAR USUARIO ---
                                    if opcion_cargar == "Registrar Usuario":
                                        ejecutando_menu_registro = True
                                        while ejecutando_menu_registro:
                                            for evento in pygame.event.get():
                                                if evento.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()
                                                elif evento.type == pygame.KEYDOWN:
                                                    resultado = menu_registro.manejar_eventos(
                                                        evento)

                                                    if isinstance(resultado, str):
                                                        if "Registrar Usuario" in resultado:
                                                            nombre = resultado.split(
                                                                ": ")[1]
                                                            menu_carga_usuario.agregar_usuario(
                                                                nombre)
                                                            # Actualizar la lista de usuarios del menú de carga de usuario
                                                            menu_carga_usuario.usuarios = menu_carga_usuario.cargar_usuarios()
                                                            ejecutando_menu_registro = False
                                                        elif resultado == "RegresarCargar":
                                                            ejecutando_menu_registro = False
                                            menu_registro.dibujar()
                                            pygame.display.flip()

                                    # --- CARGAR USUARIO ---
                                    elif opcion_cargar == "Cargar Usuario":
                                        if not menu_carga_usuario.usuarios:
                                            print(
                                                "No hay usuarios registrados.")
                                        else:
                                            ejecutando_menu_carga_usuario = True
                                            while ejecutando_menu_carga_usuario:
                                                resultado_dificultad = None  # Inicializar aquí
                                                for evento in pygame.event.get():
                                                    if evento.type == pygame.QUIT:
                                                        pygame.quit()
                                                        exit()
                                                    elif evento.type == pygame.KEYDOWN:
                                                        if evento.key == pygame.K_UP:
                                                            menu_carga_usuario.mover_seleccion(
                                                                "arriba")
                                                        elif evento.key == pygame.K_DOWN:
                                                            menu_carga_usuario.mover_seleccion(
                                                                "abajo")
                                                        elif evento.key == pygame.K_RETURN:
                                                            usuario_seleccionado = menu_carga_usuario.seleccionar_opcion()
                                                            if usuario_seleccionado == "RegresarCargar":
                                                                ejecutando_menu_carga_usuario = False
                                                            elif usuario_seleccionado:
                                                                ejecutando_menu_dificultad = True
                                                                while ejecutando_menu_dificultad:
                                                                    for evento in pygame.event.get():
                                                                        if evento.type == pygame.QUIT:
                                                                            pygame.quit()
                                                                            exit()
                                                                        elif evento.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                                                                            resultado_dificultad = menu_dificultad.manejar_eventos(
                                                                                evento)
                                                                            if resultado_dificultad == "Regresar":
                                                                                ejecutando_menu_dificultad = False
                                                                        elif resultado_dificultad in ["Facil", "Intermedio", "Dificil"]:
                                                                            print(
                                                                                f"Usuario: {usuario_seleccionado}")
                                                                            print(
                                                                                f"Dificultad seleccionada: {resultado_dificultad}")

                                                                            imagenes_cargadas = pantalla_de_carga(
                                                                                ventana)
                                                                            # Asigna el fondo precargado
                                                                            background_image = imagenes_cargadas[0]
                                                                            # Asigna el báculo precargado
                                                                            imagen_Baculo = imagenes_cargadas[3]
                                                                            # Asigna la luz precargada
                                                                            imagen_BLuz = imagenes_cargadas[4]

                                                                            ejecutando_menu_dificultad = False
                                                                            ejecutando_menu_carga_usuario = False
                                                                            ejecutando_menu_cargar = False
                                                                            ejecutando_menu = False
                                                                            print(
                                                                                "Comienza la partida")
                                                                    menu_dificultad.dibujar()
                                                                    pygame.display.flip()
                                                menu_carga_usuario.dibujar()
                                                pygame.display.flip()

                                    elif opcion_cargar == "Regresar":
                                        ejecutando_menu_cargar = False

                        menu_cargar.dibujar()
                        pygame.display.flip()

                elif opcion == "Salir":
                    pygame.quit()
                    exit()

    menu_principal.dibujar()
    pygame.display.flip()

jugando = True
pausado = False
run = True
salir_al_menu_carga = False


while run:
    reloj.tick(constante_1.FPS)

    # 1. Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pausado = not pausado  # Alternar el estado de pausa
            if not pausado:
                # Procesar otras teclas para el juego (movimiento, ataques, etc.)
                if event.key == pygame.K_a:
                    Mover_izquierda = True
                if event.key == pygame.K_d:
                    Mover_derecha = True
                if event.key == pygame.K_w:
                    Mover_arriba = True
                if event.key == pygame.K_s:
                    Mover_abajo = True
                # ATAQUE ESPECIAL "E"
                if event.key == pygame.K_e and not ataque_especial_cargando:
                    ataque_especial_cargando = True
                    print(" Cargando ataque especial (Modo apuntado activado)...")
                # ATAQUE ESPECIAL "R"
                if event.key == pygame.K_r and not ataque_especial_cargando:
                    ataque_especial_cargando = True
                    print(" Cargando ataque especial (Modo apuntado activado)...")
                # ATAQUE CON "P"
                if event.key == pygame.K_p and en_area_ataque and not ataque_especial:
                    tiempo_ahora = time.time()
                    if tiempo_ahora - tiempo_ultimo_ataque_especial >= TIEMPO_ENFIRAMIENTO:
                        ataque_especial = True
                        tiempo_ultimo_ataque_especial = tiempo_ahora
                        Baculo.incremento_dano = 2
                        print(
                            f"Ataque especial activado. Durará {DURACION_ATAQUE_ESPECIAL} segundos.")
                # ATAQUE ESPECIAL 21 "Q"
                if event.key == pygame.K_q:
                    tiempo_ahora = time.time()
                    if tiempo_ahora - tiempo_ultimo_ataque_explosion >= TIEMPO_ENFRIAMIENTO_EXPLOSION:
                        print("Ejecutando ataque de explosión...")
                        ataque_explosion_timer = tiempo_ahora
                        tiempo_ultimo_ataque_explosion = tiempo_ahora
                        nueva_explosion = Explosion(
                            ataqueExplosion_img, jugador.forma.centerx, jugador.forma.centery, 1)
                        grupo_explosiones.add(nueva_explosion)
                    else:
                        tiempo_restante_enfriamiento = int(
                            TIEMPO_ENFRIAMIENTO_EXPLOSION - (tiempo_ahora - tiempo_ultimo_ataque_explosion))
                        print(
                            f"El ataque de explosión está en enfriamiento. Tiempo restante: {tiempo_restante_enfriamiento} segundos")
                # ATAQUE ESPECIAL BÁSICO "I"
                if event.key == pygame.K_i:
                    print("Ejecutando ataque básico...")
                    avatar.ataqueEspecial21(objetos_frame, font)
                    ataque_basico_activo = True
                    ataque_basico_timer = time.time()

        elif event.type == pygame.KEYUP:
            if not pausado:
                # Procesar soltar teclas de movimiento
                if event.key == pygame.K_a:
                    Mover_izquierda = False
                if event.key == pygame.K_d:
                    Mover_derecha = False
                if event.key == pygame.K_w:
                    Mover_arriba = False
                if event.key == pygame.K_s:
                    Mover_abajo = False
                # SOLTAR "E" PARA DISPARAR ATAQUE ESPECIAL 1
                if event.key == pygame.K_e and ataque_especial_cargando:
                    if AtaEsp22.puede_usarse():
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        direccion_ataque = (
                            mouse_x - jugador.forma.centerx, mouse_y - jugador.forma.centery)
                        print(
                            f" Dirección de disparo capturada: {direccion_ataque}")
                        nuevo_proyectil = AtaEsp22(
                            ataqueEspecial11_img, jugador.forma.centerx, jugador.forma.centery, direccion_ataque)
                        grupo_ata_esp22.add(nuevo_proyectil)
                        print(
                            f" Proyectil lanzado desde ({jugador.forma.centerx}, {jugador.forma.centery}) hacia {direccion_ataque}")
                        AtaEsp22.registrar_uso()
                        print(" Ataque en enfriamiento...")
                    else:
                        tiempo_restante = constante_1.TIEMPO_ENFRIAMIENTO_ATA_ESP22 - \
                            (time.time() - AtaEsp22.ultimo_uso)
                        print(
                            f" El ataque especial está en enfriamiento. Tiempo restante: {int(tiempo_restante)} segundos")
                    ataque_especial_cargando = False  # Desactivamos la carga
                # SOLTAR "R" PARA DISPARAR ATAQUE ESPECIAL MAX
                if event.key == pygame.K_r and ataque_especial_cargando:
                    if AtaEspMAX.puede_usarse():
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        direccion_ataque = (
                            mouse_x - jugador.forma.centerx, mouse_y - jugador.forma.centery)
                        print(
                            f"Dirección de disparo capturada: {direccion_ataque}")
                        nuevo_proyectil = AtaEspMAX(
                            ataqueEspecialMAX_img, jugador.forma.centerx, jugador.forma.centery, direccion_ataque)
                        grupo_ata_espMAX.add(nuevo_proyectil)
                        print(
                            f"Proyectil AtaEspMAX lanzado hacia {direccion_ataque}")
                        AtaEspMAX.registrar_uso()
                        print("AtaEspMAX en enfriamiento...")
                    else:
                        tiempo_restante = constante_1.TIEMPO_ENFRIAMIENTO_ATA_ESPMAX - \
                            (time.time() - AtaEspMAX.ultimo_uso)
                        print(
                            f"AtaEspMAX en enfriamiento. Tiempo restante: {int(tiempo_restante)} segundos")
                    ataque_especial_cargando = False

    # 2. Actualizar el juego (solo si no está pausado)
    if not pausado:
        delta_x = 0
        delta_y = 0
        if Mover_derecha:
            delta_x = constante_1.VELOCIDAD
        if Mover_izquierda:
            delta_x = -constante_1.VELOCIDAD
        if Mover_arriba:
            delta_y = -constante_1.VELOCIDAD
        if Mover_abajo:
            delta_y = constante_1.VELOCIDAD

        if not (0 <= bg_scroll_x + delta_x <= MAP_WIDTH - constante_1.ANCHO_VENTANA):
            delta_x = 0
        if not (0 <= bg_scroll_y + delta_y <= MAP_HEIGHT - constante_1.ALTO_VENTANA):
            delta_y = 0

        jugador_rect_nuevo = jugador.forma.copy()
        jugador_rect_nuevo.x += delta_x
        jugador_rect_nuevo.y += delta_y

        colision = False
        for rect in rectangulos_arboles:
            rect.x -= bg_scroll_x
            rect.y -= bg_scroll_y
            if jugador_rect_nuevo.colliderect(rect):
                colision = True
            rect.x += bg_scroll_x
            rect.y += bg_scroll_y

        if not colision:
            bg_scroll_x += delta_x
            bg_scroll_y += delta_y

        posicion_pantalla = jugador.movimiento(delta_x, delta_y)
        jugador.update()

        BLuz_instance = Baculo.update(jugador)
        if BLuz_instance:
            grupo_BLuz.add(BLuz_instance)
        for luz in grupo_BLuz:
            damage, pos_damage = luz.update([Torre])
            if damage != 0:
                damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(
                    damage), font, constante_1.ROJO)
                grupo_damage_text.add(damage_text)

        for explosion in grupo_explosiones:
            damage, pos_damage = explosion.update(enemigos, Torre)
            if damage != 0:
                damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(
                    damage), font, constante_1.ROJO)
                grupo_damage_text.add(damage_text)

        for explosion in grupo_explosiones:
            explosion.update(enemigos, Torre)

        for proyectil in grupo_ata_esp22.copy():
            daño, pos_daño = proyectil.update(enemigos, Torre)
            if daño != 0 and pos_daño is not None:
                damage_text = DamageText(
                    pos_daño.centerx, pos_daño.centery, str(daño), font, constante_1.ROJO)
                grupo_damage_text.add(damage_text)
            if not proyectil.alive():
                grupo_ata_esp22.remove(proyectil)

        grupo_damage_text.update()

        for proyectil in grupo_ata_espMAX.copy():
            daño, pos_daño = proyectil.update(enemigos, Torre)
            if daño != 0 and pos_daño is not None:
                damage_text = DamageText(
                    pos_daño.centerx, pos_daño.centery, str(daño), font, constante_1.ROJO)
                grupo_damage_text.add(damage_text)
            if not proyectil.alive():
                grupo_ata_espMAX.remove(proyectil)

        # Validar tiempo de ataque básico
        if ataque_basico_activo and time.time() - ataque_basico_timer > DURACION_ATAQUE_BASICO:
            ataque_basico_activo = False

        # Validar tiempo de ataque especial básico
        if ataque_especial_basico1_activo and time.time() - time.time() > DURACION_ATAQUE_ESPECIAL:
            ataque_especial_basico1_activo = False

        # Validar tiempo de ataque de explosión
        if ataque_explosion_activo and time.time() - ataque_explosion_timer > DURACION_ATAQUE_EXPLOSION:
            ataque_explosion_activo = False

    # 3. Dibujar en la pantalla
    for x in range(-bg_width, constante_1.ANCHO_VENTANA + bg_width, bg_width):
        for y in range(-bg_height, constante_1.ALTO_VENTANA + bg_height, bg_height):
            ventana.blit(background_image, (x - bg_scroll_x %
                                            bg_width, y - bg_scroll_y % bg_height))

    for pos in posiciones_arboles:
        ventana.blit(arbol_image, (pos[0] - bg_scroll_x, pos[1] - bg_scroll_y))

    ventana.blit(
        torre_imagen, (torre_posicion_fija[0] - bg_scroll_x, torre_posicion_fija[1] - bg_scroll_y))
    Torre.forma.topleft = (
        torre_posicion_fija[0] - bg_scroll_x, torre_posicion_fija[1] - bg_scroll_y)

    pygame.draw.rect(ventana, constante_1.ROJO, area_ataque_rect, 2)

    Baculo.dibujar(ventana)
    for luz in grupo_BLuz:
        luz.dibujar(ventana)
    grupo_damage_text.draw(ventana)
    for proyectil in grupo_ata_esp22:
        proyectil.dibujar(ventana)
    for proyectil in grupo_ata_espMAX:
        proyectil.dibujar(ventana)

    if ataque_basico_activo:
        ventana.blit(
            ataqueEspecial21_img,
            (jugador.forma.centerx - ataqueEspecial21_img.get_width() // 2,
             jugador.forma.centery - ataqueEspecial21_img.get_height() // 2)
        )

    if ataque_especial_basico1_activo:
        ventana.blit(
            ataqueEspecial11_img,
            (jugador.forma.centerx - ataqueEspecial11_img.get_width() // 2,
             jugador.forma.centery - ataqueEspecial11_img.get_height() // 2)
        )

    for explosion in grupo_explosiones:
        explosion.dibujar(ventana)
    jugador.dibujar(ventana)
    dibujar_grid()

    if pausado:
        menu_pausa.dibujar()
        # Manejar eventos del menú de pausa
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            resultado_pausa = menu_pausa.manejar_eventos(event)
            if resultado_pausa == "Continuar":
                pausado = False
            elif resultado_pausa == "Salir":  # Asegúrate de que coincida el texto
                run = False
                pausado = False
                ejecutando_menu = True  # Volver al menú principal

    pygame.display.flip()
    pygame.display.update()

pygame.quit()
