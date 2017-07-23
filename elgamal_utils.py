import random
from utils import modular_exponentiation, modinv, square_root_mod

def MAX_ENC(p):
	return (p-1)//2

MAX_MESSAGE_LENGTH = 128

def elgamal_enc(p, q, g, pk, m):
	encoded = encode_message(m, p)
	r = random.randint(2, q-1)
	a = modular_exponentiation(g, r, p)
	b = (modular_exponentiation(pk, r, p) * encoded) % p
	return (a, b)

def elgamal_dec(p, q, g, sk, c):
	a = c[0]
	b = c[1]
	m = (modinv(modular_exponentiation(a, sk, p), p) * b) % p
	return decode_message(m, p)

def encrypt_string(p, q, g, pk, m):
	blocks = get_blocks(m, MAX_MESSAGE_LENGTH)
	c = []
	for block in blocks:
		c.append(elgamal_enc(p, q, g, pk, block))
	return c

def decrypt_string(p, q, g, sk, ciphertexts):
	m = []
	for c in ciphertexts:
		m.append(elgamal_dec(p, q, g, sk, c))
	return ''.join(m)

def encode_message(m, p):
	assert len(m) <= MAX_MESSAGE_LENGTH
	bytes = m.encode('ascii')
	number = 0
	exp = 1
	for b in bytes:
		number = number + (ord(b) * exp)
		exp = exp * 128
	assert number < MAX_ENC(p)
	return (number*number) % p

def decode_message(number, p):
	n = square_root_mod(number, p)
	# if there are two roots, use the one that is less than (p-1)/2
	if n > MAX_ENC(p):
		n = (-n) % p
	number = n
	bytes = []
	while number > 0:
		b = number % 128
		number = number - b
		number = number // 128
		bytes.append(chr(b))
	return "".join(bytes)

def get_blocks(string, length):
	return list((string[0+i:length+i] for i in range(0, len(string), length)))

