from PIL import Image
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("image", help="path to the encrypted image")
parser.add_argument("-v", "--verbose", help="more information on decryption", action="store_true")
args = parser.parse_args()

def get_data(r,g,b):
	return chr(((r&0b00000111)<<5) + ((g&0b00000011)<<3) + (b&0b00000111))


img = Image.open(args.image)
p = img.load()

MESSAGE=""

try:
	for i in range(img.size[0]):
		for j in range(img.size[1]):
			r,g,b = p[i,j]
			c = get_data(r,g,b)
			if c != "\0":
				MESSAGE += c
			else:
				raise Exception
except:
	pass

if args.verbose:
	print "Found",len(MESSAGE),"bytes:"
print MESSAGE
