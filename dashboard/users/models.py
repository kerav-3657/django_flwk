from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group
from django.template.defaultfilters import slugify
from django.utils import timezone

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        super_user = self.create_user(email, first_name, last_name, password, **other_fields)

        return super_user

    def create_user(self, email, first_name, last_name, password, **other_fields):
        # email validation
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'{instance.email}/{filename}'


# This is the new custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('', 'Choose gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, default="profile/image/default.gif")
    dob = models.CharField(max_length=150, blank=True, null=True, help_text="Pattern = dd-mm-yyyy")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    company = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=1500, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    pincode = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True)
    about = models.TextField(_('about'), max_length=500, blank=True)
    gst_in = models.CharField(max_length=150, blank=True, null=True)
    type=models.CharField(max_length=150, blank=True,  default="user")
    random_number=models.CharField(max_length=150, blank=True,  default="")
    is_verified=models.BooleanField(max_length=150, blank=True,  default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    create_date_time = models.DateTimeField(null=True, blank=True)
    

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def get_image_filename(instance, filename):
    title = instance.name
    slug = slugify(title)
    return "solution_images/%s-%s" % (slug, filename)


# This is the new custom user model
class CustomSolution(AbstractBaseUser):
    name = models.CharField(max_length=150, blank=True)
    url_structure = models.CharField(max_length=150, blank=True)
    price = models.CharField(max_length=150, blank=True)
    category = models.ForeignKey('CustomCategory', on_delete=models.CASCADE, )
    sub_category = models.ForeignKey('CustomSubCategory', on_delete=models.CASCADE, )
    tax = models.ForeignKey('CustomTax', on_delete=models.CASCADE, )
    about = models.CharField(max_length=100000, blank=True)
    overview = models.CharField(max_length=100000, blank=True)
    how_it_work = models.CharField(max_length=100000, blank=True)
    execution_time = models.CharField(max_length=100000, blank=True)
    short_description = models.CharField(max_length=100000, blank=True, default='')
    is_active = models.BooleanField(default=False)
    image = models.ImageField(verbose_name='Image', null=False, blank=False)
    image1 = models.FileField(verbose_name='Image1', null=True, blank=True)
    image2 = models.FileField(verbose_name='Image2', null=True, blank=True)
    image3 = models.FileField(verbose_name='Image3', null=True, blank=True)
    image4 = models.FileField(verbose_name='Image4', null=True, blank=True)
    image5 = models.FileField(verbose_name='Image5', null=True, blank=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['name', 'price','url_structure']

    def return_all_images(self):
        return [self.image1, self.image2, self.image3, self.image4, self.image5]

    def __str__(self):
        return f"{self.name}"


class sendMail(models.Model):
    email = models.CharField(max_length=255,blank=True)
    subject = models.CharField(max_length=255,blank=True)
    message = models.CharField(max_length=100000,blank=True)
    status = models.CharField(max_length=255,blank=True)
    name = models.CharField(max_length=255,blank=True)

class DraftsendMail(models.Model):
    solution_name = models.CharField(max_length=255,blank=True)
    number_of_audit = models.CharField(max_length=255,blank=True)
    started_date = models.CharField(max_length=255,blank=True)
    message = models.CharField(max_length=255,blank=True)
    
class NewPrjsendMail(models.Model):
    solution_name = models.CharField(max_length=255,blank=True)
    number_of_audit = models.CharField(max_length=255,blank=True)
    started_date = models.CharField(max_length=255,blank=True)
    message = models.CharField(max_length=255,blank=True)
    name = models.CharField(max_length=255,blank=True)
    

class LoginHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=255,blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

class UserHistory(models.Model):
    message = models.CharField(max_length=255,blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    
class CustomCategory(models.Model):
    category_name = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=False)  # this false work on ui not in admin
    # when user is created, than system send a email after varify  user is active
    USERNAME_FIELD = 'category_name'
    REQUIRED_FIELDS = ['category_name']

    def __str__(self):
        return f"{self.category_name}"


class CustomInterestArea(models.Model):
    interest_area_name = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=False)  # this false work on ui not in admin
    # when user is created, than system send a email after varify  user is active
    USERNAME_FIELD = 'interest_area_name'
    REQUIRED_FIELDS = ['interest_area_name']

    def __str__(self):
        return f"{self.interest_area_name}"


class CustomIndustryFilter(models.Model):
    industry_name = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=False)  # this false work on ui not in admin
    # when user is created, than system send a email after varify  user is active
    USERNAME_FIELD = 'industry_name'
    REQUIRED_FIELDS = ['industry_name']

    def __str__(self):
        return f"{self.industry_name}"


class CustomTax(models.Model):
    tax_name = models.CharField(max_length=500, blank=True)
    add_tax = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=False)  # this false work on ui not in admin
    # when user is created, than system send a email after varify  user is active
    USERNAME_FIELD = 'tax_name'
    REQUIRED_FIELDS = ['tax_name', 'add_tax']

    def __str__(self):
        return f"{self.tax_name} ({self.add_tax} %)"


class CustomSubCategory(models.Model):
    category_name = models.ForeignKey('CustomCategory', on_delete=models.CASCADE, )
    sub_category_name = models.CharField(max_length=500, blank=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sub_category_name}"

class Orders(models.Model):
    order_id = models.CharField(max_length=1000, null=True, blank=True)
    order_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey('CustomCategory', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('CustomSubCategory', on_delete=models.CASCADE)
    solution = models.ForeignKey('CustomSolution', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=1000, null=False, blank=False)
    industry_selection = models.CharField(max_length=1000, null=False, blank=False, default='')
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    audience_preference = models.BooleanField(default=False)
    age_range = models.CharField(max_length=1000, null=True, blank=True)
    occupation = models.CharField(max_length=1000, null=True, blank=True)
    income_range = models.CharField(max_length=1000, null=True, blank=True)
    car_price_range = models.CharField(max_length=1000, null=True, blank=True)
    interest_area = models.CharField(max_length=1000, null=True, blank=True)
    total_responses = models.IntegerField(default=0)
    solution_price = models.FloatField(default=0.0)
    subtotal = models.FloatField(default=0.0)
    tax_per = models.IntegerField(default=0)
    total_tax = models.FloatField(default=0.0)
    final_total = models.FloatField(default=0.0)
    order_status = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.project_name} - {self.start_date} - {self.end_date} - {self.audience_preference} - {self.age_range} - {self.occupation} - {self.income_range} - {self.car_price_range} - {self.interest_area}"

class OrderProjectData(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_project_data')
    product_desc = models.CharField(max_length=1000, null=True, blank=True)
    product_brand = models.CharField(max_length=1000, null=True, blank=True)
    product_name = models.CharField(max_length=1000, null=True, blank=True)    

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'{instance.email}/{filename}'

class OrderProductImages(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_product_data',default=1)
    image = models.ImageField(upload_to='order_product_images/',default='default.jpg')
    created_at = models.DateTimeField(default=timezone.now)

class OrderStoreData(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_store_data')
    store_name = models.CharField(max_length=1000, null=True, blank=True)
    store_address = models.CharField(max_length=1000, null=True, blank=True)
    store_city = models.CharField(max_length=1000, null=True, blank=True)
    store_state = models.CharField(max_length=1000, null=True, blank=True)
    store_postalcode = models.IntegerField(default=0)
    store_responses = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

