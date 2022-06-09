# from pprint import pprint as print

import numpy.typing as npt


def det(arr):
    """
    https://numpy.org/doc/stable/reference/arrays.ndarray.html
    https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html
    https://numpy.org/doc/stable/reference/generated/numpy.ndarray.ndim.html
    https://numpy.org/doc/stable/reference/generated/numpy.ndarray.dtype.html
    https://numpy.org/doc/stable/reference/generated/numpy.ndarray.size.html
    """
    print(type(arr))
    print(
        f"\n shape = {arr.shape} \n dimensions = {arr.ndim} \n data type = {arr.dtype} \n size(#elements) = {arr.size} \n total memory size = {arr.size * arr.itemsize}"
    )
