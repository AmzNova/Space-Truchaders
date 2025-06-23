# Naves y Rutas

import pygame
from pathlib import Path
import os
import pygame
pygame.mixer.init()

BASE_DIR = Path(__file__).resolve().parent.parent
# Rutas base
SPRITES_DIR = BASE_DIR / "Sprints"
SONIDOS_DIR = BASE_DIR / "Sonidos"
FUENTE_DIR = SPRITES_DIR / "Fuente"
POWERUPS_DIR = SPRITES_DIR / "PowerUps"

pygame.init()

### CÓDIGO PARA LA DEFINICIÓN DE SPRITES DE ANIMACIONES DE LAS NAVES ###
def CrearSetDeSprites(ruta_nave: str): #Crea un set de sprites para la animación del personaje.
    # Obtener la lista de archivos en la carpeta
    lista_archivos_nave = os.listdir(ruta_nave)
    lista_archivos_nave .sort()
    # Crear la lista de rutas completas
    rutas_archivos_nave = [os.path.join(ruta_nave, archivo) for archivo in lista_archivos_nave ]
    lista_sprites_nave = [] # lista de sprites de la animación del personaje.
    for x in range(0,len(rutas_archivos_nave)):
        lista_sprites_nave.append(pygame.image.load(rutas_archivos_nave[x]))
        
    return lista_sprites_nave
# ============= FUENTE ============ #
ruta_fuente = FUENTE_DIR / "Fuente.ttf"
fuente = pygame.font.Font(str(ruta_fuente), 30)

# ============= SPRITES ============ #
# ---------- Naves para el Jugador ------------ #
jugador_azul_sprites = CrearSetDeSprites(SPRITES_DIR / "Jugador" / "Nave azul")
jugador_rojo_sprites = CrearSetDeSprites(SPRITES_DIR / "Jugador" / "Nave roja")

# ------------- Enemigos Tier 1 --------------- #
enemigo_azul_T1 = CrearSetDeSprites(SPRITES_DIR / "Enemigo" / "Tier I" / "Azul")
enemigo_rojo_T1 = CrearSetDeSprites(SPRITES_DIR / "Enemigo" / "Tier I" / "Rojo")
enemigo_verde_T1 = CrearSetDeSprites(SPRITES_DIR / "Enemigo" / "Tier I" / "Verde")

# ------------- Enemigos Tier 2 --------------- #
enemigo_azul_T2 = CrearSetDeSprites(SPRITES_DIR / "Enemigo" / "Tier II" / "Azul")
enemigo_rojo_T2 = CrearSetDeSprites(SPRITES_DIR / "Enemigo" / "Tier II" / "Rojo")
enemigo_verde_T2 = CrearSetDeSprites(SPRITES_DIR / "Enemigo" / "Tier II" / "Verde")

# ----------------- Disparos ------------------ #
disparo_comun_sprites = CrearSetDeSprites(SPRITES_DIR / "Disparos" / "Comun")
disparo_comun_sonido = pygame.mixer.Sound(str(SONIDOS_DIR / "Disparos" / "Comun.WAV"))
disparo_comun_sonido.set_volume(0.5)

minigun_sprites = CrearSetDeSprites(SPRITES_DIR / "Disparos" / "Minigun")
minigun_sonido = pygame.mixer.Sound(str(SONIDOS_DIR / "Disparos" / "Minigun.WAV"))
minigun_sonido.set_volume(0.5)

plasma_canon_sprites = CrearSetDeSprites(SPRITES_DIR / "Disparos" / "Plasma Canon")
plasma_canon_sonido = pygame.mixer.Sound(str(SONIDOS_DIR / "Disparos" / "Plasma Canon.WAV"))
plasma_canon_sonido.set_volume(0.5)

# ----------------- Explosion ----------------- #
explosion_sprites = CrearSetDeSprites(SPRITES_DIR / "Explosion") 
explosion_sonido = pygame.mixer.Sound(str(SONIDOS_DIR / "Explosion" / "Muerte.WAV"))
explosion_sonido.set_volume(0.5)# ---------------------------------------------

class Disparo(pygame.sprite.Sprite):
    def __init__(self, set_sprites, 
                       daño, 
                       x_nave, 
                       y_nave, 
                       velocidad, 
                       tiempo_entre_disparos, 
                       ancho, 
                       alto, 
                       sonido,
                       es_enemigo=False,
                       ):
        super().__init__()
        self.daño = daño
        self.sonido = sonido
        self.velocidad = velocidad
        self.ancho = ancho
        self.alto = alto        
        self.tiempo_entre_disparos = tiempo_entre_disparos

        # Preprocesar sprites: flip y escalar solo una vez
        self.sprites = []
        for sprite in set_sprites:
            if es_enemigo:
                sprite = pygame.transform.flip(sprite, False, True)
            sprite = pygame.transform.scale(sprite, (self.ancho, self.alto))
            self.sprites.append(sprite)

        # Control de animación
        self.frame_actual = 0
        self.tiempo_cambio = 100  # milisegundos por frame
        self.last_update = pygame.time.get_ticks()

        # Imagen inicial
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x_nave
        self.rect.top = y_nave
        
        # Hitbox 
        self.hitbox_ancho = int(self.ancho * 0.6)  # por ejemplo, 60% del tamaño real
        self.hitbox_alto = int(self.alto * 0.6)
        self.hitbox = pygame.Rect(
        self.rect.x + (self.ancho - self.hitbox_ancho) // 2,
        self.rect.y + (self.alto - self.hitbox_alto) // 2,
        self.hitbox_ancho,
        self.hitbox_alto
                                )
    def get_hitbox(self):
        return self.hitbox
    
    def update(self):
        # Mover el disparo (asegúrate que velocidad ya tenga el signo correcto)
        self.rect.y += self.velocidad

        
        # Actualizar hitbox para que siga al rect
        self.hitbox.x = self.rect.x + (self.ancho - self.hitbox_ancho) // 2
        self.hitbox.y = self.rect.y + (self.alto - self.hitbox_alto) // 2
        
        # Eliminar si sale de pantalla
        if self.rect.bottom < 0 or self.rect.top > 720:
            self.kill()

        # Cambiar fotograma si corresponde
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.last_update > self.tiempo_cambio:
            self.last_update = tiempo_actual
            self.frame_actual = (self.frame_actual + 1) % len(self.sprites)
            imagen = self.sprites[self.frame_actual]
            self.image = pygame.transform.scale(imagen, (self.ancho, self.alto))
            # Asegura que el rect siga a la nueva imagen, manteniendo el centro
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Nave:
    def __init__(self, set_sprites):
        self.animacion = set_sprites
        # Atributos para gestionar la animacion
        self.tiempo_cambio = 100 # Duracion de cada frame en milisegundos
        self.frame_actual = 0  # Se trata una lista de sprites para la animacion y esta variable controla el indice
        self.last_update = pygame.time.get_ticks()  # Establece el tiempo actual

jugador_naves = {
    "azul" : Nave(jugador_azul_sprites),
    "roja" : Nave(jugador_rojo_sprites)
}

enemigos_T1 = {
    "azul" : Nave(enemigo_azul_T1),
    "roja" : Nave(enemigo_rojo_T1),
    "verde" : Nave(enemigo_verde_T1)
}

enemigos_T2 = {
    "azul" : Nave(enemigo_azul_T2),
    "rojo" : Nave(enemigo_rojo_T2),
    "verde" : Nave(enemigo_verde_T2)
}

# Jugador (disparan hacia arriba, por eso velocidad negativa)
armamento = {
    "comun": lambda x, y: Disparo(disparo_comun_sprites, 200, x, y, -10, 300, 50, 70, disparo_comun_sonido),
    "minigun": lambda x, y: Disparo(minigun_sprites, 100, x, y, -20, 100, 10, 30, minigun_sonido),
    "plasma canon": lambda x, y: Disparo(plasma_canon_sprites, 400, x, y, -6, 800, 30, 70, plasma_canon_sonido)
}

# Enemigos (disparan hacia abajo, velocidad positiva)
armamento_enemigo = {
    "comun": lambda x, y: Disparo(disparo_comun_sprites, 200, x, y, 10, 300, 50, 70, disparo_comun_sonido, True),
    "minigun": lambda x, y: Disparo(minigun_sprites, 100, x, y, 20, 100, 10, 30, minigun_sonido, True),
    "plasma canon": lambda x, y: Disparo(plasma_canon_sprites, 400, x, y, 6, 800, 30, 70, plasma_canon_sonido, True)
}

power_ups = {
    "minigun": pygame.image.load(str(POWERUPS_DIR / "Minigun.PNG")),
    "plasma canon": pygame.image.load(str(POWERUPS_DIR / "PLasma canon.PNG")),
    "escudo": pygame.image.load(str(POWERUPS_DIR / "Escudo.PNG")),
    "botiquin": pygame.image.load(str(POWERUPS_DIR / "Botiquin.PNG"))
}


