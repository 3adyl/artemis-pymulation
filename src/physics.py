from vpython import vector, mag

from config import G, M_EARTH, M_MOON


def accel_ship(ps, pm):
    re = -ps
    rm = pm - ps
    me = mag(re);
    mm = mag(rm)
    if me < 1e3 or mm < 1e3:
        return vector(0, 0, 0)
    return (G * M_EARTH / me ** 3) * re + (G * M_MOON / mm ** 3) * rm


def accel_moon(pm):
    r = -pm
    m = mag(r)
    if m < 1e3:
        return vector(0, 0, 0)
    return (G * M_EARTH / m ** 3) * r


def rk4(ps, vs, pm, h):
    def a(p):
        return accel_ship(p, pm)

    k1v = a(ps)
    k1p = vs

    k2v = a(ps + 0.5 * h * k1p)
    k2p = vs + 0.5 * h * k1v

    k3v = a(ps + 0.5 * h * k2p)
    k3p = vs + 0.5 * h * k2v

    k4v = a(ps + h * k3p)
    k4p = vs + h * k3v

    new_ps = ps + (h / 6) * (k1p + 2 * k2p + 2 * k3p + k4p)
    new_vs = vs + (h / 6) * (k1v + 2 * k2v + 2 * k3v + k4v)

    return new_ps, new_vs


def euler_moon(pm, vm, h):
    a = accel_moon(pm)
    vm2 = vm + a * h
    pm2 = pm + vm2 * h
    return pm2, vm2
