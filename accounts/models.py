from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


class MagicLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='magic_links')
    token = models.CharField(max_length=64, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)

    def gerar_token(self):
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits
        self.token = ''.join(secrets.choice(alphabet) for _ in range(40))

    def is_valido(self):
        if self.usado:
            return False
        limite = self.criado_em + timedelta(minutes=15)
        return timezone.now() < limite

    def __str__(self):
        return f'{self.user.username} - {self.criado_em}'
