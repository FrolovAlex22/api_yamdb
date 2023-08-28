from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^[a-zA-Z0-9]+$'
    message = 'Имя пользователя должно состоять только из букв и цифр'
