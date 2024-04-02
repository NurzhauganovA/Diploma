from django.db import models


class ContractPaymentPeriodType(models.TextChoices):
    """ Типы периодов оплаты контрактов """

    MONTHLY = 'MONTHLY', 'Ежемесячно'
    QUARTERLY = 'QUARTERLY', 'Ежеквартально'
    ANNUAL = 'ANNUAL', 'Ежегодно'


class ContractStatus(models.TextChoices):
    """ Статусы контрактов """

    FORMED = 'FORMED', 'Сформирован'
    CONSIDERATION = 'CONSIDERATION', 'На рассмотрении'
    SIGNED = 'SIGNED', 'Подписан'
    FINISHED = 'FINISHED', 'Завершен'
    CANCELED = 'CANCELED', 'Отменен'
    DISSOLVED = 'DISSOLVED', 'Расторгнут'
