from collections import defaultdict

from django.db import transaction
from django.db.models.aggregates import Count

from . import rozkladorg
from .models import Group, Course, Teacher, Lesson


LESSON_TYPES = {
    rozkladorg.LESSON_TYPE_LECTURE: Lesson.TYPE_LECTURE,
    rozkladorg.LESSON_TYPE_LAB: Lesson.TYPE_LAB,
    rozkladorg.LESSON_TYPE_PRACTICE: Lesson.TYPE_PRACTICE
}


def import_group(group_data: dict) -> Group:
    """
    Looks up a existing group, preparing one if necessary.

    :param group_data: info obtained from rozkladorg api
    :rtype: Group
    """
    group, _ = Group.objects.get_or_prepare(
        code=group_data['group_full_name'],
        defaults={
            'prefix': group_data['group_prefix'],
            'okr': group_data['group_okr'],
            'type': group_data['group_type'],
        }
    )
    return group


def import_teachers(lessons_data) -> dict:
    """
    Looks up a existing teachers, preparing ones if necessary.

    :param lessons_data: obtained from `rozkladorg.get_group_lessons`
    :rtype: dict[int, Teacher]
    """
    unique_teachers = dict()

    for lesson_data in lessons_data:
        for teacher_data in lesson_data['teachers']:
            unique_teachers[teacher_data['teacher_id']] = teacher_data

    teachers = dict()

    for teacher_id, data in unique_teachers.items():
        try:
            teachers[teacher_id] = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            teachers[teacher_id] = Teacher(
                name=data['teacher_name'],
                short_name=data['teacher_short_name'],
                full_name=data['teacher_full_name']
            )

    return teachers


def import_group_lessons(group_data: str):
    """
    :param group_data: obtained result from `get_group` api method.
    """
    if group_data['group_type'] == rozkladorg.GROUP_EXTRAMURAL:
        lessons_data = []
    else:
        lessons_data = rozkladorg.get_group_lessons(group_data['group_full_name'])

    group = import_group(group_data)
    teachers = import_teachers(lessons_data)

    with transaction.atomic():
        # Step 1: prepare related objects
        if group.id is None:
            group.save()

        for teacher_id, teacher in teachers.items():
            if teacher.id is None:
                teacher.id = teacher_id
                teacher.save()

        # Step 2: find out existing lessons at same time & place, add current group
        # This gives ability to identify same courses across different groups later
        new_lessons_data = []

        for lesson_data in lessons_data:
            if lesson_data['teachers']:
                teacher = teachers[lesson_data['teachers'][0]['teacher_id']]
            else:
                teacher = None

            assert lesson_data['lesson_room']

            try:
                lesson = Lesson.objects.get(
                    week=lesson_data['lesson_week'],
                    weekday=lesson_data['day_number'],
                    number=lesson_data['lesson_number'],
                    place=lesson_data['lesson_room'],
                    course__full_name=lesson_data['lesson_full_name'],
                )
            except Lesson.DoesNotExist:
                new_lessons_data.append(lesson_data)
            else:
                lesson.groups.add(group)

        # Step 3: create new lessons, try to reuse existing courses
        for lesson_data in new_lessons_data:
            if lesson_data['teachers']:
                teacher = teachers[lesson_data['teachers'][0]['teacher_id']]
            else:
                teacher = None

            course, _ = Course.objects.of_group(group).get_or_create(
                full_name=lesson_data['lesson_full_name'],
                defaults={'short_name': lesson_data['lesson_name']},
            )
            lesson = Lesson.objects.create(
                course=course,
                week=lesson_data['lesson_week'],
                weekday=lesson_data['day_number'],
                number=lesson_data['lesson_number'],
                type=LESSON_TYPES[lesson_data['lesson_type']],
                teacher=teacher,
                place=lesson_data['lesson_room'],
            )
            lesson.groups.add(group)

    return group
