from django.db import models


class SectionActionStatus(models.TextChoices):
    """ Статус посещения раздела """

    ATTENDED = 'ATTENDED', 'Посещено'
    ABSENT = 'ABSENT', 'Отсутствие'
    PERMITTED = 'PERMITTED', 'Разрешено'
    LATE = 'LATE', 'Опоздание'
    LEFT = 'LEFT', 'Покинул занятие'

    @classmethod
    def get_choices(cls):
        return [status for status in cls.choices]
