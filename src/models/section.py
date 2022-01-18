import re
from curses import flash
from typing import List, Optional, Set

REGEX = re.compile(
    r"([LMWJV]+.+\d+:\d{2}-.*\d+:\d{2}\W*(am|pm|)|Por acuerdo)", re.IGNORECASE
)

KEY_WORDS = [
    "oprima",
    "universitario",
    "universidad",
    "universidad",
    "puerto rico",
    "períodos",
    "programa",
    "horarios de",
    "--------",
    ".sem.",
    "reservada",
    "total",
    "horario",
    "curso",
    "ej.",
    "de",
    "computos",
    "error",
    "archivo",
    "terminamos?",
]


class Section:
    def __init__(self, course: Optional[str]) -> None:
        if course is None:
            return

        time = REGEX.findall(course)

        if len(time) == 0:
            self.time = None
        else:
            self.time: str = time[0][0].strip()
            course = course.replace(self.time, "")
            self.time = re.sub(r"[ \t\r]+", " ", self.time).upper().strip()
            self.time = self.time.replace("- ", "-")

        course = course.split()
        if len(course) == 0:
            self.code = None
            self.creds = None
            self.prof = None
            self.cap = None
            self.used = None
            return

        self.code = course[0]
        self.creds = course[1]
        self.prof = " ".join(course[2:-3]) or None
        print(course)
        self.cap = int(course[-3])
        self.used = int(course[-2])

    def remaining(self) -> int:
        return self.cap - self.used

    def __hash__(self) -> int:
        return hash(self.code)

    def __eq__(self, __o: object) -> bool:
        return __o.code == self.code

    def __repr__(self) -> str:
        return f"<Section code:{self.code} time:'{self.time}' creds:{self.creds} professor:'{self.prof}' cap:{self.cap} used:{self.used}>"

    def __str__(self) -> str:
        return self.__repr__()


def parse_sections(courses: List[str]) -> Set[Section]:
    filtered = set()

    for course in courses:

        if len(course.strip()) <= 1:
            continue

        print("fuck", course)
        if any(kw.lower() in course.lower().replace(" ", "") for kw in KEY_WORDS):
            if "error" in course.lower():
                print("Error: ", course)
            continue

        filtered.add(Section(course))

    return filtered
