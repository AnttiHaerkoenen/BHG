import pandas as pd

from bayesian_hierarchical_georeferencing.region import Image, GCP, Wld, Region


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
    ):
        self.full_map = full_map
        self.region_data = regions
        self.regions = None

    def split_map(self):
        self.regions = []
        for r in self.region_data.itertuples():
            image = Image(
                name=r.name,
                suffix=self.full_map.image.suffix,
                image=self.full_map.image.image[int(r.y2):int(r.y1), int(r.x2):int(r.x1)],
            )
            gcp = GCP(
                name=r.name,
                suffix=self.full_map.image.suffix,
                gcp=gcp_in_bbox(
                    (r.x1, r.y1, r.x2, r.y2),
                    self.full_map.gcp.gcp,
                ),
            )
            region = Region(
                name=r.name,
                bbox=(r.x1, r.y1, r.x2, r.y2),
                image=image,
                wld=None,
                beta=None,
                gcp=gcp,
            )
            self.regions.append(region)
        print(self.regions[0])

    def apply_bhg(self):
        pass

    def save_transform(self):
        pass


if __name__ == '__main__':
    pass
