from typing import List, NamedTuple

from numpy import ndarray

from .cvwrapper import Mat, MatBW


class AnyType:
    pass


class _RangeBaseType:
    __slots__ = ("min", "max", "decimal")

    def __init__(self, min, max, *, decimal=True):
        self.decimal = bool(decimal)

        self.min = self._convert(min)
        self.max = self._convert(max)

    def _convert(self, val):
        return float(val) if self.decimal else int(round(val))

    def in_range(self, val):
        return self.min <= self._convert(val) <= self.max

    def ensure_in_range(self, val, name):
        if not self.in_range(val):
            raise ValueError(
                f"Parameter {name} is out of range ({self.min}, {self.max}) with value {val}"
            )

        return self._convert(val)

    def serialize(self):
        return {key: getattr(self, key) for key in self.__slots__}


class Slide(_RangeBaseType):
    def create(self, val):
        return self.ensure_in_range(val, "val")


class Range(NamedTuple):
    min: float
    max: float


class RangeType(_RangeBaseType):
    def create(self, min, max):
        min = self.ensure_in_range(min, "min")
        max = self.ensure_in_range(max, "max")

        return Range(min, max)


# There's a reason why I'm declaring classes here and not doing simply
# `Mat = ndarray` or `Mat = NewType("Mat", ndarray)`
# ndarray doesn't allow me to differentiate between Mat and MatBW
# NewType is some funky object which is hard to parse
# Making new classes allows me to do simple equality testing


class Contour(ndarray):
    pass


class Contours(List[Contour]):
    pass
