from skimage import io as skio, color as skcolor, transform
from trail_maker import sample_many
from scipy.stats import binom, uniform, norm, rv_discrete
import numpy as np
from PIL import Image

nombre = "semilla.png"


deg_to_px = 640/(5*360)
# Abrir las imágenes

imagen = Image.open(nombre).resize((100,100))
print(skio.imread(nombre).shape)
TEMPLATE = skcolor.rgb2gray(skio.imread(nombre)[:, :, :3]) 
TEMPLATE = TEMPLATE * 1  / np.max(TEMPLATE)
print(TEMPLATE.shape)
# def apply_specs(enhancer, spec):    
#     if spec["ocupation"] == 0:
#         return Image.new("RGBA", (1,1), (0,0,0,0))
#     image = enhancer.enhance(spec["intensity"])
#     image = image.putalpha(128)
#     image = image.resize((int(spec["size"]), int(spec["size"])))
#     image = image.rotate(spec["rotation"])
#     return image


def apply_specs(spec):
    if spec["ocupation"] == 0:
        return Image.new("RGBA", (1,1), (0,0,0,0))
    im = TEMPLATE
    im = transform.rotate(im, spec["rotation"])
    im = transform.resize(im, (int(spec["size"]), int(spec["size"])))

    fg = im > .1
    bg = np.logical_not(fg)
    
    alpha = np.zeros_like(im)
    alpha[bg] = 0  
    alpha[fg] = min(spec["intensity"], 1)
    out = skcolor.gray2rgba(im, alpha)

    out = Image.fromarray((255 * out).astype(np.uint8), mode="RGBA")    
    return out

specs = sample_many(
            N = 20,             
            ocupation_dist=binom(n=1, p=1),
            variety_dist=rv_discrete(values=([0, 1, 2], [1/2, 1/2, 0])),
            intensities=[
                norm(loc=1, scale=0.01),
                norm(loc=0.3, scale=0.01),
                norm(loc=0, scale=0.1)
                ],
            size_dist=uniform(loc=20, scale=5),
            rotation_dist=uniform(scale=360),)

imagenes = [apply_specs(spec) for index, spec in specs.iterrows()]

# Configurar separación entre templates (en píxeles)
espacio = int(360 * deg_to_px)- 30

# Alto de la imagen final = alto máximo
alto = max(img.height for img in imagenes)

# Ancho total = suma de anchos + espacio entre cada template
ancho_total = sum(img.width for img in imagenes) + espacio * (len(imagenes) - 1)

# Crear imagen nueva grande (fondo transparente)
desfile = Image.new("RGBA", (ancho_total, alto), (0, 0, 0, 0))

# Pegar las templates con espacio
x_offset = 0
for i, img in enumerate(imagenes):
    desfile.paste(img, (x_offset, 0))
    x_offset += img.width + espacio

# Guardar resultado
desfile.save("desfile.png")
print("✅ Imagen armada como desfile.png con espacios")