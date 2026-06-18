import math

from config import V_PARK


class Controls:
    """Handle UI callbacks and control state"""

    def __init__(self, simulation, scene, labels, sliders, buttons):
        self.sim = simulation
        self.scene = scene
        self.labels = labels  # {'tli': lbl_tli, 'ship_ang': lbl_ship_ang, 'moon_ang': lbl_moon_ang}
        self.sliders = sliders  # {'tli': sl_tli, 'ship_ang': sl_ship_ang, 'moon_ang': sl_moon_ang}
        self.buttons = buttons  # {'launch': btn_launch, 'pause': btn_pause}

        self.launched = False
        self.paused = True
        self.SPEED = 1200

        self.apply_initial_state_callback = None

    def set_apply_initial_state_callback(self, callback):
        """Set callback for apply_initial_state"""
        self.apply_initial_state_callback = callback

    def on_tli_slider(self, s):
        """Handle TLI velocity slider change"""
        self.sim.V_TLI = s.value
        self.labels['tli'].text = f'{self.sim.V_TLI - V_PARK:+.0f} m/s'
        if not self.launched and self.apply_initial_state_callback:
            self.apply_initial_state_callback()

    def on_ship_ang_slider(self, s):
        """Handle ship angle slider change"""
        self.sim.SHIP_ANG = math.radians(s.value)
        self.labels['ship_ang'].text = f'{s.value:.0f} deg'
        if not self.launched and self.apply_initial_state_callback:
            self.apply_initial_state_callback()

    def on_moon_ang_slider(self, s):
        """Handle moon angle slider change"""
        self.sim.MOON_ANG = math.radians(s.value)
        self.labels['moon_ang'].text = f'{s.value:.0f} deg'
        if not self.launched and self.apply_initial_state_callback:
            self.apply_initial_state_callback()

    def on_launch(self, b):
        """Handle launch button"""
        self.launched = True
        self.paused = False
        b.disabled = True
        b.text = 'Launched'
        self.buttons['pause'].disabled = False

        self.sliders['tli'].disabled = True
        self.sliders['ship_ang'].disabled = True
        self.sliders['moon_ang'].disabled = True

    def on_pause(self, b):
        """Handle pause button"""
        if not self.launched:
            return
        self.paused = not self.paused
        b.text = 'Resume' if self.paused else 'Pause'

    def on_reset(self, b):
        """Handle reset button"""
        self.sim.reset(V_TLI=V_PARK + 3150, SHIP_ANG=math.radians(120),
                       MOON_ANG=math.radians(244))

        self.sliders['tli'].value = self.sim.V_TLI
        self.sliders['ship_ang'].value = 120
        self.sliders['moon_ang'].value = 244

        self.labels['tli'].text = f'{self.sim.V_TLI - V_PARK:+.0f} m/s'
        self.labels['ship_ang'].text = '120 deg'
        self.labels['moon_ang'].text = '244 deg'

        self.launched = False
        self.paused = True
        if self.apply_initial_state_callback:
            self.apply_initial_state_callback()

        self.buttons['launch'].disabled = False
        self.buttons['launch'].text = 'Launch Mission'
        self.buttons['pause'].disabled = True
        self.buttons['pause'].text = 'Pause'

        self.sliders['tli'].disabled = False
        self.sliders['ship_ang'].disabled = False
        self.sliders['moon_ang'].disabled = False

    def on_faster(self, b):
        """Handle faster button"""
        self.SPEED = min(self.SPEED * 2, 76800)

    def on_slower(self, b):
        """Handle slower button"""
        self.SPEED = max(self.SPEED // 2, 60)
