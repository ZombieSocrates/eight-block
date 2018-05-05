import unittest

def binary_insert(value, array, lwr = None, upr = None):
    '''
    '''
    if lwr is None:
        lwr = 0
    if upr is None:
        upr = len(array)
    if len(array[lwr:upr]) <= 1:
        loc = lwr if value <= array[lwr] else upr
        array.insert(loc,value)
    else:
        mid = int((lwr + upr)/2)
        if value <= array[mid]:
            binary_insert(value, array, lwr = lwr, upr = mid)
        else:
            binary_insert(value, array, lwr = mid, upr = upr)


class TestBinaryInsert(unittest.TestCase):

    def test_empty_array(self):
        with self.assertRaises(IndexError):
            binary_insert(0,[])

    def test_case_one(self):
        c1 = [5]
        binary_insert(3,c1)
        self.assertEqual(c1, [3,5])

    def test_case_two(self):
        c2 = sorted([8,6,7,5,3,0,9])
        binary_insert(12, c2)
        self.assertEqual(c2, [0,3,5,6,7,8,9,12])

    def test_case_three(self):
        c3 = [5,5,5,5,5,5,5]
        binary_insert(5,c3)
        self.assertEqual(c3, [5,5,5,5,5,5,5,5])

    def test_case_four(self):
        c4 = [3,3,3,3,3,3] + [8,8,8,8]
        binary_insert(5, c4)
        self.assertEqual(c4, [3,3,3,3,3,3,5,8,8,8,8])

    def test_case_five(self):
        c5 = [12,24,48]
        binary_insert(16, c5)
        self.assertEqual(c5, [12,16,24,48])
        binary_insert(30, c5, lwr = 1)
        self.assertEqual(c5, [12,16,24,30,48]) 





