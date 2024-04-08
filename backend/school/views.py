from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db.models import QuerySet
from django.contrib import messages

from authorization.models import User
from authorization import UserRoles
from school.services import GetSchoolPartData
from school.utils import CacheData


def school_part(request: HttpRequest):
    school_data = GetSchoolPartData(request.user.id).get_school_part()
    context = {
        "students": school_data["students"],
        "parents": school_data["parents"],
        "teachers": school_data["teachers"],
    }

    return render(request, "school/school_part.html", context)


def get_people(request: HttpRequest, pk: int) -> JsonResponse:
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

        return JsonResponse(data={**context, "status": 200})
    
    return JsonResponse({"error": "Not Allowed Method", "status": 405})

def get_more_info(request: HttpRequest, pk: int) -> JsonResponse:
    if request.method == "GET":
        user: User = User.objects.get(id=pk)
        parent = user.student_info.parent if hasattr(user, "student_info") else None,
        print(parent)
        user_info = {
            "photo_avatar": user.get_photo(),
            "full_name": user.full_name if user.full_name else "No data",
            "class_num": user.student_info.stud_class.class_num if user.student_info else "No data",
            "class_liter": user.student_info.stud_class.class_liter if user.student_info else "No data",
            "iin": user.user_info.iin if user.user_info.iin else "No data",
            "birth": user.user_info.birth_date.strftime("%d.%m.%Y") if user.user_info.birth_date else "No data",
            "mobile_phone": user.mobile_phone if user.mobile_phone else "No data",
            "email": user.email if user.email else "No data",
            # "contracts": user.student_info.contracts.all() if hasattr(user, "student_info") else None,
            "parent": {
                "photo_avatar": parent.get_photo(),
                "full_name": parent.full_name,
                "iin": parent.user_info.iin,
                "mobile_phone": parent.mobile_phone,
                "email": parent.email
            }
        }

        return JsonResponse({'data': user_info, 'status': 200})

    return JsonResponse({"error": "Not Allowed Method", "status": 405})


