import math

G = 6.674e-11
M_EARTH = 5.972e24
M_MOON = 7.342e22
R_EARTH = 6.371e6
R_MOON = 1.737e6
D_EM = 384_400e3

V_MOON = math.sqrt(G * M_EARTH / D_EM)
R_PARK = R_EARTH + 185_000
V_PARK = math.sqrt(G * M_EARTH / R_PARK)

V_TLI = V_PARK + 3150
SHIP_ANG = math.radians(120)
MOON_ANG = math.radians(244)

SCALE = 1.0 / 1.4e6
R_E_VIS = 4.5
R_M_VIS = 2.5
R_S_VIS = 0.5

CAM_ROT_ANG = math.radians(120)
CAMERA_OFFSET = 120.0

DT = 30.0
SPEED = 1200
