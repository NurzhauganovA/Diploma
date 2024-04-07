from django.utils import timezone

from authorization.models import User
from school.models import School


class GetSchoolRegionsService:
    @staticmethod
    def get_school_regions():
        schools = School.objects.all()
        regions = []
        for school in schools:
            if school.region not in regions:
                regions.append(school.region)

        return regions


class GetLastRegisteredUsersService:
    @classmethod
    def set_response_data(cls, response_data):
        data = []
        for user in response_data:
            data.append({
                'photo_avatar': user.get_photo()
            })

        return data

    def get_last_registered_users(self):
        users = User.objects.all().order_by('-date_joined')[:5]
        return self.set_response_data(users)


class GetCountNewUsersThisMonthService:
    @staticmethod
    def get_count_new_users_this_month():
        this_month = timezone.now().month

        users = User.objects.filter(date_joined__month=this_month)
        return users.count()


class GetOverallGoalUsersService:
    @classmethod
    def set_response_data(cls, overall_users, goal_users, count_before_month, difference_with_before_month):
        return {
            'overall_users': overall_users,
            'goal_users': goal_users,
            'percent': int(overall_users / goal_users * 100),
            'difference': goal_users - overall_users if goal_users - overall_users > 0 else 'Выполнено',
            'difference_with_before_month': difference_with_before_month,
            'is_upper': True if count_before_month / overall_users * 100 > 100 else False
        }

    @staticmethod
    def get_overall_users_analytics():
        overall_users = User.objects.all().count()
        goal_users = 1000
        count_current_month = User.objects.filter(date_joined__month=timezone.now().month).count()
        count_before_month = User.objects.filter(date_joined__month=timezone.now().month - 1).count()

        if count_before_month == 0:
            count_before_month = 1

        if count_current_month == 0:
            count_current_month = 1

        difference_with_before_month = int(count_before_month / count_current_month * 100) - 100
        if difference_with_before_month < 0:
            difference_with_before_month = difference_with_before_month - (2 * difference_with_before_month)

        return GetOverallGoalUsersService.set_response_data(overall_users, goal_users, count_before_month, difference_with_before_month)
