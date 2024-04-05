from django.shortcuts import render

from dashboard.services import GetSchoolRegionsService, GetLastRegisteredUsersService, GetCountNewUsersThisMonthService, \
    GetOverallGoalUsersService
from school.models import School


def home(request):

    regions = GetSchoolRegionsService().get_school_regions()
    last_registered_users = GetLastRegisteredUsersService().get_last_registered_users()
    count_last_registered_users = GetCountNewUsersThisMonthService().get_count_new_users_this_month()
    overall_users_analytics = GetOverallGoalUsersService().get_overall_users_analytics()

    context = {
        'regions': regions,
        'last_registered_users': last_registered_users,
        'count_last_registered_users': count_last_registered_users,
        'overall_users_analytics': overall_users_analytics
    }

    print(context)

    return render(request, 'dashboard/home.html', context)
