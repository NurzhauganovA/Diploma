import random
from django.core.mail import send_mail
from django.core.cache import cache
from django.db import transaction

from diploma import settings


def generate_random_code():
    random_code = random.randint(1000, 9999)

    return random_code


def save_generated_code_to_cache(cache_key, email, code):
    cache.set(f'{cache_key}_{email}', code, timeout=60 * 5)
    print(cache.get(f'{cache_key}_{email}'))

    return email


def send_email(email, subject, message):
    random_code = generate_random_code()

    # send_mail(
    #     subject=subject,
    #     message=f'{message}: {random_code}',
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=[email]
    # )

    saved = save_generated_code_to_cache('verify', email, random_code)

    return saved


def verify_account(email, code):
    cache_code = cache.get(f'verify_{email}')
    print(cache_code)

    if cache_code is not None and cache_code == code:
        return True

    return False
