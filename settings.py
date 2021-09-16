
class Settings():
    """存储《外星人入侵》这个游戏的所有设置的类"""

    def __init__(self):
        self.screen_width = 1200
        self.screen_heigth = 800
        self.Screen_caption = 'Alien Invasion'
        self.bg_color = (230, 230, 230)
        #飞船的设置：飞行速度
        self.ship_speed_factor=1.5
        self.ship_limit=3
        # 设置子弹的属性: 创建一个宽为3像素、高15像素的深灰色子弹 子弹速度为1
        self.bullet_speed_factor=1
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=60,60,60
        # 外星人的基本设置
        self.alien_speed_factor=1
        self.fleet_drop_speed=10
        # fleet_direction 为1表示向左移动 为-1表示向左移动
        self.fleet_direction=1

