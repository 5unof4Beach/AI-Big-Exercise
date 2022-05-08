import pygame
import sys
import BOT as bot
from settings import Settings
from gameplay import Gameplay
from settingscreen import SettingScreen
from floatingrect import Floatingrect

# Class này chứa tấy cả các thành phần cần thiết để chạy game
class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont('clear sans', 50, bold=True)
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        self.settingscreen = SettingScreen(self)
        # self.floatingrect = Floatingrect(self)
        self.gameplay = Gameplay()
        self.button_pressed_times = 0
        pygame.display.set_caption("2048")

    def run(self):  # Đây là hàm được gọi đến để chạy game
        self.settingscreen.show_screen()
        self.gameplay.settings = self.settingscreen.settings
        self.gameplay.init_grid()
        self.gameplay.next_number()
        self.not_end = True
        while True:
            self._check_events()

            if self._victory_check():
                if self.not_end:
                    self._update_screen()
                    self.not_end = False
                self._print_victory_message()
                continue

            if self._gameover_check():
                if self.not_end:
                    self._update_screen()
                    self.not_end = False
                self._print_gameover_message()
                continue
            self._update_screen()

    def botAutoPlay(self):
        while True:
            print(self.gameplay.get_grid().flatten())
            bot.createMiniMaxTree(2, self.gameplay.get_grid().flatten())
            move = bot.getMoves()
            self._button_pressed_process(move)
            print(move)

            order = self._check_events()
            
            if(order == 'stop'):
                break

            if self._victory_check():
                break
                if self.not_end:
                    self._update_screen()
                    self.not_end = False
                self._print_victory_message()
                continue

            if self._gameover_check():
                break
                if self.not_end:
                    self._update_screen()
                    self.not_end = False
                self._print_gameover_message()
                continue
            self._update_screen()

    def _update_screen(self):
        # Đây là hàm cập nhật màn hình đồ họa như đổ màu cho background,
        # cập nhật liên tục vị trí của số 2048 di chuyển trong màn hình,
        # Cập nhật lại ma trận các ô vuông,
        # Và in ra phần màn hình trống bên cạnh 2 thông số là mốc chiến thắng, số lần bấm nút và 2 huong dẫn
        self.screen.fill(self.settings.bg_color)
        # self._update_floatingrect()
        self._update_grid()
        self._draw_side_screen()
        pygame.display.flip()

    def _update_floatingrect(self):
        # Hàm này sẽ kiểm ta khi nào số 2048 trôi nổi trên màn hình chạm vào các cạnh màn hình
        # rồi update vị trí và cuối cùng là hiển thị lên trên màn hình
        self.floatingrect.check_edge_hit()
        self.floatingrect.update()
        self.floatingrect.draw()

    def _check_events(self):
        # Đây là hàm nhận và xử lý nhập liệu người dùng mà ở đây là 4 phím mũi tên
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return self._check_key_down_event(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # Hàm này nhận sự kiện bấm nút của người dùng để xử lý
    def _check_key_down_event(self, event):
        if event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_b:
            self.botAutoPlay()

        elif event.key == pygame.K_s:
            return 'stop'

        elif event.key == pygame.K_SPACE:
            print(self.gameplay.get_grid().flatten())
            bot.createMiniMaxTree(2, self.gameplay.get_grid().flatten())
            self._button_pressed_process(bot.getMoves())
            print(bot.getMoves())
            print(self.settings.grid_size)
            
        elif event.key == pygame.K_RIGHT:
            self._button_pressed_process('r')

        elif event.key == pygame.K_LEFT:
            self._button_pressed_process('l')

        elif event.key == pygame.K_UP:
            self._button_pressed_process('u')

        elif event.key == pygame.K_DOWN:
            self._button_pressed_process('d')

        elif event.key == pygame.K_ESCAPE:
            # Khi đang chơi ấn ESC để chon lại settings
            former_goal = self.settingscreen.settings.get_victory_point()
            former_size = self.settingscreen.settings.grid_size
            self.settingscreen.show_screen()
            if (former_goal != self.settingscreen.settings.get_victory_point() or
            former_size != self.settingscreen.settings.grid_size or
            self.not_end == False):
                self.gameplay.settings = self.settingscreen.settings
                self.gameplay.init_grid()
                self.gameplay.next_number()
                self.not_end = True

    def _button_pressed_process(self, key):
        self.button_pressed_times += 1
        before_pressed_grid = self.gameplay.get_grid()
        self.gameplay.move_event(key = key)
        if not self.gameplay.is_the_same(before_pressed_grid):
            self.gameplay.next_number()

    # Cập nhật lại ma trận các ô
    def _update_grid(self):
        self.draw_grid(self.screen, self.gameplay.get_grid())

    # Vẽ các ô vuông ma trận
    def draw_grid(self, screen, matrix):
        space = 10
        radius = 10
        width = self.settings.screen_height
        height = width
        for i in range(self.settings.grid_size):
            for j in range(self.settings.grid_size):
                temp = matrix[i][j]
                rect_height = (height - (self.settings.grid_size + 1) * space) / self.settings.grid_size
                rect_width = (width - (self.settings.grid_size + 1) * space) / self.settings.grid_size

                x = j * (rect_width + space) + space
                y = i * (rect_height + space) + space

                # vẽ hình vuống có màu tương ứng với số
                pygame.draw.rect(screen,
                                 self.settings.number_color.get(temp),
                                 pygame.Rect(x, y, rect_width, rect_height), False, radius)

                # thêm viền cho ô vuống
                pygame.draw.rect(screen,
                                 (10, 10, 10),
                                 pygame.Rect(x, y, rect_width, rect_height), True, radius)
                # in số ở ô vuông tương ứng
                self.draw_number(temp, x, y, rect_width, rect_height)

    # Hàm này dùng để in các số trên cac ô trên ma trân
    # Mỗi số có một màu khác nhau
    def draw_number(self, temp, x, y, rect_width, rect_height):
        if temp == 0:
            temp = ''
        number = self.myfont.render(str(temp), True, (10, 10, 10))
        number_rect = number.get_rect()
        number_rect.center = (x + rect_height // 2, y + rect_width // 2)
        self.screen.blit(number, number_rect)

    # kiểm tra xem đã đạt được con số mục tiêu hay chưa
    def _victory_check(self):
        if self.gameplay.grid.__contains__(self.settings.get_victory_point()):
            return True
        return False

    # in ra màn hinh thông báo "YOU WIN" khi đạt đc số mục tiêu
    def _print_victory_message(self):
        temp_font = pygame.font.SysFont('clear sans', 80, bold=True)
        message = temp_font.render("YOU WIN!!!", True, (10, 10, 10))
        message_rect = message.get_rect()
        message_rect.center = (self.settings.screen_height // 2, self.settings.screen_height // 2)
        self.screen.blit(message, message_rect)
        pygame.display.flip()

    # kiểm tra xem còn điều kiện kết thúc game
    def _gameover_check(self):
        for i in range(self.settings.grid_size):
            row = self.gameplay.grid[i, :]
            col = self.gameplay.grid[:, i]
            for j in range(len(row) - 1):
                if row[j] == row[j + 1] or row[j] == 0 or row[j + 1] == 0:
                    return False
            for j in range(len(col) - 1):
                if col[j] == col[j + 1] or col[j] == 0 or col[j + 1] == 0:
                    return False
        return True

    # in ra thông báo GAME OVER khi không còn nước đi
    def _print_gameover_message(self):
        temp_font = pygame.font.SysFont('clear sans', 60, bold=False)
        message = temp_font.render("OUT OF MOVES, GAME OVER !!!", True, (10, 10, 10))
        message_rect = message.get_rect()
        message_rect.center = (self.settings.screen_height // 2, self.settings.screen_height // 2)
        self.screen.blit(message, message_rect)
        pygame.display.flip()

    #in ra phan thừa bên cạnh phải manf hình các thông sô và hướng dẫ nút
    def _draw_side_screen(self):
        remain = self.settings.screen_width - self.settings.screen_height
        self.print_message("Goal: " + str(self.settings.get_victory_point()), self.settings.screen_width - remain//2, 50)
        self.print_message("Button pressed: " + str(self.button_pressed_times) + " times", self.settings.screen_width - remain//2, 100)
        self.print_message("b: AutoPlay", self.settings.screen_width - remain // 2, self.settings.screen_height - 200)
        self.print_message("s: Stop AutoPlay", self.settings.screen_width - remain // 2, self.settings.screen_height - 150)
        self.print_message("Esc: Options Screen", self.settings.screen_width - remain // 2, self.settings.screen_height - 100)
        self.print_message("q: Exit Game", self.settings.screen_width - remain//2, self.settings.screen_height - 50)

    #Hàm này đơn giản chỉ là in nội dung theo nhu cầu
    # Hàm yêu cầu nhập vào nội dung muốn in và tọa độ x, y trên màn hình
    def print_message(self, message, x, y):
        temp_font = pygame.font.SysFont('clear sans', 40, bold=False)
        message = temp_font.render(str(message), True, (10, 10, 10))
        message_rect = message.get_rect()
        message_rect.center = (x, y)
        self.screen.blit(message, message_rect)