from . import rozkladorg, import_service
from .models import Course, Group, GroupIndex, Lesson, Teacher


def find_group(group_alias: str) -> Group or None:
    """
    Look up group by some group identifier.

    If group does not exist in db, prefetch it's info from rozklad.org and
    create record.
    """
    group = GroupIndex.objects.lookup_group(group_alias)

    if group is not None:
        return group
    else:
        group_data = rozkladorg.get_group(group_alias)

        if group_data is None:
            return None
        else:
            group_code = group_data['group_full_name']

            try:
                group = Group.objects.get(code=group_code)
            except Group.DoesNotExist:
                group = import_service.import_group_lessons(group_data)

                if group.code != group_alias:
                    GroupIndex.objects.add_alias(group, group.code)

            GroupIndex.objects.add_alias(group, group_alias)
            return group


def get_group_lessons(group: Group) -> [Lesson]:
    return Lesson.objects.of_group(group)


def get_teacher_lessons(teacher: Teacher) -> [Lesson]:
    return Lesson.objects.of_teacher(teacher)


def get_course_lessons(course: Course) -> [Lesson]:
    return Lesson.objects.of_course(course)
