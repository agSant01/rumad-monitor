import unittest
from xml.dom import InvalidAccessErr

from rumad_monitor.src.exceptions import MissingOptionalProfessor
from src.models.courses import Courses


class CoursesModelTest(unittest.TestCase):
    def test_missing_professor(self):
        courses = Courses(["INEL4023", "MATE3032"], ["Manuel Toledo", None])
        
        self.assertEqual(courses._courses["MATE3032"], [])
        
        self.assertEqual(courses._courses.get("INVALID"), None)

        Courses(["INEL4023", "MATE3032"], ["Manuel Toledo", []])

    def test_missing_professor(self):
        with self.assertRaises(MissingOptionalProfessor):
            Courses(["INEL4023", "MATE3032"], ["Manuel Toledo"])

    def test_get_professors(self):
        courses = Courses(["INEL4023", "MATE3032"], ["Manuel Toledo", None])

        self.assertEqual(courses.get_professors("INEL4023"), ["Manuel Toledo"])
        self.assertEqual(courses.get_professors("MATE3032"), [])

        self.assertEqual(courses.get_professors("INVALID_CODE"), None)

        self.assertFalse("INVALID_CODE" in courses._courses)

    def test_get_courses(self):
        courses = Courses(
            ["INEL4023", "MATE3032", "CLASS3"],
            [["Manuel Toledo"], None, ["Prof1", "Prof2"]],
        )

        self.assertListEqual(
            list(courses.get_courses()),
            ["INEL4023", "MATE3032", "CLASS3"],
        )

    def test_get_pairs(self):
        courses = Courses(
            ["INEL4023", "MATE3032", "CLASS3"],
            [["Manuel Toledo"], None, ["Prof1", "Prof2"]],
        )

        self.assertListEqual(
            list(courses.get_pairs()),
            [
                ("INEL4023", ["Manuel Toledo"]),
                ("MATE3032", []),
                ("CLASS3", ["Prof1", "Prof2"]),
            ],
        )
