import pygame
from pygame.sprite import Group
import constante_1
import math
import random
import time


class Weapon():
    def __init__(self, image, imagen_BLuz):
        self.imagen_BLuz = imagen_BLuz
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(
            self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()
        self.dispara = False
        self.ultimo_disparo = pygame.time.get_ticks()
        self.incremento_dano = 1  # Variable para controlar el aumento del daño

    def update(self, personaje):
        disparo_cooldown = constante_1.COOLDOWN_BLuz
        BLuz = None
        self.forma.center = personaje.forma.center
        if personaje.flip == False:
            self.forma.x = self.forma.x + personaje.forma.width / 2.1
            self.rotar_arma(False)
        if personaje.flip == True:
            self.forma.x = self.forma.x - personaje.forma.width / 2.1
            self.rotar_arma(True)
        self.forma.y = self.forma.y + -0.3

        # Mover Baculo con Mause
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))

        # Detectar balas/golpes con mouse
        if pygame.mouse.get_pressed()[0] and self.dispara == False and (pygame.time.get_ticks() - self.ultimo_disparo >= disparo_cooldown):
            BLuz = Bullet(self.imagen_BLuz, self.forma.centerx,
                          self.forma.centery, self.angulo, self.incremento_dano)
            self.ultimo_disparo = pygame.time.get_ticks()
            self.dispara = True

        # Resetear click del mouse
        if pygame.mouse.get_pressed()[0] == False:
            self.dispara = False
        return BLuz

    def rotar_arma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(
                self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(
                self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)

    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.forma)
        # pygame.draw.rect(ventana, constante_1.COLOR_ARMA, self.forma, 1) --> Podemos ver las dimensiones del Baculo
        # pygame.draw.rect(ventana, constante_1.COLOR_ARMA, self.forma, 1) --> Podemos ver las dimensiones del Baculo


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, incremento_dano):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.incremento_dano = incremento_dano

        # Guardar la posición inicial del disparo
        self.inicial_x = x
        self.inicial_y = y

        # Calculo de la velocidad de disparo
        self.delta_x = math.cos(math.radians(
            self.angulo)) * constante_1.VELOCIDAD_BLuz
        self.delta_y = -math.sin(math.radians(self.angulo)
                                 ) * constante_1.VELOCIDAD_BLuz

    def update(self, lista_enemigos):
        daño = 0
        pos_daño = None
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        # Calcular la distancia recorrida
        distancia_recorrida = math.sqrt(
            (self.rect.x - self.inicial_x) ** 2 + (self.rect.y - self.inicial_y) ** 2)

        # Si la distancia supera el ALCANCE_MAXIMOBASICO, eliminar la bala
        if distancia_recorrida > constante_1.ALCANCE_MAXIMOBASICO:
            self.kill()

        # BLuz Fuera de pantalla
        if self.rect.right < 0 or self.rect.left > constante_1.ANCHO_VENTANA or self.rect.bottom < 0 or self.rect.top > constante_1.ALTO_VENTANA:
            self.kill()

        # Verificacion de colision con enemigos
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                daño = (100 + random.randint(-25, 20)) * \
                    self.incremento_dano  # Aplicar el incremento del daño
                pos_daño = enemigo.forma
                enemigo.energia -= daño
                self.kill()
                break

        return daño, pos_daño

    # ------------------------------------------------

    def dibujar(self, ventana):
        ventana.blit(self.image, (self.rect.centerx,
                     self.rect.centery - int(self.image.get_height())))


class Explosion(pygame.sprite.Sprite):
    def __init__(self, image, x, y, incremento_dano):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            image, (constante_1.ALCANCE_MAXIMO21 * 2, constante_1.ALCANCE_MAXIMO21 * 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.incremento_dano = incremento_dano
        self.tiempo_inicio = pygame.time.get_ticks()
        self.daño_aplicado = False

    def update(self, lista_enemigos, Torre):
        daño = 0
        pos_daño = None

        if not self.daño_aplicado:  # Verificamos si el daño ya se ha aplicado
            # Aplicar daño a enemigos en el radio
            for enemigo in lista_enemigos:
                distancia = math.sqrt((enemigo.forma.centerx - self.rect.centerx)
                                      ** 2 + (enemigo.forma.centery - self.rect.centery) ** 2)
                if distancia <= constante_1.ALCANCE_MAXIMO21:
                    daño = (250 + random.randint(-10, 10)) * \
                        self.incremento_dano
                    enemigo.energia -= daño
                    pos_daño = enemigo.forma
                    print(f"Explosión causó {daño} de daño a un enemigo.")
                    break  # Salir del bucle

            # Verificar daño a la torre
            distancia_torre = math.sqrt(
                (Torre.forma.centerx - self.rect.centerx) ** 2 + (Torre.forma.centery - self.rect.centery) ** 2)
            if distancia_torre <= constante_1.ALCANCE_MAXIMO21:
                daño = (250 + random.randint(-10, 10)) * self.incremento_dano
                Torre.recibir_dano(daño)
                pos_daño = Torre.forma
                print(f"Explosión causó {daño} de daño a la torre.")

            self.daño_aplicado = True  # Marcamos que el daño ya se ha aplicado

        # Verificar si la explosión debe desaparecer
        if pygame.time.get_ticks() - self.tiempo_inicio > constante_1.DURACION_ATAQUEBASICO21 * 1000:
            self.kill()

        return daño, pos_daño

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect.topleft)


class AtaEsp22(pygame.sprite.Sprite):
    ultimo_uso = 0  # Variable de clase para el enfriamiento

    @classmethod
    def puede_usarse(cls):
        """Verifica si el ataque está listo para usarse (enfriamiento)."""
        tiempo_actual = time.time()
        return tiempo_actual - cls.ultimo_uso >= constante_1.TIEMPO_ENFRIAMIENTO_ATA_ESP22

    @classmethod
    def registrar_uso(cls):
        """Registra el último uso del ataque para aplicar enfriamiento."""
        cls.ultimo_uso = time.time()

    def __init__(self, image, x, y, direccion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = constante_1.VELOCIDAD_ATA_ESP22
        self.daño_base = constante_1.DAÑO_BASE_ATA_ESP22
        self.incremento_dano = 1
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = constante_1.DURACION_ATA_ESP22 * 1000
        self.daño_registrado = False

        # Convertimos el radio de cuadriculas a píxeles
        self.radio_ataque = constante_1.RADIO_ATA_ESP22_CUADRICULAS * constante_1.TILE_SIZE

        # 🔹 Dirección normalizada
        dx, dy = direccion
        distancia = max(1, (dx**2 + dy**2) ** 0.5)  # Evita dividir por 0
        self.direccion_x = (dx / distancia) * self.velocidad
        self.direccion_y = (dy / distancia) * self.velocidad

    def update(self, lista_enemigos, torre):
        """Mueve el proyectil y maneja su duración e impacto."""
        tiempo_actual = pygame.time.get_ticks()

        # 🔹 Si el ataque ya superó su duración, se elimina
        if tiempo_actual - self.tiempo_inicio > self.duracion:
            print("Proyectil desapareció por duración cumplida.")
            self.kill()
            return 0, None

        # 🔹 Mover el proyectil en la dirección indicada
        self.rect.x += self.direccion_x
        self.rect.y += self.direccion_y
        print(f" Proyectil moviéndose a ({self.rect.x}, {self.rect.y})")

        # 🔹 Verificar colisión con enemigos y la torre
        for enemigo in lista_enemigos + [torre]:
            if enemigo.forma.colliderect(self.rect):
                if not self.daño_registrado:  # Evita que el daño se aplique varias veces
                    daño = (self.daño_base + random.randint(-10, 10)) * \
                        self.incremento_dano
                    enemigo.energia -= daño
                    print(
                        f" ¡Impacto! Daño de {daño} a enemigo/torre en ({enemigo.forma.centerx}, {enemigo.forma.centery})")

                    self.daño_registrado = True
                    self.kill()  # Desaparece el proyectil inmediatamente después de impactar

                    return daño, enemigo.forma

        return 0, None  # No hay colisión, el proyectil sigue moviéndose

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect.topleft)


class AtaEspMAX(pygame.sprite.Sprite):
    ultimo_uso = 0  # Control de enfriamiento

    @classmethod
    def puede_usarse(cls):
        """Verifica si el ataque está listo para usarse (enfriamiento)."""
        tiempo_actual = time.time()
        return tiempo_actual - cls.ultimo_uso >= constante_1.TIEMPO_ENFRIAMIENTO_ATA_ESPMAX

    @classmethod
    def registrar_uso(cls):
        """Registra el último uso del ataque para aplicar enfriamiento."""
        cls.ultimo_uso = time.time()

    def __init__(self, image, x, y, direccion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = constante_1.VELOCIDAD_ATA_ESPMAX
        self.daño_base = constante_1.DAÑO_BASE_ATA_ESPMAX
        self.incremento_dano = 1
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = constante_1.DURACION_ATA_ESPMAX * 1000
        self.daño_registrado = False

        # Convertimos el radio de cuadriculas a píxeles
        self.radio_ataque = constante_1.RADIO_ATA_ESPMAX_CUADRICULAS * constante_1.TILE_SIZE

        # 🔹 Dirección normalizada
        dx, dy = direccion
        distancia = max(1, (dx**2 + dy**2) ** 0.5)  # Evita dividir por 0
        self.direccion_x = (dx / distancia) * self.velocidad
        self.direccion_y = (dy / distancia) * self.velocidad

    def update(self, lista_enemigos, torre):
        """Mueve el proyectil y maneja su duración e impacto."""
        tiempo_actual = pygame.time.get_ticks()

        # 🔹 Si el ataque ya superó su duración, se elimina
        if tiempo_actual - self.tiempo_inicio > self.duracion:
            print("AtaEspMAX desapareció por duración cumplida.")
            self.kill()
            return 0, None

        # 🔹 Mover el proyectil
        self.rect.x += self.direccion_x
        self.rect.y += self.direccion_y

        # 🔹 Verificar colisión con enemigos y la torre
        for enemigo in lista_enemigos + [torre]:
            if enemigo.forma.colliderect(self.rect):
                if not self.daño_registrado:
                    daño = (self.daño_base + random.randint(-10, 10)) * \
                        self.incremento_dano
                    enemigo.energia -= daño
                    print(
                        f"AtaEspMAX impactó con daño {daño} en {enemigo.forma.center}")

                    self.daño_registrado = True
                    self.kill()  # Desaparece el proyectil al impactar
                    return daño, enemigo.forma

        return 0, None  # No hay colisión, el proyectil sigue moviéndose

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect.topleft)
