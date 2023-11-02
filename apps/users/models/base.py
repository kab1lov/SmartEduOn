__all__ = ('User',)
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.db.models import (CharField,EmailField,BooleanField,DateTimeField,TextChoices,ImageField,DateField,
                              DecimalField,TextField
)

from apps.users.models.manager import BaseManagerUser
from apps.users.services.upload_files import upload_name


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    class Gender(TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')

    # class Job(TextChoices):
    #     DEVELOPER = 'developer', _('Developer')
    #     BUSINESSMAN = 'businessman', _('Businessman')
    #     TEACHER = 'teacher', _('Teacher')
    #     STUDENT = 'student', _('Student')
    #     OTHER = 'other', _('Other')

    first_name = CharField(_("first name"), max_length=150, blank=True)
    last_name = CharField(_("last name"), max_length=150, blank=True)
    phone = CharField(_("phone"), max_length=50, blank=True)
    image = ImageField(upload_to=upload_name, default='user.png')
    balance = DecimalField(_("balance"), max_digits=1000, decimal_places=2, default=0)

    email = EmailField(_("email"),
                       unique=True,
                       help_text=_("Required. exsample@mail.com"),
                       validators=[email_validator],
                       error_messages={"unique": _("A user with that email already exists.")},
                       )

    username = CharField(_("username"),
                         max_length=150,
                         unique=True,
                         help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
                         validators=[username_validator],
                         error_messages={"unique": _("A user with that username already exists.")},
                         )
    gender = CharField(_("gender"), max_length=20, choices=Gender.choices, null=True, blank=True)
    # job = CharField(_("gender"),max_length=20, choices=Job.choices, default=Job.OTHER)
    job = CharField(max_length=255, null=True, blank=True, default='')
    birthday = DateField(_("birthday"), null=True, blank=True)
    about = TextField(_("about"), null=True, blank=True, default='')
    rating = DecimalField(max_digits=5, decimal_places=2, default=0.0)

    is_staff = BooleanField(_("staff status"),
                            default=False,
                            help_text=_("Designates whether the user can log into this admin site."))

    is_active = BooleanField(_("active"),
                             default=True,
                             help_text=_(
                                 "Designates whether this user should be treated as active. "
                                 "Unselect this instead of deleting accounts."))

    is_spiker = BooleanField(_("spiker"),
                             default=False,
                             help_text=_(
                                 "This specifies whether the user should be considered a spiker."
                                 "Unselect this instead of deleting accounts."))

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    objects = BaseManagerUser()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
