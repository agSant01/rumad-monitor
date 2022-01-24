from io import StringIO

from rumad_monitor.src.models.section import Section


class Notification:
    def __init__(self, header: str) -> None:
        self.courses = []
        self.buffer = StringIO()
        self.buffer.write(f"{header.upper()}:\n\n")

    def add_course(self, course_code: str, section: Section):
        self.courses.append((course_code, section))
        self.buffer.write(
            f"""Course: {course_code.upper()} (Section:"{section.code.upper()}") has a current availability of {section.remaining()} spaces.\n
Section details:\n{section.pretty()}\n"""
        )

    def dump(self) -> str:
        return self.buffer.getvalue()
