from api_yamdb.settings import DEFAUTL_FROM_EMAIL

from django.core.mail import send_mail


def send_mail_to_user(email, confirmation_code):
    send_mail(
        subject='Регистрация на "YaMDB", код подтверждения.',
        message='Благодарим за регистрацию на нашем портале.'
        f'Код подтверждения: {confirmation_code}',
        from_email=DEFAUTL_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
