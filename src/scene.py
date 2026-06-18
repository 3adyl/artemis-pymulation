import math

from vpython import canvas, sphere, label, curve, vector, rotate, color, \
    textures

from config import D_EM, SCALE, R_E_VIS, R_M_VIS, R_S_VIS, CAM_ROT_ANG, \
    CAMERA_OFFSET
from styles import STYLES


def setup_scene():
    """Initialize the 3D scene"""
    scene = canvas(
        title=STYLES,
        width=2100,
        height=900,
        background=color.black,
        range=D_EM * SCALE * 0.40,
    )

    scene.camera.up = rotate(vector(0, 1, 0), angle=CAM_ROT_ANG,
                             axis=vector(0, 0, 1))
    screen_left = rotate(vector(-1, 0, 0), angle=CAM_ROT_ANG,
                         axis=vector(0, 0, 1))
    scene.center = vector(0, 0, 0) + screen_left * CAMERA_OFFSET

    return scene


def setup_earth():
    """Create Earth sphere and label"""
    earth = sphere(
        pos=vector(0, 0, 0),
        radius=R_E_VIS,
        texture=textures.earth,
        axis=vector(1, 0, 0),
        up=vector(0, 0, 1)
    )
    earth_label = label(
        pos=earth.pos,
        text='Earth',
        height=20,
        color=color.green,
        box=False,
        line=False,
        opacity=0,
        yoffset=-5,
        xoffset=30
    )
    return earth, earth_label


def setup_moon(pm_scaled):
    """Create Moon sphere, label, and orbit"""
    moon = sphere(
        pos=pm_scaled,
        radius=R_M_VIS,
        color=color.gray(0.65),
    )
    moon_label = label(
        pos=moon.pos,
        text='Moon',
        height=20,
        color=color.white,
        box=False,
        line=False,
        opacity=0,
        yoffset=20
    )

    moon_orbit = curve(color=color.gray(0.4), radius=0.5)
    for i in range(201):
        ang = 2 * math.pi * i / 200
        moon_orbit.append(vector(D_EM * SCALE * math.cos(ang),
                                 D_EM * SCALE * math.sin(ang), 0))

    return moon, moon_label, moon_orbit


def setup_ship(ps_scaled):
    """Create spacecraft sphere and label"""
    ship = sphere(
        pos=ps_scaled,
        radius=R_S_VIS,
        color=color.yellow,
        emissive=True,
        make_trail=True,
        trail_type='curve',
        trail_color=color.orange,
        trail_radius=0.5,
        retain=12000,
    )
    ship_label = label(
        pos=ship.pos,
        text='Integrity',
        height=20,
        color=color.yellow,
        box=False,
        line=False,
        opacity=0,
        yoffset=15
    )
    return ship, ship_label
