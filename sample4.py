import pygame
import sys
from map_data import MAP, BLOCK_MAP, BLOCK_OFFSET_X

width, height = 1200, 720
floor_y = 600
size = 24
fps = 30

speed = 12
jump_power = -60
gravity = 6

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("jump action game - block map")
clock = pygame.time.Clock()

bg = pygame.image.load("image/bg.png").convert()
block = pygame.image.load("image/block.png").convert_alpha()
princess = pygame.image.load("image/princess.png").convert_alpha()
player_imgs = [
    pygame.image.load("image/player0.png").convert_alpha(),
    pygame.image.load("image/player1.png").convert_alpha(),
    pygame.image.load("image/player0.png").convert_alpha(),
    pygame.image.load("image/player2.png").convert_alpha(),
]

font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)

# map 初期化
floor = [int(c) for line in MAP.split() for c in line]
goal_map_x = len(floor) - 3

BLOCK_H = len(BLOCK_MAP)
BLOCK_W = len(BLOCK_MAP[0])

camera_x = 0
pl_x = width // 2
pl_y = floor_y
pl_yp = 0
pl_jump = False
scene = "タイトル"
timer = 0


def render_text(surface, x, y, txt, font, color):
    surf = font.render(txt, True, color)
    rect = surf.get_rect(center=(x, y))
    surface.blit(surf, rect.topleft)


def on_block_top(px, py, vy):
    tx = int(px // size) - BLOCK_OFFSET_X
    if 0 <= tx < BLOCK_W:
        for by in range(BLOCK_H):
            if BLOCK_MAP[by][tx] == "1":
                block_y = floor_y - (BLOCK_H - by) * size
                if py <= block_y and py >= block_y - abs(vy) - 2:
                    return block_y
    return None


def game_loop():
    global scene, pl_x, pl_y, pl_yp, pl_jump, camera_x, timer

    bg_w = bg.get_width()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if scene == "タイトル":
                    camera_x = 0
                    pl_x = width // 2
                    pl_y = floor_y
                    pl_yp = 0
                    pl_jump = False
                    scene = "ゲーム"
                    timer = 0
                elif scene == "ゲーム" and not pl_jump:
                    pl_jump = True
                    pl_yp = jump_power

        timer += 1

        if scene == "ゲーム":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                camera_x += speed
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                camera_x = max(0, camera_x - speed)

            pl_x = camera_x + width // 2

            pl_y += pl_yp
            pl_yp += gravity

            by = on_block_top(pl_x, pl_y, pl_yp)
            if by is not None:
                pl_y = by
                pl_yp = 0
                pl_jump = False
            elif pl_y >= floor_y:
                pl_y = floor_y
                pl_yp = 0
                pl_jump = False

            if pl_y > floor_y + 200:
                scene = "ゲームオーバー"
                timer = 0

            goal_world_x = goal_map_x * size
            if abs(pl_x - goal_world_x) < size:
                scene = "クリア"
                timer = 0

        elif scene in ["ゲームオーバー", "クリア"]:
            if timer > 150:
                scene = "タイトル"

        # 背景
        start_x = -(camera_x % bg_w)
        x = start_x
        while x < width:
            screen.blit(bg, (x, 0))
            x += bg_w

        # 地面
        first_map = int(camera_x // size)
        for i in range(width // size + 2):
            map_i = first_map + i
            if map_i < len(floor) and floor[map_i] == 1:
                world_x = map_i * size
                screen_x = world_x - camera_x
                rect = block.get_rect(center=(screen_x + size // 2, floor_y + 56))
                screen.blit(block, rect.topleft)

        # ブロックマップ
        for y in range(BLOCK_H):
            for x in range(BLOCK_W):
                if BLOCK_MAP[y][x] == "1":
                    world_x = (x + BLOCK_OFFSET_X) * size
                    world_y = floor_y - (BLOCK_H - y) * size
                    screen_x = world_x - camera_x
                    screen.blit(block, (screen_x, world_y))

        # ゴール
        goal_screen_x = goal_map_x * size - camera_x
        princess_rect = princess.get_rect(center=(goal_screen_x + size // 2, floor_y - 40))
        screen.blit(princess, princess_rect.topleft)

        # プレイヤー
        ani = int(timer / 3) % 4
        player_rect = player_imgs[ani].get_rect(center=(width // 2, pl_y))
        screen.blit(player_imgs[ani], player_rect.topleft)

        # UI
        if scene == "タイトル":
            render_text(screen, width // 2, height * 0.3,
                        "jump action game", font_large, (255, 215, 0))
            render_text(screen, width // 2, height * 0.6,
                        "click to start", font_medium, (135, 206, 250))
        elif scene == "ゲームオーバー":
            render_text(screen, width // 2, height // 2,
                        "game over", font_large, (255, 0, 0))
        elif scene == "クリア":
            render_text(screen, width // 2, height // 2,
                        "game clear!", font_large, (255, 255, 0))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()

#sorcetree