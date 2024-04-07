from django.utils import timezone
import datetime
from decimal import Decimal

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
    def get_count_new_users_current_month():
        current_month = timezone.now().month
        users = User.objects.filter(date_joined__month=current_month)

        return users.count()


class GetOverallGoalUsersService:
    @classmethod
    def set_response_data(cls, overall, goal, difference):
        return {
            'overall_users': overall,
            'goal_users': goal,
            'percent': Decimal(overall / goal * 100).quantize(Decimal(".01")),
            'difference': goal - overall if goal - overall > 0 else 'Выполнено',
            'difference_with_before_month': abs(difference),
            'is_upper': True if difference < 0 else False
        }

    @staticmethod
    def get_overall_users_analytics():
        overall, goal = User.objects.all().count(), 1_000

        date = timezone.now() - datetime.timedelta(days=30)
        last_month = User.objects.filter(date_joined__month=date.month).count()
        current_month = User.objects.filter(date_joined__month=timezone.now().month).count()

        difference = last_month - current_month

        return GetOverallGoalUsersService.set_response_data(overall, goal, difference)


class WeekLoginCount:
    
    def __init__(self, user_count: list[int], week_days: list[str]):
        self.user_count = user_count
        self.week_days = week_days


class DailyUsersService:

    week = {
        1: "MON", 2: "TUE", 3: "WED", 4: "THU", 5: "FRI", 6: "SAT", 7: "SUN",
    }

    def get_daily_users(self) -> WeekLoginCount:
        today = timezone.now().date()
        print(today)
        result = {}

        for day in range(6, -1, -1):
            date = today - datetime.timedelta(days=day)
            result[self.week[date.isoweekday()]] = (
                User.objects.filter(login_days__icontains=date.strftime("%d.%m.%Y")).count()
            )

        return WeekLoginCount(
            user_count=[value for value in result.values()],
            week_days=[key for key in result.keys()],
        )
