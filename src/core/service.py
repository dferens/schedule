from datetime import timedelta

from django.utils import timezone
from django.db.models.query import Q

from . import models, rozkladorg, import_service
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


def get_week_number() -> int:
    """
    Returns current week number, either 1 or 2.
    """
    settings = models.SiteSettings.objects.get()
    monday_date = settings.first_week_monday
    today = timezone.now().date()
    current_week_monday = today - timedelta(days=today.weekday())
    is_primary = ((current_week_monday - monday_date).days % 14) == 0
    return 1 if is_primary else 2


def search_objects(raw_query: str):
    eng_to_ru = {
        'a': 'а',
        'e': 'е',
        'i': 'і',
        'k': 'к',
        'o': 'о',
        'p': 'р',
        't': 'т',
        'x': 'х',
        'y': 'у'
    }
    filtered_query = raw_query.strip()
    query = ''.join(eng_to_ru.get(char, char) for char in filtered_query)
    return {
        'groups': Group.objects.filter(
            Q(code__icontains=query) |
            Q(groupindex__alias__icontains=query)
        ).distinct(),
        'teachers': Teacher.objects.filter(full_name__icontains=query),
        'courses': Course.objects.filter(
            Q(full_name__icontains=query) |
            Q(short_name__icontains=query)
        )
    }
