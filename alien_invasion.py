from os import stat
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import BUtton


def run_game():
    # 初始化游戏并创建一个对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_heigth))
    pygame.display.set_caption(ai_settings.Screen_caption)
    # 设置背景色
    # bg_color = ai_settings.bg_color
    # 创建一个play按钮
    play_button = BUtton(250, screen, "Play")
    replay_button=BUtton(600,screen,"Play Again ")
    quit_button=BUtton(450,screen,"Quit Game")
    # 创建一个用于储存游戏统计信息的实例
    stats = GameStats(ai_settings)
    # 创建一个飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个外星人编组
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)
    # 加载音乐
    pygame.mixer.init()
    pygame.mixer.music.load(r'resourses\\bg.mp3')
    # 开始游戏的主循环
    while True:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(-1)
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats,
                        play_button,quit_button,replay_button, ship, bullets, aliens)       
        if not stats.game_start:
            gf.update_screen_menu(ai_settings, screen, stats,
                              play_button, quit_button)
        elif stats.game_active:
            ship.update()
        # bullets.update()
        #  删除已经消失的子弹
        # for bullet in bullets.copy():
        #     if bullet.rect.bottom <= 0:
        #         bullets.remove(bullet)
            gf.update_bullets(ai_settings, screen, ship, bullets, aliens)
        # print(len(bullets)) 测试子弹编组bullets中还有几颗子弹
        # 每次循环都重绘屏幕
        # screen.fill(ai_settings.bg_color)
        # ship.blitme()
        # 让最近绘制的屏幕可见
        # pygame.display.flip()
            gf.update_aliens(ai_settings, ship, screen, stats, aliens, bullets)
            gf.update_screen(ai_settings, screen, ship,
                         bullets, aliens)

        else:
            gf.update_screen_over(ai_settings,screen,stats,replay_button)
run_game()
