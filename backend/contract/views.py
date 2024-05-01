from django.http import JsonResponse
from django.shortcuts import render
from django.http.request import HttpRequest

from school.services import GetSchoolPartData
from school.models import School
from contract.models import Contract, Transaction


def get_all_contracts(req: HttpRequest):
    school = School.objects.get(
        id=GetSchoolPartData(req.user.id).get_school_pk()
    )
    contracts = school.contracts.all()
    context = {
        "contracts": contracts
    }

    return render(req, "contract/contract.html", context)


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
                    "payment_type": transaction.payment_type if hasattr(transaction, "payment_type") else "CASH",
                })

        return JsonResponse({'data': transactions_info, 'status': 200})

    return JsonResponse({"error": "Not Allowed Method", "status": 405})