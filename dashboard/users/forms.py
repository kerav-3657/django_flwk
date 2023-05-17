from django import forms
from users.models import CustomUser
from users.models import CustomSolution
from users.models import CustomCategory
from users.models import CustomTax
from users.models import CustomSubCategory
from users.models import CustomInterestArea
from users.models import CustomIndustryFilter
from users.models import LoginHistory

from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from django_summernote.widgets import SummernoteWidget
from django.forms import ClearableFileInput
from django.utils import timezone


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2',
                  )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Add User Form
class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    dob = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    
    GENDER_CHOICES = (
        ('', 'Choose gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'gender',
                  'avatar',
                  'dob',
                  'phone_number',
                  'groups',
                  'about',
                  'address',
                  'is_active',
                  'password1',
                  'password2',
                  'create_date_time',
                  'type'
                  )
        widgets = {
            'avatar': forms.FileInput(),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Add User Form
class CustomSolutionForm(forms.ModelForm):
    name = forms.CharField(required=True)
    price = forms.CharField(required=True)
    url_structure = forms.CharField(required=True)
    about = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    overview = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    how_it_work = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    execution_time = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    short_description = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    image = forms.ImageField(label='Image')

    class Meta:
        model = CustomSolution
        fields = ('name',
                  'price',
                  'url_structure',
                  'category',
                  'sub_category',
                  'tax',
                  'about',
                  'overview',
                  'how_it_work',
                  'execution_time',
                  'short_description',
                  'is_active',
                  'image'
                  
                  )
        # widgets = {
        #     'image1': ClearableFileInput(attrs={"multiple": False}),

        # }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class EditSolutionForm(forms.ModelForm):
    name = forms.CharField(required=True)
    price = forms.CharField(required=True)
    url_structure = forms.CharField(required=True)
    about = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    overview = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    how_it_work = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    execution_time = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    short_description = forms.CharField(required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%'}}))
    image = forms.ImageField(label='Image')

    class Meta:
        model = CustomSolution
        fields = ('name',
                  'price',
                  'url_structure',
                  'category',
                  'sub_category',
                  'tax',
                  'about',
                  'overview',
                  'how_it_work',
                  'execution_time',
                  'short_description',
                  'is_active',
                  'image',
                  'image1',
                  'image2',
                  'image3',
                  'image4',
                  'image5',
                  
                  )
       

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save()
        return user


class CustomCategoryForm(forms.ModelForm):
    category_name = forms.CharField(required=True)

    class Meta:
        model = CustomCategory
        fields = ('category_name',
                  )
        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomInterestAreaForm(forms.ModelForm):
    interest_area_name = forms.CharField(required=True)

    class Meta:
        model = CustomInterestArea
        fields = ('interest_area_name',
                  )
        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomIndustryFilterForm(forms.ModelForm):
    industry_name = forms.CharField(required=True)

    class Meta:
        model = CustomIndustryFilter
        fields = ('industry_name',
                  )
        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomTaxForm(forms.ModelForm):
    tax_name = forms.CharField(required=True)
    add_tax = forms.CharField(required=True)

    class Meta:
        model = CustomTax
        fields = ('tax_name',
                  'add_tax',
                  )
        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomSubCategoryForm(forms.ModelForm):
    # category_name = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    # sub_category_name = forms.CharField(required=True)

    class Meta:
        model = CustomSubCategory
        fields = ('category_name', 'sub_category_name',)
        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    dob = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)

    GENDER_CHOICES = (
        ('', 'Choose gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'gender',
                  'avatar',
                  'dob',
                  'phone_number',
                  'groups',
                  'about',
                  'address',
                  'city',
                  'state',
                  'pincode',
                  'is_active',
                  )

        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save()
        return user


class EditTaxForm(forms.ModelForm):
    # tax_name = forms.CharField(required=True)
    # add_tax = forms.CharField(required=True)

    class Meta:
        model = CustomTax
        fields = ('tax_name',
                  'add_tax',
                  )
        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save()
        return user


class EditCategoryForm(forms.ModelForm):
    category_name = forms.CharField(required=True)

    class Meta:
        model = CustomCategory
        fields = ('category_name',
                  'is_active',
                  )

        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save()
        return user


class EditInterestAreaForm(forms.ModelForm):
    interest_area_name = forms.CharField(required=True)

    class Meta:
        model = CustomInterestArea
        fields = ('interest_area_name',
                  'is_active',
                  )

        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save()
        return user


class EditIndustryFilterForm(forms.ModelForm):
    industry_name = forms.CharField(required=True)

    class Meta:
        model = CustomIndustryFilter
        fields = ('industry_name',
                  'is_active',
                  )

        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save()
        return user


class EditSubCategoryForm(forms.ModelForm):
    # GENDER_CHOICES = (
    #     ('', 'Choose Category'),
    #     ('25', 'First'),
    #     ('26', 'Second'),
    # )
    # category_name = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    # sub_category_name = forms.CharField(required=True)

    class Meta:
        model = CustomSubCategory
        fields = ('category_name',
                  'sub_category_name',
                  'is_active',
                  )

        widgets = {
            'avatar': forms.FileInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save()
        return user




class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            username = user.first_name + ' ' + user.last_name
            LoginHistory.objects.create(user=user,username=username)
        return user


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")
        return email


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')


class PermissionsForm(forms.ModelForm):
    name = forms.CharField(label='Name', help_text="Example: Can action modelname")
    codename = forms.CharField(label='Code Name', help_text="Example: action_modelname")

    class Meta:
        model = Permission
        fields = ('name', 'codename', 'content_type')


class UserPermissionsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('user_permissions',)
