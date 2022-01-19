from typing import List, Set

from rumad_monitor.src.models.section import Section

KEY_WORDS = [
    "oprima",
    "universitario",
    "universidad",
    "u n i v e r s i d a d",
    "puerto rico",
    "períodos",
    "programa",
    "horarios de",
    "--------",
    ".sem.",
    "reservada",
    "total",
    "horario",
    "h o r a r i o",
    "c u r s o",
    "ej.",
    "computos",
    "error",
    "archivo",
    "terminamos?",
    "INCORRECTO",
    "Semestre",
]

import copy


def parse_sections(courses: List[str]) -> Set[Section]:
    filtered = set()

    for course in courses:
        if len(course.strip()) <= 1:
            continue

        if any(kw.lower() in course.lower() for kw in KEY_WORDS):
            if "error" in course.lower():
                print("Error: ", course)
            continue

        try:
            filtered.add(Section(copy.copy(course)))
        except Exception as e:
            print("Course:", course)
            raise e

    return filtered
