from vpython import *
import math

# ── Wstrzykiwanie CSS (Modern Space Theme) ──────────────────
STYLES = """
<style>
    * { box-sizing: border-box; }
    body, html {
        margin: 0 !important;
        padding: 0 !important;
        background-color: #0b0c10 !important;
        overflow: hidden !important; 
        width: 100vw;
        height: 100vh;
    }

    /* Węższy nagłówek = więcej miejsca na grafikę 3D */
    .dashboard-title {
        position: fixed;
        top: 0; left: 0; width: 100vw;
        padding: 10px 0; margin: 0 !important;
        font-size: 20px; font-weight: 900; letter-spacing: 4px;
        text-transform: uppercase; color: #66fcf1;
        background: #1f2833; text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.8);
        z-index: 9999;
    }

    #glowscript {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        width: 100vw;
        padding-top: 25px; /* Delikatne odsunięcie od nagłówka */
    }

    /* Kinowy format ULTRAWIDE (21:9) sterowany automatycznie! */
    canvas {
        /* Przeglądarka sama dobierze max rozmiar chroniąc przyciski i boki */
        width: min(96vw, calc(76vh * 21 / 9)) !important;
        height: min(76vh, calc(96vw * 9 / 21)) !important;
        box-shadow: 0px 0px 30px rgba(0, 0, 0, 0.9);
        border-radius: 8px;
        border: 1px solid #1f2833;
    }

    /* Przyciski na samym dole */
    #glowscript > div:last-child {
        position: fixed !important;
        bottom: 15px !important; 
        left: 0 !important;
        width: 100vw !important;
        display: flex !important;
        justify-content: center !important;
        gap: 15px !important; 
        z-index: 10000 !important;
    }

    button {
        background-color: #1f2833 !important;
        color: #66fcf1 !important;
        border: 1px solid #45a29e !important;
        border-radius: 4px;
        padding: 10px 30px !important;
        margin: 0 !important; 
        font-size: 14px !important;
        font-weight: bold;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    button:hover {
        background-color: #45a29e !important;
        color: #0b0c10 !important;
        box-shadow: 0px 0px 15px #66fcf1;
        transform: translateY(-2px);
    }
</style>
<div class="dashboard-title">Artemis II mission trajectory</div>
"""

# ── Stałe fizyczne ──────────────────────────────────────────
G         = 6.674e-11
M_EARTH   = 5.972e24
M_MOON    = 7.342e22
R_EARTH   = 6.371e6
R_MOON    = 1.737e6
D_EM      = 384_400e3

V_MOON    = math.sqrt(G * M_EARTH / D_EM)        # ~1022 m/s
R_PARK    = R_EARTH + 185_000
V_PARK    = math.sqrt(G * M_EARTH / R_PARK)       # ~7796 m/s
V_TLI     = V_PARK + 3150                          # ~10946 m/s

# ── Warunki początkowe (dobrane numerycznie dla ósemki) ─────
SHIP_ANG  = math.radians(120)
MOON_ANG  = math.radians(244)

def init_state():
    ps = vector(R_PARK * math.cos(SHIP_ANG),
                R_PARK * math.sin(SHIP_ANG), 0)
    vs = vector(-math.sin(SHIP_ANG) * V_TLI,
                math.cos(SHIP_ANG) * V_TLI, 0)
    pm = vector(D_EM * math.cos(MOON_ANG),
                D_EM * math.sin(MOON_ANG), 0)
    vm = vector(-math.sin(MOON_ANG) * V_MOON,
                math.cos(MOON_ANG) * V_MOON, 0)
    return ps, vs, pm, vm

# ── Skala ───────────────────────────────────────────────────
SCALE   = 1.0 / 1.4e6
R_E_VIS = 4.5
R_M_VIS = 2.5
R_S_VIS = 0.5

def sv(pos_m):
    return vector(pos_m.x * SCALE, pos_m.y * SCALE, pos_m.z * SCALE)

# ── Scena ────────────────────────────────────────────────────
scene = canvas(
    title      = STYLES,
    width      = 2100,            # Zwiększona szerokość
    height     = 900,          # Kinowa, niska wysokość (Format 21:9)
    background = color.black,
    range      = D_EM * SCALE * 0.40, # Zwiększono zasięg widzenia!
)

CAM_ROT_ANG = math.radians(120)
scene.camera.up = rotate(vector(0, 1, 0), angle=CAM_ROT_ANG, axis=vector(0, 0, 1))
screen_left = rotate(vector(-1, 0, 0), angle=CAM_ROT_ANG, axis=vector(0, 0, 1))
CAMERA_OFFSET = 120.0
scene.center = vector(0, 0, 0) + screen_left * CAMERA_OFFSET

# ── Ziemia ───────────────────────────────────────────────────
earth = sphere(
    pos     = vector(0, 0, 0),
    radius  = R_E_VIS,
    texture = textures.earth,
)
earth_label = label(
    pos     = earth.pos,       # Idealnie w środku Ziemi
    text    = 'Ziemia',
    height  = 20,
    color   = color.green,
    box     = False,
    line    = False,           # Wyłącza kreskę łączącą środek z napisem
    opacity = 0,
    yoffset = 25               # Przesunięcie o 25 PIKSELI ZAWSZE w górę ekranu
)

# ── Księżyc ──────────────────────────────────────────────────
ps0, vs0, pm0, vm0 = init_state()

moon = sphere(
    pos    = sv(pm0),
    radius = R_M_VIS,
    color  = color.gray(0.65),
)
moon_label = label(
    pos     = moon.pos,
    text    = 'Księżyc',
    height  = 20,
    color   = color.white,
    box     = False,
    line    = False,
    opacity = 0,
    yoffset = 20
)

# Orbita Księżyca
moon_orbit = curve(color=color.gray(0.4), radius=0.5)
N_ORBIT_PTS = 200
for i in range(N_ORBIT_PTS + 1):
    ang = 2 * math.pi * i / N_ORBIT_PTS
    moon_orbit.append(vector(D_EM * SCALE * math.cos(ang),
                             D_EM * SCALE * math.sin(ang), 0))

# ── Statek ───────────────────────────────────────────────────
ship = sphere(
    pos          = sv(ps0),
    radius       = R_S_VIS,
    color        = color.yellow,
    emissive     = True,
    make_trail   = True,
    trail_type   = 'curve',
    trail_color  = color.orange,
    trail_radius = 0.5,
    retain       = 12000,
)
ship_label = label(
    pos     = ship.pos,
    text    = 'Integrity',
    height  = 20,
    color   = color.yellow,
    box     = False,
    line    = False,
    opacity = 0,
    yoffset = 15
)

# ── Stan symulacji ───────────────────────────────────────────
pos_ship, vel_ship, pos_moon, vel_moon = init_state()
t      = 0.0
dt     = 30.0
SPEED  = 1200
paused = False
done   = False

# ── Fizyka ───────────────────────────────────────────────────
def accel_ship(ps, pm):
    re = -ps
    rm = pm - ps
    me = mag(re); mm = mag(rm)
    if me < 1e3 or mm < 1e3:
        return vector(0, 0, 0)
    return (G * M_EARTH / me**3) * re + (G * M_MOON / mm**3) * rm

def accel_moon(pm):
    r = -pm
    m = mag(r)
    if m < 1e3:
        return vector(0, 0, 0)
    return (G * M_EARTH / m**3) * r

def rk4(ps, vs, pm, dt):
    def a(p): return accel_ship(p, pm)
    k1v = a(ps);                      k1p = vs
    k2v = a(ps + 0.5*dt*k1p);        k2p = vs + 0.5*dt*k1v
    k3v = a(ps + 0.5*dt*k2p);        k3p = vs + 0.5*dt*k2v
    k4v = a(ps +     dt*k3p);        k4p = vs +     dt*k3v
    new_ps = ps + (dt/6) * (k1p + 2*k2p + 2*k3p + k4p)
    new_vs = vs + (dt/6) * (k1v + 2*k2v + 2*k3v + k4v)
    return new_ps, new_vs

def euler_moon(pm, vm, dt):
    a  = accel_moon(pm)
    vm2 = vm + a * dt
    pm2 = pm + vm2 * dt
    return pm2, vm2

# ── Przyciski sterowania ─────────────────────────────────────
def on_pause(b):
    global paused
    paused = not paused
    b.text = 'Wznów' if paused else 'Pauza'

def on_reset(b):
    global pos_ship, vel_ship, pos_moon, vel_moon, t, done
    pos_ship, vel_ship, pos_moon, vel_moon = init_state()
    t = 0.0; done = False
    ship.clear_trail()
    ship.pos = sv(pos_ship)
    moon.pos = sv(pos_moon)
    # Zmienione, by napis podążał dokładnie za statkiem (z uwzględnieniem yoffset)
    ship_label.pos = ship.pos
    moon_label.pos = moon.pos

def on_faster(b):
    global SPEED
    SPEED = min(SPEED * 2, 76800)

def on_slower(b):
    global SPEED
    SPEED = max(SPEED // 2, 60)

# Ustawiamy DIV dla przycisków
scene.append_to_caption('\n') # Mały odstęp bezpieczeństwa pod płótnem
button(text='Pauza',    bind=on_pause)
button(text='Reset',    bind=on_reset)
button(text='Szybciej', bind=on_faster)
button(text='Wolniej',  bind=on_slower)

# ── Główna pętla ─────────────────────────────────────────────
while True:
    rate(60)
    if paused or done:
        continue

    steps = max(1, int(SPEED / dt / 60))

    for _ in range(steps):
        pos_moon, vel_moon = euler_moon(pos_moon, vel_moon, dt)
        pos_ship, vel_ship = rk4(pos_ship, vel_ship, pos_moon, dt)
        t += dt

    ship.pos = sv(pos_ship)
    moon.pos = sv(pos_moon)

    # Zmienione, by napis podążał dokładnie za statkiem
    ship_label.pos = ship.pos
    moon_label.pos = moon.pos

    earth.rotate(angle=0.001, axis=vector(0, 0, 1))

    if t / 86400 > 0.5 and mag(pos_ship) < R_EARTH * 1.3:
        done = True

    if t / 86400 > 13:
        done = True
