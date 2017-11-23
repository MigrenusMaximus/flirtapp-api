from FlirtAPI.settings import BASE_DIR, STATIC_URL, STATIC_ROOT, SELFIE_URL # MEDIA_URL, MEDIA_ROOT, 
from django.db import models
from django.utils.timezone import now
from datetime import date
import os


LAST_CLEAN_TIME = None
ONE_DAY_IN_SECONDS = 60 * 60 * 24


def selfie_directory(instance, filename):
    return SELFIE_URL + '/' + instance.imei + '.' + filename.split('.')[-1]
    # return '/'.join(STATIC_ROOT, instance.imei, 'selfie.' + filename.split('.')[-1])
    # return os.path.join(MEDIA_URL, 'user_%s' % instance.imei, filename)


class Message(models.Model):
    message_text = models.CharField(max_length=255, unique=True, blank=False, null=False)
    
    def __str__(self):
        return self.message_text


# TODO: Implement session keys instead of boolean for authentication and auth status
# TODO: Implement session key expiration
class User(models.Model):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None'),
    )

    imei = models.CharField(max_length=16, unique=True, blank=False, primary_key=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=False)
    time_of_creation = models.DateTimeField(null=False, blank=False, default=now)
    liked_users = models.ManyToManyField('self', symmetrical=False, related_name='selected_users', blank=True)
    photo = models.ImageField(upload_to=selfie_directory, blank=True, null=True)
    imei_hash = models.CharField(max_length=255, blank=False, null=False, default='default_hash')
    is_authenticated = models.BooleanField(blank=False, null=False, default=False)
    # session_key = models.CharField(max_length=255, unique=False, blank=False, null=True)
    fcm_id = models.CharField(max_length=255, blank=True, null=True)
    login_time = models.IntegerField(blank=True, null=False, default=0)
    last_check = models.IntegerField(blank=True, null=False, default=0)

    def get_matches(self):
        return list(self.liked_users.filter(liked_users__imei__contains=self.imei).values_list('imei', flat=True))

    def __str__(self):
        return self.gender + ' - ' + self.imei


class Place(models.Model):
    # apparently, place_ids have been reported
    # to be as long as 172 chars, hence the max_length
    place_id = models.CharField(max_length=255, primary_key=True, null=False, blank=False, default='null_id')
    name = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=40, blank=False, null=False)
    # max length of 20 is pretty generous,
    # but better to be on the safe side
    latitude = models.DecimalField(max_digits=15, decimal_places=10, blank=False)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, blank=False)
    current_users = models.ManyToManyField('User', blank=True)

    def add_user(self, user):
        self.current_users.add(user)

    def __str__(self):
        return self.name


class Statistics(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=False, blank=False, default=date.today)
    total_logins = models.IntegerField()
    total_matches = models.IntegerField()

    def __str__(self):
        return self.id + ' - ' + self.date


def clean_db():
    for message in Message.objects.all():
        if now().timestamp() - message.time_created.timestamp() > ONE_DAY_IN_SECONDS:
            message.delete()

# loop = asyncio.get_event_loop()
# loop.run_forever(asyncio.ensure_future(db_manager()))
