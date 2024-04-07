from django.shortcuts import render

from dashboard.services import GetSchoolRegionsService, GetLastRegisteredUsersService, GetCountNewUsersThisMonthService, \
    GetOverallGoalUsersService, DailyUsersService
from school.models import School


def home(request):

    regions = GetSchoolRegionsService().get_school_regions() # work
    last_registered_users = GetLastRegisteredUsersService().get_last_registered_users() # work
    count_last_registered_users = GetCountNewUsersThisMonthService().get_count_new_users_current_month() # work
    overall_users_analytics = GetOverallGoalUsersService().get_overall_users_analytics() # work
    daily_users_analytics = DailyUsersService().get_daily_users()

    context = {
        'regions': regions,
        'last_registered_users': last_registered_users,
        'count_last_registered_users': count_last_registered_users,
        'overall_users_analytics': overall_users_analytics,
        'daily_users_analytics': daily_users_analytics,
    }

    print(context)
    print(context["daily_users_analytics"].user_count)
    print(context['daily_users_analytics'].week_days)

    return render(request, 'dashboard/home.html', context)
