import pygame
import cv2
from ui_elements import InputBox, ScrollableMessageBox
from chat_manager import ChatManager


class PizzaBotUI:
    def __init__(self, width=800, height=600, video_path="background.mp4"):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("AI Pizza Bot")

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)

        # UI components
        self.input_box = InputBox(50, self.HEIGHT - 60, 700, 40)
        self.message_box = ScrollableMessageBox(50, 100, 700, 400)
        self.chat_manager = ChatManager()

        # Video background
        self.video = cv2.VideoCapture(video_path)

        # Clock
        self.clock = pygame.time.Clock()

    def get_background_frame(self):
        """Fetch a frame from the video and convert to Pygame surface."""
        ret, frame = self.video.read()
        if not ret:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video.read()

        frame = cv2.resize(frame, (self.WIDTH, self.HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    def draw(self):
        # Draw video background
        bg_surface = self.get_background_frame()
        self.screen.blit(bg_surface, (0, 0))

        # Title
        title_surface = self.title_font.render("🍕 AI Pizza Bot 🍕", True, (255, 255, 0))
        title_rect = title_surface.get_rect(center=(self.WIDTH // 2, 40))
        self.screen.blit(title_surface, title_rect)

        # Chat + Input
        self.message_box.draw(self.screen)
        self.input_box.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            self.input_box.handle_event(event, self.chat_manager, self.message_box)
            self.message_box.handle_event(event)
        return True

    def cleanup(self):
        self.video.release()
        pygame.quit()
