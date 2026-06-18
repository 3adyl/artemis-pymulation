import math

from vpython import vector, mag

from config import (
    R_EARTH, R_MOON, D_EM, V_MOON, R_PARK, V_TLI, SHIP_ANG, MOON_ANG
)
from physics import rk4, euler_moon


class Simulation:
    def __init__(self):
        self.V_TLI = V_TLI
        self.SHIP_ANG = SHIP_ANG
        self.MOON_ANG = MOON_ANG

        self.pos_ship = None
        self.vel_ship = None
        self.pos_moon = None
        self.vel_moon = None

        self.t = 0.0
        self.done = False

        self.init_state()

    def init_state(self):
        """Initialize spacecraft and moon positions"""
        ps = vector(R_PARK * math.cos(self.SHIP_ANG),
                    R_PARK * math.sin(self.SHIP_ANG), 0)
        vs = vector(-math.sin(self.SHIP_ANG) * self.V_TLI,
                    math.cos(self.SHIP_ANG) * self.V_TLI, 0)
        pm = vector(D_EM * math.cos(self.MOON_ANG),
                    D_EM * math.sin(self.MOON_ANG), 0)
        vm = vector(-math.sin(self.MOON_ANG) * V_MOON,
                    math.cos(self.MOON_ANG) * V_MOON, 0)

        self.pos_ship = ps
        self.vel_ship = vs
        self.pos_moon = pm
        self.vel_moon = vm

        self.t = 0.0
        self.done = False

    def step(self, dt, num_steps=1):
        """Execute one or more physics steps"""
        for _ in range(num_steps):
            self.pos_moon, self.vel_moon = euler_moon(
                self.pos_moon, self.vel_moon, dt
            )
            self.pos_ship, self.vel_ship = rk4(
                self.pos_ship, self.vel_ship, self.pos_moon, dt
            )
            self.t += dt

        self.check_termination_conditions()

    def check_termination_conditions(self):
        """Check if mission should end"""
        if self.t / 86400 > 0.5 and mag(self.pos_ship) < R_EARTH * 1.3:
            self.done = True

        if self.t / 86400 > 13:
            self.done = True

    def get_telemetry(self):
        """Return telemetry data as dictionary"""
        days = int(self.t // 86400)
        hours = int((self.t % 86400) // 3600)
        minutes = int((self.t % 3600) // 60)
        seconds = int(self.t % 60)

        dist_e = mag(self.pos_ship)
        alt_e = max(0.0, (dist_e - R_EARTH) / 1000.0)
        vel_e = mag(self.vel_ship) / 1000.0

        dist_m = mag(self.pos_ship - self.pos_moon)
        alt_m = max(0.0, (dist_m - R_MOON) / 1000.0)
        vel_m = mag(self.vel_ship - self.vel_moon) / 1000.0

        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'alt_e': alt_e,
            'vel_e': vel_e,
            'alt_m': alt_m,
            'vel_m': vel_m,
            't': self.t,
        }

    def reset(self, V_TLI=None, SHIP_ANG=None, MOON_ANG=None):
        """Reset simulation with new or default parameters"""
        if V_TLI is not None:
            self.V_TLI = V_TLI
        if SHIP_ANG is not None:
            self.SHIP_ANG = SHIP_ANG
        if MOON_ANG is not None:
            self.MOON_ANG = MOON_ANG

        self.init_state()
