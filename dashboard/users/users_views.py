from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, Permission, User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import LoginHistory
from django.utils import timezone
from django.contrib.auth import get_user_model
CustomUserAdd = get_user_model()

from users.forms import (CustomUserForm,
                         CustomCategoryForm,
                         CustomInterestAreaForm,
                         CustomSubCategoryForm,
                         CustomTaxForm,
                         CustomSolutionForm,
                         CustomIndustryFilterForm,
                         SignupForm,
                         LoginForm,
                         GroupForm,
                         PermissionsForm,
                         UserPermissionsForm,
                         EditUserForm,
                         EditCategoryForm,
                         EditSubCategoryForm,
                         EditSolutionForm,
                         EditTaxForm,
                         EditIndustryFilterForm,
                         EditInterestAreaForm
                         )
from users.models import Orders,OrderStoreData,OrderProjectData,OrderProductImages,CustomUser, CustomCategory, CustomSubCategory, CustomSolution, CustomTax, CustomIndustryFilter, \
    CustomInterestArea
from users.tokens import account_activation_token


@login_required(login_url='vora:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Update Successfully')
            return redirect('/password/')
        else:
            messages.warning(request, 'Form is not valid')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'vora/modules/change-password.html', {'form': form, "page_title": "Change Password"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def users(request):
    user_list = CustomUser.objects.filter(type='user',is_superuser=False).order_by('groups__name')
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Users"
    }
    return render(request, "vora/modules/users.html", context)


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def customers(request):
    user_list = CustomUser.objects.filter(type='customer',is_superuser=False).order_by('groups__name')
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "customers"
    }
    return render(request, "vora/modules/customer.html", context)

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def category(request):
    user_list = CustomCategory.objects.order_by('-id').values()
    paginator = Paginator(user_list, 10)  #
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Category"
    }
    return render(request, "vora/modules/category.html", context)

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def login_history(request):
    user_list = CustomUser.objects.filter(is_superuser=False).order_by('groups__name')
    paginator = Paginator(user_list, 10)  #
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "User History",
        "page_no":request.GET.get('page'),
    }
    return render(request, "vora/modules/login_history.html", context)


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def interest_area(request):
    user_list = CustomInterestArea.objects.order_by('-id').values()
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Interest Area"
    }
    return render(request, "vora/modules/interest-area.html", context)


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def industry_filter(request):
    user_list = CustomIndustryFilter.objects.order_by('-id').values()
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Industry Filter"
    }
    return render(request, "vora/modules/industry_filter.html", context)


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def tax(request):
    user_list = CustomTax.objects.order_by('-id').values()
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Tax"
    }
    return render(request, "vora/modules/tax.html", context)


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def solutions(request):
    user_list = CustomSolution.objects.filter(is_active=True).order_by('-id')
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "solutions"
    }
    return render(request, "vora/modules/solutions.html", context)

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def all_orders(request):
    user_list = Orders.objects.order_by('-id')
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "All Orders"
    }
    return render(request, "vora/modules/orders.html", context)    

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def active_orders(request):
    user_list = Orders.objects.filter(order_status='Active').order_by('-id')
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "All Orders"
    }
    return render(request, "vora/modules/orders.html", context)    

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def draft_orders(request):
    user_list = Orders.objects.filter(order_status='Draft').order_by('-id')
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "All Orders"
    }
    return render(request, "vora/modules/orders.html", context)    

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def complete_orders(request):
    user_list = Orders.objects.filter(order_status='Completed').order_by('-id')
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "All Orders"
    }
    return render(request, "vora/modules/orders.html", context)    

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def view_order_solution(request, id):
    order_obj = get_object_or_404(Orders, id=id)
    order_store_data = OrderStoreData.objects.filter(order=id)
    order_project_data = OrderProjectData.objects.filter(order=id)
    order_user = CustomUserAdd.objects.filter(id=order_obj.user.id).values('first_name', 'last_name','gender','city','company','email', 'phone_number', 'address', 'pincode','state','company','gst_in').first()
    
    context = {
        "order_obj": order_obj,
        "order_store_data": order_store_data,
        "order_project_data": order_project_data,
        "order_user":order_user,
        "page_title": "Order Details"
    }

    return render(request, "vora/modules/order-details.html", context)

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def view_customer(request, id):
    order_user = CustomUserAdd.objects.filter(id=id).values('first_name', 'last_name','gender','city','company','email', 'phone_number', 'address', 'pincode','state','company','gst_in').first()
    
    context = {
        "order_user":order_user,
        "page_title": "Customer Details"
    }

    return render(request, "vora/modules/customer-details.html", context)

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def archieved_solutions(request):
    user_list = CustomSolution.objects.filter(is_active=False).order_by('-id')
    paginator = Paginator(user_list, 10)
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "solutions"
    }
    return render(request, "vora/modules/archieved_solutions.html", context)

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def sub_category(request):
    user_list = CustomSubCategory.objects.order_by('-id')
    # print(user_list)
    paginator = Paginator(user_list, 10)
    context = {
        "subcategory_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Sub-Category"
    }
    return render(request, "vora/modules/sub_category.html", context)


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def user_details(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    context = {
        "user_obj": user_obj,
        "user_group_perms": user_obj.get_group_permissions(),
        "user_perms": user_obj.get_user_permissions(),
        "page_title": "User Details"
    }

    return render(request, "vora/modules/user-details.html", context)


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_user(request, id):
    u = CustomUser.objects.get(id=id)
    u.delete()
    messages.success(request, "User deleted successfully")
    return redirect('vora:users')


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_category(request, id):
    u = CustomCategory.objects.get(id=id)
    u.delete()
    messages.success(request, "Category deleted successfully")
    return redirect('vora:category')

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_solution(request, id):
    solution = CustomSolution.objects.get(id=id)
    solution.is_active = not solution.is_active
    solution.save()
    status = "activated" if solution.is_active else "deactivated"
    messages.success(request, f"Solution {status} successfully")
    return redirect('vora:solutions')

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def change_order_status(request, id):
    order = Orders.objects.get(id=id)
    order.order_status = "Completed"
    order.save()
    status = "Completed"
    messages.success(request, f"Order {status} successfully")
    return redirect('vora:all-orders')

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_industry_filter(request, id):
    u = CustomIndustryFilter.objects.get(id=id)
    u.delete()
    messages.success(request, "Industry Filter deleted successfully")
    return redirect('vora:industry-filter')


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_interest_area(request, id):
    u = CustomInterestArea.objects.get(id=id)
    u.delete()
    messages.success(request, "Interest Area deleted successfully")
    return redirect('vora:interest-area')


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_tax(request, id):
    u = CustomTax.objects.get(id=id)
    u.delete()
    messages.success(request, "Tax deleted successfully")
    return redirect('vora:tax')


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_sub_category(request, id):
    u = CustomSubCategory.objects.get(id=id)
    u.delete()
    messages.success(request, "Sub Category deleted successfully")
    return redirect('vora:sub-category')


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_multiple_user(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = CustomUser.objects.get(pk=id)
        user_obj.delete()

    response = JsonResponse({"success": 'user deleted successfully'})
    response.status_code = 200
    return response


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_multiple_category(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = CustomCategory.objects.get(pk=id)
        user_obj.delete()

    response = JsonResponse({"success": 'Category deleted successfully'})
    response.status_code = 200
    return response

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def active_multiple_solution(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:

        solution = CustomSolution.objects.get(pk=id)
        solution.is_active = not solution.is_active
        solution.save()

    response = JsonResponse({"success": 'Solution unarchieved successfully'})
    response.status_code = 200
    return response


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_multiple_industry_filter(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = CustomIndustryFilter.objects.get(pk=id)
        user_obj.delete()

    response = JsonResponse({"success": 'Category deleted successfully'})
    response.status_code = 200
    return response


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_multiple_interest_area(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = CustomInterestArea.objects.get(pk=id)
        user_obj.delete()

    response = JsonResponse({"success": 'Interest Area deleted successfully'})
    response.status_code = 200
    return response


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_multiple_tax(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = CustomTax.objects.get(pk=id)
        user_obj.delete()

    response = JsonResponse({"success": 'Tax deleted successfully'})
    response.status_code = 200
    return response


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_multiple_sub_category(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = CustomSubCategory.objects.get(pk=id)
        user_obj.delete()

    response = JsonResponse({"success": 'Sub Category deleted successfully'})
    response.status_code = 200
    return response


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.add_customuser'}, raise_exception=True)
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save()
            user_obj.groups.clear()
            for i in form.cleaned_data.get('groups'):
                user_obj.groups.add(i)
            messages.success(request, f'{user_obj.first_name} {user_obj.last_name} is created successfully')
            return redirect('vora:users')
    else:
        form = CustomUserForm()
    return render(request, 'vora/modules/add-user.html', {'form': form, "page_title": "Add User",'time':timezone.now()})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.add_customuser'}, raise_exception=True)
def add_solution(request):
    if request.method == 'POST':
        form = CustomSolutionForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            images = request.FILES.getlist("images[]")
            user_obj.image1 = None if len(images) < 1 else images[0]
            user_obj.image2 = None if len(images) < 2 else images[1]
            user_obj.image3 = None if len(images) < 3 else images[2]
            user_obj.image4 = None if len(images) < 4 else images[3]
            user_obj.image5 = None if len(images) < 5 else images[4]
            user_obj.is_active = True
            user_obj.save()
            messages.success(request, f'{user_obj.name} is created successfully')
            return redirect('vora:solutions')
    else:
        form = CustomSolutionForm()
    return render(request, 'vora/modules/add-solution.html', {'form': form, "page_title": "Add solution"})

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def edit_solution(request, id):
    user_obj = get_object_or_404(CustomSolution, id=id)
    if request.method == 'POST':
        form = EditSolutionForm(request.POST,request.FILES,instance=user_obj)
        if form.is_valid():
            user_obj.is_active = True
            user_obj = form.save()
            messages.success(request, f'{user_obj.name} is updated successfully')
            return redirect('vora:solutions')
    else:
        form = EditSolutionForm(instance=user_obj)
    return render(request, 'vora/modules/edit_solution.html', {'form': form, "page_title": "Edit Solution"})

@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.add_customuser'}, raise_exception=True)
def add_category(request):
    if request.method == 'POST':
        form = CustomCategoryForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            messages.success(request, f'{user_obj.category_name} is created successfully')
            return redirect('vora:category')
    else:
        form = CustomCategoryForm()

    return render(request, 'vora/modules/add-category.html', {'form': form, "page_title": "Add Category"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.add_customuser'}, raise_exception=True)
def add_interest_area(request):
    if request.method == 'POST':
        form = CustomInterestAreaForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            messages.success(request, f'{user_obj.interest_area_name} is created successfully')
            return redirect('vora:interest-area')
    else:
        form = CustomInterestAreaForm()

    return render(request, 'vora/modules/add_interest_area.html', {'form': form, "page_title": "Add Interest Area"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.add_customuser'}, raise_exception=True)
def add_industry_filter(request):
    if request.method == 'POST':
        form = CustomIndustryFilterForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            messages.success(request, f'{user_obj.industry_name} is created successfully')
            return redirect('vora:industry-filter')
    else:
        form = CustomIndustryFilterForm()

    return render(request, 'vora/modules/add-industry-filter.html', {'form': form, "page_title": "Add Industry Filter"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.add_customuser'}, raise_exception=True)
def add_tax(request):
    if request.method == 'POST':
        form = CustomTaxForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            messages.success(request, f'{user_obj.tax_name} is created successfully')
            return redirect('vora:tax')
    else:
        form = CustomTaxForm()

    return render(request, 'vora/modules/add-tax.html', {'form': form, "page_title": "Add Tax"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.add_customuser'}, raise_exception=True)
def add_sub_category(request):
    if request.method == 'POST':
        form = CustomSubCategoryForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            messages.success(request, f'{user_obj.sub_category_name} is created successfully')
            return redirect('vora:sub-category')
    else:
        form = CustomSubCategoryForm()

    return render(request, 'vora/modules/add-sub-category.html', {'form': form, "page_title": "Add SUB Category"})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.is_active = False
            user_obj.save()
            # Default Group assign Start -------------------------------------------------------
            if Group.objects.filter(name='Customer'):
                user_obj.groups.add(Group.objects.filter(name='Customer')[0])

            else:
                Customer_group, created = Group.objects.get_or_create(name="Customer")
                # content_type = ContentType.objects.get_for_model(CustomUser)
                # CustomUser_permission = Permission.objects.filter(content_type=content_type)
                # for perm in CustomUser_permission:
                # 	if perm.codename == "view_customuser":
                # 		Customer_group.permissions.add(perm)
                user_obj.groups.add(Customer_group)
            # Default Group assign End-----------------------------------------------------------
            current_site = get_current_site(request)
            subject = 'Activate Your vora Account'
            message = render_to_string('vora/modules/account_activation/account_activation_email.html', {
                'user': user_obj,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
                'token': account_activation_token.make_token(user_obj),
            })
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('first_name')
            ReceiversList = [email]
            EmailSender = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, EmailSender, ReceiversList, fail_silently=False)
                if user_obj.is_active == False:
                    messages.warning(request, 'Please confirm your email address to complete the registration.')
                return redirect('vora:signup')
            except:
                messages.warning(request, 'Email Not valid')
                user_obj.delete()

        else:
            messages.warning(request, 'Form is not valid')
    else:
        if request.user.is_authenticated:
            return redirect('vora:index')
        form = SignupForm()
    return render(request, 'vora/modules/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('vora:index')
    else:
        # return render(request, 'vora/modules/account_activation/account_activation_invalid.html')
        return HttpResponse('Invalid')


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def edit_user(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            user_obj = form.save()
            user_obj.groups.clear()
            for i in form.cleaned_data['groups']:
                user_obj.groups.add(i)
            return redirect('vora:users')
    else:
        form = EditUserForm(instance=user_obj)
    return render(request, 'vora/modules/add-user.html', {'form': form, "page_title": "Edit User"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def edit_category(request, id):
    user_obj = get_object_or_404(CustomCategory, id=id)
    if request.method == 'POST':
        form = EditCategoryForm(request.POST, instance=user_obj)
        if form.is_valid():
            user_obj = form.save()
            return redirect('vora:category')
    else:
        form = EditCategoryForm(instance=user_obj)
    return render(request, 'vora/modules/add-category.html', {'form': form, "page_title": "Edit Category"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def edit_interest_area(request, id):
    user_obj = get_object_or_404(CustomInterestArea, id=id)
    if request.method == 'POST':
        form = EditInterestAreaForm(request.POST, instance=user_obj)
        if form.is_valid():
            user_obj = form.save()
            return redirect('vora:interest-area')
    else:
        form = EditInterestAreaForm(instance=user_obj)
    return render(request, 'vora/modules/add_interest_area.html', {'form': form, "page_title": "Edit Interest Area"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def edit_industry_filter(request, id):
    user_obj = get_object_or_404(CustomIndustryFilter, id=id)
    if request.method == 'POST':
        form = EditIndustryFilterForm(request.POST, instance=user_obj)
        if form.is_valid():
            user_obj = form.save()
            return redirect('vora:industry-filter')
    else:
        form = EditIndustryFilterForm(instance=user_obj)
    return render(request, 'vora/modules/add-industry-filter.html',
                  {'form': form, "page_title": "Edit Industry Filter"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def edit_tax(request, id):
    user_obj = get_object_or_404(CustomTax, id=id)
    if request.method == 'POST':
        form = EditTaxForm(request.POST, instance=user_obj)
        if form.is_valid():
            user_obj = form.save()
            return redirect('vora:tax')
    else:
        form = EditTaxForm(instance=user_obj)
    return render(request, 'vora/modules/add-tax.html', {'form': form, "page_title": "Edit Tax"})


@login_required(login_url='vora:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def edit_sub_category(request, id):
    user_obj = get_object_or_404(CustomSubCategory, id=id)
    if request.method == 'POST':
        form = EditSubCategoryForm(request.POST, instance=user_obj)
        if form.is_valid():
            user_obj = form.save()
            return redirect('vora:sub-category')
    else:
        form = EditSubCategoryForm(instance=user_obj)
    return render(request, 'vora/modules/add-sub-category.html', {'form': form, "page_title": "Edit Category"})

def login_user(request):
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user is not None and user.is_active:
                login(request, user)
                usergroup = ','.join(request.user.groups.values_list('name', flat=True))
                messages.success(request, f'Welcome To {usergroup} Dashborad')
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect('vora:index')
            else:
                messages.warning(request, 'User is Not Active')

        else:
            messages.warning(request, 'Form is Not valid! Please Check The Email and Password')
            return render(request, 'vora/modules/login.html', context={'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('vora:index')
        form = LoginForm()
    return render(request, 'vora/modules/login.html', context={'form': form})


def logout_user(request):
    user = request.user
    login_history = LoginHistory.objects.filter(user=user).latest('login_time')
    login_history.logout_time = timezone.now()
    login_history.save()
    logout(request)
    messages.success(request, 'Logout Successfully')
    return redirect('vora:login')


@login_required(login_url='vora:login')
@permission_required({'auth.view_group'}, raise_exception=True)
def groups_list(request):
    context = {
        "groups": Group.objects.annotate(user_count=Count('customuser', distinct=True)).annotate(
            perms_count=Count('permissions', distinct=True)),
        "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
        "page_title": "Groups"
    }

    return render(request, 'vora/modules/group-list.html', context)


@login_required(login_url='vora:login')
@permission_required({'auth.view_group', 'auth.change_group'}, raise_exception=True)
def group_edit(request, id):
    group_obj = get_object_or_404(Group, id=id)

    if request.method == 'POST':
        queryDict = request.POST
        data = dict(queryDict)

        try:
            group_obj.name = data['name'][0]
            group_obj.save()
        except:
            response = JsonResponse({"error": "Group Name already exist"})
            response.status_code = 403
            return response

        if 'permissions[]' in data:
            group_obj.permissions.clear()
            group_obj.permissions.set(data['permissions[]'])
        else:
            group_obj.permissions.clear()

        response = JsonResponse({"success": "Save Successfully"})
        response.status_code = 200
        return response

    else:
        form = GroupForm(instance=group_obj)

    return render(request, 'vora/modules/group-edit.html', {'form': form, "page_title": "Edit Group"})


@login_required(login_url='vora:login')
@permission_required({'auth.view_group', 'auth.delete_group'}, raise_exception=True)
def group_delete(request, id):
    g = get_object_or_404(Group, id=id)
    g.delete()
    messages.success(request, 'Group Deleted Sucessfully')
    return redirect('vora:groups')


@login_required(login_url='vora:login')
@permission_required({'auth.view_group', 'auth.add_group'}, raise_exception=True)
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group Created Successfully')
            return redirect('vora:groups')
        else:
            messages.warning(request, 'Name Already Exist')
            return render(request, 'vora/modules/group-add.html', {'form': form, 'page_title': 'Add Group'})
    else:
        form = GroupForm()
        return render(request, 'vora/modules/group-add.html', {'form': form, "page_title": "Add Group"})


@login_required(login_url='vora:login')
@permission_required({'auth.view_permission'}, raise_exception=True)
def permissions(request):
    permission_list = Permission.objects.all()
    paginator = Paginator(permission_list, 10)
    context = {
        "permissions_obj": paginator.get_page(request.GET.get('page')),
        "page_title": "Permissions"
    }

    return render(request, 'vora/modules/permissions.html', context)


@login_required(login_url='vora:login')
@permission_required({'auth.view_permission', 'auth.change_permission'}, raise_exception=True)
def edit_permissions(request, id):
    perm_obj = get_object_or_404(Permission, id=id)
    if request.method == 'POST':
        form = PermissionsForm(request.POST, instance=perm_obj)
        if form.is_valid():
            form.save()
            return redirect('vora:permissions')
    else:
        form = PermissionsForm(instance=perm_obj)
        return render(request, 'vora/modules/edit-permissions.html', {'form': form, "page_title": "Edit Permissions"})


@login_required(login_url='vora:login')
@permission_required({'auth.view_permission', 'auth.delete_permission'}, raise_exception=True)
def delete_permissions(request, id):
    perm_obj = get_object_or_404(Permission, id=id)
    perm_obj.delete()
    messages.success(request, 'Permission Delete Successfully')
    return redirect('vora:permissions')


@login_required(login_url='vora:login')
@permission_required({'auth.view_permission', 'auth.add_permission', 'auth.change_permission'}, raise_exception=True)
def assign_permissions_to_user(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        queryDict = request.POST
        data = dict(queryDict)

        if 'user_permissions[]' in data:
            user_obj.user_permissions.clear()
            user_obj.user_permissions.set(data['user_permissions[]'])
        else:
            user_obj.user_permissions.clear()
        response = JsonResponse({"success": "Save Successfully"})
        response.status_code = 200
        return response

    else:
        form = UserPermissionsForm(instance=user_obj)
    return render(request, 'vora/modules/assign_permissions_to_user.html',
                  {'form': form, "page_title": "Assign Permissions"})


# from users import serializers
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        data = serializer.validated_data
        user = serializer.user
        data['id'] = user.id
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        data['company'] = user.company
        data['phone_number'] = user.phone_number
        data['address'] = user.address
        data['city'] = user.city
        data['state'] = user.state
        data['pincode'] = user.pincode
        data['gstin'] = user.gst_in
        
        return Response(data, status=status.HTTP_200_OK)
