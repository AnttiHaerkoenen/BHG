from typing import Union, Mapping
from pathlib import Path

from PIL import Image
import numpy as np
import pandas as pd


class Raster:
    def __init__(
            self,
            name: str,
            suffix: str,
            image: Image,
    ):
        self.name = name
        self.suffix = suffix
        self.image = image

    def save(
            self,
            path: Path,
    ):
        format_ = self.suffix if self.suffix != 'jpg' else 'jpeg'
        self.image.save(
            path / f'region_{self.name}.{self.suffix}',
            format=format_,
        )

    @property
    def data(self):
        return np.array(self.image)


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
        self.gcp.to_csv(path / f'region_{self.name}.{self.suffix}.points')


class Projection:
    def __init__(
            self,
            name: str,
            suffix: str,
            wld: Union[Mapping, None],
    ):
        self.wld = wld
        self.name = name
        self.suffix = suffix

    def to_wld(
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
            projection: Projection,
            raster: Raster,
            gcp: GCP,
    ):
        self.name = name
        self.bbox = bbox
        self.beta = beta
        self.projection = projection
        self.raster = raster
        self.gcp = gcp

    @classmethod
    def from_map(
            cls,
            name: str,
            suffix: str,
            image: Image,
            gcp: pd.DataFrame,
    ):
        raster = Raster(
            name=name,
            suffix=suffix,
            image=image,
        )
        gcp = GCP(
            name=name,
            suffix=suffix,
            gcp=gcp,
        )
        bbox = 0, 0, image.size[0], image.size[1]
        projection = Projection(
            name=name,
            suffix=suffix,
            wld=None,
        )

        return cls(
            name=name,
            raster=raster,
            gcp=gcp,
            bbox=bbox,
            beta=None,
            projection=projection,
        )

    def to_map(
            self,
            path: Path,
    ):
        self.raster.save(path)
        self.projection.to_wld(path)
        self.gcp.save(path)

    def __str__(self):
        return f'Region: {self.name}, bounds: {self.bbox}'


if __name__ == '__main__':
    pass
