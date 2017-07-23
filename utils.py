import random

# from http://www.math.umn.edu/~garrett/crypto/Code/FastPow_Python.html
def modular_exponentiation(x, e, m):
	X = x
	E = e
	Y = 1
	while E > 0:
		if E % 2 == 0:
				X = (X * X) % m
				E = E//2
		else:
				Y = (X * Y) % m
				E = E - 1
	return Y % m

# from wikibooks
def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)

# from wikibooks
def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('modular inverse does not exist')
	else:
		return x % m

# according to https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm
def square_root_mod(n, p):
	# assert n is quadratic residue
	assert modular_exponentiation(n, (p-1)//2, p) == 1
	if (p % 4) == 3:
		return modular_exponentiation(n, (p+1)/4, p)
	else:
		Q = p - 1
		S = 0
		while Q % 2 == 0:
			Q = Q // 2
			S = S + 1
		# p-1 = 2^S * Q, Q odd
		while True:
			z = random.randint(2, p-1)
			# find quadratic non-residue
			if modular_exponentiation(z, (p-1)//2, p) == (-1) % p:
				break
		# z is quadratic non-residue
		
		R = modular_exponentiation(n, (Q+1)//2, p)
		c = modular_exponentiation(z, Q, p)
		t = modular_exponentiation(n, Q, p)
		M = S
		while t != 1:
			i = 1
			while i < M:
				if modular_exponentiation(t, 2**i, p) == 1:
					break
				i = i + 1
			b = modular_exponentiation(c, 2**(M-i-1), p)
			R = (R * b) % p
			c = (b * b) % p
			t = (t * b * b) % p
			M = i
		return R





