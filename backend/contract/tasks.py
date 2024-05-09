from django.core import mail
from django.conf import settings

from contract.services import _prepare_dataframe, export_dataframe
from diploma import celery_app

@celery_app.task()
def async_export_report_task(queryset: list[dict], columns: list, sheet_name: str, filename: str, email: str):
    df_output = _prepare_dataframe(queryset, columns)
    report = export_dataframe(df_output, sheet_name)

    message = mail.EmailMessage(sheet_name, from_email=settings.EMAIL_HOST_USER, to=email)
    message.attach(filename, report.read())
    message.send()
