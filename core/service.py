from . import rozkladorg, import_service
from .models import Group, Lesson


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
                group = import_service.import_group(group_data)
                return group
            else:
                try:
                    return Group.objects.get(code__iexact=new_group_code)
                except Group.DoesNotExist:
                    group = import_service.import_group(group_data)
                    return group


def get_schedule(group: Group):
    lessons = Lesson.objects.of_group(group)
    return lessons
