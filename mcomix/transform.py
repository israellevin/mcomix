""" A series of a few simple linear transforms. """

from functools import reduce

class Transform(object): # 2D only

    @staticmethod
    def from_rotation(deg):
        if deg == 0:
            return Transform.ID
        if deg == 90:
            return Transform.ROT90
        if deg == 180:
            return Transform.ROT180
        if deg == 270:
            return Transform.ROT270
        raise ValueError("illegal rotation angle: " + str(deg))

    @staticmethod
    def from_scales(s0, s1):
        if s0 == 0 or s1 == 0:
            raise ValueError("illegal scaling factor(s): " + str((s0, s1)))
        return Transform(s0, 0, 0, s1)

    @staticmethod
    def from_flips(f0, f1):
        if (f0, f1) == (False, False):
            return Transform.ID
        if (f0, f1) == (True, False):
            return Transform.INVX
        if (f0, f1) == (False, True):
            return Transform.INVY
        if (f0, f1) == (True, True):
            return Transform.ROT180
        raise ValueError("illegal flips: " + str((f0, f1)))

    @staticmethod
    def from_image_transforms(t):
        return Transform.from_scales(*t[0]).and_then_all(
            Transform.from_rotation(t[1]), Transform.from_flips(*t[2]))

    def __init__(self, *matrix):
        """ Creates a new transform described by a row-major matrix. Note that
        the current implementation does not support arbitrary matrices. Instead,
        one should use one of the eight predefined matrices or one of the
        constructor-like functions. """
        self.m = matrix

    def __str__(self):
        return str(self.m)

    def and_then(self, next_transform):
        """ Returns a new matrix describing the current transform followed by
        next_transform. """
        dp = lambda i11, i21, i12, i22: next_transform.m[i11] * self.m[i21] + \
            next_transform.m[i12] * self.m[i22]
        return Transform(
            dp(0, 0, 1, 2),
            dp(0, 1, 1, 3),
            dp(2, 0, 3, 2),
            dp(2, 1, 3, 3)
        )

    def and_then_all(self, *next_transforms):
        """ Returns a new matrix describing the current transform followed by
        each of the transforms in next_transforms in the order given. """
        return reduce(Transform.and_then, next_transforms, self)

    def swaps_axes(self):
        """ Determines whether this transform includes a transpose of the axes. """
        return self.m[0] == 0

    def to_image_transforms(self):
        """ Decomposes the transform to a sequence of hints to basic transform
        instructions typically found in image processing libraries. The sequence
        will refer to the positive scaling factors to be applied for each axis
        first, followed by at most one rotation, and finally followed by at most
        one flip.
        @return a tuple (s, r, f) where s is a sequence of positive scaling
        factors for the corresponding axes, r is one of (0, 90, 180, 270),
        referring to the clockwise rotation to be applied, and f is a sequence
        of bools where True refers to the corresponding axis to be flipped. """
        s = tuple(map(lambda i, j: abs(self.m[i] + self.m[j]), (0, 1), (2, 3)))
        r, f0 = (90, True) if self.swaps_axes() else (0, False)
        f1 = self.m[2] < 0 or self.m[3] < 0
        f0 ^= self.m[0] < 0 or self.m[1] < 0
        if f0 and f1:
            f0, f1 = False, False
            r += 180
        if f0 and r == 90:
            # Try to avoid horizontal flips because they tend to be slow, given
            # a certain combination of hardware, memory layout and libraries.
            f0, f1 = False, True
            r = 270
        return (s, r, (f0, f1))

Transform.ID = Transform(1, 0, 0, 1)
Transform.ROT90 = Transform(0, -1, 1, 0)
Transform.ROT180 = Transform(-1, 0, 0, -1)
Transform.ROT270 = Transform(0, 1, -1, 0)
Transform.INVX = Transform(-1, 0, 0, 1)
Transform.INVY = Transform(1, 0, 0, -1)
Transform.TRP = Transform(0, 1, 1, 0)
Transform.TRPINV = Transform(0, -1, -1, 0)


# vim: expandtab:sw=4:ts=4
