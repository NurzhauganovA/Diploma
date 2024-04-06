from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db.models import QuerySet
from django.contrib import messages

from authorization.models import User
from authorization import UserRoles
from school.utils import CacheData


def get_people(request: HttpRequest, pk: int) -> None:
    if request.method == "GET":
        cache = CacheData("school", pk)

        students: QuerySet = User.objects.filter(school__id=pk, role=UserRoles.STUDENT)
        parents: QuerySet = User.objects.filter(school__id=pk, role=UserRoles.PARENT)
        teachers: QuerySet = User.objects.filter(school__id=pk, role=UserRoles.EMPLOYEE)

        context: dict[str, QuerySet] = {
            "students": students,
            "parents": parents,
            "teachers": teachers,
        }

        cache.cache_data(context)

        return render(request, "school/people.html", context)
    
    return JsonResponse({"error": "Not Allowed Method"})


def get_more_info(request: HttpRequest, pk: int) -> None:
    if request.method == "GET":
        cache = CacheData("user", pk)
        user: User = User.objects.get(id=pk)

        user_info = {
            "full_name": user.full_name,
            "class": user.student_info if hasattr(user, "student_info") else None,
            "iin": user.user_info.iin,
            "birth": user.user_info.birth_date.strftime("%d.%m.%Y"),
            "mobile_phone": user.mobile_phone,
            "email": user.email,
            "contracts": user.student_info.contracts.all() if hasattr(user, "student_info") else None,
            "parents": user.student_info.parent if hasattr(user, "student_info") else None,
        }

        cache.cache_data(user_info)

        return render(request, "school/more_info.html", user_info)

    return JsonResponse({"error": "Not Allowed Method"})


