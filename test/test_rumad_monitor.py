import unittest

from rumad_monitor.src.controllers.rumad import Semesters


class RumadMonitorTest(unittest.TestCase):
    def test_semester_code(self):
        self.assertEqual(Semesters.Horario.FIRST, 1)
        self.assertEqual(Semesters.Horario.SECOND, 2)
        self.assertEqual(Semesters.Horario.SUMMER, 3)


if __name__ == "__main__":
    unittest.main()
