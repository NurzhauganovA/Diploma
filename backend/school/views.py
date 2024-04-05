from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.db.models import QuerySet
from django.contrib import messages

from authorization.models import User
from authorization import UserRoles


def get_people(request: HttpRequest) -> None:
    if request.method == "GET":
        school_id: int = int(request.GET.get("id", 1))
        # school_id: int = int(request.user.)

        if school_id == 0:
            messages.error(request, "There is no school with this ID.")
            return redirect("get_people")

        students: QuerySet = User.objects.filter(school__id=school_id, role=UserRoles.STUDENT)
        parents: QuerySet = User.objects.filter(school__id=school_id, role=UserRoles.PARENT)
        teachers: QuerySet = User.objects.filter(school__id=school_id, role=UserRoles.EMPLOYEE)

        context: dict[str, QuerySet] = {
            "students": students,
            "parents": parents,
            "teachers": teachers,
        }

        return render(request, "people.html", context)
    
    return render(request, ".html")


def get_more_info(request: HttpRequest) -> None:
    if request.method == "GET":
        user_id: int = int(request.GET.get("id"))

        user: QuerySet = User.objects.get(id=user_id)

        user_info = {
            ""
        }


