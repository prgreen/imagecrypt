from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("base_image", help="path to the (existing) base image")
parser.add_argument("result_image", help="path to the (created) result image")
parser.add_argument("message", help="message in the result image")
parser.add_argument("-v", "--verbose", help="more information on encryption", action="store_true")
args = parser.parse_args()

def zero_out(number, bits):
	return number-number%(2**bits)

MESSAGE = args.message
MESSAGE_COUNT = len(MESSAGE)+1

img = Image.open(args.base_image)
p = img.load()
max_data = img.size[0]*img.size[1]
if args.verbose:
	print "maximum data: ", max_data, " bytes"
	print "message data: ", MESSAGE_COUNT-1, "+1 bytes"
#add extra 0
MESSAGE = MESSAGE + "\0"
MESSAGE_INDEX = 0
for i in range(img.size[0]):
	for j in range(img.size[1]):
		r,g,b = p[i,j]
		if MESSAGE_INDEX < MESSAGE_COUNT:
			if MESSAGE[MESSAGE_INDEX] == "\0":
				p[i,j] = (zero_out(r,3),zero_out(g,2),zero_out(b,3))
			else:
				p[i,j] = (zero_out(r,3)+((ord(MESSAGE[MESSAGE_INDEX]) & 0b11100000)>>5),
					zero_out(g,2)+((ord(MESSAGE[MESSAGE_INDEX]) & 0b00011000)>>3),
					zero_out(b,3)+(ord(MESSAGE[MESSAGE_INDEX]) & 0b00000111))
		else:
			p[i,j]=(r,g,b)
		MESSAGE_INDEX += 1
if MESSAGE_INDEX < MESSAGE_COUNT:
	print "WARNING: only a part of the message was encoded, use a bigger image or a smaller message"
img.save(args.result_image, format="PNG")