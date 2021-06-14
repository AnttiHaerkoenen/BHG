from typing import Union
from pathlib import Path

import matplotlib.pyplot as plt
import pymc3 as pm
import numpy as np
import pandas as pd


class Image:
    def __init__(
            self,
            name: str,
            suffix: str,
            image: np.ndarray,
    ):
        self.name = name
        self.suffix = suffix
        self.image = image

    def save(
            self,
            path: Path,
    ):
        plt.imsave(path / f'{self.name}.{self.suffix}')


class GCP:
    def __init__(
            self,
            name: str,
            suffix: str,
            gcp: pd.DataFrame,
    ):
        self.name = name
        self.suffix = suffix
        self.gcp = gcp

    def save(
            self,
            path: Path,
    ):
        self.gcp.to_csv(path / f'{self.name}.{self.suffix}')


class Wld:
    def __init__(
            self,
            name: str,
            suffix: str,
            wld: Union[np.ndarray, None],
    ):
        self.wld = wld
        self.name = name
        self.suffix = suffix

    def save(
            self,
            path: Path,
    ):
        if self.wld is not None:
            path = path / f'{self.name}.{self.suffix}.wld'
            txt = '\n'.join(list(self.wld))
            path.write_text(txt)


class Region:
    def __init__(
            self,
            name: str,
            bbox: tuple,
            beta: Union[np.ndarray, None],
            wld: Union[Wld, None],
            image: Image,
            gcp: GCP,
    ):
        self.name = name
        self.bbox = bbox
        self.beta = beta
        self.wld = wld
        self.image = image
        self.gcp = gcp

    @classmethod
    def from_map(
            cls,
            name: str,
            suffix: str,
            image: np.ndarray,
            gcp: pd.DataFrame,
    ):
        image_ = Image(
            name=name,
            suffix=suffix,
            image=image,
        )

        gcp = GCP(
            name=name,
            suffix=suffix,
            gcp=gcp,
        )

        bbox = 0, 0, image.shape[2], image.shape[1]

        wld = Wld(
            name=name,
            suffix=suffix,
            wld=None,
        )

        return cls(
            name=name,
            image=image_,
            gcp=gcp,
            bbox=bbox,
            beta=None,
            wld=wld,
        )

    def to_map(
            self,
            path: Path,
    ):
        self.image.save(path)
        self.wld.save(path)
        self.gcp.save(path)


if __name__ == '__main__':
    pass
