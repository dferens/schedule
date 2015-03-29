from .. import service


def is_block(obj):
    return hasattr(obj, 'get_context')


def expand(obj):
    if isinstance(obj, dict):
        return {k: expand(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return list(map(expand, obj))
    elif isinstance(obj, (map, tuple)):
        return tuple(map(expand, obj))
    elif is_block(obj):
        return expand(obj.get_context())
    else:
        return obj


class GroupBlock(object):

    def __init__(self, group):
        self.group = group

    def get_context(self):
        return {
            'code': self.group.code
        }


class CourseBlock(object):

    def __init__(self, course):
        self.course = course

    def get_context(self):
        return {
            'id': self.course.id,
            'short_name': self.course.short_name,
            'full_name': self.course.full_name
        }


class TeacherBlock(object):

    def __init__(self, teacher):
        self.teacher = teacher

    def get_context(self):
        return {
            'id': self.teacher.id,
            'short_name': self.teacher.short_name,
            'full_name': self.teacher.full_name,
        }


class LessonBlock(object):

    def __init__(self, lesson):
        self.lesson = lesson

    def get_context(self):
        return {
            'id': self.lesson.id,
            'course': CourseBlock(self.lesson.course),
            'week': self.lesson.week,
            'weekday': self.lesson.weekday,
            'number': self.lesson.number,
            'place': self.lesson.place,
            'type': self.lesson.type,
            'teacher': TeacherBlock(self.lesson.teacher) if self.lesson.teacher else None,
            'groups': [GroupBlock(g) for g in self.lesson.groups.all()],
        }


class ScheduleBlock(object):

    def __init__(self, lessons_list):
        self.lessons = lessons_list

    def get_context(self):
        return {
            'current_week': service.get_week_number(),
            'lessons': [LessonBlock(l) for l in self.lessons]
        }
