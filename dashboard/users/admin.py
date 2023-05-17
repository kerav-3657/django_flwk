from django.contrib import admin
from users.models import CustomUser, CustomCategory, CustomInterestArea, CustomIndustryFilter, CustomTax, \
    CustomSolution, CustomSubCategory
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('about','overview','how_it_work','execution_time','short_description')

class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('email', 'first_name', 'last_name', 'gender')
    list_filter = ('email', 'first_name', 'last_name', 'gender', 'is_active', 'is_staff')
    ordering = ('-dob',)
    list_display = ('email', 'first_name', 'last_name', 'gender', 'company', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'company', 'gender', 'avatar', 'dob')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Personal', {'fields': ('phone_number', 'about',)}),
    )

    formfield_overrides = {
        CustomUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'phone_number', 'first_name', 'last_name', 'gender', 'avatar', 'dob', 'password1', 'password2',
                'is_active', 'is_staff', 'groups', 'user_permissions')
        }
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(CustomCategory)
admin.site.register(CustomInterestArea)
admin.site.register(CustomIndustryFilter)
admin.site.register(CustomTax)
admin.site.register(CustomSolution,PostAdmin)
admin.site.register(CustomSubCategory)
# Register your models here.
