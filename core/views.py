from django.views.generic import TemplateView
from django.shortcuts import redirect

from . import service


class GroupScheduleView(TemplateView):
    template_name = 'core/group_schedule.html'

    def get(self, request, code=None):
        group = service.find_group(code)

        if group and group.code != code:
            return redirect('schedule:group', code=group.code)
        else:
            context = self.get_context_data(group)
            return self.render_to_response(context)

    def get_context_data(self, group):
        if group is None:
            return {'group': None, 'schedule': None}
        else:
            return {
                'group': group,
                'schedule': service.get_schedule(group)
            }
