import pygame
import random
from Naves import enemigos_T1, enemigos_T2, armamento_enemigo, explosion_sprites, explosion_sonido
from Jugador import crear_powerup_aleatorio
pygame.mixer.init()
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.ancho = 70
        self.alto = 70
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

        # Hitbox 
        self.hitbox_ancho = int(self.ancho * 0.6)  # por ejemplo, 60% del tamaño real
        self.hitbox_alto = int(self.alto * 0.6)
        self.hitbox = pygame.Rect(
        self.rect.x + (self.ancho - self.hitbox_ancho) // 2,
        self.rect.y + (self.alto - self.hitbox_alto) // 2,
        self.hitbox_ancho,
        self.hitbox_alto
                                )
        # === NAVE ALEATORIA desde los diccionarios ===
        diccionario_elegido = random.choice([enemigos_T1, enemigos_T2])
        color_nave, nave_obj = random.choice(list(diccionario_elegido.items()))
        self.nave = nave_obj
        self.animacion = self.nave.animacion  # Usamos los sprites de la nave

        # Asignar vida según el Tier de Nave
        if diccionario_elegido == enemigos_T1:
            self.vida = 400  # vida base para T1
            self.prob_drop_pu = 0.30
            self.puntos = 100
        else:
            self.vida = 600  # vida base para T2 (el doble, por ejemplo)
            self.prob_drop_pu = 0.50
            self.puntos = 200
        # Animación
        self.frame_actual = 0
        self.tiempo_cambio = 100
        self.last_update = pygame.time.get_ticks()
        self.imagen = pygame.transform.scale(self.animacion[0], (self.ancho, self.alto))
        self.image = self.imagen

        # Movimiento
        self.vel_y = 2
        self.vel_x = random.choice([-2, -1, 1, 2])
        self.direccion_anim = 1 if self.vel_x >= 0 else -1
        self.mirar_derecha = self.vel_x >= 0

        # Disparo
        self.armamento = armamento_enemigo
        self.tipo_disparo_actual = random.choice(list(self.armamento.keys()))
        self.disparo_actual = self.armamento[self.tipo_disparo_actual](self.x, self.y)
        self.ultimo_disparo = 0
        
        # Control de ráfagas de disparo
        self.en_ráfaga = True
        self.disparos_en_ráfaga = random.randint(1, 5)
        self.tiempo_espera_entre_rafagas = random.randint(1000, 4000) # entre 1 y 4 segundos
        self.tiempo_inicio_descanso = 0
        # Muerte
        self.muriendo = False # Booleano para simular ele stado de muerte
        self.explosion_sprites = explosion_sprites
        self.explosion_frame = 0 # Indice de frames para la explosion
        self.explosion_cambio = 50  # Tiempo entre frames en ms
        self.last_explosion_update = pygame.time.get_ticks()
        self.sonido_explosion = explosion_sonido

    def update(self, grupo_powerups):
        if self.muriendo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.last_explosion_update >= self.explosion_cambio:
                self.last_explosion_update = tiempo_actual
                if self.explosion_frame < len(self.explosion_sprites):
                    self.image = pygame.transform.scale(self.explosion_sprites[self.explosion_frame], (self.ancho, self.alto))
                    self.explosion_frame += 1
                else:
                    if random.random() < self.prob_drop_pu:
                        nuevo_pu = crear_powerup_aleatorio(self.rect.centerx - 25, self.rect.centery - 15)
                        grupo_powerups.add(nuevo_pu)
                    self.kill()  # Termina la animación y elimina el sprite
            return  # No hacer nada más si está muriendo

        # Movimiento normal
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        self.hitbox.x = self.rect.x + (self.ancho - self.hitbox_ancho) // 2
        self.hitbox.y = self.rect.y + (self.alto - self.hitbox_alto) // 2

        if self.rect.left <= 0 or self.rect.right >= 800:
            self.vel_x *= -1
            self.direccion_anim *= -1
            self.mirar_derecha = self.vel_x >= 0
        if self.rect.top > 720:
            self.kill()

        self.animacion_direccionada(self.direccion_anim)

    def disparar(self, grupo_disparos):
        # No dispara hasta que esté completamente dentro de la pantalla
        if self.rect.top < 0 or self.muriendo:
            return

        tiempo_actual = pygame.time.get_ticks()

        if self.en_ráfaga:
            if tiempo_actual - self.ultimo_disparo >= self.disparo_actual.tiempo_entre_disparos:
                self.ultimo_disparo = tiempo_actual
                nuevo_disparo = self.armamento[self.tipo_disparo_actual](self.rect.centerx, self.rect.bottom)
                grupo_disparos.add(nuevo_disparo)
                nuevo_disparo.sonido.play()
                self.disparos_en_ráfaga -= 1

                if self.disparos_en_ráfaga <= 0:
                    self.en_ráfaga = False
                    self.tiempo_inicio_descanso = tiempo_actual
        else:
            if tiempo_actual - self.tiempo_inicio_descanso >= self.tiempo_espera_entre_rafagas:
                self.en_ráfaga = True
                self.disparos_en_ráfaga = random.randint(1, 5)
                self.tiempo_espera_entre_rafagas = random.randint(1000, 4000)
    
    def recibir_dano(self, cantidad):
        if self.muriendo:
            return
        self.vida -= cantidad
        if self.vida <= 0:
            self.iniciar_explosion()

    def iniciar_explosion(self):
        self.muriendo = True
        self.explosion_frame = 0
        self.last_explosion_update = pygame.time.get_ticks()
        self.sonido_explosion.play()
        
        

    def animacion_direccionada(self, direccion):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.last_update > self.tiempo_cambio:
            self.last_update = tiempo_actual
            self.frame_actual += direccion

            if self.frame_actual >= len(self.animacion):
                self.frame_actual = len(self.animacion) - 1
            elif self.frame_actual < 0:
                self.frame_actual = 0

            nueva_imagen = self.animacion[self.frame_actual]
            imagen = pygame.transform.scale(nueva_imagen, (self.ancho, self.alto))
            if self.mirar_derecha:
                imagen = pygame.transform.flip(imagen, True, False)
            self.image = imagen  # ¡ACTUALIZA self.image correctamente!

class Marcador:
    def __init__(self, fuente):
        self.puntaje = 0
        self.fuente = fuente
        self.color = (255, 255, 255)  # blanco
        self.actualizar_texto()

    def actualizar_texto(self):
        self.formato = self.fuente.render(f"Puntaje: {self.puntaje}", True, self.color)

    def sumar_puntos(self, cantidad):
        self.puntaje += cantidad
        self.actualizar_texto()

    def imprimir(self, ventana):
        ventana.blit(self.formato, (10, 10))  # posición en la esquina superior derecha
         