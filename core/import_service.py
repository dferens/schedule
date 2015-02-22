from django.db import transaction

from . import rozkladorg
from .models import Group, Course, Teacher, Lesson


LESSON_TYPES = {
    rozkladorg.LESSON_TYPE_LECTURE: Lesson.TYPE_LECTURE,
    rozkladorg.LESSON_TYPE_LAB: Lesson.TYPE_LAB,
    rozkladorg.LESSON_TYPE_PRACTICE: Lesson.TYPE_PRACTICE
}


def import_group(group_data: str):
    """
    :param group_data: obtained result from `get_group` api method.
    """
    unique_teachers = dict()  # id -> dict
    unique_courses = dict()   # full name -> dict

    if group_data['group_type'] == rozkladorg.GROUP_EXTRAMURAL:
        lessons_data = []
    else:
        lessons_data = rozkladorg.get_group_lessons(group_data['group_full_name'])

    for lesson_data in lessons_data:
        unique_courses[lesson_data['lesson_full_name']] = {
            'lesson_name': lesson_data['lesson_name']
        }

        for teacher_data in lesson_data['teachers']:
            unique_teachers[teacher_data['teacher_id']] = teacher_data

    with transaction.atomic():
        teachers = dict()  # id -> Teacher object
        courses = dict()  # course full name -> Course object

        # Create group if necessary
        group, _ = Group.objects.get_or_create(
            code=group_data['group_full_name'],
            defaults={
                'prefix': group_data['group_prefix'],
                'okr': group_data['group_okr'],
                'type': group_data['group_type'],
            }
        )

        # Create teachers if necessary, identify them by site id
        for teacher_id, data in unique_teachers.items():
            teacher, _ = Teacher.objects.get_or_create(
                id=teacher_id,
                defaults={
                    'name': data['teacher_name'],
                    'full_name': data['teacher_full_name'],
                    'short_name': data['teacher_short_name']
                }
            )
            teachers[teacher_id] = teacher

        # Create courses if necessary, identify them by (group, name) pair
        for course_full_name, data in unique_courses.items():
            course, _ = Course.objects.get_or_create(
                group=group,
                full_name=course_full_name,
                defaults={'short_name': data['lesson_name']}
            )
            courses[course.full_name] = course

        # Finally, create lessons records
        for lesson_data in lessons_data:
            if lesson_data['teachers']:
                teacher = teachers[lesson_data['teachers'][0]['teacher_id']]
            else:
                teacher = None

            Lesson.objects.get_or_create(
                course=courses[lesson_data['lesson_full_name']],
                week=lesson_data['lesson_week'],
                weekday=lesson_data['day_number'],
                number=lesson_data['lesson_number'],
                defaults={
                    'teacher': teacher,
                    'type': LESSON_TYPES[lesson_data['lesson_type']],
                },
            )

    return group
