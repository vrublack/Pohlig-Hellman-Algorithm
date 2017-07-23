from utils import modular_exponentiation as me, modinv
from bsgs import bsgs


def pohe(g, h, p, order, factors):
    """
    Pohlig-Hellman-Algorithm
    :param g: 
    :param h: 
    :param p: 
    :param order: 
    :param factors: 
    :return: alpha
    """
    alphas = []

    for p_i, e_i in factors:  # CRT
        p_e = p_i ** e_i  # necessarily < p
        order_i = p_e - 1
        print('Mod {}^{} = {}...'.format(p_i, e_i, p_e))
        # compute all the l
        l = []
        a_i = 0
        for k in range(e_i):  # k is the exponent
            base = me(g, order // p_i, p)
            # compute power (power = base**lk)
            tmp_exp = 0
            for j in range(k):
                tmp_exp += l[j] * p_i ** j
            tmp_base = me(g, order // (p_i ** (k + 1)), p)
            tmp_power = me(tmp_base, tmp_exp, p)
            tmp_power = modinv(tmp_power, p)
            power = (me(h, order // (p_i ** (k + 1)), p) * tmp_power) % p

            # baby-step-giant-step
            lk = bsgs(power, base, order, p) % p_i
            l.append(lk)

            a_i += lk * p_i ** k

            print('\tFound l_{} = {}'.format(k, lk))

        alphas.append(a_i)
        print('alpha for p_i {} = {}'.format(p_i, a_i))

    # reverse CRT: construct alpha from all a_i
    alpha = 0
    for i in range(len(factors)):
        p_i, e_i = factors[i]
        p_e = p_i ** e_i
        product = alphas[i]
        for j in range(len(factors)):
            if j == i:
                continue
            p_e_j = factors[j][0] ** factors[j][1]
            product *= p_e_j * modinv(p_e_j, p_e)
            product %= order
        alpha += product
        alpha %= order

    print('---- Final alpha: {} -----'.format(alpha))
    return alpha
