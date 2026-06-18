import math

from vpython import rate, wtext, slider, button, vector

from config import V_PARK, V_TLI, SHIP_ANG, MOON_ANG, DT, SCALE
from controls import Controls
from scene import setup_scene, setup_earth, setup_moon, setup_ship
from simulation import Simulation
from telemetry import format_telemetry


def sv(pos_m):
    """Scale vector for visualization"""
    return vector(pos_m.x * SCALE, pos_m.y * SCALE, pos_m.z * SCALE)


def main():
    # Simulation and scene setup
    sim = Simulation()
    scene = setup_scene()

    # Create celestial bodies and spacecraft
    earth, earth_label = setup_earth()
    ps0, _, pm0, _ = sim.pos_ship, sim.vel_ship, sim.pos_moon, sim.vel_moon
    moon, moon_label, _ = setup_moon(sv(pm0))
    ship, ship_label = setup_ship(sv(ps0))

    # controls
    controls = Controls(sim, scene, {}, {}, {})

    # sliders panel
    scene.append_to_caption('<div id="slider-panel"></div>')

    lbl_tli = wtext(text=f'{V_TLI - V_PARK:+.0f} m/s')
    sl_tli = slider(min=V_PARK + 2500, max=V_PARK + 3800, value=V_TLI, step=10,
                    length=260, bind=controls.on_tli_slider)

    lbl_ship_ang = wtext(text=f'{math.degrees(SHIP_ANG):.0f} deg')
    sl_ship_ang = slider(min=0, max=360, value=math.degrees(SHIP_ANG), step=1,
                         length=260, bind=controls.on_ship_ang_slider)

    lbl_moon_ang = wtext(text=f'{math.degrees(MOON_ANG):.0f} deg')
    sl_moon_ang = slider(min=0, max=360, value=math.degrees(MOON_ANG), step=1,
                         length=260, bind=controls.on_moon_ang_slider)

    # buttons
    scene.append_to_caption('<div id="control-buttons"></div>')
    btn_launch = button(text='Launch Mission', bind=controls.on_launch)
    btn_pause = button(text='Pause', disabled=True, bind=controls.on_pause)
    btn_reset = button(text='Reset', bind=controls.on_reset)
    btn_faster = button(text='Faster', bind=controls.on_faster)
    btn_slower = button(text='Slower', bind=controls.on_slower)

    # telemetry
    telemetry_hud = wtext(text="")

    # populate controls
    controls.labels = {'tli': lbl_tli, 'ship_ang': lbl_ship_ang,
                       'moon_ang': lbl_moon_ang}
    controls.sliders = {'tli': sl_tli, 'ship_ang': sl_ship_ang,
                        'moon_ang': sl_moon_ang}
    controls.buttons = {'launch': btn_launch, 'pause': btn_pause}

    def apply_initial_state():
        sim.reset(V_TLI=sim.V_TLI, SHIP_ANG=sim.SHIP_ANG, MOON_ANG=sim.MOON_ANG)
        ship.clear_trail()
        ship.pos = sv(sim.pos_ship)
        moon.pos = sv(sim.pos_moon)
        ship_label.pos = ship.pos
        moon_label.pos = moon.pos

    controls.set_apply_initial_state_callback(apply_initial_state)

    # Main loop
    while True:
        rate(60)

        if not (controls.paused or sim.done):
            steps = max(1, int(controls.SPEED / DT / 60))
            sim.step(DT, num_steps=steps)

            ship.pos = sv(sim.pos_ship)
            moon.pos = sv(sim.pos_moon)
            ship_label.pos = ship.pos
            moon_label.pos = moon.pos
            earth.rotate(angle=0.001, axis=vector(0, 0, 1))

        telemetry_data = sim.get_telemetry()
        telemetry_hud.text = format_telemetry(telemetry_data, controls.launched,
                                              sim.done, controls.paused)


if __name__ == "__main__":
    main()
