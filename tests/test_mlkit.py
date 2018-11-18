import unittest
from selector.mlkit import MLKit


class TestMLKit(unittest.TestCase):

    def test_1d(self):
        ml = MLKit(['x'], ['y'])
        ml.fit([[1], [2], [3], [4]], [[1], [2], [3], [4]])
        self.assertListEqual([ml.predict([1]), ml.predict([2]), ml.predict([3]), ml.predict([4])],
                             [[1.0], [2.0], [3.0], [4.0]])

    def test_1d_bias(self):
        ml = MLKit(['x'], ['y'])
        ml.fit([[1], [2], [3], [4]], [[2], [3], [4], [5]])
        self.assertListEqual([ml.predict([1]), ml.predict([2]), ml.predict([3]), ml.predict([4])],
                             [[2.0], [3.0], [4.0], [5.0]])

    def test_2d(self):
        ml = MLKit(['x', 'y'], ['a', 'b'])
        ml.fit([[1, 4], [2, 3], [3, 2], [4, 1]], [[1, 1], [2, 2], [3, 3], [4, 4]])

        pred = ml.predict([1.1, 3.9])
        self.assertTrue(abs(pred[0] - 1.1) < 0.01)
        self.assertTrue(abs(pred[1] - 1.1) < 0.01)

        pred = ml.predict([1.9, 3.1])
        self.assertTrue(abs(pred[0] - 1.9) < 0.01)
        self.assertTrue(abs(pred[1] - 1.9) < 0.01)

        pred = ml.predict([3.1, 1.9])
        self.assertTrue(abs(pred[0] - 3.1) < 0.01)
        self.assertTrue(abs(pred[1] - 3.1) < 0.01)

        pred = ml.predict([3.9, 1.1])
        self.assertTrue(abs(pred[0] - 3.9) < 0.01)
        self.assertTrue(abs(pred[1] - 3.9) < 0.01)

    def test_additional_training(self):
        ml_1 = MLKit(['x'], ['y'])
        ml_1.fit([[1], [2]], [[1], [1]])
        ml_1.fit([[3], [4]], [[4], [4]])
        print(ml_1.predict([1]), ml_1.predict([2]), ml_1.predict([3]), ml_1.predict([4]))

        ml_2 = MLKit(['x'], ['y'])
        ml_2.fit([[1], [2], [3], [4]], [[1], [1], [4], [4]])
        print(ml_2.predict([1]), ml_2.predict([2]), ml_2.predict([3]), ml_2.predict([4]))


if __name__ == '__main__':
    unittest.main()