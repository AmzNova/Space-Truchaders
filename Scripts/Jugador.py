import pygame 
import random
from Naves import armamento, explosion_sprites, explosion_sonido, power_ups, jugador_naves
pygame.mixer.init()

# Jugador ========================================
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, nave):
        super().__init__()
        self._vida_maxima = 800
        self._vida = self._vida_maxima
        self._escudo = 0

        self.x = x
        self.y = y 
        self.ancho = 70
        self.alto = 70
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

        self.hitbox_ancho = 50
        self.hitbox_alto = 50
        self.x_hitbox = self.x + (self.ancho - self.hitbox_ancho) // 2
        self.y_hitbox = self.y + (self.alto - self.hitbox_alto) // 2
        self.hitbox = pygame.Rect(self.x_hitbox, self.y_hitbox, self.hitbox_ancho, self.hitbox_alto)

        self.velocidad = 10
        self.mirar_derecha = False
        self.nave = nave
        self.imagen = self.nave.animacion[0]

        self.tipo_disparo_actual = "comun"
        self.armamento = armamento
        self.disparo_actual = self.armamento[self.tipo_disparo_actual](self.x, self.y)
        self.ultimo_disparo = 0

        self.muriendo = False
        self.explosion_sprites = explosion_sprites
        self.explosion_frame = 0
        self.explosion_cambio = 50
        self.last_explosion_update = pygame.time.get_ticks()
        self.sonido_explosion = explosion_sonido

        self.tiempo_powerup_aplicado = None
        self.duracion_powerup = 0

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        self._vida = max(0, min(valor, self._vida_maxima))

    @property
    def escudo(self):
        return self._escudo

    @escudo.setter
    def escudo(self, valor):
        self._escudo = max(0, min(valor, self._vida_maxima))

    @property
    def vida_maxima(self):
        return self._vida_maxima

    def establecer_nave(self):
        self.imagen = pygame.transform.scale(self.nave.animacion[0], (self.ancho, self.alto))

    def actualizar(self): 
        self.rect.topleft = (self.x, self.y)

        if self.tipo_disparo_actual != "comun" and self.tiempo_powerup_aplicado:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_powerup_aplicado > self.duracion_powerup:
                self.tipo_disparo_actual = "comun"
                self.disparo_actual = self.armamento["comun"](self.x, self.y)
                self.tiempo_powerup_aplicado = None
                self.duracion_powerup = 0

        if self.muriendo:
            if self.explosion_frame < len(self.explosion_sprites):
                self.imagen = self.explosion_sprites[self.explosion_frame]
                self.explosion_frame += 1
            else:
                self.imagen = self.explosion_sprites[-1]
            self.hitbox.topleft = (-100, -100)
        else:
            self.hitbox.topleft = (
                self.x + (self.ancho - self.hitbox_ancho) // 2,
                self.y + (self.alto - self.hitbox_alto) // 2
            )

    def dibujar_jugador(self, ventana): 
        ventana.blit(self.imagen, (self.x, self.y))

    def dibujar_vida(self, ventana):
        ancho_barra = 250
        alto_barra = 25
        x_barra = 20
        y_barra = 720 - alto_barra - 20
        grosor_borde = 2

        pygame.draw.rect(ventana, (255, 225, 225), (x_barra - grosor_borde, y_barra - grosor_borde, ancho_barra + 2 * grosor_borde, alto_barra + 2 * grosor_borde))
        pygame.draw.rect(ventana, (0, 0, 0), (x_barra, y_barra, ancho_barra, alto_barra))

        vida_ratio = self.vida / self.vida_maxima
        pygame.draw.rect(ventana, (0,255,0), (x_barra, y_barra, ancho_barra * vida_ratio, alto_barra))

        if self.escudo > 0:
            escudo_ratio = self.escudo / self.vida_maxima
            pygame.draw.rect(ventana, (0, 200, 255), (x_barra, y_barra, ancho_barra * escudo_ratio, alto_barra))

    def Controles(self, arriba, abajo, izquierda, derecha, disparar):
        return {'arriba' : arriba, 'abajo' : abajo, 'izquierda' : izquierda, 'derecha' : derecha, 'disparar' : disparar}

    def gestionar_teclas(self, teclas, ancho, alto, grupo_disparos):
        movio = False

        if teclas['arriba'] and self.y > 0:
            self.y -= self.velocidad
        if teclas['abajo'] and self.y + self.alto < alto:
            self.y += self.velocidad

        if teclas['izquierda'] and not teclas['derecha'] and self.x > 0:
            self.x -= self.velocidad
            movio = True
            if self.mirar_derecha:
                self.imagen = pygame.transform.flip(self.imagen, True, False)
                self.mirar_derecha = False

        if teclas['derecha'] and not teclas['izquierda'] and self.x + self.ancho < ancho:
            self.x += self.velocidad
            movio = True
            if not self.mirar_derecha:
                self.imagen = pygame.transform.flip(self.imagen, True, False)
                self.mirar_derecha = True

        if movio:
            self.animacion_direccionada(1)
        elif self.nave.frame_actual > 0:
            self.animacion_direccionada(-1)

        if teclas['disparar']:
            self.disparar(grupo_disparos)

        if self.muriendo:
            return 

    def cambiar_disparo(self, nuevo_tipo):
        self.tipo_disparo_actual = nuevo_tipo
        self.disparo_actual = self.armamento[nuevo_tipo](0, 0)

    def disparar(self, grupo_disparos):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo >= self.disparo_actual.tiempo_entre_disparos:
            self.ultimo_disparo = tiempo_actual
            nuevo_disparo = self.armamento[self.tipo_disparo_actual](self.x + self.rect.width // 2, self.y)
            grupo_disparos.add(nuevo_disparo)
            nuevo_disparo.sonido.play()

    def aplicar_powerup(self, powerup):
        if powerup.nombre == "botiquin":
            self.vida += 400
        elif powerup.nombre == "escudo":
            self.escudo += 300
        else:
            self.cambiar_disparo(powerup.nombre)
            self.tiempo_powerup_aplicado = pygame.time.get_ticks()
            self.duracion_powerup = powerup.duracion

    def recibir_dano(self, cantidad):
        if self.escudo > 0:
            if cantidad > self.escudo:
                self.escudo = 0
            else:
                self.escudo -= cantidad
        else:
            self.vida -= cantidad

    def iniciar_explosion(self):
        self.muriendo = True
        self.animacion = self.explosion_sprites
        self.frame_actual = 0
        self.last_update = pygame.time.get_ticks()
        self.tiempo_cambio = 100
        self.sonido_explosion.play()

    def animacion_direccionada(self, direccion):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nave.last_update > self.nave.tiempo_cambio:
            self.nave.last_update = tiempo_actual
            self.nave.frame_actual += direccion

            if self.nave.frame_actual >= len(self.nave.animacion):
                self.nave.frame_actual = len(self.nave.animacion) - 1
            elif self.nave.frame_actual < 0:
                self.nave.frame_actual = 0

            nueva_imagen = self.nave.animacion[self.nave.frame_actual]
            self.imagen = pygame.transform.scale(nueva_imagen, (self.rect.width, self.rect.height))
            if self.mirar_derecha:
                self.imagen = pygame.transform.flip(self.imagen, True, False)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, nombre, imagen, duracion = False):
        super().__init__()
        self.nombre = nombre
        self.image = pygame.transform.scale(imagen, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = 6
        if duracion:
            self.duracion = 10000

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > 720:
            self.kill()

# Diccionario con información de cada tipo de power-up
tipos_powerup = {
    "Disparo" : {
        "minigun" : power_ups["minigun"],
        "plasma canon" : power_ups["plasma canon"]
    },
    "Bufo" : {
        "escudo" : power_ups["escudo"],
        "botiquin" : power_ups["botiquin"]
    }
}

def crear_powerup_aleatorio(x, y):
    categoria = random.choice(list(tipos_powerup.keys()))
    nombre = random.choice(list(tipos_powerup[categoria].keys()))
    imagen = tipos_powerup[categoria][nombre]
    duracion = True if categoria == "Disparo" else False
    return PowerUp(x, y, nombre, imagen, duracion=duracion)
