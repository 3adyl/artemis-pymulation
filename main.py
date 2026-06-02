"""
Artemis II – Free-Return Trajectory Simulation
Wymagania: pip install vpython
Uruchomienie: python artemis2_simulation.py
"""

from vpython import *
import math

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
#   statek startuje pod kątem 120°, Księżyc pod kątem 244°
#   → przelot ~19 000 km od Księżyca, powrót po ~9.2 dnia
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
SCALE   = 1.0 / 1.4e6      # 1 jednostka VPython ≈ 1400 km
R_E_VIS = 4.5               # Ziemia – powiększona dla czytelności
R_M_VIS = 2.5               # Księżyc – powiększony
R_S_VIS = 0.5               # statek

def sv(pos_m):
    return vector(pos_m.x * SCALE, pos_m.y * SCALE, pos_m.z * SCALE)

# ── Scena ────────────────────────────────────────────────────
scene = canvas(
    title      = 'Artemis II – Free-Return Trajectory',
    width      = 1200,
    height     = 750,
    background = color.black,
    range      = D_EM * SCALE * 0.85,
)
# Wyśrodkuj między Ziemią a Księżycem
cx = 0.5 * D_EM * SCALE * math.cos(MOON_ANG)
cy = 0.5 * D_EM * SCALE * math.sin(MOON_ANG)
scene.center = vector(cx, cy, 0)

# ── Ziemia ───────────────────────────────────────────────────
earth = sphere(
    pos     = vector(0, 0, 0),
    radius  = R_E_VIS,
    texture = textures.earth,
)

# ── Księżyc ──────────────────────────────────────────────────
ps0, vs0, pm0, vm0 = init_state()

moon = sphere(
    pos    = sv(pm0),
    radius = R_M_VIS,
    color  = color.gray(0.65),
)

# ── Statek ───────────────────────────────────────────────────
ship = sphere(
    pos          = sv(ps0),
    radius       = R_S_VIS,
    color        = color.yellow,
    emissive     = True,
    make_trail   = True,
    trail_type   = 'curve',
    trail_color  = color.orange,
    trail_radius = 0.12,
    retain       = 12000,
)

# ── Stan symulacji ───────────────────────────────────────────
pos_ship, vel_ship, pos_moon, vel_moon = init_state()
t      = 0.0
dt     = 30.0          # krok RK4 [s]
SPEED  = 1200          # sekund symulacji na sekundę rzeczywistą
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

def on_faster(b):
    global SPEED
    SPEED = min(SPEED * 2, 76800)

def on_slower(b):
    global SPEED
    SPEED = max(SPEED // 2, 60)

scene.append_to_caption('\n')
button(text='Pauza',    bind=on_pause)
scene.append_to_caption('  ')
button(text='Reset',    bind=on_reset)
scene.append_to_caption('  ')
button(text='Szybciej', bind=on_faster)
scene.append_to_caption('  ')
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

    earth.rotate(angle=0.001, axis=vector(0, 0, 1))

    if t / 86400 > 0.5 and mag(pos_ship) < R_EARTH * 1.3:
        done = True

    if t / 86400 > 13:
        done = True
