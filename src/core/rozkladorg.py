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
LESSON_TYPES = (
    LESSON_TYPE_LECTURE,
    LESSON_TYPE_LAB,
    LESSON_TYPE_PRACTICE
)


class ApiError(Exception):
    """
    Any unexpected rozkladorg error - timeout, 500 etc.
    """
    def __init__(self, caused):
        self.caused = caused


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

    Raises:
        ApiError
    """
    url = urljoin(API_URL, 'groups/%s' % group_code)

    try:
        resp = requests.get(url).json()
    except requests.ConnectionError as e:
        raise ApiError(e)

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
            'lesson_type': str (Лек | Лаб | Прак) or None
            'lesson_week': int, (1 = first week, 2 = second week)
            'lesson_room': str ("517-18" etc.) or None
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

    Raises:
        ApiError

    """
    url = urljoin(API_URL, 'groups/%s/lessons' % group_code)

    try:
        resp = requests.get(url).json()
    except requests.ConnectionError as e:
        raise ApiError(e)

    def clean_lesson_number(num):
        assert num in map(str, range(1, 6))
        return int(num)

    def clean_lesson_type(type):
        cleaned_type = type or None
        assert cleaned_type is None or cleaned_type in LESSON_TYPES
        return cleaned_type

    def clean_lesson_week(week):
        assert week in ['1', '2']
        return int(week)

    def clean_lesson_room(room):
        cleaned_room = room or None
        assert cleaned_room is None or isinstance(cleaned_room, str)
        return cleaned_room

    return [{
        'lesson_id': int(lesson_data['lesson_id']),
        'lesson_name': lesson_data['lesson_name'],
        'lesson_full_name': lesson_data['lesson_full_name'],
        'lesson_number': clean_lesson_number(lesson_data['lesson_number']),
        'lesson_type': clean_lesson_type(lesson_data['lesson_type']),
        'lesson_week': clean_lesson_week(lesson_data['lesson_week']),
        'lesson_room': clean_lesson_room(lesson_data['lesson_room']),
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
