
##==============##
##===ASCIIART===##
##==============##

import pygame
import random
import numpy as np

# ==============================
# 1. Pygame 초기화
# ==============================

pygame.init()

WIDTH = 800
HEIGHT = 800
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASCII ART")

font = pygame.font.SysFont("consolas", 16)
clock = pygame.time.Clock()

BACKGROUND = (7, 13, 22)

# ==============================
# 2. 눈송이 설정 (기존 코드)
# ==============================

SNOWCHARACTERS = [".", "+", "*"]
snowflakes = []

for i in range(200):
    snowflake = {
        "x": random.randint(0, WIDTH - 1),
        "y": random.randint(0, HEIGHT - 1),
        "speed": random.uniform(20, 100),
        "character": random.choice(SNOWCHARACTERS),
        "brightness": random.randint(70, 255)
    }

    snowflakes.append(snowflake)


## 크리스마스트리 좌표 생성
TREE_HEIGHT = 3.0
TREE_RADIUS = 1.5

HEIGHT_LEVELS = 35
POINTS_PER_LEVEL = 32

# 트리의 높이와 원형 각도
heights = np.linspace(
    0,
    TREE_HEIGHT,
    HEIGHT_LEVELS
)

angles = np.linspace(
    0,
    2 * np.pi,
    POINTS_PER_LEVEL,
    endpoint=False
)

# 높이와 각도의 모든 조합 생성
height_grid, angle_grid = np.meshgrid(
    heights,
    angles,
    indexing="ij"
)

# 높이에 따른 반지름 계산
radius_grid = TREE_RADIUS * (
    1 - height_grid / TREE_HEIGHT
)

# 원뿔의 X, Y, Z 좌표 계산
x_grid = radius_grid * np.cos(angle_grid)
y_grid = height_grid - TREE_HEIGHT / 2
z_grid = radius_grid * np.sin(angle_grid)

# 1차원 배열로 변환 후 좌표 결합
tree_points = np.column_stack((
    x_grid.ravel(),
    y_grid.ravel(),
    z_grid.ravel()
))


## 트리 줄기 좌표 생성
trunk_points = []

for y in np.linspace(-1.8, -1.3, 8):

    for a in np.linspace(
        0, 2 * np.pi, 12, endpoint=False
    ):

        x = 0.18 * np.cos(a)
        z = 0.18 * np.sin(a)

        trunk_points.append([x, y, z])

trunk_points = np.array(trunk_points)

# ==============================
# 5. 회전 및 카메라 설정
# ==============================

angle = 0.0
ROTATION_SPEED = 0.6

CAMERA_DISTANCE = 6.0
FOCAL_LENGTH = 600

TREE_COLOR = (45, 200, 100)
TRUNK_COLOR = (145, 95, 50)
STAR_COLOR = (255, 220, 90)

# 미리 문자 Surface 생성
tree_surface = font.render("#", True, TREE_COLOR)
trunk_surface = font.render("|", True, TRUNK_COLOR)

star_font = pygame.font.SysFont("consolas", 32, bold=True)
star_surface = star_font.render("*", True, STAR_COLOR)

# ==============================
# 6. 메인 게임 루프
# ==============================

running = True

while running:

    dt = clock.tick(FPS) / 1000

    # 이벤트 처리
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # --------------------------
    # 눈송이 위치 변경
    # --------------------------

    for snowflake in snowflakes:

        snowflake["y"] += snowflake["speed"] * dt

        if snowflake["y"] > HEIGHT:

            snowflake["y"] = -20

            snowflake["x"] = random.randint(
                0, WIDTH - 1
            )

    # --------------------------
    # 트리 회전 계산
    # --------------------------

    angle += ROTATION_SPEED * dt

    rotation_matrix = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])

    rotated_tree = tree_points @ rotation_matrix.T

    rotated_trunk = trunk_points @ rotation_matrix.T

    # --------------------------
    # 화면 지우기
    # --------------------------

    screen.fill(BACKGROUND)

    # --------------------------
    # 눈송이 출력
    # --------------------------

    for snowflake in snowflakes:

        brightness = snowflake["brightness"]

        color = (
            brightness,
            brightness,
            min(brightness + 15, 255)
        )

        character_surface = font.render(
            snowflake["character"],
            True,
            color
        )

        screen.blit(
            character_surface,
            (
                int(snowflake["x"]),
                int(snowflake["y"])
            )
        )

    # --------------------------
    # 트리 줄기와 나뭇잎 출력
    # --------------------------

    # 두 종류의 점과 Surface를 연결
    render_objects = [
        (rotated_tree, tree_surface),
        (rotated_trunk, trunk_surface)
    ]

    for points, character_surface in render_objects:

        # 멀리 있는 점부터 출력
        sorted_points = sorted(
            points,
            key=lambda point: point[2],
            reverse=True
        )

        for x, y, z in sorted_points:

            depth = z + CAMERA_DISTANCE

            scale = FOCAL_LENGTH / depth

            screen_x = WIDTH / 2 + x * scale
            screen_y = HEIGHT / 2 - y * scale

            screen.blit(
                character_surface,
                (int(screen_x), int(screen_y))
            )

    # --------------------------
    # 꼭대기 별 출력
    # --------------------------

    star_x = WIDTH // 2
    star_y = int(
        HEIGHT / 2
        - (TREE_HEIGHT / 2 + 0.1)
        * FOCAL_LENGTH / CAMERA_DISTANCE
    )

    star_rect = star_surface.get_rect(
        center=(star_x, star_y)
    )

    screen.blit(star_surface, star_rect)

    # --------------------------
    # 화면 갱신
    # --------------------------

    pygame.display.flip()

pygame.quit()
