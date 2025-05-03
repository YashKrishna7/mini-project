from django.db import models
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth.models import AbstractUser,Group,Permission
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        extra_fields.setdefault('user_type', 'student')  # Default to 'student'
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'admin')  # Force 'admin' for superusers
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(username, password, **extra_fields)

class User(AbstractUser):
    USER_TYPES = [
        ('student', 'Student'),
        ('college_admin', 'College Admin'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    # Set the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username


# class User(AbstractUser):
#     USER_TYPES = [
#         ('student', 'Student'),
#         ('college_admin', 'College Admin'),
#         ('admin', 'Admin'),
#     ]
#     user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
#     # Additional fields
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
    
#     groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
#     user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
    
#     def __str__(self):
#         return self.username

# Automatically create a Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Ensure Profile model exists to create
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Optional: For tracking login attempts (useful for security)
class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    user_agent = models.TextField(blank=True)
    
    def __str__(self):
        status = "Successful" if self.successful else "Failed"
        return f"{status} login attempt for {self.user} from {self.ip_address}"

# Profile model (optional, assuming it’s referenced in the above code)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional profile-specific fields here
    # e.g., profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"



# class Menu(models.Model):
#     CATEGORY_CHOICES = [
#         ('breakfast', 'Breakfast'),
#         ('lunch', 'Lunch'),
#         ('snacks', 'Snacks'),
#         ('dinner', 'Dinner'),
#     ]

#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
#     available = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
class Menu(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
    ]

    day = models.CharField(max_length=100, choices=DAYS_OF_WEEK)  # <-- Add choices here for clarity
    name = models.CharField(max_length=100)  # <- You missed this field
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name


User = get_user_model()
class Order(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    menu_item = models.ForeignKey('Menu', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)
    is_in_option = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.student.username} - {self.menu_item.name} - {self.order_date}"
