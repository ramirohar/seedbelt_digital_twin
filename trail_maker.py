from scipy.stats import rv_discrete, rv_continuous
import pandas as pd


def fila(
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
        fila(
            rng,
            ocupation_dist=ocupation_dist,
            variety_dist=variety_dist,
            intensities=intensities,
            size_dist=size_dist,
            rotation_dist=rotation_dist,
        )
        for _ in range(N)
    )
