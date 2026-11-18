##==============##
##===ASCIIART===##
##==============##
import pygame
import random
import numpy as np

##=====================================
## Pygame 초기화
pygame.init()
# 화면 크기
WIDTH = 800
HEIGHT = 800
FPS = 30
# 프로그램 창 생성
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASCII ART")
# 글꼴 설정
font = pygame.font.SysFont("consolas", 16)
# 프레임 속도 관리
clock = pygame.time.Clock()
# 색상 설정
BACKGROUND = (7, 13, 22)
##=====================================

## ASCII 문자 설정
CHARACTERS = ".,-~:;=!*#%@"

CELL_WIDTH = 9
CELL_HEIGHT = 16

# 밝기에 따른 문자 Surface 생성
character_surfaces = []

for i, char in enumerate(CHARACTERS):

    ratio = i / (len(CHARACTERS) - 1)

    color = (
        int(100 + ratio * 155),
        int(10 + ratio * 35),
        int(15 + ratio * 35)
    )

    surface = font.render(char, True, color)
    character_surfaces.append(surface)


## 2D 하트 곡선 생성
# 하트 크기
HEART_SIZE = 1.8
# 하트 앞뒤 두께
HEART_DEPTH = 0.65

angles = np.linspace(
    0, 2 * np.pi, 120, endpoint=False
)

heart_x = 16 * np.sin(angles) ** 3

heart_y = (
    13 * np.cos(angles)
    - 5 * np.cos(2 * angles)
    - 2 * np.cos(3 * angles)
    - np.cos(4 * angles)
)

# 좌표 크기와 중심 조정
heart_x = heart_x / 18 * HEART_SIZE
heart_y = (heart_y + 2) / 18 * HEART_SIZE


## 3D 하트 표면 생성
heart_points = []

# 중심에서 외곽선까지의 비율
radius_levels = np.linspace(0, 1, 28)

for radius in radius_levels:

    # 중심에서 외곽으로 갈수록 Z 두께 감소
    depth = HEART_DEPTH * np.sqrt(1 - radius ** 2)

    for side in [-1, 1]:

        x = heart_x * radius
        y = heart_y * radius
        z = np.full_like(x, side * depth)

        points = np.stack((x, y, z), axis=1)

        heart_points.append(points)

# 모든 표면 점을 하나의 배열로 결합
heart_points = np.concatenate(heart_points, axis=0)

# 하트의 가장 낮은 점과 높은 점
MIN_Y = heart_points[:, 1].min()
MAX_Y = heart_points[:, 1].max()


## 하트 표면의 법선 벡터 계산
# 좌표 배열을 원래 생성 구조로 변환
surface_grid = heart_points.reshape(
    len(radius_levels),
    2,
    len(angles),
    3
)
# 각도 방향의 접선 벡터
tangent_angle = (np.roll(surface_grid, -1, axis=2)
                 - np.roll(surface_grid, 1, axis=2))

# 반지름 방향의 접선 벡터
tangent_radius = np.gradient(surface_grid, axis=0)

# 두 접선에 수직인 벡터 계산
normal_grid = np.cross(tangent_angle, tangent_radius)

# 뒷면 법선의 방향 반전
normal_grid[:, 0, :, :] *= -1

# 법선 벡터의 길이 계산
normal_lengths = np.linalg.norm(normal_grid, axis=3, keepdims=True)

# 길이가 0인 경우를 고려하여 정규화
normal_grid = normal_grid / np.maximum(normal_lengths, 1e-8)

# 중심부의 법선 방향 보정
normal_grid[0, 0, :, :] = [0, 0, -1]
normal_grid[0, 1, :, :] = [0, 0, 1]

# 모든 법선 벡터를 (점 개수, 3) 형태로 변환
heart_normals = normal_grid.reshape(-1, 3)


## 물방울 3D 좌표 생성
# 하트의 각 점이 전체 높이에서 차지하는 비율
# 가장 아래쪽은 0, 가장 위쪽은 1
height_ratio = (
    (heart_points[:, 1] - MIN_Y)
    / (MAX_Y - MIN_Y)
)

# 하트의 X, Z좌표를 -1~1 범위로 정규화
normalized_x = (
    heart_points[:, 0]
    / np.max(np.abs(heart_points[:, 0]))
)

normalized_z = (
    heart_points[:, 2]
    / HEART_DEPTH
)

# 물방울의 높이에 따른 반지름
drop_radius = (
    np.sqrt(
        np.clip(np.sin(np.pi * height_ratio), 0, 1)
    )
    * (0.35 + 0.65 * (1 - height_ratio))
)

# 물방울 X좌표
drop_x = (
    normalized_x
    * drop_radius
    * 0.38
)

# 물방울 Y좌표
drop_y = (
    height_ratio - 0.5
) * 0.8

# 물방울 Z좌표
drop_z = (
    normalized_z
    * drop_radius
    * 0.26
)

# X, Y, Z좌표 결합
drop_points = np.column_stack((
    drop_x,
    drop_y,
    drop_z
))

print("하트 좌표:", heart_points.shape)
print("물방울 좌표:", drop_points.shape)



## 눈송이 설정
SNOWCHARACTERS = [".", "+", "*"]
snowflakes = []
# 눈송이 생성 (200개)
for i in range(200):
    snowflake = {
        "x": random.randint(0, WIDTH -1),
        "y": random.randint(0, HEIGHT -1),
        "speed": random.uniform(20, 100),
        "character": random.choice(SNOWCHARACTERS),
        "brightness": random.randint(70, 255)
    }
    snowflakes.append(snowflake)


## 회전 및 카메라 설정
# 회전 각도 (Radian)
angle = 0.0
# 회전 속도 (Radian/sec)
ROTATION_SPEED = 0.4

# 투영 설정
CAMERA_DISTANCE = 5.0
FOCAL_LENGTH = 850


## 조명 설정
# 빛이 들어오는 방향
LIGHT_DIRECTION = np.array([
    -0.45,
    0.65,
    0.65
])
# 광원 방향 벡터 정규화
LIGHT_DIRECTION = (
    LIGHT_DIRECTION
    / np.linalg.norm(LIGHT_DIRECTION)
)

# 주변광: 빛을 직접 받지 않는 면의 최소 밝기
AMBIENT_LIGHT = 0.25
# 확산광: 빛을 직접 받는 정도에 따른 밝기
DIFFUSE_STRENGTH = 0.75


## 애니메이션 설정
animation_time = 0.0

DROP_DURATION = 2.2
SPLASH_DURATION = 0.35
GROW_DURATION = 2.4

DROP_START_Y = 4.0
DROP_END_Y = MIN_Y + 0.4


## 모핑 시작 좌표 준비
# 물방울이 낙하를 마친 위치
drop_end_points = drop_points.copy()
drop_end_points[:, 1] += DROP_END_Y

# 물방울이 납작하게 퍼진 형태
splash_points = drop_end_points.copy()

# 가로 방향으로 퍼짐
splash_points[:, 0] *= 2.6

# 세로 방향으로 납작해짐
splash_points[:, 1] = (
    DROP_END_Y
    + (splash_points[:, 1] - DROP_END_Y) * 0.18
)

# 깊이 방향으로도 퍼짐
splash_points[:, 2] *= 2.0

## 부드러운 움직임을 위한 함수
def smoothstep(t):

    t = np.clip(t, 0, 1)

    return t * t * (3 - 2 * t)



## 메인 게임 루프
running = True
while running:
    # 프레임 시간 계산 (초 단위)
    dt = clock.tick(FPS) / 1000
    animation_time += dt

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # R키로 애니메이션 다시 시작
            if event.key == pygame.K_r:
                animation_time = 0.0
                angle = 0.0


    ## 눈송이 위치 변경
    for snowflake in snowflakes:
        snowflake["y"] += snowflake["speed"] * dt
        # 화면 아래를 벗어나면 다시 위로 이동
        if snowflake["y"] > HEIGHT:
            snowflake["y"] = -20
            snowflake["x"] = random.randint(0, WIDTH -1)


    ## 애니메이션 단계별 좌표 생성
    if animation_time < DROP_DURATION:

        # 1단계: 물방울 낙하
        progress = animation_time / DROP_DURATION

        # 점점 빠르게 떨어지는 효과
        fall = progress ** 2

        center_y = (
            DROP_START_Y
            + (DROP_END_Y - DROP_START_Y) * fall
        )

        active_points = drop_points.copy()
        active_points[:, 1] += center_y

    elif animation_time < (
        DROP_DURATION + SPLASH_DURATION
    ):

        # 2단계: 물방울이 납작하게 퍼짐
        elapsed = animation_time - DROP_DURATION
        progress = elapsed / SPLASH_DURATION

        # 부드러운 진행률 계산
        t = smoothstep(progress)

        # 물방울 -> 퍼진 물방울
        active_points = (
            drop_end_points
            + (splash_points - drop_end_points) * t
        )

    elif animation_time < (
        DROP_DURATION + SPLASH_DURATION + GROW_DURATION
    ):

        ## 3단계: 아래에서 위로 흐르는 하트 모핑
        elapsed = (
            animation_time
            - DROP_DURATION
            - SPLASH_DURATION
        )

        progress = elapsed / GROW_DURATION

        # 전체 모핑 진행률
        t = smoothstep(progress)

        # 높이에 따라 각 점의 시작 시간을 다르게 설정
        # 아래쪽 점은 바로 시작하고 위쪽 점은 늦게 시작
        delay = height_ratio * 0.35

        # 각 점별 진행률 계산
        local_t = np.clip(
            (t - delay) / (1 - delay),
            0,
            1
        )

        # 점별 움직임을 부드럽게 조정
        local_t = smoothstep(local_t)

        # 물방울에서 하트로 좌표 보간
        active_points = (
            splash_points
            + (
                heart_points - splash_points
            ) * local_t[:, np.newaxis]
        )

        # 액체처럼 살짝 출렁이는 효과
        wave = (
            0.05
            * np.sin(np.pi * local_t)
            * np.sin(
                8 * np.pi * t
                - 4 * height_ratio
            )
        )

        # Y좌표에 물결 효과 추가
        active_points[:, 1] += wave

    else:

        # 4단계: 완성된 하트 회전
        angle += ROTATION_SPEED * dt

        active_points = heart_points


    ## 회전 행렬
    rotation_matrix = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [      0,       1,       0      ],
        [-np.sin(angle),0, np.cos(angle)]
    ])
    
    rotated_points = (active_points @ rotation_matrix.T)

    ## 조명 밝기 계산
    # 법선 벡터도 하트와 함께 회전
    rotated_normals = (heart_normals @ rotation_matrix.T)

    # 법선 벡터와 광원 방향의 내적
    light_dot = (rotated_normals @ LIGHT_DIRECTION)

    # 확산광 계산
    diffuse = np.clip(light_dot, 0, 1)

    # 최종 조명 밝기
    lighting = (AMBIENT_LIGHT + DIFFUSE_STRENGTH * diffuse)

    # 기존의 깊이 기반 밝기
    z_values = rotated_points[:, 2]

    depth_brightness = np.clip(
        (z_values + HEART_SIZE) / (2 * HEART_SIZE),
        0,
        1
    )

    # 물방울에서 하트로 변할 때
    # 조명 효과가 서서히 적용되도록 설정
    morph_start = DROP_DURATION + SPLASH_DURATION

    if animation_time < morph_start:
        light_blend = 0.0

    elif animation_time < morph_start + GROW_DURATION:
        progress = ((animation_time - morph_start) / GROW_DURATION)

        light_blend = smoothstep(progress)

    else:
        light_blend = 1.0

    # 기존 명암과 새로운 조명 사이의 보간
    point_brightness = (
        depth_brightness * (1 - light_blend)
        + lighting * light_blend
    )


    ## 3D 좌표를 2D 좌표로 반환
    x = rotated_points[:, 0]
    y = rotated_points[:, 1]
    z = rotated_points[:, 2]

    depth = CAMERA_DISTANCE - z

    scale = FOCAL_LENGTH / depth

    screen_x = WIDTH / 2 + x * scale
    screen_y = HEIGHT / 2 - y * scale


    ## ASCII 문자 격자 만들기
    columns = (screen_x / CELL_WIDTH).astype(int)
    rows = (screen_y / CELL_HEIGHT).astype(int)

    # 깊이 값을 저장할 딕셔너리
    visible_points = {}

    # 하트가 차지하는 가로 범위 저장
    heart_bounds = {}

    for i in range(len(rotated_points)):
        col = columns[i]
        row = rows[i]
        if not (
            0 <= col < WIDTH // CELL_WIDTH
            and 0 <= row < HEIGHT // CELL_HEIGHT
        ): continue

        position = (col, row)
        # 각 문자 칸의 가장 가까운 점 저장
        if (
            position not in visible_points
            or z[i] > visible_points[position][0]
        ): visible_points[position] = (z[i], point_brightness[i])

        # 행별 하트의 가로 범위 계산
        if row not in heart_bounds:
            heart_bounds[row] = [col, col]
        else:
            heart_bounds[row][0] = min(
                heart_bounds[row][0], col
            )
            heart_bounds[row][1] = max(
                heart_bounds[row][1], col
            )

    
    ## 화면 지우기
    screen.fill(BACKGROUND)

    ## 눈송이 출력
    for snowflake in snowflakes:
        # 눈송이가 위치한 문자 격자
        snow_col = int(snowflake["x"] / CELL_WIDTH)
        snow_row = int(snowflake["y"] / CELL_HEIGHT)

        # 하트가 차지하는 행인지 확인
        if snow_row in heart_bounds:
            left, right = heart_bounds[snow_row]
            # 하트 내부라면 눈송이 출력 생략
            if left <= snow_col <= right:
                continue

        # 눈송이의 색상 계산
        brightness = snowflake["brightness"]

        color = (
            brightness,
            brightness,
            min(brightness + 15, 255)
        )

        # 문자 Surface 생성
        character_surface = font.render(
            snowflake["character"],
            True,
            color
        )

        # 눈송이를 화면에 출력
        screen.blit(character_surface, (int(snowflake["x"]), int(snowflake["y"])))


    ## 하트 + 물방울 출력
    for position, (point_z, brightness) in visible_points.items():

        col, row = position

        # 밝기에 따라 문자 선택
        char_index = int(brightness * (len(CHARACTERS) - 1))

        character_surface = (character_surfaces[char_index])

        screen.blit(character_surface, (col * CELL_WIDTH, row * CELL_HEIGHT))

    ## 화면 갱신(완성된 화면을 디스플레이에 표시)
    pygame.display.flip()

pygame.quit()
