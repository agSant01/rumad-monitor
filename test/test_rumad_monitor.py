import unittest

from rumad_monitor.src.controllers.rumad import Semesters


class RumadMonitorTest(unittest.TestCase):
    def test_semester_code(self):
        self.assertEqual(Semesters.Horario.FIRST_SUMMER_CLASSES.value, 1)
        self.assertEqual(Semesters.Horario.FALL_SEMESTER.value, 2)
        self.assertEqual(Semesters.Horario.SPRING_SEMESTER.value, 3)
        self.assertEqual(Semesters.Horario.SECOND_SUMMER_CLASSES.value, 4)

    def test_semester_string(self):
        self.assertEqual(
            Semesters.Horario.FIRST_SUMMER_CLASSES.name, "FIRST_SUMMER_CLASSES"
        )
        self.assertEqual(
            Semesters.Horario.SECOND_SUMMER_CLASSES.name,
            "SECOND_SUMMER_CLASSES",
        )


if __name__ == "__main__":
    unittest.main()
