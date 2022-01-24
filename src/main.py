from rumad_monitor.src import vt100
from rumad_monitor.src.controllers.rumad import RumadMonitor, Semesters


def main():
    term = vt100.Terminal(verbosity=False, height=25, width=80)
    monitor = RumadMonitor("horario", "", term)

    course = "INEL4207"
    courses = monitor.get_sections(
        year=2021, semester=Semesters.Horario.SPRING_SEMESTER, course_code=course
    )

    print(course)


if __name__ == "__main__":
    main()
