import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

pygame.init()

WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Optimization Methods Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (240, 240, 240)

def f(x):
    return x**2 - 4*x + 4

def df(x):
    return 2*x - 4

def newton_step(x):
    derivative = df(x)
    if abs(derivative) < 1e-10:  
        return x
    return x - f(x)/derivative

def gradient_step(x, learning_rate):
    return x - learning_rate * df(x)

def draw_help_section(screen):
    # Draw help section background
    help_rect = pygame.Rect(900, 0, 300, HEIGHT)
    pygame.draw.rect(screen, GRAY, help_rect)
    pygame.draw.line(screen, BLACK, (900, 0), (900, HEIGHT), 2)
    
    help_font = pygame.font.Font(None, 24)
    help_text = [
        "Help Guide",
        "",
        "Optimization Methods:",
        "1. Newton's Method",
        "2. Gradient Descent",
        "",
        "Controls:",
        "- X+/X-: Change starting point",
        "- Iter+/Iter-: Change iterations",
        "- Toggle Method: Switch method",
        "- Restart: Reset animation",
        "- Next Step: Step through",
        "",
        "Graph Elements:",
        "- Blue: f(x) = x² - 4x + 4",
        "- Red: Optimization steps",
        "- Green: Current position",
        "",
        "Tips:",
        "- Try different start points",
        "- Compare methods' speeds",
        "- Watch learning rate effect"
    ]
    
    y_offset = 20
    for line in help_text:
        text_surface = help_font.render(line, True, BLACK)
        screen.blit(text_surface, (920, y_offset))
        y_offset += 30

def create_plot(x_start, max_iter, method='newton', animation_step=None):
    fig, ax = plt.subplots(figsize=(7, 6))  
    
    x = np.linspace(-2, 6, 1000)
    y = f(x)
    ax.plot(x, y, 'b-', label='f(x)')
    
    iterations = []
    x_current = x_start
    learning_rate = 0.1
    
    if method == 'newton':
        for i in range(max_iter):
            iterations.append(x_current)
            if abs(df(x_current)) < 1e-10:
                break
            x_current = newton_step(x_current)
            if abs(f(x_current)) < 1e-10:
                break
    else:
        for i in range(max_iter):
            iterations.append(x_current)
            x_current = gradient_step(x_current, learning_rate)
            if abs(f(x_current)) < 1e-10:
                break
    
    if animation_step is not None:
        iterations = iterations[:animation_step+1]
    
    for i in range(len(iterations)-1):
        x_curr = iterations[i]
        x_next = iterations[i+1]
        ax.plot([x_curr, x_curr], [0, f(x_curr)], 'r--')
        ax.plot([x_curr, x_next], [f(x_curr), 0], 'r--')
    
    if iterations:
        current_x = iterations[-1]
        ax.plot(current_x, f(current_x), 'go', markersize=15)
        
    ax.grid(True)
    ax.set_title(f"{'Newton' if method == 'newton' else 'Gradient Descent'} Method Visualization")
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    
    return fig, iterations[-1] if iterations else x_start, len(iterations)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        
    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

running = True
x_start = 0
max_iterations = 10
current_method = 'newton'
animation_frame = 0
animation_speed = 5
frame_counter = 0
current_x = x_start
iteration_count = 0

increase_x = Button(50, 650, 100, 40, "X +")
decrease_x = Button(160, 650, 100, 40, "X -")
increase_iter = Button(50, 700, 100, 40, "Iter +")
decrease_iter = Button(160, 700, 100, 40, "Iter -")
toggle_method = Button(50, 600, 210, 40, "Toggle Method")
restart_animation = Button(50, 550, 210, 40, "Restart Animation")
next_step = Button(50, 500, 210, 40, "Next Step")

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if increase_x.rect.collidepoint(mouse_pos):
                x_start += 0.5
                animation_frame = 0
                current_x = x_start
            elif decrease_x.rect.collidepoint(mouse_pos):
                x_start -= 0.5
                animation_frame = 0
                current_x = x_start
            elif increase_iter.rect.collidepoint(mouse_pos):
                max_iterations += 1
                animation_frame = 0
            elif decrease_iter.rect.collidepoint(mouse_pos):
                max_iterations = max(1, max_iterations - 1)
                animation_frame = 0
            elif toggle_method.rect.collidepoint(mouse_pos):
                current_method = 'newton' if current_method == 'gradient' else 'gradient'
                animation_frame = 0
                current_x = x_start
            elif restart_animation.rect.collidepoint(mouse_pos):
                animation_frame = 0
                current_x = x_start
            elif next_step.rect.collidepoint(mouse_pos):
                if current_method == 'newton':
                    current_x = newton_step(current_x)
                else:
                    current_x = gradient_step(current_x, 0.1)
                animation_frame = max_iterations
    
    frame_counter += 1
    if frame_counter >= animation_speed:
        frame_counter = 0
        animation_frame = min(animation_frame + 1, max_iterations)
    
    fig, current_x, iteration_count = create_plot(x_start, max_iterations, current_method, animation_frame)
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    plt.close(fig)
    
    plot_surface = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(plot_surface, (300, 50))
    
    increase_x.draw(screen)
    decrease_x.draw(screen)
    increase_iter.draw(screen)
    decrease_iter.draw(screen)
    toggle_method.draw(screen)
    restart_animation.draw(screen)
    next_step.draw(screen)
    
    font = pygame.font.Font(None, 36)
    x_text = font.render(f"Starting x: {x_start:.2f}", True, BLACK)
    current_x_text = font.render(f"Current x: {current_x:.4f}", True, BLACK)
    current_fx_text = font.render(f"f(x): {f(current_x):.4f}", True, BLACK)
    iter_text = font.render(f"Max iterations: {max_iterations}", True, BLACK)
    method_text = font.render(f"Method: {current_method.title()}", True, BLACK)
    iter_count_text = font.render(f"Iterations taken: {iteration_count}", True, BLACK)
    
    screen.blit(x_text, (50, 450))
    screen.blit(current_x_text, (50, 400))
    screen.blit(current_fx_text, (50, 300))
    screen.blit(iter_text, (50, 350))
    screen.blit(method_text, (50, 250))
    screen.blit(iter_count_text, (50, 200))
    
    if current_method == 'newton':
        next_x = newton_step(current_x)
        formula = font.render(f"Next x = {current_x:.4f} - {f(current_x):.4f}/{df(current_x):.4f}", True, BLACK)
    else:
        next_x = gradient_step(current_x, 0.1)
        formula = font.render(f"Next x = {current_x:.4f} - 0.1 * {df(current_x):.4f}", True, BLACK)
    screen.blit(formula, (50, 750))
    
    # Draw help section
    draw_help_section(screen)
    
    pygame.display.flip()

pygame.quit()
