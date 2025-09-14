import pygame
import cv2
from ui_elements import InputBox, ScrollableMessageBox
from chat_manager import ChatManager

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Pizza Bot")

# Load video
cap = cv2.VideoCapture("background.mp4")
fps = cap.get(cv2.CAP_PROP_FPS) or 30

# UI Elements
message_box = ScrollableMessageBox(50, 100, WIDTH - 100, HEIGHT - 200)
input_box = InputBox(50, HEIGHT - 80, WIDTH - 100, 60)
chat_manager = ChatManager()  # Instantiate class

clock = pygame.time.Clock()
running = True

def draw_video():
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
    screen.blit(surface, (0,0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_box.handle_event(event, chat_manager, message_box)
        message_box.handle_event(event)

    draw_video()
    
    # Title
    font = pygame.font.Font(None, 64)
    title_surface = font.render("AI Pizza Bot", True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(WIDTH//2, 50))
    screen.blit(title_surface, title_rect)

    message_box.draw(screen)
    input_box.draw(screen)

    pygame.display.update()
    clock.tick(fps)

cap.release()
pygame.quit()
