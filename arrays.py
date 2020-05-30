"""
File : arrays.py

An Abstract Data Type (ADT) for presenting
a collection with fixed size

"""
import datetime
import ctypes
import pandas as pd


class Array(object):

    def __init__(self, length, values=None):
        """
        Constructor for array creates inner collection
        and initialize it with values if provided
        :param length: Size of collection
        :param values: Elements of collection
        """
        assert length > 0, "Length of array must be > 0"
        self._len = length
        py_array = ctypes.py_object * length
        self._values = py_array()
        if values:
            if len(values) > length:
                raise Exception('Income data is too big')
            for i, v in enumerate(values):
                self._values[i] = v
        else:
            self.erase(None)

    def __len__(self):
        """
        :return: the length of array
        """
        return self._len

    def erase(self, stub):
        for i in range(self._len):
            self._values[i] = stub

    def __getitem__(self, index):
        """
        :param index: position of element
        :return: element on position index
        """
        assert 0 <= index < len(self), "Index out of range"
        return self._values[index]

    def __setitem__(self, index, value):
        """
        Set value on position index in collection
        :param index: position of element
        :param value: new value at index
        """
        assert 0 <= index < len(self), "Index out of range"
        self._values[index] = value

    def __iter__(self):
        """
        :return: Iterator for collection
        """
        return _ArrayIterator(self._values)


class _ArrayIterator:

    def __init__(self, arr):
        """
        Constructor for iterator for ADT.
        Initializes inner collection
        and sets current index
        :param arr: Array that will be iterated
        """
        self._collection = arr
        self._current_position = 0

    def __iter__(self):
        """
        :return: Iterator for collection
        """
        return self

    def __next__(self):
        """
        :return: Next element in collection
        """
        if self._current_position < len(self._collection):
            el = self._collection[self._current_position]
            self._current_position += 1
            return el
        else:
            raise StopIteration


class ArrayDateIndex(Array):
    """
    ADT with possibility to index collection with dates
    """

    def __init__(self, length, dates, values=None):
        """
        Constructor for array creates inner collection
        and initialize it with values if provided.
        Also, initialize list to keep indices as dates
        and check if provided list with dates is
        the same size as array
        :param length: Size of collection
        :param dates: Sorted list with dates. Must be the same size as length
        :param values: Elements of collection
        """
        assert len(dates) == length, "List with dates must be the same size as array"
        self._dates = dates
        super().__init__(length, values)

    def __getitem__(self, index):
        if type(index) == int:
            assert 0 <= index < len(self), "Index out of range"
            return self._values[index]
        elif type(index) == datetime.date:
            i = self._binary_date_search(0, len(self._dates), index)
            return self._values[i]
        else:
            raise Exception("Wrong index type!")

    def __setitem__(self, index, value):
        if type(index) == int:
            assert 0 <= index < len(self), "Index out of range"
            self._values[index] = value
        elif type(index) == datetime.datetime:
            i = self._binary_date_search(0, len(self._dates), index)
            self._values[i] = value
        else:
            raise Exception("Wrong index type!")

    def _binary_date_search(self, s, f, index):
        mid = (s+f)//2
        curr = self._dates[mid]
        if curr < index:
            return self._binary_date_search(mid, f, index)
        elif curr > index:
            return self._binary_date_search(s, mid, index)
        else:
            return mid

    def to_pandas(self):
        data = {'Date': self._dates,
                'Price': self._values}
        df = pd.DataFrame(data, columns=['Date', 'Price'])
        return df
