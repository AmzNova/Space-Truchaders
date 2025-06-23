import pygame # Para interfacces de videojuegos
import sys # Para controlar la salida y argumentos
import os  # Para manejar rutas de archivos
import random # Para generar numero aleatorios
import math # Para operaciones matematicas
import GameOver # Modulo de Pantalla Game Over
import Pantalla # Modulo del Gameplay
import traceback # Para manejo de exepciones
# Configuración
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (255, 100, 100)
TITLE_COLOR = (255, 200, 0)

# Estados del menú
MENU_MAIN = 0
MENU_OPTIONS = 1
MENU_SHIP = 2
SHIP_SELECTION = "azul" 

#==============================================================================================================================#
##CLase para los botones

class Button:
    def __init__(self, x, y, text, font, action=None, width=250, height=60):
        self._rect = pygame.Rect(x, y, width, height)
        self._text = text
        self._font = font
        self._action = action

    @property
    def rect(self):
        return self._rect

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, nuevo_texto):
        self._text = nuevo_texto

    @property
    def action(self):
        return self._action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = HOVER_COLOR if self._rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(surface, color, self._rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self._rect, 2, border_radius=8)
        text_render = self._font.render(self._text, True, BLACK)
        surface.blit(text_render, (self._rect.centerx - text_render.get_width() // 2,
                                   self._rect.centery - text_render.get_height() // 2))

#==============================================================================================================================#
# Configuracion de gameplay
def load_and_run_game(ventana):
    global SHIP_SELECTION
    try:
        pygame.mixer.music.stop()
        print(f"DEBUG - Nave seleccionada al iniciar juego: {SHIP_SELECTION}")
        Pantalla.bucle_partida(ventana, SHIP_SELECTION)
        
        pygame.init()
        pygame.mixer.init()

        Ruta = os.path.dirname(__file__)
        music_path = os.path.join(Ruta, "..", "Sonidos", "MenuMusic.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
        else:
            print(f"Archivo de música no encontrado: {music_path}")
    except Exception as e:
        print("Error al ejecutar el juego:")
        traceback.print_exc()   # Esto muestra la traza del error en consola
        # Intentar reiniciar pygame y la música, si falla avisar
        try:
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.play(-1)
        except Exception as inner_e:
            print("Error al intentar reiniciar pygame y reproducir música:")
            traceback.print_exc()

#==============================================================================================================================#
# Fondo animado de estrellas
class Star:
    def __init__(self):
        self._angle_rad = math.radians(45)
        self._color = WHITE
        self.reset()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, nuevo_color):
        self._color = nuevo_color

    def reset(self):
        self._x = random.uniform(0, SCREEN_WIDTH)
        self._y = random.uniform(0, SCREEN_HEIGHT)
        speed = random.uniform(3, 6)
        self._speed_x = speed * math.cos(self._angle_rad)
        self._speed_y = speed * math.sin(self._angle_rad)
        self._length = random.randint(5, 15)

    def move(self):
        self._x += self._speed_x
        self._y += self._speed_y

        if self._x > SCREEN_WIDTH or self._y > SCREEN_HEIGHT:
            if random.getrandbits(1):
                self._x = random.uniform(-50, 0)
                self._y = random.uniform(0, SCREEN_HEIGHT)
            else:
                self._x = random.uniform(0, SCREEN_WIDTH)
                self._y = random.uniform(-50, 0)

    def draw(self, surface):
        x1, y1 = int(self._x), int(self._y)
        x2 = int(self._x - self._speed_x * self._length / 3)
        y2 = int(self._y - self._speed_y * self._length / 3)
        pygame.draw.line(surface, self._color, (x1, y1), (x2, y2), 2)

#==============================================================================================================================#
#Funciones del menu( Vista, Bucle running, sub-menus)

def show_menu(ventana):
    global SHIP_SELECTION
    pygame.init()
    pygame.mixer.init()

    sound_enabled = True
    Ruta = os.path.dirname(__file__)  # Obtener ruta base fuera del try
    music_path = os.path.join(Ruta, "..", "Sonidos", "MenuMusic.mp3")
    volume = 1.0 if sound_enabled else 0.0

    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
        print(f"Sonido {'activado' if sound_enabled else 'desactivado'}")
    except Exception as e:
        print(f"Error al cargar música: {e}")

    pygame.display.set_caption("Space Truchaders")
    clock = pygame.time.Clock()
    
    # Estado inicial
    current_menu = MENU_MAIN
    

    # Cargamos fuentes personalizadas
    try:
        fonts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Sprints", "Fonts"))
        bold_path = os.path.join(fonts_path, "MachineStd-Bold.otf")
        medium_path = os.path.join(fonts_path, "MachineStd-Medium.otf")
        title_path = os.path.join(fonts_path, "ElectronPulseItalic.ttf")

        font_general = pygame.font.Font(bold_path, 26)
        font_general2 = pygame.font.Font(medium_path, 26)
        title_font = pygame.font.Font(title_path, 50)
    except Exception:
        font_general = pygame.font.SysFont("Arial", 26, bold=True)
        font_general2 = pygame.font.SysFont("Arial", 26)
        title_font = pygame.font.SysFont("Arial", 50, bold=True)

    
    # Botones del menú principal
    main_buttons = [
        Button(SCREEN_WIDTH//2 - 150, 200, "Comenzar Juego", font_general, "play", width=300),
        Button(SCREEN_WIDTH//2 - 125, 280, "Opciones", font_general2, "options"),
        Button(SCREEN_WIDTH//2 - 125, 360, "Nave", font_general2, "ship"),
        Button(SCREEN_WIDTH//2 - 125, 440, "Cerrar Juego", font_general, "quit")
    ]
    
    # Botones para menu nave
    ship_buttons = [
        Button(SCREEN_WIDTH//2 - 125, 250, "Nave Roja", font_general, "red_ship"),
        Button(SCREEN_WIDTH//2 - 125, 350, "Nave Azul", font_general, "blue_ship"),
        Button(SCREEN_WIDTH//2 - 125, 450, "Atrás", font_general, "back")
]
    
    # Botones del menú de opciones
    options_buttons = [
        Button(SCREEN_WIDTH//2 - 125, 250, f"Sonido: {'ON' if sound_enabled else 'OFF'}", font_general2, "toggle_sound"),
        Button(SCREEN_WIDTH//2 - 125, 350, "Atrás", font_general2, "back")
    ]
    # Titulo del menu
    text = "SPACE TRUCHADERS"
    top_color = (255, 255, 0)
    shadow_color = (255, 0, 0)

    # Renderizado del titulo
    title_surface = title_font.render(text, True, top_color)
    shadow_surface = title_font.render(text, True, shadow_color)

    # Posición base
    base_x = SCREEN_WIDTH // 2
    base_y = 80
    stars = [Star() for _ in range(300)]
    running = True

    #Bucle(Corriendo menu)
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Menú principal
                if current_menu == MENU_MAIN:
                    for button in main_buttons:
                        if button.rect.collidepoint(mouse_pos):
                            if button.action == "play": # Comenzar juego
                                running = False  # Detener el bucle del menú
                                pygame.mixer.music.stop()
                                return  # Salir de show_menu y continuar en Pantalla
                            elif button.action == "options":
                                current_menu = MENU_OPTIONS # Acedder a la opciones
                            elif button.action == "ship":
                                current_menu = MENU_SHIP #Acceder a las naves
                            elif button.action == "quit":
                                running = False
                
                # Menú de opciones
                elif current_menu == MENU_OPTIONS:
                    for button in options_buttons:
                        if button.rect.collidepoint(mouse_pos):
                            if button.action == "toggle_sound":
                                sound_enabled = not sound_enabled #Mutear juego
                                button.text = f"Sonido: {'ON' if sound_enabled else 'OFF'}"
                                print(f"Sonido {'activado' if sound_enabled else 'desactivado'}")

                                # Ajustamos volumen global de música
                                pygame.mixer.music.set_volume(1.0 if sound_enabled else 0.0)
                            elif button.action == "back": # Volver al menú principal
                                current_menu = MENU_MAIN 

                # Menú de selección de nave
                elif current_menu == MENU_SHIP:
                    for button in ship_buttons:
                        if button.rect.collidepoint(mouse_pos):
                            if button.action == "red_ship":
                                SHIP_SELECTION = "roja" 
                                print("Seleccionada nave roja")
                                current_menu = MENU_MAIN  
                            elif button.action == "blue_ship":
                                SHIP_SELECTION = "azul"
                                print("Seleccionada nave azul")
                                current_menu = MENU_MAIN
                            elif button.action == "back": # Volver al menú principal
                                current_menu = MENU_MAIN
        
        # Dibujado de estrellas( Fondo animado )
        ventana.fill(BLACK)
        for star in stars:
            star.move()
            star.draw(ventana)

        # Dibujar profundidad del titulo (ya renderizada)
        for depth in range(6, 0, -1):
            offset_x = depth
            offset_y = depth
            ventana.blit(
                shadow_surface,
                (base_x - shadow_surface.get_width() // 2 + offset_x, base_y + offset_y)
            )

        # Dibujar texto principal
        ventana.blit(title_surface, (base_x - title_surface.get_width() // 2, base_y))

        
        # Dibujar título secundario según el menú actual( Opciones, Naves)
        if current_menu == MENU_MAIN:
            buttons_to_draw = main_buttons
        elif current_menu == MENU_OPTIONS:
            options_title = title_font.render("OPCIONES", True, TITLE_COLOR)
            ventana.blit(options_title, (SCREEN_WIDTH//2 - options_title.get_width()//2, 150))
            buttons_to_draw = options_buttons
        elif current_menu == MENU_SHIP:
            ship_title = title_font.render("SELECCIONAR NAVE", True, TITLE_COLOR)
            ventana.blit(ship_title, (SCREEN_WIDTH//2 - ship_title.get_width()//2, 150))
            buttons_to_draw = ship_buttons

        # Dibuja los botones del menú actual
        for button in buttons_to_draw:
            button.draw(ventana)

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()
#Flujo del juegos ( Invocaciones de Vista, runing, etc )
if __name__ == "__main__":
    pygame.init()
    ventana = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.FULLSCREEN | pygame.SCALED,
        vsync=True
    )

    try:
        while True:
            # Mostrar menú principal (hasta que se inicie o salga)
            show_menu(ventana)

            while True:
                # Correr la partida
                load_and_run_game(ventana)

                # Mostrar menú de Game Over y decidir siguiente acción
                accion = GameOver.show_game_over_menu(ventana)

                if accion == "retry":
                    continue  # Volver a jugar( Correr partida )
                elif accion == "main_menu":
                    break  # Volver al menú principal
                elif accion == "quit": # Cerrar juego
                    pygame.quit()
                    sys.exit()

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        # Asegura que pygame se cierre bien
        pygame.quit()
