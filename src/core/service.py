from . import rozkladorg, import_service
from .models import Course, Group, Lesson, Teacher


def find_group(group_code: str) -> Group or None:
    """
    Look up group by it's code.

    If group does not exist in db, prefetch it's info from rozklad.org and
    create record.
    """
    group_code = group_code.strip()

    try:
        return Group.objects.get(code__iexact=group_code)
    except Group.DoesNotExist:
        group_data = rozkladorg.get_group(group_code)

        if group_data is None:
            return None
        else:
            new_group_code = group_data['group_full_name']

            if new_group_code == group_code:
                group = import_service.import_group_lessons(group_data)
                return group
            else:
                try:
                    return Group.objects.get(code__iexact=new_group_code)
                except Group.DoesNotExist:
                    group = import_service.import_group_lessons(group_data)
                    return group


def get_group_lessons(group: Group) -> [Lesson]:
    return Lesson.objects.of_group(group)


def get_teacher_lessons(teacher: Teacher) -> [Lesson]:
    return Lesson.objects.of_teacher(teacher)


def get_course_lessons(course: Course) -> [Lesson]:
    return Lesson.objects.of_course(course)
