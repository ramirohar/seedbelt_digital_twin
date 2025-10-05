from PIL import Image

img = Image.new("RGB", (width, height), color=(0, 0, 0))

# Draw red borders
draw = ImageDraw.Draw(img)
border_thickness = 10  # pixels
# Rectangle: (left, top, right, bottom)
draw.rectangle(
    [0, 0, width-1, height-1],
    outline=(255, 0, 0),  # red color
    width=border_thickness
)