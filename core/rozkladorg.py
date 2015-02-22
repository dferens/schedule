"""
Wrapper for api.rozklad.org.ua.
"""
import requests
from urllib.parse import urljoin


API_URL = 'http://api.rozklad.org.ua/v2/'

GROUP_DAILY = 'daily'
GROUP_EXTRAMURAL = 'extramural'

LESSON_TYPE_LECTURE = 'Лек'
LESSON_TYPE_LAB = 'Лаб'
LESSON_TYPE_PRACTICE = 'Прак'
LESSON_TYPE = (
    LESSON_TYPE_LECTURE,
    LESSON_TYPE_LAB,
    LESSON_TYPE_PRACTICE
)


def get_group(group_code: str) -> dict:
    """
    Get info about given group.

    Returns:
        {
            'group_id': int
            'group_full_name': str, full group code name ("ia-12")
            'group_prefix': str, group code prefix ("ia" for "ia-12" name)
            'group_okr': str (bachelor | magister | specialist)
            'group_type': str (daily | extramural)
        }
    """
    url = urljoin(API_URL, 'groups/%s' % group_code)
    resp = requests.get(url).json()

    if resp['statusCode'] == 200:
        data = resp['data']
        assert data['group_okr'] in ('bachelor', 'magister', 'specialist')
        assert data['group_type'] in (GROUP_DAILY, GROUP_EXTRAMURAL)
        return {
            'group_id': int(data['group_id']),
            'group_full_name': data['group_full_name'],
            'group_prefix': data['group_prefix'],
            'group_okr': data['group_okr'],
            'group_type': data['group_type'],
        }
    elif resp['statusCode'] == 404:
        return None


def get_group_lessons(group_code: str) -> dict:
    """
    Get lessons for given group.

    Returns:
        {
            'lesson_id': int
            'lesson_name': str, short lesson name
            'lesson_full_name': str, full lesson name
            'lesson_number': int, in range [1..5]
            'lesson_type': str (Лек | Лаб | Прак)
            'lesson_week': int, (1 = first week, 2 = second week)
            'lesson_room': str
            'group_id': int
            'day_number': int, in range [1..7] (1 = Monday, 2 = Tuesday etc.)
            'teachers': [] or list of {
                'teacher_id': int
                'teacher_name': str
                'teacher_full_name': str
                'teacher_short_name': str
            }
            'rooms': [] or list of {
                'room_id': int
                'room_name': str
            }
        }

    """
    url = urljoin(API_URL, 'groups/%s/lessons' % group_code)
    resp = requests.get(url).json()

    def clean_lesson_number(num):
        assert num in map(str, range(1, 6))
        return int(num)

    def clean_lesson_week(week):
        assert week in ['1', '2']
        return int(week)

    def clean_lesson_type(type):
        assert type in LESSON_TYPE
        return type

    return [{
        'lesson_id': int(lesson_data['lesson_id']),
        'lesson_name': lesson_data['lesson_name'],
        'lesson_full_name': lesson_data['lesson_full_name'],
        'lesson_number': clean_lesson_number(lesson_data['lesson_number']),
        'lesson_type': lesson_data['lesson_type'],
        'lesson_week': clean_lesson_week(lesson_data['lesson_week']),
        'lesson_room': lesson_data['lesson_room'],
        'group_id': int(lesson_data['group_id']),
        'day_number': int(lesson_data['day_number']),
        'teachers': [{
            'teacher_id': int(teacher_data['teacher_id']),
            'teacher_name': teacher_data['teacher_name'],
            'teacher_full_name': teacher_data['teacher_full_name'],
            'teacher_short_name': teacher_data['teacher_short_name'],
        } for teacher_data in lesson_data['teachers']],
        'rooms': [{
            'room_id': int(room_data['room_id']),
            'room_name': room_data['room_name'],
        } for room_data in lesson_data['rooms']],
    } for lesson_data in resp['data']]
