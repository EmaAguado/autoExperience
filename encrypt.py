minus = "abcdefghijklmnopqrstuvwxyz"
mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
longDic = len(minus)

def encode(text, code):
	
	encode = ""

	for letter in text:
		if not letter.isalpha():# or letter.lower() == '':
			encode += letter
			continue

		valueLetter = ord(letter)
		dictType = minus
		limit = 97

		if letter.isupper():
			limit = 65
			dictType = mayus

		position = (valueLetter - limit + code) % longDic

		encode += dictType[position]

	hex_string = encode.encode('utf-8')
	encode = hex_string.hex()

	return encode


def decode(text, code):

	try: text = bytearray.fromhex(text).decode()
	except: pass
	
	decode = ""

	for letter in text:
		if not letter.isalpha():# or letter.lower() == '':
			decode += letter
			continue

		valueLetter = ord(letter)
		dictType = minus
		limit = 97  

		if letter.isupper():
			limit = 65
			dictType = mayus

		position = (valueLetter - limit - code) % longDic

		decode += dictType[position]

	return decode


if __name__ == '__main__':
	
	password = "M12v12c12+"
	key = int("".join([str(ord(char)) for char in password]))
	test_encode = encode(password,10)
	print(test_encode)
	# test_decode = encode("Example","test")