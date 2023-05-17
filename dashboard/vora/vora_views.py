from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
def index(request):
    user_list = Orders.objects.filter(order_status='Active').order_by('-id')[:10]
    draft_list = Orders.objects.filter(order_status='Draft').order_by('-id')[:10]
    complete_list = Orders.objects.filter(order_status='Completed').order_by('-id')[:10]
    total_active_count = Orders.objects.filter(order_status='Active').order_by('-id').count()
    total_draft_count = Orders.objects.filter(order_status='Draft').order_by('-id').count()
    total_user = CustomUser.objects.filter(is_superuser=False,type='customer').order_by('groups__name').count()
    total_active_solution = CustomSolution.objects.filter(is_active=True).order_by('-id').count()
    # print(user_list)
    paginator = Paginator(user_list, 10)
    draft_paginator = Paginator(draft_list, 10)
    complete_paginator = Paginator(complete_list, 10)
    
    context={
        "user_list": paginator.get_page(request.GET.get('page')),
        "draft_list": draft_paginator.get_page(request.GET.get('page')),
        "complete_list": complete_paginator.get_page(request.GET.get('page')),
        'total_active_count':total_active_count,
        'total_draft_count':total_draft_count,
        'total_user':total_user,
        'total_active_solution':total_active_solution,
        "page_title":"Dashboard"
    }
    return render(request,'vora/index.html',context)


@login_required(login_url='vora:login')
def index_2(request):
    context={
        "page_title":"Dashboard"
    }
    return render(request,'vora/index-2.html',context)

@login_required(login_url='vora:login')
def projects(request):
    context={
        "page_title":"Projects"
    }
    return render(request,'vora/projects.html',context)

@login_required(login_url='vora:login')
def contacts(request):
    context={
        "page_title":"Contacts"
    }
    return render(request,'vora/contacts.html',context)

@login_required(login_url='vora:login')
def kanban(request):
    context={
        "page_title":"Kanban"
    }
    return render(request,'vora/kanban.html',context)


@login_required(login_url='vora:login')
def calendar(request):
    context={
        "page_title":"Calendar"
    }
    return render(request,'vora/calendar.html',context)

@login_required(login_url='vora:login')
def messages(request):
    context={
        "page_title":"Messages"
    }
    return render(request,'vora/messages.html',context)

@login_required(login_url='vora:login')
def app_profile(request):
    context={
        "page_title":"App Profile"
    }
    return render(request,'vora/apps/app-profile.html',context)

@login_required(login_url='vora:login')
def post_details(request):
    context={
        "page_title":"Post Details"
    }
    return render(request,'vora/apps/post-details.html',context)

@login_required(login_url='vora:login')
def email_compose(request):
    context={
        "page_title":"Compose"
    }
    return render(request,'vora/apps/email/email-compose.html',context)

@login_required(login_url='vora:login')
def email_inbox(request):
    context={
        "page_title":"Inbox"
    }
    return render(request,'vora/apps/email/email-inbox.html',context)

@login_required(login_url='vora:login')
def email_read(request):
    context={
        "page_title":"Read"
    }
    return render(request,'vora/apps/email/email-read.html',context)

@login_required(login_url='vora:login')
def app_calender(request):
    context={
        "page_title":"Calendar"
    }
    return render(request,'vora/apps/app-calender.html',context)


@login_required(login_url='vora:login')
def ecom_product_grid(request):
    context={
        "page_title":"Product Grid"
    }
    return render(request,'vora/apps/shop/ecom-product-grid.html',context)

@login_required(login_url='vora:login')
def ecom_product_list(request):
    context={
        "page_title":"Product List"
    }
    return render(request,'vora/apps/shop/ecom-product-list.html',context)

@login_required(login_url='vora:login')
def ecom_product_detail(request):
    context={
        "page_title":"Product Detail"
    }
    return render(request,'vora/apps/shop/ecom-product-detail.html',context)

@login_required(login_url='vora:login')
def ecom_product_order(request):
    context={
        "page_title":"Product Order"
    }
    return render(request,'vora/apps/shop/ecom-product-order.html',context)

@login_required(login_url='vora:login')
def ecom_checkout(request):
    context={
        "page_title":"Checkout"
    }
    return render(request,'vora/apps/shop/ecom-checkout.html',context)

@login_required(login_url='vora:login')
def ecom_invoice(request):
    context={
        "page_title":"Invoice"
    }
    return render(request,'vora/apps/shop/ecom-invoice.html',context)

@login_required(login_url='vora:login')
def ecom_customers(request):
    context={
        "page_title":"Customers"
    }
    return render(request,'vora/apps/shop/ecom-customers.html',context)


@login_required(login_url='vora:login')
def chart_flot(request):
    context={
        "page_title":"Chart Flot"
    }
    return render(request,'vora/charts/chart-flot.html',context)

@login_required(login_url='vora:login')
def chart_morris(request):
    context={
        "page_title":"Chart Morris"
    }
    return render(request,'vora/charts/chart-morris.html',context)

@login_required(login_url='vora:login')
def chart_chartjs(request):
    context={
        "page_title":"Chart Chartjs"
    }
    return render(request,'vora/charts/chart-chartjs.html',context)

@login_required(login_url='vora:login')
def chart_chartist(request):
    context={
        "page_title":"Chart Chartist"
    }
    return render(request,'vora/charts/chart-chartist.html',context)

@login_required(login_url='vora:login')
def chart_sparkline(request):
    context={
        "page_title":"Chart Sparkline"
    }
    return render(request,'vora/charts/chart-sparkline.html',context)

@login_required(login_url='vora:login')
def chart_peity(request):
    context={
        "page_title":"Chart Peity"
    }
    return render(request,'vora/charts/chart-peity.html',context)


@login_required(login_url='vora:login')
def ui_accordion(request):
    context={
        "page_title":"Accordion"
    }
    return render(request,'vora/bootstrap/ui-accordion.html',context)

@login_required(login_url='vora:login')
def ui_alert(request):
    context={
        "page_title":"Alert"
    }
    return render(request,'vora/bootstrap/ui-alert.html',context)

@login_required(login_url='vora:login')
def ui_badge(request):
    context={
        "page_title":"Badge"
    }
    return render(request,'vora/bootstrap/ui-badge.html',context)

@login_required(login_url='vora:login')
def ui_button(request):
    context={
        "page_title":"Button"
    }
    return render(request,'vora/bootstrap/ui-button.html',context)

@login_required(login_url='vora:login')
def ui_modal(request):
    context={
        "page_title":"Modal"
    }
    return render(request,'vora/bootstrap/ui-modal.html',context)

@login_required(login_url='vora:login')
def ui_button_group(request):
    context={
        "page_title":"Button Group"
    }
    return render(request,'vora/bootstrap/ui-button-group.html',context)

@login_required(login_url='vora:login')
def ui_list_group(request):
    context={
        "page_title":"List Group"
    }
    return render(request,'vora/bootstrap/ui-list-group.html',context)


@login_required(login_url='vora:login')
def ui_media_object(request):
    context={
        "page_title":"Media Oobject"
    }
    return render(request,'vora/bootstrap/ui-media-object.html',context)


@login_required(login_url='vora:login')
def ui_card(request):
    context={
        "page_title":"Card"
    }
    return render(request,'vora/bootstrap/ui-card.html',context)

@login_required(login_url='vora:login')
def ui_carousel(request):
    context={
        "page_title":"Carousel"
    }
    return render(request,'vora/bootstrap/ui-carousel.html',context)

@login_required(login_url='vora:login')
def ui_dropdown(request):
    context={
        "page_title":"Dropdown"
    }
    return render(request,'vora/bootstrap/ui-dropdown.html',context)

@login_required(login_url='vora:login')
def ui_popover(request):
    context={
        "page_title":"Popover"
    }
    return render(request,'vora/bootstrap/ui-popover.html',context)

@login_required(login_url='vora:login')
def ui_progressbar(request):
    context={
        "page_title":"Progressbar"
    }
    return render(request,'vora/bootstrap/ui-progressbar.html',context)

@login_required(login_url='vora:login')
def ui_tab(request):
    context={
        "page_title":"Tab"
    }
    return render(request,'vora/bootstrap/ui-tab.html',context)

@login_required(login_url='vora:login')
def ui_typography(request):
    context={
        "page_title":"Typography"
    }
    return render(request,'vora/bootstrap/ui-typography.html',context)

@login_required(login_url='vora:login')
def ui_pagination(request):
    context={
        "page_title":"Pagination"
    }
    return render(request,'vora/bootstrap/ui-pagination.html',context)

@login_required(login_url='vora:login')
def ui_grid(request):
    context={
        "page_title":"Grid"
    }
    return render(request,'vora/bootstrap/ui-grid.html',context)



@login_required(login_url='vora:login')
def uc_select2(request):
    context={
        "page_title":"Select"
    }
    return render(request,'vora/plugins/uc-select2.html',context)

@login_required(login_url='vora:login')
def uc_nestable(request):
    context={
        "page_title":"Nestable"
    }
    return render(request,'vora/plugins/uc-nestable.html',context)

@login_required(login_url='vora:login')
def uc_noui_slider(request):
    context={
        "page_title":"UI Slider"
    }
    return render(request,'vora/plugins/uc-noui-slider.html',context)

@login_required(login_url='vora:login')
def uc_sweetalert(request):
    context={
        "page_title":"Sweet Alert"
    }
    return render(request,'vora/plugins/uc-sweetalert.html',context)

@login_required(login_url='vora:login')
def uc_toastr(request):
    context={
        "page_title":"Toastr"
    }
    return render(request,'vora/plugins/uc-toastr.html',context)

@login_required(login_url='vora:login')
def map_jqvmap(request):
    context={
        "page_title":"Jqvmap"
    }
    return render(request,'vora/plugins/map-jqvmap.html',context)

@login_required(login_url='vora:login')
def uc_lightgallery(request):
    context={
        "page_title":"LightGallery"
    }
    return render(request,'vora/plugins/uc-lightgallery.html',context)

@login_required(login_url='vora:login')
def widget_basic(request):
    context={
        "page_title":"Widget"
    }
    return render(request,'vora/widget-basic.html',context)

@login_required(login_url='vora:login')
def form_element(request):
    context={
        "page_title":"Form Element"
    }
    return render(request,'vora/forms/form-element.html',context)

@login_required(login_url='vora:login')
def form_wizard(request):
    context={
        "page_title":"Form Wizard"
    }
    return render(request,'vora/forms/form-wizard.html',context)

@login_required(login_url='vora:login')
def form_editor_ckeditor(request):
    context={
        "page_title":"CkEditor"
    }
    return render(request,'vora/forms/form-editor-ckeditor.html',context)

@login_required(login_url='vora:login')
def form_pickers(request):
    context={
        "page_title":"Pickers"
    }
    return render(request,'vora/forms/form-pickers.html',context)

@login_required(login_url='vora:login')
def form_validation(request):
    context={
        "page_title":"Form Validation"
    }
    return render(request,'vora/forms/form-validation.html',context)

@login_required(login_url='vora:login')
def table_bootstrap_basic(request):
    context={
        "page_title":"Table Bootstrap"
    }
    return render(request,'vora/table/table-bootstrap-basic.html',context)

@login_required(login_url='vora:login')
def table_datatable_basic(request):
    context={
        "page_title":"Table Datatable"
    }
    return render(request,'vora/table/table-datatable-basic.html',context)






def page_lock_screen(request):
    return render(request,'vora/pages/page-lock-screen.html')

def page_error_400(request):
    return render(request,'400.html')
    
def page_error_403(request):
    return render(request,'403.html')

def page_error_404(request):
    return render(request,'404.html')

def page_error_500(request):
    return render(request,'500.html')

def page_error_503(request):
    return render(request,'503.html')














