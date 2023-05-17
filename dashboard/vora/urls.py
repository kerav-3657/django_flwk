from django.urls import path,include
from vora import vora_views
from users import users_views, users_api_views
from django.contrib import admin
app_name = 'vora'
urlpatterns = [
  path('admin_base/', admin.site.urls),
    # added by raj
    path('api/register', users_api_views.RegisterUserAPIView.as_view()),
    path('api/update_register_data/<int:pk>/', users_api_views.update_register_dataUserAPIView.as_view()),
    path('api/checkEmailWithToken', users_api_views.checkEmailWithToken.as_view()),
    path('api/checkEmailWithSendMail', users_api_views.checkEmailWithSendMail.as_view()),
    path('api/changePassword/<int:pk>/', users_api_views.changePassword.as_view()),
    path('api/changeoldtonewPassword/<int:pk>/', users_api_views.changeoldtonewPassword.as_view()),
    path('api/update_verify_data/<int:pk>/', users_api_views.update_verify_dataUserAPIView.as_view()),
    
    # path('loginapi/', users_api_views.LoginView.as_view()),
    path('api/add-order-detail', users_api_views.CreateOrderAPIView.as_view()),
    path('api/send_mail', users_api_views.send_mail.as_view()),
path('api/active_project_email', users_api_views.active_project_email.as_view()),
path('api/draft_project_email', users_api_views.draft_project_email.as_view()),
path('api/new_project_email', users_api_views.new_project_email.as_view()),

path('api/confirm_send_mail', users_api_views.confirm_send_mail.as_view()),

    path('back/users/', users_views.users, name="users"),
    path('back/customers/', users_views.customers, name="customers"),
    path('back/inactiveCustomers/', users_views.customers, name="inactiveCustomers"),
    path('back/category/', users_views.category, name="category"),
    path('back/user_history/', users_views.login_history, name="login_history"),
    
    path('back/interest-area/', users_views.interest_area, name="interest-area"),
    path('back/industry-filter/', users_views.industry_filter, name="industry-filter"),
    path('back/sub-category/', users_views.sub_category, name="sub-category"),
    path('back/solutions/', users_views.solutions, name="solutions"),
    path('back/all-orders/', users_views.all_orders, name="all-orders"),
    path('back/all-active-orders/', users_views.active_orders, name="all-active-orders"),
    path('back/all-draft-orders/', users_views.draft_orders, name="all-draft-orders"),
    path('back/all-complete-orders/', users_views.complete_orders, name="all-complete-orders"),
    
    path('back/view-order-detail/<int:id>/', users_views.view_order_solution, name="view-order-detail"),
    path('back/view-customer-detail/<int:id>/', users_views.view_customer, name="view-customer-detail"),
    path('back/archieved-solutions/', users_views.archieved_solutions, name="archieved-solutions"),
    path('back/tax/', users_views.tax, name="tax"),

    path('back/user-details/<int:id>/', users_views.user_details, name="user-details"),
    path('back/add-user/', users_views.add_user, name="add-user"),
    path('back/add-category/', users_views.add_category, name="add-category"),

    path('back/add-interest-area/', users_views.add_interest_area, name="add-interest-area"),

    path('back/add-industry-filter/', users_views.add_industry_filter, name="add-industry-filter"),

    path('back/add-solution/', users_views.add_solution, name="add-solution"),

    path('back/add-tax/', users_views.add_tax, name="add-tax"),

    path('back/add-sub-category/', users_views.add_sub_category, name="add-sub-category"),

    path('back/edit-user/<int:id>/', users_views.edit_user, name="edit-user"),
    path('back/edit-solution/<int:id>/', users_views.edit_solution, name="edit-solution"),
    path('back/edit-category/<int:id>/', users_views.edit_category, name="edit-category"),

    path('back/edit-interest-area/<int:id>/', users_views.edit_interest_area, name="edit-interest-area"),

    path('back/edit-sub-category/<int:id>/', users_views.edit_sub_category, name="edit-sub-category"),
    path('back/edit-tax/<int:id>/', users_views.edit_tax, name="edit-tax"),
    path('back/edit-industry-filter/<int:id>/', users_views.edit_industry_filter, name="edit-industry-filter"),

    path('back/delete-user/<int:id>/', users_views.delete_user, name="delete-user"),
    path('back/delete-multiple-user/', users_views.delete_multiple_user, name="delete-multiple-user"),

    path('back/delete-solution/<int:id>/', users_views.delete_solution, name="delete-solution"),
    path('back/change-order-status/<int:id>/', users_views.change_order_status, name="change-order-status"),
    path('back/active-multiple-solution/', users_views.active_multiple_solution, name="active-multiple-solution"),
    path('back/delete-category/<int:id>/', users_views.delete_category, name="delete-category"),
    path('back/delete-industry-filter/<int:id>/', users_views.delete_industry_filter, name="delete-industry-filter"),

    path('back/delete-interest-area/<int:id>/', users_views.delete_interest_area, name="delete-interest-area"),

    path('back/delete-sub-category/<int:id>/', users_views.delete_sub_category, name="delete-sub-category"),
    path('back/delete-tax/<int:id>/', users_views.delete_tax, name="delete-tax"),

    path('back/delete-multiple-category/', users_views.delete_multiple_category, name="delete-multiple-category"),
    path('back/delete-multiple-industry-filter/', users_views.delete_multiple_industry_filter,
         name="delete-multiple-industry-filter"),

    path('back/delete-multiple-interest-area/', users_views.delete_multiple_interest_area,
         name="delete-multiple-interest-area"),

    path('delete-multiple-sub-category/', users_views.delete_multiple_sub_category,
         name="delete-multiple-sub-category"),
    path('delete-multiple-tax/', users_views.delete_multiple_tax, name="delete-multiple-tax"),

    path('admin_login/', users_views.login_user, name="login"),
    path('back/logout/', users_views.logout_user, name="logout"),
    path('back/groups/', users_views.groups_list, name="groups"),
    path('back/group-edit/<int:id>/', users_views.group_edit, name="group-edit"),
    path('back/group-delete/<int:id>/', users_views.group_delete, name="group-delete"),
    path('back/group-add/', users_views.group_add, name="group-add"),
    path('back/permissions/', users_views.permissions, name="permissions"),
    path('back/edit-permissions/<int:id>/', users_views.edit_permissions, name="edit-permissions"),
    path('back/delete-permissions/<int:id>/', users_views.delete_permissions, name="delete-permissions"),
    path('back/assign-permissions-to-user/<int:id>/', users_views.assign_permissions_to_user,
         name="assign-permissions-to-user"),
    path('back/signup/', users_views.signup, name="signup"),
    path('back/activate/<uidb64>/<token>/', users_views.activate, name='activate'),

#    path('', vora_views.index, name="index"),
    path('back/index/', vora_views.index, name="index"),
    path('back/index_2/', vora_views.index_2, name="index_2"),
    path('back/projects/', vora_views.projects, name="projects"),
    path('back/contacts/', vora_views.contacts, name="contacts"),
    path('back/kanban/', vora_views.kanban, name="kanban"),

    path('back/calendar/', vora_views.calendar, name="calendar"),
    path('back/messages/', vora_views.messages, name="messages"),

    path('back/app-profile/', vora_views.app_profile, name="app-profile"),
    path('back/post-details/', vora_views.post_details, name="post-details"),
    path('back/email-compose/', vora_views.email_compose, name="email-compose"),
    path('back/email-inbox/', vora_views.email_inbox, name="email-inbox"),
    path('back/email-read/', vora_views.email_read, name="email-read"),
    path('back/app-calender/', vora_views.app_calender, name="app-calender"),
    path('back/ecom-product-grid/', vora_views.ecom_product_grid, name="ecom-product-grid"),
    path('back/ecom-product-list/', vora_views.ecom_product_list, name="ecom-product-list"),
    path('back/ecom-product-detail/', vora_views.ecom_product_detail, name="ecom-product-detail"),
    path('back/ecom-product-order/', vora_views.ecom_product_order, name="ecom-product-order"),
    path('back/ecom-checkout/', vora_views.ecom_checkout, name="ecom-checkout"),
    path('back/ecom-invoice/', vora_views.ecom_invoice, name="ecom-invoice"),
    path('back/ecom-customers/', vora_views.ecom_customers, name="ecom-customers"),
    path('back/chart-flot/', vora_views.chart_flot, name="chart-flot"),
    path('back/chart-morris/', vora_views.chart_morris, name="chart-morris"),
    path('back/chart-chartjs/', vora_views.chart_chartjs, name="chart-chartjs"),
    path('back/chart-chartist/', vora_views.chart_chartist, name="chart-chartist"),
    path('back/chart-sparkline/', vora_views.chart_sparkline, name="chart-sparkline"),
    path('back/chart-peity/', vora_views.chart_peity, name="chart-peity"),

    path('back/ui-accordion/', vora_views.ui_accordion, name="ui-accordion"),
    path('back/ui-alert/', vora_views.ui_alert, name="ui-alert"),
    path('back/ui-badge/', vora_views.ui_badge, name="ui-badge"),
    path('back/ui-button/', vora_views.ui_button, name="ui-button"),
    path('back/ui-modal/', vora_views.ui_modal, name="ui-modal"),
    path('back/ui-button-group/', vora_views.ui_button_group, name="ui-button-group"),
    path('back/ui-list-group/', vora_views.ui_list_group, name="ui-list-group"),
    path('back/ui-media-object/', vora_views.ui_media_object, name="ui-media-object"),
    path('back/ui-card/', vora_views.ui_card, name="ui-card"),
    path('back/ui-carousel/', vora_views.ui_carousel, name="ui-carousel"),
    path('back/ui-dropdown/', vora_views.ui_dropdown, name="ui-dropdown"),
    path('back/ui-popover/', vora_views.ui_popover, name="ui-popover"),
    path('back/ui-progressbar/', vora_views.ui_progressbar, name="ui-progressbar"),
    path('back/ui-tab/', vora_views.ui_tab, name="ui-tab"),
    path('back/ui-typography/', vora_views.ui_typography, name="ui-typography"),
    path('back/ui-pagination/', vora_views.ui_pagination, name="ui-pagination"),
    path('back/ui-grid/', vora_views.ui_grid, name="ui-grid"),

    path('back/uc-select2/', vora_views.uc_select2, name="uc-select2"),
    path('back/uc-nestable/', vora_views.uc_nestable, name="uc-nestable"),
    path('back/uc-noui-slider/', vora_views.uc_noui_slider, name="uc-noui-slider"),
    path('back/uc-sweetalert/', vora_views.uc_sweetalert, name="uc-sweetalert"),
    path('back/uc-toastr/', vora_views.uc_toastr, name="uc-toastr"),
    path('back/map-jqvmap/', vora_views.map_jqvmap, name="map-jqvmap"),
    path('back/uc-lightgallery/', vora_views.uc_lightgallery, name="uc-lightgallery"),
    path('back/uc-lightgallery/', vora_views.uc_lightgallery, name="uc-lightgallery"),
    path('back/widget-basic/', vora_views.widget_basic, name="widget-basic"),

    path('back/form-element/', vora_views.form_element, name="form-element"),
    path('back/form-wizard/', vora_views.form_wizard, name="form-wizard"),
    path('back/form-editor-ckeditor/', vora_views.form_editor_ckeditor, name="form-editor-ckeditor"),
    path('back/form-pickers/', vora_views.form_pickers, name="form-pickers"),
    path('back/form-validation/', vora_views.form_validation, name="form-validation"),

    path('back/table-bootstrap-basic/', vora_views.table_bootstrap_basic, name="table-bootstrap-basic"),
    path('back/table-datatable-basic/', vora_views.table_datatable_basic, name="table-datatable-basic"),

    path('back/page-lock-screen/', vora_views.page_lock_screen, name="page-lock-screen"),
    path('back/page-error-400/', vora_views.page_error_400, name="page-error-400"),
    path('back/page-error-403/', vora_views.page_error_403, name="page-error-403"),
    path('back/page-error-404/', vora_views.page_error_404, name="page-error-404"),
    path('back/page-error-500/', vora_views.page_error_500, name="page-error-500"),
    path('back/page-error-503/', vora_views.page_error_503, name="page-error-503"),
]
