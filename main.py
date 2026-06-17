from vpython import *
import math

# ── CSS ──────────────────
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
        padding-top: 60px; /* Przestrzeń pod nagłówkiem */
        padding-bottom: 60px; /* Przestrzeń nad przyciskami */
    }

    /* Kinowy format ULTRAWIDE - Pancerny Cross-Clamping */
    canvas {
        /* Próbuje zająć maksimum bezpiecznej przestrzeni */
        width: 96vw !important;
        height: 75vh !important;
        
        /* Ale żelazna matematyka ucina to, co próbuje wyjść za proporcje 21:9 */
        max-width: calc(75vh * 21 / 9) !important;
        max-height: calc(96vw * 9 / 21) !important;
        
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

    /* Panel telemetrii w prawym górnym rogu */
    .telemetry-panel {
        position: fixed !important;
        top: 60px !important;
        right: 20px !important;
        background: rgba(31, 40, 51, 0.85) !important;
        border: 1px solid #45a29e !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #66fcf1 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.6) !important;
        z-index: 10000 !important;
        width: 280px !important;
        pointer-events: none !important;
    }
    .telemetry-row {
        margin-bottom: 8px !important;
        display: flex !important;
        justify-content: space-between !important;
    }
    .telemetry-row:last-child {
        margin-bottom: 0 !important;
    }
    .telemetry-label {
        color: #c5c6c7 !important;
        font-weight: bold !important;
    }
    .telemetry-val {
        color: #66fcf1 !important;
        text-align: right !important;
    }
</style>
<div class="dashboard-title">Artemis II mission trajectory</div>
"""

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

# ── Scale ───────────────────────────────────────────────────
SCALE   = 1.0 / 1.4e6
R_E_VIS = 4.5
R_M_VIS = 2.5
R_S_VIS = 0.5

def sv(pos_m):
    return vector(pos_m.x * SCALE, pos_m.y * SCALE, pos_m.z * SCALE)

# ── Scene ────────────────────────────────────────────────────
scene = canvas(
    title      = STYLES,
    width      = 2100,
    height     = 900,
    background = color.black,
    range      = D_EM * SCALE * 0.40,
)

CAM_ROT_ANG = math.radians(120)
scene.camera.up = rotate(vector(0, 1, 0), angle=CAM_ROT_ANG, axis=vector(0, 0, 1))
screen_left = rotate(vector(-1, 0, 0), angle=CAM_ROT_ANG, axis=vector(0, 0, 1))
CAMERA_OFFSET = 120.0
scene.center = vector(0, 0, 0) + screen_left * CAMERA_OFFSET

# ── Earth ───────────────────────────────────────────────────
earth = sphere(
    pos     = vector(0, 0, 0),
    radius  = R_E_VIS,
    texture = textures.earth,
    axis    = vector(1, 0, 0),
    up      = vector(0, 0, 1)
)
earth_label = label(
    pos     = earth.pos,
    text    = 'Earth',
    height  = 20,
    color   = color.green,
    box     = False,
    line    = False,
    opacity = 0,
    yoffset = -5,
    xoffset = 30
)

# ── Moon ──────────────────────────────────────────────────
ps0, vs0, pm0, vm0 = init_state()

moon = sphere(
    pos    = sv(pm0),
    radius = R_M_VIS,
    color  = color.gray(0.65),
)
moon_label = label(
    pos     = moon.pos,
    text    = 'Moon',
    height  = 20,
    color   = color.white,
    box     = False,
    line    = False,
    opacity = 0,
    yoffset = 20
)

# Moon orbit
moon_orbit = curve(color=color.gray(0.4), radius=0.5)
N_ORBIT_PTS = 200
for i in range(N_ORBIT_PTS + 1):
    ang = 2 * math.pi * i / N_ORBIT_PTS
    moon_orbit.append(vector(D_EM * SCALE * math.cos(ang),
                             D_EM * SCALE * math.sin(ang), 0))

# ── ship ───────────────────────────────────────────────────
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
    b.text = 'Resume' if paused else 'Pause'

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
button(text='Pause',    bind=on_pause)
button(text='Reset',    bind=on_reset)
button(text='Faster', bind=on_faster)
button(text='Slower',  bind=on_slower)

# ── Panel Telemetrii ─────────────────────────────────────────
# Tworzymy pojedynczy obiekt wtext, który będzie renderował cały kontener telemetryczny.
# Zapobiega to automatycznemu zamykaniu tagów HTML przez przeglądarkę i umieszcza dane wewnątrz panelu.
telemetry_hud = wtext(text="")

# ── Główna pętla ─────────────────────────────────────────────
while True:
    rate(60)
    
    if not (paused or done):
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

    # ── Aktualizacja panelu telemetrii ────────────────────────
    days = int(t // 86400)
    hours = int((t % 86400) // 3600)
    minutes = int((t % 3600) // 60)
    seconds = int(t % 60)

    # Earth
    dist_e = mag(pos_ship)
    alt_e = (dist_e - R_EARTH) / 1000.0
    if alt_e < 0: alt_e = 0.0
    vel_e = mag(vel_ship) / 1000.0

    # Księżyc
    dist_m = mag(pos_ship - pos_moon)
    alt_m = (dist_m - R_MOON) / 1000.0
    if alt_m < 0: alt_m = 0.0
    vel_m = mag(vel_ship - vel_moon) / 1000.0

    # Tworzymy pełen blok HTML z wartościami i przypisujemy do jedynego obiektu wtext
    telemetry_hud.text = f"""
    <div class='telemetry-panel'>
        <div class='telemetry-row'>
            <span class='telemetry-label'>MET:</span>
            <span class='telemetry-val'>{days:02d}d {hours:02d}h {minutes:02d}m {seconds:02d}s</span>
        </div>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Altitude (Earth):</span>
            <span class='telemetry-val'>{alt_e:,.1f} km</span>
        </div>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Velocity (Earth):</span>
            <span class='telemetry-val'>{vel_e:.3f} km/s</span>
        </div>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Altitude (Moon):</span>
            <span class='telemetry-val'>{alt_m:,.1f} km</span>
        </div>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Velocity (Moon):</span>
            <span class='telemetry-val'>{vel_m:.3f} km/s</span>
        </div>
    </div>
    """.replace(",", " ")
