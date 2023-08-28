import random
from string import ascii_letters, digits

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from users.models import User


def sender_confirmation_code(request):
    user = get_object_or_404(User, username=request.data.get('username'))
    confirmation_code = random.choices(
        ascii_letters + digits,
        k=settings.CONFIRM_CODE_LEN
    )
    user.confirmation_code = ''.join(confirmation_code)
    user.save()
    send_mail(
        'Код подтвержения',
        f'Ваш код: {user.confirmation_code}',
        settings.NO_REPLY_MAIL,
        [request.data.get('email')],
        fail_silently=False,
    )
