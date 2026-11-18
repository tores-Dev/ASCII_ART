# ASCII_ART

Python의 **Pygame과 NumPy**를 활용하여 움직이는 3D ASCII 아트를 구현하는 개인 학습 프로젝트입니다.

3차원 공간의 점들을 2차원 화면에 투영하고, 문자와 색상의 밝기를 이용해 입체적인 애니메이션을 표현합니다.

## 주요 기능

### 1. 3D ASCII 하트 애니메이션

- 빨간 물방울이 화면 위에서 떨어지는 낙하 애니메이션
- 물방울이 충돌하며 퍼지는 효과
- 물방울의 입자들이 이동하면서 3D 하트로 변하는 모핑(Morphing)
- 완성된 하트의 Y축 회전
- 표면 법선 벡터를 활용한 조명 효과
- 눈송이가 하트 뒤로 떨어지는 배경 애니메이션

### 2. 애니메이션 제어

| 키 | 기능 |
|---|---|
| `R` | 애니메이션 처음부터 다시 시작 |
| `ESC` | 프로그램 종료 |

## 사용 기술

| 기술 | 활용 내용 |
|---|---|
| Python 3.11 | 프로그램의 전체 구조 및 로직 |
| Pygame | 화면 출력, 문자 렌더링, 실시간 애니메이션 |
| NumPy | 3D 좌표 생성, 행렬 연산, 좌표 보간 |
| 3D Projection | 원근 투영을 통한 3D → 2D 좌표 변환 |
| Z-buffer | 문자 격자별 깊이 비교 |
| Morphing | LERP와 Smoothstep을 활용한 형태 변환 |
| Lighting | 법선 벡터와 광원 방향을 이용한 명암 처리 |

## 프로젝트 구조

```text
ASCII_ART/
├── source/
│   └── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## 설치 및 실행

**1. 저장소 복제**

```bash
git clone https://github.com/tores-Dev/ASCII_ART.git
cd ASCII_ART
```

**2. 라이브러리 설치**

Python 3.11 환경을 기준으로 합니다.

```bash
python -m pip install -r requirements.txt
```

**3. 프로그램 실행**

```bash
python source/main.py
```

## 학습 내용

이 프로젝트를 진행하면서 다음 개념을 학습하고 직접 구현했습니다.

- Pygame의 Surface, 게임 루프, FPS와 Delta Time
- NumPy의 다차원 배열과 브로드캐스팅
- 삼각함수를 이용한 3D 좌표 생성
- 회전 행렬과 행렬 곱셈
- 원근 투영과 깊이 비교
- 선형 보간(LERP)과 이징(Easing)
- 법선 벡터, 내적, 외적과 확산광 조명

## 개발 기록

- [x] Pygame 기본 화면 구현
- [x] 눈 내리는 ASCII 배경
- [x] 회전하는 3D ASCII 정육면체
- [x] 3D ASCII 크리스마스트리
- [x] 3D ASCII 하트
- [x] 물방울 낙하 및 충돌 애니메이션
- [x] 물방울에서 하트로 변하는 모핑
- [x] 높이에 따른 모핑 지연 및 물결 효과
- [x] 표면 법선 벡터를 활용한 조명
- [ ] 코드 모듈화 및 구조 개선
- [ ] Windows EXE 실행 파일 제작

## 프로젝트 목적

이 프로젝트는 완성된 3D 그래픽 엔진을 사용하는 대신, **3D 그래픽의 기초 원리를 직접 계산하고 ASCII 문자로 시각화하는 것**을 목표로 합니다.

학습 과정에서 구현한 기능들을 바탕으로 다양한 형태의 3D ASCII 애니메이션을 제작하고, 프로젝트를 지속적으로 개선할 예정입니다.