from typing import Union
from pathlib import Path

import pymc3 as pm
import numpy as np
import pandas as pd


class Image:
    def __init__(
            self,
            title: str,
            image: np.ndarray,
    ):
        self.title = title
        self.image = image


class GCP:
    def __init__(
            self,
            gcp: pd.DataFrame,
    ):
        self.gcp = gcp


class Wld:
    def __init__(
            self,
            wld: np.ndarray,
    ):
        self.wld = wld

    def to_wld(
            self,
            path: Path,
    ):
        path = path / f'{self.name}.{self.suffix}.wld'
        txt = '\n'.join(self.wld)
        path.write_text(txt)


class Region:
    def __init__(
            self,
            name: str,
            bbox: tuple,
            beta: Union[None, np.ndarray],
            wld: Union[None, Wld],
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
            image: np.ndarray,
            gcp: pd.DataFrame,
    ):
        image_ = Image(name, image)
        gcp = GCP(gcp)
        bbox = 0, 0, image.shape[2], image.shape[1]
        return cls(
            name=name,
            image=image_,
            gcp=gcp,
            bbox=bbox,
            beta=None,
            wld=None,
        )

    def to_map(self):
        pass


if __name__ == '__main__':
    pass
