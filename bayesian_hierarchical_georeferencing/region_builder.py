from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

from bayesian_hierarchical_georeferencing.region import Raster, GCP, Wld, Region


def gcp_in_bbox(
        bbox: tuple,
        gcp_data: pd.DataFrame,
):
    x_min, y_max, x_max, y_min = bbox
    in_box = [
        r for r in gcp_data.itertuples()
        if ((x_min <= r.pixelX <= x_max) and (y_min <= r.pixelY <= y_max))
    ]
    return pd.DataFrame(in_box)


class RegionBuilder:
    def __init__(
            self,
            full_map: Region,
            regions: pd.DataFrame,
            path: Path,
    ):
        self.full_map = full_map
        self.region_data = regions
        self.regions = None
        self.path = path

    def split_map(self):
        self.regions = []

        for reg in self.region_data.itertuples():
            r, c, _ = self.full_map.raster.data.shape
            bbox = int(reg.x1), int(-reg.y1), int(reg.x2), int(-reg.y2)
            print(bbox)
            if not all((
                    0 <= bbox[0] <= c,
                    0 <= bbox[2] <= c,
                    0 <= bbox[1] <= r,
                    0 <= bbox[3] <= r,
            )):
                raise ValueError('Incorrect region bounds')

            # cropped = self.full_map.raster.image.copy().crop(bbox)
            cropped = self.full_map.raster.data[bbox[1]: bbox[3], bbox[0]: bbox[2]]
            plt.imshow(cropped)
            plt.show()
            #Tähän asti ok
            raster = Raster(
                name=reg.name,
                suffix=self.full_map.raster.suffix,
                image=cropped,
            )
            gcp = GCP(
                name=reg.name,
                suffix=self.full_map.raster.suffix,
                gcp=gcp_in_bbox(
                    bbox,
                    self.full_map.gcp.gcp,
                ),
            )
            wld = Wld(
                reg.name,
                self.full_map.raster.suffix,
                None,
            )
            region = Region(
                name=reg.name,
                bbox=bbox,
                raster=raster,
                wld=wld,
                beta=None,
                gcp=gcp,
            )
            self.regions.append(region)

        self.save_regions()

    def save_regions(self):
        for reg in self.regions:
            reg.to_map(self.path)

    def apply_bhg(self):
        pass

    def save_transform(self):
        pass


if __name__ == '__main__':
    pass
