import sys
import pygame

#Đây là class quản lý màn hình settings trước khi vào game
class SettingScreen:
    def __init__(self, game):
        super().__init__()
        self.mainscreen = game.screen
        self.settings = game.settings
        margin = 50
        self.x = margin
        self.y = margin
        self.option_button = []
        self.screen_width = game.settings.screen_width - margin * 2
        self.screen_height = game.settings.screen_height - margin * 2
        self.screen_rect = (self.x, self.y, self.screen_width, self.screen_height)

    def show_screen(self):# hàm này được gọi ngay khi bật game để hiển thị màn hình settings
        while True:
            stop = self._check_events()
            self._update_screen()
            if stop:
                break

    def _update_screen(self):#Cập nhật màn hình tương tự bên class game
        self.mainscreen.fill(self.settings.bg_color)
        pygame.draw.rect(self.mainscreen, (233, 233, 233), pygame.Rect(self.screen_rect), False, 15)
        self._show_option()
        self._mouse_pointing_show()
        pygame.display.flip()

    def _check_events(self): #Hàm này kiểm tra sự kiện nhập dữ liêu của người dùng bao gồm cả chuột
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = pygame.mouse.get_pressed() # Kiểm tra event khi chuột được ấn
                if button_pressed[0]: # nếu chuột trái được ấn
                    cursor_pos = pygame.mouse.get_pos() # lấy tọa đọ của trỏ chuột trên màn hình
                    #nếu trỏ chuột nằm trong nút lựa chọn thì thực hiên các các phản ứng của nút như đổi màu khi được ấn tới
                    if self.option_button[6][0].collidepoint(cursor_pos): #đây là nút play
                        return True
                    elif self.option_button[0][0].collidepoint(cursor_pos): # đây là nút mốc cần đạt 16
                        self.settings._victory_point = 16
                        self._draw_button_reaction(self.option_button[0][0], color=(20, 20, 20)) #đổi màu của nút khi được ấn
                    elif self.option_button[1][0].collidepoint(cursor_pos):
                        self.settings._victory_point = 2048
                        self._draw_button_reaction(self.option_button[1][0], color=(20, 20, 20))#Tương tự
                    elif self.option_button[2][0].collidepoint(cursor_pos):
                        self.settings._victory_point = 4096
                        self._draw_button_reaction(self.option_button[2][0], color=(20, 20, 20))#Tương tự
                    elif self.option_button[3][0].collidepoint(cursor_pos):
                        self.settings.grid_size = 2
                        self._draw_button_reaction(self.option_button[3][0], color=(20, 20, 20))#Tương tự
                    elif self.option_button[4][0].collidepoint(cursor_pos):
                        self.settings.grid_size = 4
                        self._draw_button_reaction(self.option_button[4][0], color=(20, 20, 20))#Tương tự
                    elif self.option_button[5][0].collidepoint(cursor_pos):
                        self.settings.grid_size = 8
                        self._draw_button_reaction(self.option_button[5][0], color=(20, 20, 20))#Tương tự

    def _mouse_pointing_show(self): #hàm này kiểm tra và đổi màu nút khi được chuột trỏ tới
        cursor_pos = pygame.mouse.get_pos()
        if self.option_button[0][0].collidepoint(cursor_pos):
            self._draw_button_reaction(self.option_button[0][0], self.option_button[0][1])
        elif self.option_button[1][0].collidepoint(cursor_pos):
            self._draw_button_reaction(self.option_button[1][0], self.option_button[1][1])
        elif self.option_button[2][0].collidepoint(cursor_pos):
            self._draw_button_reaction(self.option_button[2][0], self.option_button[2][1])
        elif self.option_button[3][0].collidepoint(cursor_pos):
            self._draw_button_reaction(self.option_button[3][0], self.option_button[3][1])
        elif self.option_button[4][0].collidepoint(cursor_pos):
            self._draw_button_reaction(self.option_button[4][0], self.option_button[4][1])
        elif self.option_button[5][0].collidepoint(cursor_pos):
            self._draw_button_reaction(self.option_button[5][0], self.option_button[5][1])
        elif self.option_button[6][0].collidepoint(cursor_pos):
            self._draw_button_reaction(self.option_button[6][0], self.option_button[6][1])



    def _show_option(self): #Vẽ ra các ô vương lựa chọn trên màn hình
        self._draw_whatever("CHOOSE GOAL:", self.settings.screen_width // 2 - 120 // 2, self.y + 10, 120, 60)
        self._draw_option_box(self.settings.screen_width // 2 - 120 // 2, self.y + 90, 120, 60, "16", 1)
        self._draw_option_box(self.settings.screen_width // 2 - 120 // 2, self.y + 160, 120, 60, "2048", 1)
        self._draw_option_box(self.settings.screen_width // 2 - 120 // 2, self.y + 230, 120, 60, "4096", 1)

        self._draw_whatever("CHOOSE SIZE:", self.settings.screen_width // 2 - 120 // 2, self.y + 300, 120, 60)
        self._draw_option_box(self.settings.screen_width // 2 - 120 // 2, self.y + 380, 120, 60, "2", 3)
        self._draw_option_box(self.settings.screen_width // 2 - 120 // 2, self.y + 450, 120, 60, "4", 3)
        self._draw_option_box(self.settings.screen_width // 2 - 120 // 2, self.y + 520, 120, 60, "8", 3)

        self._draw_option_box(self.settings.screen_width - self.x - 110,
                              self.settings.screen_height - self.y - 110, 60, 60, "PLAY", 2)

    def _draw_option_box(self, x, y, box_width, box_height, number, color_num):# Hàm hỗ trợ cho việc vẽ các ô vuông
        option_box_color = {1: (246, 124, 96),
                            2: (150, 90, 70),
                            3: (238, 199, 82)}
        box = pygame.Rect(x, y, box_width, box_height)
        self.option_button.append([box,number])
        pygame.draw.rect(self.mainscreen, option_box_color[color_num],
                         box, False, 15)
        self._draw_whatever(number, x, y, box_width, box_height)

    def _draw_whatever(self, message, x, y, rect_width, rect_height, size=30):# Hàm hỗ trợ cho việc in số lên các ô vuông lựa chọn đã được vẽ ra màn hình
        temp_font = pygame.font.SysFont('clear sans', size, bold=True)
        number = temp_font.render(str(message), True, (10, 10, 10))
        number_rect = number.get_rect()
        number_rect.center = (x + rect_width // 2, y + rect_height // 2)
        self.mainscreen.blit(number, number_rect)

    def _draw_button_reaction(self, button, number = 'clicked',color = (187, 173, 160)):# Hàm này được gọi đến để đổi màu nút(các ô vuông) khi được chuột trỏ đén
        pygame.draw.rect(self.mainscreen, color, button, False, 15)
        self._draw_whatever(number, button.x, button.y, button.width, button.height)
        pygame.display.flip()
