import pygame
import constante_1
import os  # Importar el módulo os


class MenuPrin:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.opciones = ["Iniciar Juego", "Salir"]
        self.opcion_seleccionada = 0
        self.fuente = pygame.font.Font(None, 50)  # Fuente predeterminada

    def dibujar(self):
        self.pantalla.fill((0, 0, 0))  # Fondo negro

        titulo_principal = pygame.font.Font(None, 100)

        titulos = [("MOBA CSCOG", (725, 200)),
                   (("Presiona Enter para continuar", (450, 350)))]  # Lista de títulos

        for texto, posicion in titulos:
            renderizado = titulo_principal.render(texto, True, (255, 255, 255))
            self.pantalla.blit(renderizado, posicion)

        for i, opcion in enumerate(self.opciones):
            color = (255, 255, 255) if i == self.opcion_seleccionada else (
                150, 150, 150)
            texto = self.fuente.render(opcion, True, color)
            self.pantalla.blit(texto, (800, 600 + i * 60)
                               )  # Posición de los textos

    def mover_seleccion(self, direccion):
        if direccion == "arriba":
            self.opcion_seleccionada = (
                self.opcion_seleccionada - 1) % len(self.opciones)
        elif direccion == "abajo":
            self.opcion_seleccionada = (
                self.opcion_seleccionada + 1) % len(self.opciones)

    def seleccionar_opcion(self):
        if self.opciones[self.opcion_seleccionada] == "Iniciar Juego":
            return "Iniciar Juego"
        elif self.opciones[self.opcion_seleccionada] == "Salir":
            return "Salir"


class MenuCargar:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.opciones = ["Registrar Usuario", "Cargar Usuario", "Regresar"]
        self.opcion_seleccionada = 0
        self.fuente = pygame.font.Font(None, 50)

    def dibujar(self):
        self.pantalla.fill((0, 0, 0))
        for i, opcion in enumerate(self.opciones):
            color = (255, 255, 255) if i == self.opcion_seleccionada else (
                150, 150, 150)
            texto = self.fuente.render(opcion, True, color)
            self.pantalla.blit(texto, (300, 200 + i * 60))

    def mover_seleccion(self, direccion):
        if direccion == "arriba":
            self.opcion_seleccionada = (
                self.opcion_seleccionada - 1) % len(self.opciones)
        elif direccion == "abajo":
            self.opcion_seleccionada = (
                self.opcion_seleccionada + 1) % len(self.opciones)

    def seleccionar_opcion(self):
        return self.opciones[self.opcion_seleccionada]


# En tu archivo Menus.py
class MenuCargaUsuario:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.font = pygame.font.Font(None, 36)
        # Cargar los usuarios al inicializar el menú
        self.usuarios = self.cargar_usuarios()
        self.seleccionado_indice = 0
        self.alto_elemento = 40
        self.margen_superior = 150

    def cargar_usuarios(self):
        usuarios_registrados = []
        if os.path.exists('usuarios'):
            for nombre_archivo in os.listdir('usuarios'):
                if nombre_archivo.endswith('.txt'):
                    # Remover la extensión .txt
                    nombre_usuario = nombre_archivo[:-4]
                    usuarios_registrados.append(nombre_usuario)
        return usuarios_registrados

    def agregar_usuario(self, nombre):
        if nombre not in self.usuarios:
            self.usuarios.append(nombre)
            # No es necesario volver a leer del disco aquí, ya lo hicimos al registrar

    def dibujar(self):
        self.pantalla.fill((0, 0, 0))
        titulo = self.font.render("Cargar Usuario", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(
            center=(constante_1.ANCHO_VENTANA // 2, 80))
        self.pantalla.blit(titulo, titulo_rect)

        for i, usuario in enumerate(self.usuarios):
            color = (200, 200, 200)
            if i == self.seleccionado_indice:
                color = (255, 255, 0)
            texto = self.font.render(usuario, True, color)
            rect = texto.get_rect(
                center=(constante_1.ANCHO_VENTANA // 2, self.margen_superior + i * self.alto_elemento))
            self.pantalla.blit(texto, rect)

        # Opción de regresar
        color_regresar = (200, 200, 200)
        # Si la selección está después de la lista
        if len(self.usuarios) == self.seleccionado_indice:
            color_regresar = (255, 255, 0)
        texto_regresar = self.font.render("Regresar", True, color_regresar)
        rect_regresar = texto_regresar.get_rect(center=(
            constante_1.ANCHO_VENTANA // 2, self.margen_superior + len(self.usuarios) * self.alto_elemento + 20))
        self.pantalla.blit(texto_regresar, rect_regresar)

    def mover_seleccion(self, direccion):
        if self.usuarios:
            if direccion == "arriba":
                self.seleccionado_indice = (
                    self.seleccionado_indice - 1) % (len(self.usuarios) + 1)
            elif direccion == "abajo":
                self.seleccionado_indice = (
                    self.seleccionado_indice + 1) % (len(self.usuarios) + 1)
        elif direccion == "abajo":  # Si no hay usuarios, permitir seleccionar "Regresar"
            # Cambiado a len(self.usuarios)
            self.seleccionado_indice = len(self.usuarios)

    def seleccionar_opcion(self):
        if self.usuarios:
            if self.seleccionado_indice < len(self.usuarios):
                return self.usuarios[self.seleccionado_indice]
            else:
                return "RegresarCargar"  # Modificado el retorno
        else:
            if self.seleccionado_indice == 0:  # Cambiado a 0
                return "RegresarCargar"  # Modificado el retorno
            return None


class MenuRegistro:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.opciones = ["Confirmar", "Regresar"]
        self.opcion_seleccionada = 0
        self.fuente = pygame.font.Font(None, 50)
        self.texto_nombre = ""
        self.cuadro_texto = pygame.Rect(300, 150, 400, 50)
        self.cuadro_activo = True

    def dibujar(self):
        self.pantalla.fill((0, 0, 0))

        # Dibujar cuadro de texto
        color_cuadro = (255, 255, 255) if self.cuadro_activo else (
            150, 150, 150)
        pygame.draw.rect(self.pantalla, (50, 50, 50), self.cuadro_texto)
        pygame.draw.rect(self.pantalla, color_cuadro, self.cuadro_texto, 2)

        texto_ingresado = self.fuente.render(
            self.texto_nombre, True, (255, 255, 255))
        self.pantalla.blit(
            texto_ingresado, (self.cuadro_texto.x + 10, self.cuadro_texto.y + 10))

        # Dibujar opciones
        for i, opcion in enumerate(self.opciones):
            color = (255, 255, 255) if i == self.opcion_seleccionada else (
                150, 150, 150)
            texto = self.fuente.render(opcion, True, color)
            self.pantalla.blit(texto, (300, 250 + i * 60))

    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if self.cuadro_activo:
                if evento.key == pygame.K_BACKSPACE:
                    self.texto_nombre = self.texto_nombre[:-1]
                elif evento.key == pygame.K_RETURN:
                    self.cuadro_activo = False
                else:
                    self.texto_nombre += evento.unicode
            else:
                if evento.key == pygame.K_UP:
                    self.mover_seleccion("arriba")
                elif evento.key == pygame.K_DOWN:
                    self.mover_seleccion("abajo")
                elif evento.key == pygame.K_RETURN:
                    return self.seleccionar_opcion()

    def mover_seleccion(self, direccion):
        if direccion == "arriba":
            self.opcion_seleccionada = (
                self.opcion_seleccionada - 1) % len(self.opciones)
        elif direccion == "abajo":
            self.opcion_seleccionada = (
                self.opcion_seleccionada + 1) % len(self.opciones)

    def seleccionar_opcion(self):
        if self.opciones[self.opcion_seleccionada] == "Confirmar":
            if self.texto_nombre:
                # Crear la carpeta 'usuarios' si no existe
                if not os.path.exists('usuarios'):
                    os.makedirs('usuarios')
                # Crear el archivo del usuario
                nombre_archivo = os.path.join(
                    'usuarios', f'{self.texto_nombre}.txt')
                try:
                    with open(nombre_archivo, 'w') as archivo:
                        archivo.write(
                            self.texto_nombre)  # Por ahora, solo guardamos el nombre
                    self.texto_nombre = ''  # Limpiar el campo de entrada
                    return f"Registrar Usuario: {self.texto_nombre}"
                except Exception as e:
                    print(f"Error al guardar el usuario: {e}")
                    return "Error al registrar"
            else:
                return "Por favor, introduce un nombre."
        elif self.opciones[self.opcion_seleccionada] == "Regresar":
            return "RegresarCargar"  # Modificado el retorno


class MenuDificultad:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.opciones = ["Facil", "Intermedio",
                         "Dificil", "Regresar"]
        self.opcion_seleccionada = 0
        self.fuente = pygame.font.Font(None, 50)

        self.cuadro_opciones = [pygame.Rect(
            200, 200 + i * 60, 200, 50) for i in range(len(self.opciones))]
        self.checklist = [False] * \
            (len(self.opciones) - 1)  # No incluir "Regresar"

        # Posiciones libres para cada checkbox (puedes ajustarlas como quieras)
        self.checkbox_posiciones = [
            (200, 600), (200, 650), (200, 700), (200, 750)]

    def dibujar(self):
        self.pantalla.fill((0, 0, 0))  # Fondo negro

        fuente_ex = pygame.font.Font(None, 36)
        # Lista de textos
        textos = [
            ("Habilitar Items.", (240, 605)),
            ("Habilitar enemigos.", (240, 655)),
            ("Habilitar torres.", (240, 705))
        ]  # posicison del texto

        # Dibujar cada texto en su posición
        for texto, posicion in textos:
            renderizado = fuente_ex.render(texto, True, (255, 255, 255))
            self.pantalla.blit(renderizado, posicion)

        # Dibujar opciones del menú
        for i, opcion in enumerate(self.opciones):
            color = (255, 255, 255) if i == self.opcion_seleccionada else (
                150, 150, 150)
            texto = self.fuente.render(opcion, True, color)
            cuadro = self.cuadro_opciones[i]
            pygame.draw.rect(self.pantalla, color, cuadro, 2)
            self.pantalla.blit(texto, (cuadro.x + 10, cuadro.y + 10))

        # Dibujar los checkboxes en posiciones personalizadas
        for i in range(len(self.checklist)):
            # Usa coordenadas personalizadas
            x, y = self.checkbox_posiciones[i]
            checkbox_rect = pygame.Rect(x, y, 30, 30)
            pygame.draw.rect(self.pantalla, (255, 255, 255), checkbox_rect, 2)

            if self.checklist[i]:
                pygame.draw.line(self.pantalla, (255, 255, 255), (checkbox_rect.x, checkbox_rect.y),
                                 (checkbox_rect.x + 30, checkbox_rect.y + 30), 3)
                pygame.draw.line(self.pantalla, (255, 255, 255), (checkbox_rect.x, checkbox_rect.y + 30),
                                 (checkbox_rect.x + 30, checkbox_rect.y), 3)

    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.mover_seleccion("arriba")
            elif evento.key == pygame.K_DOWN:
                self.mover_seleccion("abajo")
            elif evento.key == pygame.K_RETURN:
                return self.seleccionar_opcion()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(self.checklist)):
                x, y = self.checkbox_posiciones[i]
                checkbox_rect = pygame.Rect(x, y, 30, 30)
                if checkbox_rect.collidepoint(evento.pos):
                    # Alternar selección
                    self.checklist[i] = not self.checklist[i]

    def mover_seleccion(self, direccion):
        if direccion == "arriba":
            self.opcion_seleccionada = (
                self.opcion_seleccionada - 1) % len(self.opciones)
        elif direccion == "abajo":
            self.opcion_seleccionada = (
                self.opcion_seleccionada + 1) % len(self.opciones)

    def seleccionar_opcion(self):
        return self.opciones[self.opcion_seleccionada]


class MenuPausa:
    def __init__(self, ventana):
        self.ventana = ventana
        self.pantalla = ventana  # Asignamos la ventana a self.pantalla
        self.opciones = ["Continuar", "Salir"]
        self.opcion_seleccionada = 0
        self.fuente = pygame.font.Font(None, 50)
        # Calcular la posición centrada del fondo del menú
        ancho_fondo = 500
        alto_fondo = 300
        x_fondo = (constante_1.ANCHO_VENTANA - ancho_fondo) // 2
        y_fondo = (constante_1.ALTO_VENTANA - alto_fondo) // 2
        self.rect_fondo = pygame.Rect(
            x_fondo, y_fondo, ancho_fondo, alto_fondo)

        # Calcular la posición de las opciones dentro del fondo centrado
        self.cuadro_opciones = []
        y_offset_inicial = self.rect_fondo.y + 100  # Ajuste vertical inicial
        for i, opcion in enumerate(self.opciones):
            y_opcion = y_offset_inicial + i * 60
            rect_opcion = pygame.Rect(
                self.rect_fondo.x + 100, y_opcion, 300, 50)  # Ajuste horizontal
            self.cuadro_opciones.append(rect_opcion)

    def dibujar(self):
        pygame.draw.rect(self.pantalla, (50, 50, 50), self.rect_fondo)
        for i, opcion in enumerate(self.opciones):
            color = (255, 255, 255) if i == self.opcion_seleccionada else (
                150, 150, 150)
            texto_renderizado = self.fuente.render(opcion, True, color)
            cuadro = self.cuadro_opciones[i]

            # Calcular la posición centrada del texto
            x_texto = cuadro.x + \
                (cuadro.width - texto_renderizado.get_width()) // 2
            y_texto = cuadro.y + \
                (cuadro.height - texto_renderizado.get_height()) // 2

            pygame.draw.rect(self.pantalla, color, cuadro, 2)
            self.pantalla.blit(texto_renderizado, (x_texto, y_texto))

    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.opcion_seleccionada = (
                    self.opcion_seleccionada - 1) % len(self.opciones)
            elif evento.key == pygame.K_DOWN:
                self.opcion_seleccionada = (
                    self.opcion_seleccionada + 1) % len(self.opciones)
            elif evento.key == pygame.K_RETURN:
                return self.opciones[self.opcion_seleccionada]
        return None
