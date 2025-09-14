import pygame
import threading
import time

# -----------------------------
# Scrollable message box
# -----------------------------
class ScrollableMessageBox:
    def __init__(self, x, y, w, h, max_messages=100):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.Font(None, 28)
        self.messages = []
        self.scroll_offset = 0
        self.max_messages = max_messages
        self.line_spacing = 5

    def add_message(self, message, color=(255,255,255)):
        if len(self.messages) >= self.max_messages:
            self.messages.pop(0)
        self.messages.append((message, color))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # scroll up
                self.scroll_offset = min(self.scroll_offset + 20, 0)
            elif event.button == 5:  # scroll down
                total_height = self.get_total_height()
                max_offset = min(0, self.rect.height - total_height)
                self.scroll_offset = max(self.scroll_offset - 20, max_offset)

    def wrap_text(self, text: str):
        words = text.split(' ')
        lines, current_line = [], ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] <= self.rect.width - 10:  # padding
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines


    def get_total_height(self):
        total = 0
        for msg, sender in self.messages:  # unpack here
            total += len(self.wrap_text(msg)) * (self.font.get_height() + self.line_spacing)
        return total

    def draw(self, screen):
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        screen.blit(s, (self.rect.x, self.rect.y))

        y = self.rect.y + self.scroll_offset
        for msg, color in self.messages:
            lines = self.wrap_text(msg)
            for line in lines:
                txt_surface = self.font.render(line, True, color)
                screen.blit(txt_surface, (self.rect.x + 5, y))
                y += self.font.get_height() + self.line_spacing

# -----------------------------
# Input box
# -----------------------------
class InputBox:
    def __init__(self, x, y, w, h, max_lines=5):
        self.bottom = y + h
        self.rect = pygame.Rect(x, y, w, h)
        self.color_active = (255, 255, 255)
        self.color_inactive = (200, 200, 200)
        self.color = self.color_inactive
        self.text_lines = [""]
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.padding = 10
        self.max_lines = max_lines
        self.line_spacing = 5

    def handle_event(self, event, chat_manager, message_box):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM if self.active else pygame.SYSTEM_CURSOR_ARROW)

        if event.type == pygame.KEYDOWN and self.active:
            current_line = self.text_lines[-1]
            if event.key == pygame.K_RETURN:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if len(self.text_lines) < self.max_lines:
                        self.text_lines.append("")
                else:
                    self.send_message(chat_manager, message_box)
            elif event.key == pygame.K_BACKSPACE:
                if current_line:
                    self.text_lines[-1] = current_line[:-1]
                elif len(self.text_lines) > 1:
                    self.text_lines.pop()
            else:
                self.text_lines[-1] += event.unicode

    def send_message(self, chat_manager, message_box):
        full_text = "\n".join(self.text_lines).strip()
        if not full_text:
            return
    # Add user message in light blue
        message_box.add_message(f"You: {full_text}", color=(173,216,230))
        threading.Thread(target=self.get_ai_response, args=(chat_manager, message_box, full_text), daemon=True).start()
        self.text_lines = [""]

    def get_ai_response(self, chat_manager, message_box, question):
        """
        Stream AI response letter by letter
        """
        full_response = ""
        # Add empty AI message first
        message_box.add_message("", color=(144,238,144))  # light green
        ai_index = len(message_box.messages) - 1

        for token in chat_manager.get_ai_response(question):
            full_response += token
            # Update last message in messages list
            message_box.messages[ai_index] = (full_response, (144,238,144))
            time.sleep(0.01)  # adjust speed here for streaming effect

    def draw(self, screen):
        height = (self.font.get_height() + self.line_spacing) * len(self.text_lines) + 2 * self.padding
        self.rect.height = height
        self.rect.top = self.bottom - self.rect.height

        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill((50, 50, 50, 180))
        screen.blit(s, (self.rect.x, self.rect.y))

        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=10)

        y_offset = self.rect.y + self.padding
        for line in self.text_lines:
            txt_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(txt_surface, (self.rect.x + self.padding, y_offset))
            y_offset += self.font.get_height() + self.line_spacing
