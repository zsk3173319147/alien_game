from os import stat
import sys
import pygame
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_s, K_w
from bullet import Bullet
from alien import Alien
from time import sleep
from random import randint


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == K_RIGHT or event.key == K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == K_a:
        ship.moving_left = True
    elif event.key == K_UP or event.key == K_w:
        ship.moving_up = True
    elif event.key == K_DOWN or event.key == K_s:
        ship.moving_down = True
    elif event.key == pygame.K_j:
        # 创建一颗子弹，并将其加入编组bullets中
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """按键松开"""
    if event.key == K_RIGHT or event.key == K_d:
        ship.moving_right = False
    elif event.key == K_LEFT or event.key == K_a:
        ship.moving_left = False
    elif event.key == K_UP or event.key == K_w:
        ship.moving_up = False
    elif event.key == K_DOWN or event.key == K_s:
        ship.moving_down = False


def check_events(ai_settins, screen, stats, play_button,quit_button,replay_button, ship, bullets, aliens):
    """响应鼠标和键盘事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settins, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settins, stats, screen, ship,
                              aliens, bullets, play_button, mouse_x, mouse_y)
            check_quit_button(quit_button,stats,mouse_x,mouse_y)
            check_replay_button(ai_settins,screen,ship,aliens,bullets,replay_button,stats,mouse_x,mouse_y)

def check_play_button(ai_settings, stats, screen, ship, aliens, bullets, play_button, mouse_x, mouse_y):
    """在玩家单击play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏的统计信息
        ai_settings.initilalize_dynamic_settings()
        stats.reset_stats()
        stats.game_start=True
        stats.game_active = True
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人 并让飞船居中
        create_fleet(ai_settings, screen, aliens, ship)
        ship.ship_center()

def check_quit_button(quit_button,stats,mouse_x,mouse_y):
    button_clicked = quit_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_start:
        sys.exit()

def check_replay_button(ai_settings,screen,ship,aliens,bullets,replay_button,stats,mouse_x,mouse_y):
    button_clicked = replay_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏的统计信息
        ai_settings.initilalize_dynamic_settings()
        stats.reset_stats()
        stats.game_start = True
        stats.game_active = True
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人 并让飞船居中
        create_fleet(ai_settings, screen, aliens, ship)
        ship.ship_center()

def update_screen_menu(ai_settings,screen,stats,play_button,quit_button):
    image=ai_settings.bg_image
    screen.blit(image,image.get_rect())
    if not stats.game_start:
        # 如果游戏处于非启动状态 就绘制 play按钮和quit按钮
        play_button.draw_button()
        quit_button.draw_button()
    pygame.display.flip()

def update_screen_over(ai_settings,screen,stats,replay_button):
    image = ai_settings.gameover_image
    screen.blit(image, image.get_rect())
    if not stats.game_active:
        replay_button.draw_button()
    pygame.display.update()

def update_screen(ai_settings, screen,  ship, bullets, aliens):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # screen.blit(ai_settings.bg_image,(0,0))
    # 在飞船后面重绘所有子弹
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 如果游戏处于非活动状态 就绘制 play按钮
    # if not stats.game_active:
    #     play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, bullets, aliens):
    """更新子弹位置"""
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """响应子弹和外星人的碰撞事件"""
    """检查是否有子弹击中了外星人 是的话就删除子弹和相应的外星人"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # 删除现有子弹,加快游戏节奏并进建一批外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens, ship)


def get_number_alien_x(ai_settings, alien_width):
    # 计算一行可以容纳多少个外星人
    available_space_x = ai_settings.screen_width-2*alien_width
    number_alien_x = int(available_space_x/(2*alien_width))
    return number_alien_x


def get_number_rows(ai_settings, ship_height, alien_height):
    # 计算整个屏幕能容纳多少个外星人
    available_space_y = (ai_settings.screen_heigth -
                         (3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人 并加入当前行"""
    alien = Alien(ai_settings, screen)
    aliens_width = alien.rect.width
    alien.x = aliens_width+2*aliens_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应外星人撞到飞船事件"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
    # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
    # 创建一群新的外星人 将飞船重新放回屏幕中央
        create_fleet(ai_settings, screen, aliens, ship)
        ship.ship_center()
    # 这时暂停 0.5秒 让玩家反应过来
        sleep(0.5)
    else:
        stats.game_active = False


def create_fleet(ai_settings, screen, aliens, ship):
    """创建外星人群体"""
    # 创建一个外星人 并计算一行可以容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)
    random_rows = randint(0, number_rows)
    random_number_alien_x = randint(0, number_alien_x)
    for row_number in range(random_rows):
        random_number1 = randint(0, 1)
        if random_number1 == 1:
            continue
        for alien_number in range(random_number_alien_x):
            random_number2 = randint(0, 1)
            if random_number2 == 1:
                create_alien(ai_settings, screen, aliens,
                             alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    """将整体外星人下移 并改变移动方向"""
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """当有外星人到达边缘时采取的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            # 像被飞船撞到一样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, ship, screen, stats, aliens, bullets):
    """检查是否有外星人处于屏幕边缘 并更新外星人群体中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    """检测外星人和飞船之间的碰撞"""
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
