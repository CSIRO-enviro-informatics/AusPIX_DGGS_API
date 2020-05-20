from auspixdggs.callablemodules.point_DGGSvalue import latlong_to_DGGS
from pyproj import Transformer
import pytest

def test_transform_3577_to_4326():
   epsg_from = "epsg:{}".format(3577)
   epsg_to = "epsg:{}".format(4326)
   transformer = Transformer.from_crs(epsg_from, epsg_to, always_xy=True)
   x = 1549652.93
   y = -3960378.34
   res = transformer.transform(x, y)
   print(res)
   answer = latlong_to_DGGS(res, 7)
   print(answer)
   assert str(answer) == "R7852372"

def test_transform_4326_to_4326():
   epsg_from = "epsg:{}".format(4326)
   epsg_to = "epsg:{}".format(4326)
   transformer = Transformer.from_crs(epsg_from, epsg_to, always_xy=True)
   x = 149.124413
   y = -35.307934
   res = transformer.transform(x, y)
   print(res)
   answer = latlong_to_DGGS(res, 7)
   print(answer)
   assert str(answer) == "R7852372"

if __name__ == "__main__":
   test_transform_3577_to_4326()
   test_transform_4326_to_4326()
