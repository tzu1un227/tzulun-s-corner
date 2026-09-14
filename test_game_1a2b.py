"""
驗證 game_1a2b.py 的 GUI 初始化與元件運作
"""
import sys
import unittest
from game_1a2b import Game1A2B

class Test1A2BLogic(unittest.TestCase):
    def test_validation(self):
        self.assertTrue(Game1A2B.validate_number("1234")[0])
        self.assertTrue(Game1A2B.validate_number("0987")[0])
        self.assertFalse(Game1A2B.validate_number("1123")[0])
        self.assertFalse(Game1A2B.validate_number("123")[0])
        self.assertFalse(Game1A2B.validate_number("12345")[0])
        self.assertFalse(Game1A2B.validate_number("abcd")[0])
        self.assertFalse(Game1A2B.validate_number("12-4")[0])

    def test_calculation(self):
        # 測試各種情境
        self.assertEqual(Game1A2B.calculate_ab("1234", "1234"), (4, 0))
        self.assertEqual(Game1A2B.calculate_ab("1234", "4321"), (0, 4))
        self.assertEqual(Game1A2B.calculate_ab("1234", "1324"), (2, 2))
        self.assertEqual(Game1A2B.calculate_ab("1234", "5678"), (0, 0))
        self.assertEqual(Game1A2B.calculate_ab("9876", "9867"), (2, 2))

if __name__ == "__main__":
    unittest.main()
