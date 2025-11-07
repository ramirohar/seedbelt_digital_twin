from scipy.stats import rv_discrete, rv_continuous
from skimage import io as skio, color as skcolor, transform
import numpy as np
import pandas as pd


def sample_single(
    rng=None,
    *,
    ocupation_dist: rv_discrete,
    variety_dist: rv_discrete,
    intensities: list[rv_continuous],
    size_dist: rv_continuous,
    rotation_dist: rv_continuous,
):
    ocupation = ocupation_dist.rvs(random_state=rng)
    variety = variety_dist.rvs(random_state=rng)
    intensity = intensities[variety].rvs(random_state=rng)
    size = size_dist.rvs(random_state=rng)
    rotation = rotation_dist.rvs(random_state=rng)

    return {
        "ocupation": ocupation,
        "variety": variety,
        "intensity": intensity,
        "size": size,
        "rotation": rotation,
    }


def sample_many(
    N: int,
    rng=None,
    *,
    ocupation_dist: rv_discrete,
    variety_dist: rv_discrete,
    intensities: list[rv_continuous],
    size_dist: rv_continuous,
    rotation_dist: rv_continuous,
):
    return pd.DataFrame(
        sample_single(
            rng,
            ocupation_dist=ocupation_dist,
            variety_dist=variety_dist,
            intensities=intensities,
            size_dist=size_dist,
            rotation_dist=rotation_dist,
        )
        for _ in range(N)
    )

def apply_specs(im,spec):
    if spec["ocupation"] == 0:
        pass
    im = transform.rotate(im, spec["rotation"])
    im = transform.resize(im, (int(spec["size"]), int(spec["size"])))

    fg = im > .1
    bg = np.logical_not(fg)
    
    alpha = np.zeros_like(im)
    alpha[bg] = 0  
    alpha[fg] = min(spec["intensity"], 1)
    out = skcolor.gray2rgba(im, alpha)
    out = (255 * out).astype(np.uint8)    
    return out
