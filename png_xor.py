from PIL import Image

file1 = Image.open('scrambled1.png')
file2 = Image.open('scrambled2.png')

width,height = file1.size

flag = Image.new('RGB', (width, height))

pixels = flag.load()

for x in range(width):
    for y in range(height):
        r = file1.getpixel((x,y))[0] ^ file2.getpixel((x,y))[0]
        g = file1.getpixel((x,y))[1] ^ file2.getpixel((x,y))[1]
        b = file1.getpixel((x,y))[2] ^ file2.getpixel((x,y))[2]

        # if all white then convert to black
        if (r, g, b) == (255, 255, 255):
            (r, g, b) = (0, 0, 0)

        flag.putpixel((x,y), (r,g,b))

flag.save('flag.png','PNG')