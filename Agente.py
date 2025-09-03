class Agente(object):
    def __init__(self, x=0, y=0, equipo=1, ID=None):
        self.objId = ID
        self.type = "Unidad jugable"
        self.x = x
        self.y = y
        self.equipo = equipo
        self.salud = int()
        self.salud_max = int()
        self.nivel = int()
        self.nivel_max = int()
        self.bonus_ataque = float()
        self.estado = str()
        self.porta_llave = False
        self.multilabel = True
        self.labels = list()
        self.codificacion = str()
        self.direccion = 0
        self.move = False
        self.fila_cursor = 0
        self.columna_cursor = 0
        self.click = False
        self.click_time = 0
        self.boton1 = False
        self.boton2 = False
        self.boton3 = False
        self.boton4 = False

    def direccionMov(self):
        """Define la direccion en la que se moverá el agente"""
        raise NotImplemented("Tiene que implementar el metodo direccionMov.")

    def mover(self):
        """Activa el movimiento en una dirección selecionada"""
        raise NotImplemented("Tiene que implementar el metodo mover.")

    def mueveCursor(self, mapa):
        """Selecciona un cuadrante del mapa"""
        raise NotImplemented("Tiene que implementar el metodo mueveCursor.")

    def hacerClick(self):
        """Activa una acción en el cuadrante seleccionado"""
        raise NotImplemented("Tiene que implementar el metodo hacerClick.")

    def ataqueBasico(self):
        """"Activa el ataque básico"""
        raise NotImplemented("Tiene que implementar el metodo ataqueBasico.")

    def ataqueEspecial1(self):
        """"Activa el ataque especial 1"""
        raise NotImplemented(
            "Tiene que implementar el metodo ataqueEspecial1.")

    def ataqueEspecial2(self):
        """"Activa el ataque especial 2"""
        raise NotImplemented(
            "Tiene que implementar el metodo ataqueEspecial2.")

    def ataqueEspecialMaximo(self):
        """"Activa el ataque especial maximo"""
        raise NotImplemented(
            "Tiene que implementar el metodo ataqueEspecialMaximo.")

    def recibeGolpe(self, daño, efecto):
        """Daño y/o efecto recibidos"""
        raise NotImplemented("Tiene que implementar el metodo recibeGolpe.")

    def reaparece():
        """Cambia el estado del agente a 'Normal' y volver a posicionarlo en su base"""
        raise NotImplemented("Tiene que implementar el metodo reaparece.")

    def revive(self):
        """Despues de una cantidad de tiempo, activa la funcion reaparece"""
        raise NotImplemented("Tiene que implementar el metodo revive.")

    def draw(self, screen):
        """Dibujando avatar"""
        raise NotImplemented("Tiene que implementar el metodo draw.")
