from PIL import Image, ImageEnhance
from trail_maker import sample_many
from scipy.stats import binom, uniform, norm, rv_discrete

nombre = "semilla.png"

# Abrir las imágenes

imagen = Image.open(nombre).resize((100,100))

def apply_specs(enhancer, spec):    
    if spec["ocupation"] == 0:
        return Image.new("RGBA", (1,1), (0,0,0,0))
    image = enhancer.enhance(spec["intensity"])
    image = image.resize((int(spec["size"]), int(spec["size"])))
    image = image.rotate(spec["rotation"])
    return image

specs = sample_many(
            N = 100,             
            ocupation_dist=binom(n=1, p=1),
            variety_dist=rv_discrete(values=([0, 1, 2], [1 / 3, 1 / 3, 1 / 3])),
            intensities=[
                norm(loc=0.5, scale=0.25)
                for i in range(3)
                ],
            size_dist=uniform(loc=15, scale=5),
            rotation_dist=uniform(scale=360),)

imagenes = [apply_specs(ImageEnhance.Brightness(imagen), spec) for index, spec in specs.iterrows()]

# Configurar separación entre templates (en píxeles)
espacio = 50  

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