import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import QuerySet

from authorization.models import User, Student
from authorization import UserRoles
from school.services import GetSchoolPartData
from school.utils import CacheData
from contract.models import Contract, Transaction
from django.db.models import Sum


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
        if parent:
            parent = parent[0]
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
                "photo_avatar": parent.get_photo() if parent.get_photo() else "No data",
                "full_name": parent.full_name if parent.full_name else "No data",
                "iin": parent.user_info.iin if parent.user_info.iin else "No data",
                "mobile_phone": parent.mobile_phone if parent.mobile_phone else "No data",
                "id_number": parent.user_info.num_of_doc if parent.user_info.num_of_doc else "No data",
                "issued_by": parent.user_info.issued_by if parent.user_info.issued_by else "No data",
                "address": parent.user_info.address if parent.user_info.address else "No data",
                "email": parent.email if parent.email else "No data",
            }
        }

        return JsonResponse({'data': user_info, 'status': 200})

    return JsonResponse({"error": "Not Allowed Method", "status": 405})


def get_contract_info(request: HttpRequest, pk: int) -> JsonResponse:
    if request.method == "GET":
        user: User = User.objects.get(id=pk)
        contracts = user.student_info.contracts.all() if hasattr(user, "student_info") else None

        contract_info = {
            "contracts": []
        }

        if contracts:
            for index, contract in enumerate(contracts):
                sum_transactions = Transaction.objects.filter(contract=contract).aggregate(Sum('amount'))['amount__sum']
                if not sum_transactions:
                    sum_transactions = 0

                contract_info["contracts"].append({
                    "id": contract.id,
                    "number": index + 1,
                    "name": contract.name if contract.name else "No data",
                    "status": contract.status if contract.status else "No data",
                    "date": contract.date.strftime("%Y-%m-%d") if contract.date else "No data",
                    "class": f'{contract.classroom.class_num} "{contract.classroom.class_liter}"' if contract.classroom else "No data",
                    "edu_year": contract.edu_year if contract.edu_year else "No data",
                    "amount": contract.final_amount if contract.final_amount else "No data",
                    "discount": contract.discount.all().first().percent if contract.discount.all() else "No data",
                    "debt": contract.final_amount - sum_transactions,
                })

        return JsonResponse({'data': contract_info, 'status': 200})

    return JsonResponse({"error": "Not Allowed Method", "status": 405})


def get_contract_transactions(request: HttpRequest, pk: int) -> JsonResponse:
    if request.method == "GET":
        contract = Contract.objects.get(id=pk)
        transactions = Transaction.objects.filter(contract=contract)

        transactions_info = {
            "transactions": []
        }

        if transactions:
            for transaction in transactions:
                transactions_info["transactions"].append({
                    "id": transaction.id,
                    "date": transaction.datetime.strftime("%d.%m.%Y") if transaction.datetime else "No data",
                    "amount": transaction.amount if transaction.amount else "No data",
                    "description": transaction.description if transaction.description else "No data",
                    "payment_type": transaction.payment_type if transaction.payment_type else "No data",
                })

        return JsonResponse({'data': transactions_info, 'status': 200})

    return JsonResponse({"error": "Not Allowed Method", "status": 405})


def create_transaction(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        data = json.loads(request.body)

        contract = Contract.objects.get(id=pk)
        amount = float(data.get("amount"))
        date = data.get("date")
        payment_type = data.get("payment_type")

        Transaction.objects.create(
            contract=contract,
            datetime=date,
            amount=amount,
            description=contract.name,
            payment_type=payment_type,
        )

        return JsonResponse({"status": 200})
    return JsonResponse({"error": "Not Allowed Method", "status": 405})


def edit_transaction(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        data = json.loads(request.body)

        transaction = Transaction.objects.get(id=pk)
        amount = data.get("amount")
        date = data.get("date")
        payment_type = data.get("payment_type")

        amount = int(amount.split(".")[0])

        transaction.amount = amount
        transaction.datetime = date
        transaction.payment_type = payment_type
        transaction.save()
        print(transaction.amount, transaction.datetime, transaction.payment_type)

        return JsonResponse({"status": 200})
    return JsonResponse({"error": "Not Allowed Method", "status": 405})


def delete_transaction(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        transaction = Transaction.objects.get(id=pk)
        transaction.delete()

        return JsonResponse({"status": 200})
    return JsonResponse({"error": "Not Allowed Method", "status": 405})


def distribution(request: HttpRequest) -> HttpResponse:
    school_data = GetSchoolPartData(request.user.id).get_school_distribution_statements()

    context = {
        "statements": school_data["statements"],
        "classes": school_data["classes"],
    }

    return render(request, "school/distribution.html", context)


def approve_to_class(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        student = Student.objects.get(id=data.get("student_id"))
        student.stud_class_id = data.get("class_id")
        student.save()

        return JsonResponse({"status": 200})
    return JsonResponse({"error": "Not Allowed Method", "status": 405})


def remove_from_class(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        student = Student.objects.get(id=data.get("student_id"))
        student.stud_class_id = None
        student.save()

        return JsonResponse({"status": 200})
    return JsonResponse({"error": "Not Allowed Method", "status": 405})
