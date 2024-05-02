from django.db import models


class ContractPaymentPeriodType(models.TextChoices):
    """ Типы периодов оплаты контрактов """

    MONTHLY = 'MONTHLY', 'Ежемесячно'
    QUARTERLY = 'QUARTERLY', 'Ежеквартально'
    ANNUAL = 'ANNUAL', 'Ежегодно'


class ContractStatus(models.TextChoices):
    """ Статусы контрактов """

    FORMED = 'Formed', 'Сформирован'
    CONSIDERATION = 'Consideration', 'На рассмотрении'
    SIGNED = 'Signed', 'Подписан'
    FINISHED = 'Finished', 'Завершен'
    CANCELED = 'Canceled', 'Отменен'
    DISSOLVED = 'Dissolved', 'Расторгнут'
