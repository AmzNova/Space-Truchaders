import pygame
import sys
import os

# Configuración
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (255, 100, 100)
TITLE_COLOR = (255, 0, 0)

#==============================================================================================================================#

class Button:
    def __init__(self, x, y, text, font, action=None, width=250, height=60):
        self._rect = pygame.Rect(x, y, width, height)
        self._font = font
        self._action = action
        self._text = text
        self._update_text_surface()

    def _update_text_surface(self):
        self._text_surf = self._font.render(self._text, True, BLACK)
        self._text_rect = self._text_surf.get_rect(center=self._rect.center)

    @property
    def rect(self):
        return self._rect

    @property
    def action(self):
        return self._action

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, nuevo_texto):
        self._text = nuevo_texto
        self._update_text_surface()

    def draw(self, surface, mouse_pos):
        color = HOVER_COLOR if self._rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(surface, color, self._rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self._rect, 2, border_radius=8)
        surface.blit(self._text_surf, self._text_rect)

#==============================================================================================================================#

def show_game_over_menu(ventana):
    pygame.init()
    pygame.mixer.init()

    ancho = pygame.display.Info().current_w
    alto = pygame.display.Info().current_h
    pygame.display.set_caption("Game Over")
    clock = pygame.time.Clock()

    base_path = os.path.dirname(__file__)

    # Música
    try:
        music_path = os.path.join(base_path, "..", "Sonidos", "GameOverMusic.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error al cargar música de Game Over: {e}")

    # Fondo
    try:
        bg_path = os.path.join(base_path, "..", "Sprints", "Backgrounds", "Fondo_GameOver.jpeg")
        background_img = pygame.image.load(bg_path).convert()
        background_img = pygame.transform.scale(background_img, (ancho, alto))
    except Exception as e:
        print(f"Error al cargar fondo: {e}")
        background_img = None

    # Fuentes
    fonts_path = os.path.abspath(os.path.join(base_path, "..", "Sprints", "Fonts"))
    try:
        font = pygame.font.Font(os.path.join(fonts_path, "MachineStd-Bold.otf"), 26)
        title_font = pygame.font.Font(os.path.join(fonts_path, "ElectronPulseItalic.ttf"), 50)
    except:
        font = pygame.font.SysFont("Arial", 26)
        title_font = pygame.font.SysFont("Arial", 50, bold=True)

    # Botones
    buttons = [
        Button(ancho // 2 - 125, 250, "Reintentar", font, "retry"),
        Button(ancho // 2 - 125, 350, "Menú Principal", font, "main_menu"),
        Button(ancho // 2 - 125, 450, "Salir del Juego", font, "quit")
    ]

    # Bucle principal
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.action == "retry":
                            return "retry"
                        elif button.action == "main_menu":
                            return "main_menu"
                        elif button.action == "quit":
                            pygame.quit()
                            sys.exit()

        # Fondo
        if background_img:
            ventana.blit(background_img, (0, 0))
        else:
            ventana.fill(BLACK)

        # Texto "GAME OVER" 3D simulado
        text = "GAME OVER"
        base_x = ancho // 2
        base_y = 100
        top_color = (255, 255, 0)
        shadow_color = (255, 0, 0)

        for depth in range(6, 0, -1):
            offset_x = depth
            offset_y = depth
            shadow = title_font.render(text, True, shadow_color)
            ventana.blit(shadow, (base_x - shadow.get_width() // 2 + offset_x,
                                  base_y + offset_y))

        title = title_font.render(text, True, top_color)
        ventana.blit(title, (base_x - title.get_width() // 2, base_y))

        # Dibujar botones
        for button in buttons:
            button.draw(ventana, mouse_pos)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
