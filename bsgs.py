from math import sqrt, ceil
from utils import square_root_mod as sqrtm
from utils import modular_exponentiation as me
from utils import modinv


def bsgs(h, g, order, p):
    """
    Baby-Step-Giant-Step algorithm
    :param h: g^a
    :param g: g
    :param order: order of the group
    :return: a
    """

    max_list_size = 50000000
    m = min(sqrtm(order, p), max_list_size)  # list size
    m_giant = order // m + 1
    l = {}

    # baby steps
    power = 1
    for i in range(m + 1):
        if i > 0:
            # faster than calling me every iteration
            power *= g
            power %= p
        l[power] = i

    # giant steps
    # g^(-j*m) = (g^-m)^j
    gminv = modinv(me(g, m, p) % p, p)
    gminv_j = gminv
    power = 1
    for j in range(m_giant + 1):
        if j > 0:
            # faster than calling me every iteration
            power *= gminv_j
            power %= p

        z = (power * h) % p
        if z in l:
            # found!
            i = l[z]
            a = (i + j * m) % order
            return a

    # not found
    return None
