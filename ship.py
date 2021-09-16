import pygame


class Ship():
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其所在位置"""
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载图像并获取其外接矩形
        self.image = pygame.image.load('resourses\\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将新飞船放在屏幕底部的正中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 在飞船的属性center和bottom中存储小数值
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)
        # 移动的标志
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        # 根据移动标志调整飞船位置

    def update(self):
        if self.moving_left and self.rect.left > 0:
            # and后面的判断是为了限制飞船的飞行范围
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.bottom -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.height:
            self.bottom += self.ai_settings.ship_speed_factor
        # 根据self.center和self.bottom更新rect对象
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def ship_center(self):
        """让飞船位置居中"""
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
