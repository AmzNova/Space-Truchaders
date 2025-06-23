from pathlib import Path
import pygame
import random 
from Jugador import Jugador
from Enemigo import Enemigo, Marcador
from Naves import fuente, jugador_naves

# Roles del desarrollo juego
roles = ["directores", 
         "programadores", 
         "artistas", 
         "diseñadores", 
         "musica", 
         "sonido", 
         "testers", 
         "agradecimientos"]
# Roles en diferentee idiomas
idiomas = {
        "español": {
            "directores": "Directores",
            "programadores": "Programadores",
            "artistas": "Artistas",
            "diseñadores": "Diseñadores",
            "musica": "Música",
            "sonido": "Efectos de sonido",
            "testers": "Testers",
            "agradecimientos": "Agradecimientos especiales"
        },
        "inglés": {
            "directores": "Directors",
            "programadores": "Programmers",
            "artistas": "Artists",
            "diseñadores": "Designers",
            "musica": "Music",
            "sonido": "Sound Effects",
            "testers": "Testers",
            "agradecimientos": "Special Thanks"
        },
        "portugués": {
            "directores": "Diretores",
            "programadores": "Programadores",
                "artistas": "Artistas",
            "diseñadores": "Designers",
            "musica": "Música",
            "sonido": "Efeitos Sonoros",
            "testers": "Testadores",
            "agradecimientos": "Agradecimentos Especiais"
        },
        "francés": {
            "directores": "Directeurs",
            "programadores": "Programmeurs",
            "artistas": "Artistes",
            "diseñadores": "Concepteurs",
            "musica": "Musique",
            "sonido": "Effets Sonores",
            "testers": "Testeurs",
            "agradecimientos": "Remerciements"
        },
        "italiano": {
            "directores": "Direttori",
            "programadores": "Programmatori",
            "artistas": "Artisti",
            "diseñadores": "Designer",
            "musica": "Musica",
            "sonido": "Effetti Sonori",
            "testers": "Tester",
            "agradecimientos": "Ringraziamenti"
        }
    }
# Nombres random
nombres_divertidos = {
    "directores" : [
        "Gabriel Benítez",
        "Bruno Benítez"
        ] ,
    "programadores" : [
        "Gabriel Benítez",
        "Bruno Benítez"
        ] ,
    "Artistas" : [
        "Armando Esteban Quito",
        "Aquiles Meo de la Torre",
        "Elza Pato"
        ] ,
    "diseñadores" : [
        "Lola Mento",
        "Rosa Melano",
        "Benito Camela"
        ] ,
    "musica" : [
        "Ana Tomía",
        "Elsa Polindo",
        "Paco Merte"
        ] ,
    "sonido" : [
        "Aitor Tilla",
        "Pablo Marmol",
        "Elver Galarga"
        ] ,
    "testers" : [
        "Alan Brito Delgado",
        "Susana Oria",
        "Esteban Dido"        
    ] ,
    "agradecimientos" : [
        "Susana Oria",
        "Aitor Menta",
        "Jorge Nitales",
        "Mario Neta",
        "Elena Nito"
    ] 
}

def generar_creditos(ventana, tiempo_desde_game_over, ancho, alto, roles, nombres_divertidos, idiomas):
    DURACION_TOTAL = 6000  # milisegundos
    TIEMPO = max(tiempo_desde_game_over - 6000, 0)

    # Colores
    COLOR_ROL = (255, 255, 255)      # Blanco
    COLOR_NOMBRE = (255, 255, 255)   # Blanco

    # Fuentes
    fuente_roles = pygame.font.SysFont("Arial", 36, bold=True)
    fuente_nombres = pygame.font.SysFont("Arial", 30)

    # Fondo negro
    ventana.fill((0, 0, 0))

    # Preparar bloques de texto
    lineas = []
    for idioma in idiomas:
        for rol in roles:
            nombre_rol = idiomas[idioma][rol]
            lineas.append((nombre_rol, COLOR_ROL, fuente_roles))  # Rol en blanco negrita
            for nombre in nombres_divertidos.get(rol, []):
                lineas.append((nombre, COLOR_NOMBRE, fuente_nombres))  # Nombre en blanco normal
            lineas.append(("", COLOR_NOMBRE, fuente_nombres))  # Espacio

    # Medir altura total
    altura_linea = fuente_nombres.get_height()
    altura_total_creditos = len(lineas) * altura_linea

    # Calcular desplazamiento: de abajo hacia arriba en 6 segundos
    desplazamiento_total = altura_total_creditos + alto
    velocidad = desplazamiento_total / DURACION_TOTAL  # píxeles por milisegundo

    # Posición Y inicial
    pos_y = alto - (TIEMPO * velocidad)

    for texto, color, fuente in lineas:
        if pos_y + altura_linea > 0 and pos_y < alto:
            superficie_texto = fuente.render(texto, True, color)
            ventana.blit(superficie_texto, (ancho // 2 - superficie_texto.get_width() // 2, int(pos_y)))
        pos_y += altura_linea

# Para usar Rect personalizados()las hitbox
def collide_hitboxes(disparo, enemigo):
    return disparo.get_hitbox().colliderect(enemigo.hitbox)

def bucle_partida( ventana, nave_seleccionada):
    BASE_DIR = Path(__file__).resolve().parent.parent
    SPRITES_DIR = BASE_DIR / "Sprints"
    FONDOS_DIR = SPRITES_DIR / "Fondos"
    PANTALLA_DIR = SPRITES_DIR / "Pantalla"
    SONIDOS_DIR = BASE_DIR / "Sonidos"
    
    pygame.init()
    pygame.mixer.init()
    
    ruta_imagen_fondo = FONDOS_DIR / "PixelBackgroundSeamless.PNG"
    fondo = pygame.image.load(ruta_imagen_fondo)

    ancho = pygame.display.Info().current_w
    alto = pygame.display.Info().current_h

    fondo = pygame.transform.scale(fondo, (ancho, alto))

    # Game Over     ruta_Game_Over = PANTALLA_DIR / "Game-Over.PNG"
    ruta_Game_Over = PANTALLA_DIR / "Game-Over.PNG"
    
    Game_Over_imagen = pygame.transform.scale(pygame.image.load(ruta_Game_Over), (ancho, alto))
    game_Over_sound = pygame.mixer.Sound(SONIDOS_DIR / "Game Over" / "Game-Over.WAV")
    mostrar_primera_imagen = False

    # Sega Man
    ruta_Sega = PANTALLA_DIR / "Sega.PNG"
    Sega_imagen = pygame.transform.scale(pygame.image.load(ruta_Sega).convert_alpha(), (270, 270))
    sonido_segunda_imagen = pygame.mixer.Sound(Path(SONIDOS_DIR / "Game Over" / "Alerta.WAV"))
    sonido_segunda_imagen_rep = False

    # Demanda
    ruta_demanda = PANTALLA_DIR / "Demanda.PNG"
    demanda_imagen = pygame.transform.scale(pygame.image.load(ruta_demanda).convert_alpha(), (270, 270))
    sonido_tercera_imagen = pygame.mixer.Sound(Path(SONIDOS_DIR / "Game Over" / "Demanda.WAV"))
    sonido_tercera_imagen_rep = False

    tiempo_game_over = None

    Ejecutando = True
    Game_Over = False

    grupo_enemigos = pygame.sprite.Group()
    grupo_disparos_enemigos = pygame.sprite.Group()
    tiempo_ultimo_spawn = 0
    intervalo_spawn = 5000
    
    # 3. Crear jugador
    jugador = Jugador(ancho // 2 - 45, alto - 130, jugador_naves[nave_seleccionada])

    grupo_disparos = pygame.sprite.Group()
    # Power ups
    grupo_powerups = pygame.sprite.Group()
    sonido_power_up = pygame.mixer.Sound(Path(SONIDOS_DIR / "PowerUp" / "PowerUp.WAV"))

    marcador = Marcador(fuente)
    # Sonido de creditos
    sonido_creditos = pygame.mixer.Sound(Path(SONIDOS_DIR / "creditos finales" / "creditos-finales.WAV"))
    sonido_creditos_rep = False

    # Bucle principal
    while Ejecutando:
        eventos = pygame.event.get()
        teclas = pygame.key.get_pressed()

        for evento in eventos:
            if evento.type == pygame.QUIT or teclas[pygame.K_ESCAPE]:
                Ejecutando = False

        if not Game_Over:
            if not jugador.muriendo:
                controles = jugador.Controles(teclas[pygame.K_w],
                                              teclas[pygame.K_s],
                                              teclas[pygame.K_a],
                                              teclas[pygame.K_d],
                                              teclas[pygame.K_SPACE])
                jugador.gestionar_teclas(controles, ancho, alto, grupo_disparos)

                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - tiempo_ultimo_spawn > intervalo_spawn:
                    tiempo_ultimo_spawn = tiempo_actual
                    cantidad_enemigos = random.randint(1, 3)
                    for _ in range(cantidad_enemigos):
                        x = random.randint(0, 800 - 70)
                        y = -70
                        enemigo = Enemigo(x, y)
                        grupo_enemigos.add(enemigo)

                grupo_disparos.update()
                grupo_disparos_enemigos.update()
                grupo_enemigos.update(grupo_powerups)
                grupo_powerups.update()

                for enemigo in grupo_enemigos:
                    if not enemigo.muriendo:
                        enemigo.disparar(grupo_disparos_enemigos)

                for disparo in grupo_disparos:
                    enemigos_impactados = pygame.sprite.spritecollide(disparo, grupo_enemigos, False, collided=collide_hitboxes)
                    for enemigo in enemigos_impactados:
                        if enemigo.muriendo:
                            continue
                        enemigo.vida -= disparo.daño
                        disparo.kill()
                        if enemigo.vida <= 0:
                            marcador.sumar_puntos(enemigo.puntos)
                            enemigo.iniciar_explosion()
                
                for powr_up in grupo_powerups:
                    if powr_up.rect.colliderect(jugador.hitbox):
                        sonido_power_up.play()
                        jugador.aplicar_powerup(powr_up)
                        powr_up.kill()

                for disparo in grupo_disparos_enemigos:
                    if disparo.hitbox.colliderect(jugador.hitbox):
                        jugador.recibir_dano(disparo.daño)
                        disparo.kill()


        if jugador.vida <= 0 and not jugador.muriendo:
            jugador.iniciar_explosion()

        if jugador.muriendo and jugador.explosion_frame >= len(jugador.explosion_sprites):
            Game_Over = True
            if tiempo_game_over is None:
                tiempo_game_over = pygame.time.get_ticks()
                game_Over_sound.play()
                mostrar_primera_imagen = True

        jugador.actualizar()

        ventana.blit(fondo, (0, 0))
        grupo_disparos.draw(ventana)
        grupo_disparos_enemigos.draw(ventana)
        grupo_enemigos.draw(ventana)
        grupo_powerups.draw(ventana)
        jugador.dibujar_jugador(ventana)
        jugador.dibujar_vida(ventana)
        marcador.imprimir(ventana)

        # =============================== GAME OVER ===================================
        if Game_Over and tiempo_game_over:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_desde_game_over = tiempo_actual - tiempo_game_over

            if mostrar_primera_imagen:
                ventana.blit(Game_Over_imagen, (0, 0))

            if tiempo_desde_game_over > 2000:
                ventana.blit(Sega_imagen, (10, alto - 270))
                if not sonido_segunda_imagen_rep:
                    sonido_segunda_imagen.play()
                    sonido_segunda_imagen_rep = True

            if tiempo_desde_game_over > 3000:
                ventana.blit(demanda_imagen, (ancho - 270 - 10, alto - 270))
                if not sonido_tercera_imagen_rep:
                    sonido_tercera_imagen.play()
                    sonido_tercera_imagen_rep = True

            if tiempo_desde_game_over > 6000:
                # Reproducir sonido una sola vez
                if not sonido_creditos_rep:
                    sonido_creditos.play()
                    sonido_creditos_rep = True
                generar_creditos(ventana, tiempo_desde_game_over, ancho, alto, roles, nombres_divertidos, idiomas)

                if tiempo_desde_game_over > 12000:
                    Ejecutando = False

        pygame.display.update()

    return  # vuelve al menú
