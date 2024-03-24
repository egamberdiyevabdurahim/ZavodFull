from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# from Post.models import Xodim


class User(AbstractUser):
    GENDER = (
        ('Erkak', 'Erkak'),
        ('Ayol', 'Ayol'),
        ('Null', 'Null'),
    )

    is_direktor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_tekshiruvchi = models.BooleanField(default=False)
    is_bulim = models.BooleanField(default=False)
    is_xodim = models.BooleanField(default=True)
    phone = models.CharField(max_length=14, null=True, blank=True)
    photo = models.ImageField(upload_to='user_photo/', default='base.jpg')
    gender = models.CharField(max_length=10, choices=GENDER, default='Null')
    # status = models.CharField(max_length=12, choices=STATUS, default='Tekshiruvchi')

    def __str__(self):
        return f'{self.first_name}/{self.username}'


class Ish_Turi(models.Model):
    name = models.CharField(max_length=40, unique=True)
    ish_id = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return f'{self.name}/{self.ish_id}'


class Bulim(models.Model):
    name = models.CharField(max_length=90, unique=True)
    bulim_id = models.CharField(max_length=9, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}/{self.bulim_id}/{self.user}'


class Xodim(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='xodim_user')
    ish_turi = models.ManyToManyField(Ish_Turi, related_name='xodim_ish_turi')
    bulimi = models.ForeignKey(Bulim, on_delete=models.CASCADE, related_name='xodim_bulim', null=True)

    # def __str__(self):
    #     return f'{self.user.username}/{self.user.first_name}'


@receiver(post_save, sender=User)
def create_xodim(sender, instance, created=False, **kwargs):
    if created:
        if instance.is_xodim==True:
            xodim = Xodim.objects.create(user=instance)
            return xodim
        else:
            return False
    else:
        return False