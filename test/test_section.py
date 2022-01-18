import pathlib
import unittest

from rumad_monitor.src.models.section import Section, parse_sections


class SectionTest(unittest.TestCase):
    def test_time(self):
        secObj = Section("LMV 1:30- 3:45PM     ")
        self.assertEqual(secObj.time, "LMV 1:30-3:45PM")

        secObj = Section("   LJV       1:30-   3:45PM     ")
        self.assertEqual(secObj.time, "LJV 1:30-3:45PM")

        secObj = Section("   LJV       1:30-   3:45am     ")
        self.assertEqual(secObj.time, "LJV 1:30-3:45AM")

        secObj = Section("   LJV       8:30-   9:20     ")
        self.assertEqual(secObj.time, "LJV 8:30-9:20")

    def test_empty(self):
        secObjs = [Section(" "), Section(""), Section(None)]

        for secObj in secObjs:
            for attr in vars(secObj):
                self.assertIsNone(getattr(secObj, attr))

    def test_parse(self):
        file_path = pathlib.Path(__file__).parent / "test_section_data.txt"
        checks = [
            "<Section code:003D time:'POR ACUERDO' creds:4 professor:'UROYOAN WALKER' cap:30 used:30>",
            "<Section code:072E time:'L 1:30-2:20PM' creds:4 professor:'None' cap:30 used:20>",
            "<Section code:005D time:'POR ACUERDO' creds:4 professor:'FREDDIE SANTIAGO HER' cap:30 used:30>",
            "<Section code:070 time:'LW 1:30-3:20PM' creds:4 professor:'ROBERT ACAR' cap:30 used:19>",
            "<Section code:066H time:'MJ 12:30-2:20PM' creds:4 professor:'REYES ORTIZ ALBINO' cap:30 used:30>",
            "<Section code:007D time:'POR ACUERDO' creds:4 professor:'FREDDIE SANTIAGO HER' cap:30 used:30>",
            "<Section code:004D time:'POR ACUERDO' creds:4 professor:'UROYOAN WALKER' cap:30 used:30>",
            "<Section code:006D time:'POR ACUERDO' creds:4 professor:'FREDDIE SANTIAGO HER' cap:30 used:30>",
            "<Section code:110H* time:'LW 5:30-7:20PM' creds:4 professor:'WILLIAM FELICIANO VE' cap:31 used:31>",
            "<Section code:106 time:'MJ 4:30-6:20PM' creds:4 professor:'ROBERT ACAR' cap:30 used:9>",
            "<Section code:002D time:'POR ACUERDO' creds:4 professor:'UROYOAN WALKER' cap:30 used:30>",
            "<Section code:096H time:'None' creds:4 professor:'REYES ORTIZ ALBINO' cap:30 used:23>",
            "<Section code:071E time:'L 1:30-2:20PM' creds:4 professor:'ANGEL CRUZ DELGADO' cap:30 used:22>",
        ]

        with open(file_path) as data:
            section_list = parse_sections(data.readlines())
            section_list = set(str(sec) for sec in section_list)
            for check in checks:
                self.assertIn(check, section_list)


if __name__ == "__main__":
    unittest.main()
