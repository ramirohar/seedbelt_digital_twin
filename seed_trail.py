from skimage import io as skio, color as skcolor, transform
from spec_generation import sample_many
from spec_generation import apply_specs
from scipy.stats import binom, uniform, norm, rv_discrete
import numpy as np
from PIL import Image

nombre = "semilla.png"

deg_to_px = 640/(5*360)

# Abrir las imágenes
TEMPLATE = skcolor.rgb2gray(skio.imread(nombre)[:, :, :3]) 
TEMPLATE = TEMPLATE * 1  / np.max(TEMPLATE)
TEMPLATE = transform.rescale(TEMPLATE, 0.25)

def main():
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

    imagenes = [Image.fromarray(apply_specs(spec), mode="RGBA") for index, spec in specs.iterrows()]

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

if __name__ == "__main__":
    main()