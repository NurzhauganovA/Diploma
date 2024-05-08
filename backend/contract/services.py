import pandas as pd
from django.http import HttpResponse
from django.db.models import QuerySet
from typing import Any

try:
    from io import BytesIO as IO
except ImportError:
    from io import StringIO as IO


def export_dataframe(df: pd.core.frame.DataFrame, sheet_name: str | None = None):
    excel_file = IO()

    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as xlwriter:
        df.to_excel(xlwriter, sheet_name if sheet_name is not None else "", index=False)

    excel_file.seek(0)

    return excel_file


def prepare_response(file, filename: str) -> HttpResponse:
    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = HttpResponse(file.read(), content_type=content_type)

    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


def report_response(
    query: list[dict], columns: list, sheet_name: str, filename: str
) -> HttpResponse:
    df = pd.DataFrame(query)

    if not df.empty:
        df.columns = columns

    file = export_dataframe(df, sheet_name)

    return prepare_response(file, filename)


def _get_contracts_list(queries: QuerySet) -> list[dict[str, Any]]:
    result = [
        {
            "student_full_name": query.student.user.full_name
            if query.student.user
            else "No data",
            "date": query.date.strftime("%d.%m.%Y") if query.date else "No data",
            "termination": query.date_close.strftime("%d.%m.%Y")
            if query.date_close
            else "No data",
            "final_amount": int(query.final_amount)
            if query.final_amount
            else "No data",
            "status": query.status if query.status else "No data",
            "payment_type": query.payment_type if query.payment_type else "No data",
            "discounts": [discount.name for discount in query.discount.all()],
        }
        for query in queries
    ]

    return result
