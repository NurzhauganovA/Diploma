from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.core.cache import cache

from authorization import UserRoles
from authorization.models import User
from school.models import School


class GetSchoolPartData:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_school_pk(self) -> int:
        school_cache = cache.get(f'school_{self.user_id}')
        if not school_cache:
            try:
                school_pk = User.objects.get(id=self.user_id).school.first().id
            except AttributeError:
                school_pk = School.objects.first().id

            return school_pk

        school_pk = int(school_cache.split("_")[-1])
        return school_pk

    def get_school_part(self) -> dict:
        school_pk = self.get_school_pk()

        students: QuerySet = User.objects.filter(school__id=school_pk, role=UserRoles.STUDENT)
        parents: QuerySet = User.objects.filter(school__id=school_pk, role=UserRoles.PARENT)
        teachers: QuerySet = User.objects.filter(school__id=school_pk, role=UserRoles.EMPLOYEE)

        return {
            "students": students,
            "parents": parents,
            "teachers": teachers,
        }
