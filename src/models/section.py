import re
from typing import Optional

REGEX = re.compile(
    r"([LMWJV]+.+\d+:\d{2}-.*\d+:\d{2}\W*(am|pm|)|Por acuerdo)", re.IGNORECASE
)


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
        self.cap = int(course[-3])
        self.used = int(course[-2])

    def remaining(self) -> int:
        return self.cap - self.used

    def pretty(self) -> str:
        return f"""    - Code: {self.code}
    - Professor: {self.prof or 'Fantasma'}
    - Time: {self.time or 'No disponible'}
    - Credits: {self.creds}
    - Capacity: {self.cap}
    - Used spaces: {self.used}
    - Remaining spaces: {self.remaining()}"""

    def __hash__(self) -> int:
        return hash(self.code)

    def __eq__(self, __o: object) -> bool:
        return __o.code == self.code

    def __repr__(self) -> str:
        return f"<Section code:{self.code} time:'{self.time}' creds:{self.creds} professor:'{self.prof}' cap:{self.cap} used:{self.used}>"

    def __str__(self) -> str:
        return self.__repr__()
