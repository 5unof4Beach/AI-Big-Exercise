import pygame.image

#Class này để quản lý việc vễ ra số 2048 di chuyển liên tục trên màn hình và sau ma trận các ô vuống
class Floatingrect:
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.image = pygame.image.load('assets/floating_picture_fit.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.speed = 1.0

    def update(self): # Hàm này sẽ cập nhật tọa độ số 2048 trôi nổi trên màn hình
        self.rect.x += self.settings.floatingrect_speed * self.settings.floatingrect_direction_horizontal
        self.rect.y += self.settings.floatingrect_speed * self.settings.floatingrect_direction_vertical

    def check_edge_hit(self):# hàm này kiêm tra xem hình có chạm vào các cạnh hay không,
        # nếu chạm mép trên hoặc dưới thì đảo ngược hướng theo chiều dọc
        # ngược lại thì đảo ngược hướng theo chiều ngang
        if self.rect.right >= self.screen_rect.right or self.rect.left < 0:
            self.settings.floatingrect_direction_horizontal *= -1
        if self.rect.top < 0 or self.rect.bottom >= self.screen_rect.bottom:
            self.settings.floatingrect_direction_vertical *= -1

    def draw(self): # Hàm này để vẽ hình
        self.screen.blit(self.image, self.rect)
