import constante_1

# class Mundo():
   def __init__(self):
        self.map_tiles = []

    def process_data(self, data, tile_list):
        self.level_length = len(data)
        # print(len(tile_list),"len(tile_list)")
        for y, row in enumerate(data):
            # print(len(row),"len(row)")
            for x, tile in enumerate(row):
                if tile < len(tile_list):
                    image = tile_list[tile]
                    image_rect = image.get_rect()
                    image_x = x * constante_1.TILE_SIZE
                    image_y = y * constante_1.TILE_SIZE
                    image_rect.center = (image_x, image_y)
                    tile_data = [image, image_rect, image_x, image_y]
                    self.map_tiles.append(tile_data)
                else:
                    print(f"Índice fuera de rango: {tile}")
                    # verificamos si tenemos tiles fuera de rango

    def update(self, posicion_pantalla):
        for tile in self.map_tiles:
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
