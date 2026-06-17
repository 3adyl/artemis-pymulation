from vpython import *
import math

# ── CSS ──────────────────────────────────────────────────────
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
        padding-top: 60px;
        padding-bottom: 60px;
    }

    /* Kinowy format ULTRAWIDE */
    canvas {
        width: 96vw !important;
        height: 75vh !important;
        max-width: calc(75vh * 21 / 9) !important;
        max-height: calc(96vw * 9 / 21) !important;
        box-shadow: 0px 0px 30px rgba(0, 0, 0, 0.9);
        border-radius: 8px;
        border: 1px solid #1f2833;
    }

    /* ── Panel sliderów ── */
    #slider-panel {
        position: fixed !important;
        top: 60px !important;
        left: 20px !important;
        background: rgba(31, 40, 51, 0.85) !important;
        border: 1px solid #45a29e !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #66fcf1 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.6) !important;
        z-index: 10000 !important;
        width: 290px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 14px !important;
    }

    .param-container {
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
        width: 100% !important;
    }

    .param-header {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
    }

    .param-label {
        color: #c5c6c7 !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }

    /* Wtext wewnątrz param-header */
    .param-header span {
        color: #66fcf1 !important;
        font-weight: bold !important;
    }

    /* jQuery UI Slider (używany przez GlowScript w VPython) */
    .ui-slider {
        background: #1f2833 !important;
        border: 1px solid #45a29e !important;
        height: 6px !important;
        border-radius: 3px !important;
        position: relative !important;
        margin: 6px 0 !important;
        cursor: pointer !important;
    }
    
    .ui-slider-handle {
        background: #66fcf1 !important;
        border: 1px solid #66fcf1 !important;
        width: 14px !important;
        height: 14px !important;
        border-radius: 50% !important;
        top: -5px !important;
        margin-left: -7px !important;
        cursor: pointer !important;
        box-shadow: 0 0 8px rgba(102, 252, 241, 0.8) !important;
        outline: none !important;
        position: absolute !important;
        z-index: 2 !important;
    }
    
    .ui-slider-handle:hover, .ui-slider-handle:focus {
        background: #45a29e !important;
        border-color: #45a29e !important;
        box-shadow: 0 0 12px #66fcf1 !important;
    }

    /* Gdy slider jest zablokowany */
    .ui-state-disabled {
        opacity: 0.35 !important;
        cursor: not-allowed !important;
    }
    .ui-state-disabled .ui-slider-handle {
        cursor: not-allowed !important;
        background: #45a29e !important;
        border-color: #45a29e !important;
        box-shadow: none !important;
    }

    /* Standardowy input range (na wszelki wypadek) */
    input[type=range] {
        -webkit-appearance: none !important;
        width: 100% !important;
        height: 6px !important;
        background: #1f2833 !important;
        border: 1px solid #45a29e !important;
        border-radius: 3px !important;
        outline: none !important;
        cursor: pointer !important;
        margin: 6px 0 !important;
    }
    input[type=range]::-webkit-slider-thumb {
        -webkit-appearance: none !important;
        width: 14px !important;
        height: 14px !important;
        border-radius: 50% !important;
        background: #66fcf1 !important;
        cursor: pointer !important;
        box-shadow: 0 0 8px rgba(102, 252, 241, 0.8) !important;
    }
    input[type=range][disabled] {
        opacity: 0.35 !important;
        cursor: not-allowed !important;
    }

    /* ── Panel przycisków ── */
    #control-buttons {
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
        padding: 10px 28px !important;
        margin: 0 !important;
        font-size: 14px !important;
        font-weight: bold;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    button:hover:not([disabled]) {
        background-color: #45a29e !important;
        color: #0b0c10 !important;
        box-shadow: 0px 0px 15px #66fcf1;
        transform: translateY(-2px);
    }

    button[disabled] {
        opacity: 0.35 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }

    /* Przycisk Launch — pulsujący efekt */
    #control-buttons button:first-child:not([disabled]) {
        background-color: #0d3b2e !important;
        border-color: #66fcf1 !important;
        animation: pulse-glow 1.6s ease-in-out infinite;
    }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 8px rgba(102, 252, 241, 0.3); }
        50%       { box-shadow: 0 0 22px rgba(102, 252, 241, 0.75); }
    }

    /* Panel telemetrii */
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
        width: 290px !important;
        pointer-events: none !important;
    }
    .telemetry-row {
        margin-bottom: 8px !important;
        display: flex !important;
        justify-content: space-between !important;
    }
    .telemetry-row:last-child { margin-bottom: 0 !important; }
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
<script>
    (function() {
        function organizeLayout() {
            var panel = $("#slider-panel");
            if (panel.length) {
                var siblings = panel.nextAll();
                // We expect at least 6 widgets (3 labels + 3 sliders) to exist
                if (siblings.length >= 6) {
                    var w1 = siblings.eq(0);
                    var s1 = siblings.eq(1);
                    var w2 = siblings.eq(2);
                    var s2 = siblings.eq(3);
                    var w3 = siblings.eq(4);
                    var s3 = siblings.eq(5);

                    var c1 = $('<div class="param-container"></div>');
                    var h1 = $('<div class="param-header"><span class="param-label">Prędkość wyjściowa:</span></div>').append(w1);
                    c1.append(h1, s1);

                    var c2 = $('<div class="param-container"></div>');
                    var h2 = $('<div class="param-header"><span class="param-label">Kat startu statku:</span></div>').append(w2);
                    c2.append(h2, s2);

                    var c3 = $('<div class="param-container"></div>');
                    var h3 = $('<div class="param-header"><span class="param-label">Pozycja Ksiezyca:</span></div>').append(w3);
                    c3.append(h3, s3);

                    panel.append(c1, c2, c3);
                    
                    var controls = $("#control-buttons");
                    if (controls.length) {
                        var buttons = controls.nextAll("button");
                        controls.append(buttons);
                    }
                    
                    clearInterval(layoutInterval);
                }
            }
        }
        var layoutInterval = setInterval(organizeLayout, 50);
        setTimeout(function() { clearInterval(layoutInterval); }, 5000);
    })();
</script>
"""

# ── Stałe fizyczne ────────────────────────────────────────────
G       = 6.674e-11
M_EARTH = 5.972e24
M_MOON  = 7.342e22
R_EARTH = 6.371e6
R_MOON  = 1.737e6
D_EM    = 384_400e3

V_MOON  = math.sqrt(G * M_EARTH / D_EM)        # ~1022 m/s
R_PARK  = R_EARTH + 185_000
V_PARK  = math.sqrt(G * M_EARTH / R_PARK)       # ~7796 m/s

# ── Parametry misji (modyfikowane przez slidery) ──────────────
V_TLI    = V_PARK + 3150                         # ~10946 m/s
SHIP_ANG = math.radians(120)
MOON_ANG = math.radians(244)

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

# ── Skala wizualna ────────────────────────────────────────────
SCALE   = 1.0 / 1.4e6
R_E_VIS = 4.5
R_M_VIS = 2.5
R_S_VIS = 0.5

def sv(pos_m):
    return vector(pos_m.x * SCALE, pos_m.y * SCALE, pos_m.z * SCALE)

# ── Scena ─────────────────────────────────────────────────────
scene = canvas(
    title      = STYLES,
    width      = 2100,
    height     = 900,
    background = color.black,
    range      = D_EM * SCALE * 0.40,
)

CAM_ROT_ANG   = math.radians(120)
scene.camera.up = rotate(vector(0, 1, 0), angle=CAM_ROT_ANG, axis=vector(0, 0, 1))
screen_left   = rotate(vector(-1, 0, 0), angle=CAM_ROT_ANG, axis=vector(0, 0, 1))
CAMERA_OFFSET = 120.0
scene.center  = vector(0, 0, 0) + screen_left * CAMERA_OFFSET

# ── Ziemia ────────────────────────────────────────────────────
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

# ── Księżyc ───────────────────────────────────────────────────
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

# Orbita Księżyca (linia pomocnicza)
moon_orbit = curve(color=color.gray(0.4), radius=0.5)
for i in range(201):
    ang = 2 * math.pi * i / 200
    moon_orbit.append(vector(D_EM * SCALE * math.cos(ang),
                             D_EM * SCALE * math.sin(ang), 0))

# ── Statek ────────────────────────────────────────────────────
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

# ── Stan symulacji ────────────────────────────────────────────
pos_ship, vel_ship, pos_moon, vel_moon = init_state()
t        = 0.0
dt       = 30.0
SPEED    = 1200
paused   = True    # Czeka na naciśnięcie Launch
launched = False   # Czy misja wystartowała
done     = False

# ── Fizyka ────────────────────────────────────────────────────
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

def rk4(ps, vs, pm, h):
    def a(p): return accel_ship(p, pm)
    k1v = a(ps);                      k1p = vs
    k2v = a(ps + 0.5*h*k1p);        k2p = vs + 0.5*h*k1v
    k3v = a(ps + 0.5*h*k2p);        k3p = vs + 0.5*h*k2v
    k4v = a(ps +     h*k3p);        k4p = vs +     h*k3v
    new_ps = ps + (h/6) * (k1p + 2*k2p + 2*k3p + k4p)
    new_vs = vs + (h/6) * (k1v + 2*k2v + 2*k3v + k4v)
    return new_ps, new_vs

def euler_moon(pm, vm, h):
    a   = accel_moon(pm)
    vm2 = vm + a * h
    pm2 = pm + vm2 * h
    return pm2, vm2

# ── Helper: odśwież pozycję wg aktualnych parametrów ─────────
def apply_initial_state():
    global pos_ship, vel_ship, pos_moon, vel_moon, t, done
    pos_ship, vel_ship, pos_moon, vel_moon = init_state()
    t = 0.0
    done = False
    ship.clear_trail()
    ship.pos = sv(pos_ship)
    moon.pos = sv(pos_moon)
    ship_label.pos = ship.pos
    moon_label.pos = moon.pos

# ── Callbacki sliderów ────────────────────────────────────────
def on_tli_slider(s):
    global V_TLI
    V_TLI = s.value
    lbl_tli.text = f'{V_TLI - V_PARK:+.0f} m/s'
    if not launched:
        apply_initial_state()

def on_ship_ang_slider(s):
    global SHIP_ANG
    SHIP_ANG = math.radians(s.value)
    lbl_ship_ang.text = f'{s.value:.0f} deg'
    if not launched:
        apply_initial_state()

def on_moon_ang_slider(s):
    global MOON_ANG
    MOON_ANG = math.radians(s.value)
    lbl_moon_ang.text = f'{s.value:.0f} deg'
    if not launched:
        apply_initial_state()

# ── Callbacki przycisków ──────────────────────────────────────
def on_launch(b):
    global launched, paused
    launched = True
    paused   = False
    b.disabled       = True
    b.text           = 'Launched'
    btn_pause.disabled = False
    
    # Blokowanie sliderów po starcie
    sl_tli.disabled = True
    sl_ship_ang.disabled = True
    sl_moon_ang.disabled = True

def on_pause(b):
    global paused
    if not launched:
        return
    paused  = not paused
    b.text  = 'Resume' if paused else 'Pause'

def on_reset(b):
    global pos_ship, vel_ship, pos_moon, vel_moon, t, done, launched, paused
    global V_TLI, SHIP_ANG, MOON_ANG
    
    # Przywrócenie domyślnych wartości parametrów misji
    V_TLI    = V_PARK + 3150
    SHIP_ANG = math.radians(120)
    MOON_ANG = math.radians(244)
    
    # Resetowanie wartości widgetów suwaków
    sl_tli.value = V_TLI
    sl_ship_ang.value = 120
    sl_moon_ang.value = 244
    
    # Resetowanie tekstu etykiet suwaków
    lbl_tli.text = f'{V_TLI - V_PARK:+.0f} m/s'
    lbl_ship_ang.text = '120 deg'
    lbl_moon_ang.text = '244 deg'
    
    launched = False
    paused   = True
    apply_initial_state()
    btn_launch.disabled = False
    btn_launch.text     = 'Launch Mission'
    btn_pause.disabled  = True
    btn_pause.text      = 'Pause'
    
    # Odblokowanie sliderów po resecie
    sl_tli.disabled = False
    sl_ship_ang.disabled = False
    sl_moon_ang.disabled = False

def on_faster(b):
    global SPEED
    SPEED = min(SPEED * 2, 76800)

def on_slower(b):
    global SPEED
    SPEED = max(SPEED // 2, 60)

# ── Panel sliderów ────────────────────────────────────────────
scene.append_to_caption('<div id="slider-panel"></div>')

lbl_tli = wtext(text=f'{V_TLI - V_PARK:+.0f} m/s')
sl_tli = slider(
    min=V_PARK + 2500, max=V_PARK + 3800,
    value=V_TLI, step=10, length=260,
    bind=on_tli_slider
)

lbl_ship_ang = wtext(text=f'{math.degrees(SHIP_ANG):.0f} deg')
sl_ship_ang = slider(
    min=0, max=360,
    value=math.degrees(SHIP_ANG), step=1, length=260,
    bind=on_ship_ang_slider
)

lbl_moon_ang = wtext(text=f'{math.degrees(MOON_ANG):.0f} deg')
sl_moon_ang = slider(
    min=0, max=360,
    value=math.degrees(MOON_ANG), step=1, length=260,
    bind=on_moon_ang_slider
)

# ── Przyciski sterowania ──────────────────────────────────────
scene.append_to_caption('<div id="control-buttons"></div>')
btn_launch = button(text='Launch Mission', bind=on_launch)
btn_pause  = button(text='Pause',          bind=on_pause)
btn_pause.disabled = True
button(text='Reset',  bind=on_reset)
button(text='Faster', bind=on_faster)
button(text='Slower', bind=on_slower)

# ── Panel Telemetrii ──────────────────────────────────────────
telemetry_hud = wtext(text="")

# ── Główna pętla ──────────────────────────────────────────────
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

        ship_label.pos = ship.pos
        moon_label.pos = moon.pos

        earth.rotate(angle=0.001, axis=vector(0, 0, 1))

        if t / 86400 > 0.5 and mag(pos_ship) < R_EARTH * 1.3:
            done = True

        if t / 86400 > 13:
            done = True

    # ── Aktualizacja HUD telemetrii ───────────────────────────
    days    = int(t // 86400)
    hours   = int((t % 86400) // 3600)
    minutes = int((t % 3600) // 60)
    seconds = int(t % 60)

    dist_e = mag(pos_ship)
    alt_e  = max(0.0, (dist_e - R_EARTH) / 1000.0)
    vel_e  = mag(vel_ship) / 1000.0

    dist_m = mag(pos_ship - pos_moon)
    alt_m  = max(0.0, (dist_m - R_MOON) / 1000.0)
    vel_m  = mag(vel_ship - vel_moon) / 1000.0

    if not launched:
        status_color = '#f2a90b'
        status_text  = 'AWAITING LAUNCH'
    elif done:
        status_color = '#e83f3f'
        status_text  = 'MISSION COMPLETE'
    elif paused:
        status_color = '#c5c6c7'
        status_text  = 'PAUSED'
    else:
        status_color = '#66fcf1'
        status_text  = 'IN FLIGHT'

    telemetry_hud.text = f"""
    <div class='telemetry-panel'>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Status:</span>
            <span class='telemetry-val' style='color:{status_color}'>{status_text}</span>
        </div>
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
