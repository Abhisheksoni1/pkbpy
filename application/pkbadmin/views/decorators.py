from django.http import Http404, HttpResponseRedirect
from django.urls import reverse


class GroupRequiredMixin(object):
    """
        group_required - list of strings, required param
    """

    group_required = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('custom-admin:auth_login'))
        else:
            user_groups = []
            for group in list(request.user.groups.values_list('name', flat=True)):
                user_groups.append(group)
            if len(set(user_groups).intersection(self.group_required)) <= 0:
                return HttpResponseRedirect(reverse('custom-admin:error_404'))

        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)
