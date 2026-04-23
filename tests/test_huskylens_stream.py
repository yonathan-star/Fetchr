import unittest

from fetchr.vision.huskylens_stream import HuskyLensDetection, parse_detection_line


class HuskyLensStreamTests(unittest.TestCase):
    def test_parse_detection_line_success(self) -> None:
        line = 'ID=1 x=156 y=148'
        self.assertEqual(
            parse_detection_line(line),
            HuskyLensDetection(object_id=1, x=156, y=148),
        )

    def test_parse_detection_line_ignores_non_detection_line(self) -> None:
        line = 'HUSKYLENS begin: OK'
        self.assertIsNone(parse_detection_line(line))


if __name__ == '__main__':
    unittest.main()
