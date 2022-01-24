from collections import defaultdict
from typing import Any, Dict, ItemsView, KeysView, List, Optional, Tuple, Union

from rumad_monitor.src.exceptions import MissingOptionalProfessor


class Courses:
    def __init__(
        self,
        courses_to_monitor: List[str],
        professors: Optional[Union[str, List[str]]],
    ) -> None:
        if len(courses_to_monitor) != len(professors):
            raise MissingOptionalProfessor(
                "Every course must have a matching Optional professor."
            )

        self._courses: Dict[str, list] = defaultdict(list)

        for idx, course in enumerate(courses_to_monitor):
            self.add(course, professors[idx])

    def add(self, course_code, professors: Optional[Union[str, List[str]]] = None):
        if isinstance(professors, str):
            self._courses[course_code].append(professors)
        elif isinstance(professors, list):
            self._courses[course_code].extend(professors)
        else:
            self._courses[course_code]

    def get_courses(self) -> KeysView[str]:
        return self._courses.keys()

    def get_professors(self, course_code) -> Optional[List[str]]:
        if course_code not in self._courses:
            return None
        return self._courses[course_code]

    def get_pairs(self) -> ItemsView[str, Optional[List[str]]]:
        return self._courses.items()
