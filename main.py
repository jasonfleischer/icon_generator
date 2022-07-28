from PIL import Image, ImageDraw
from pathlib import Path
import cairosvg
import shutil
import os

def main():
	changeToWorkingDirectory()

	output_dir = "output"
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	res_directory = "res/svg"
	for filename in os.listdir(res_directory):
		f = os.path.join(res_directory, filename)
		if os.path.isfile(f) and filename.endswith('.svg'):
			generateImages(f, Path(f).stem, output_dir)

def generateImages(path, filename, output_dir):
	output_dir = output_dir+"/"+filename
	if os.path.exists(output_dir):
		shutil.rmtree(output_dir)
	os.mkdir(output_dir)

	sizes = [152, 180, 192, 512]
	for size in sizes:
		generateImage(path, filename, size, output_dir)
	print("	"+filename)

def generateImage(path, filename, size, output_dir, bg_color=(80, 80, 80)):
	padding = int(size*.18)
	image_size = int(size-padding*2)
	svg_img = convertSVGToImg(path, image_size)
	img = Image.new('RGB', (size,size), color=bg_color)
	img.paste(svg_img, (padding,padding), svg_img)
	img = addCornersToImage(img, int(size*.13))
	img.save(output_dir+"/"+str(size)+".png", "PNG")

def convertSVGToImg(path, size):
	output_path = 'temp_file.png'
	cairosvg.svg2png(url=path, write_to=output_path, output_width=size, output_height=size )
	img = Image.open(output_path)
	os.remove(output_path)
	return img

def addCornersToImage(img, rad):
	circle = Image.new('L', (rad * 2, rad * 2), 0)
	draw = ImageDraw.Draw(circle)
	draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
	alpha = Image.new('L', img.size, 255)
	w, h = img.size
	alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
	alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
	alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
	alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
	img.putalpha(alpha)
	return img

def changeToWorkingDirectory():
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)

print("CREATING IMGS:")
main()
print("FINISHED")
