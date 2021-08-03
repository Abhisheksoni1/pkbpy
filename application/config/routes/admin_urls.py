from django.urls import path
from apps.authentiation import views as admin
from pkbadmin.views import dashboard_view as dashboard, contact_view as contact
from pkbadmin.views import group_views as groups
from pkbadmin.views import faqs_view as faqs
from django.views.generic.base import TemplateView
from pkbadmin.views import page_view as page
from pkbadmin.views import promo_view as promo
# from django.conf import settings
# from django.conf.urls.static import static
from pkbadmin.views import categories_views as categories
from pkbadmin.views import stores_views as stores
from pkbadmin.views import kitchens_views as kitchens
from pkbadmin.views import items_views as items
from pkbadmin.views import client_views as clients
from pkbadmin.views import manager_views as managers
from pkbadmin.views import order_views as orders
from pkbadmin.views import discount_views as discount
from pkbadmin.views import tax_views as tax
from pkbadmin.views import user_views as user
from pkbadmin.views import feedback_views as feedback
from pkbadmin.views import financial_year_views as fyear
from pkbadmin.views import notification_views as notifications
from pkbadmin.views import timingsOnOff as time
from pkbadmin.views import promo_code_view as promocode
from pkbadmin.views import delivery_boy_view as delivery
from pkbadmin.views import managepoints_views

app_name = 'custom-admin'

urlpatterns = [
    path('', dashboard.DashboardIndex.as_view(), name="index"),
    path('404-Error/', admin.erro_404, name='error_404'),
    path('login/', admin.auth_login, name='auth_login'),
    path('forget_password/', admin.UserPasswordForgot.as_view(), name='auth_forget'),
    path('reset-password/', admin.UserPasswordConfirm.as_view(), name='auth_confirm'),
    path('logout/', admin.auth_logout, name='auth_logout'),
    path('dashboard/', dashboard.DashboardIndex.as_view(), name="index_dashboard"),
    path('register-verify/', admin.UserRegisterVerify, name='sign-up-verify'),
    path('change-password/', admin.ChangePassword.as_view(), name='auth_change_password'),
    path('user-profile/<int:pk>/', admin.UserProfile.as_view(), name='user_profile'),
    path('user-profile/get/', admin.GetOrders.as_view(), name="get_profile_orders"),

    # Contact Management urls
    path('contact/', contact.ContactIndex.as_view(), name="contact_index"),
    path('contact/create/', contact.AddContact.as_view(), name="add_contact"),
    path('contact/edit/<int:pk>/', contact.UpdateContact.as_view(), name='edit_contact'),
    path('contact/delete/<int:pk>/', contact.DeleteContact.as_view(), name='delete_contact'),
    path('contact/get/', contact.ContactGet.as_view()),

    # Group Management urls
    path('groups/', view=groups.GroupsIndex.as_view(), name='group_index'),
    path('groups/create/', view=groups.AddGroup.as_view(), name='add_group'),
    path('groups/edit/<int:pk>/', view=groups.UpdateGroup.as_view(), name='update_group'),
    path('groups/delete/<int:pk>/', groups.DeleteGroup.as_view(), name='delete_group'),
    path('groups/get/', groups.GetGroups.as_view()),

    # Client Management urls
    path('clients/', clients.ClientIndex.as_view(), name='client_index'),
    path('clients/create/', clients.AddClient.as_view(), name='add_client'),
    path('clients/detail/<int:pk>', clients.DetailClient.as_view(), name='detail_client'),
    path('clients/edit/<int:pk>/', clients.UpdateClient.as_view(), name='edit_client'),
    path('clients/delete/<int:pk>/', clients.DeleteClient.as_view(), name='delete_client'),
    path('clients/get/', clients.ClientGet.as_view()),

    # Managers Management urls
    path('manager/', managers.ManagerIndex.as_view(), name='manager_index'),
    path('manager/create/', managers.AddManager.as_view(), name='add_manager'),
    path('manager/profile/<int:pk>', managers.ManagerProfile.as_view(), name='detail_manager'),
    path('manager/edit/<int:pk>/', managers.UpdateManager.as_view(), name='edit_manager'),
    path('manager/delete/<int:pk>/', managers.DeactivateManager.as_view(), name='delete_manager'),
    path('manager/get/', managers.GetManager.as_view()),
    path('manager/get/stores/', managers.GetStores.as_view()),
    path('manager/get/kitchens/', managers.GetKitchens.as_view()),
    path('manager/get/update_manager_status/', managers.UpdateManagerStatus.as_view(), name='update_manager_status'),

    # FAQ's Management urls
    path('faqs/', view=faqs.FaqsIndex.as_view(), name='faqs_index'),
    path('faqs/get/', view=faqs.GetFaqs.as_view()),
    path('faqs/create/', view=faqs.AddFaqs.as_view(), name="add_faqs"),
    path('faqs/edit/<int:pk>/', view=faqs.UpdateFaqs.as_view(), name='edit_faqs'),
    path('faqs/delete/<int:pk>/', view=faqs.DeleteFaqs.as_view(), name='delete_faqs'),

    # Page Management urls
    path('pages/', view=page.PageIndex.as_view(), name='page_main'),
    path('pages/create/', view=page.AddPage.as_view(), name='add_page'),
    path('pages/edit/<int:pk>/', view=page.UpdatePage.as_view(), name='edit_page'),
    path('pages/delete/<int:pk>/', view=page.DeletePage.as_view(), name='delete_page'),
    path('pages/get/', view=page.GetPage.as_view(), name='get_page'),

    # Promo Management urls
    path('promo-banners/', view=promo.PromoBannersIndex.as_view(), name='promo_banner'),
    path('promo-banners/create/', view=promo.AddPromoBanner.as_view(), name='add_promo_banner'),
    path('promo-banners/edit/<int:pk>/', view=promo.UpdatePromoBanner.as_view(), name='edit_promo-banner'),
    path('promo-banners/delete/<int:pk>/', view=promo.DeletePromoBanner.as_view(), name='delete_promo-banner'),
    path('promo-banners/get/', view=promo.GetPromoBanners.as_view(), name='get_promo-banners'),

    # Stores Managements urls
    path('stores/', view=stores.StoresIndex.as_view(), name='stores_index'),
    path('stores/get/', view=stores.GetStores.as_view(), name='get_stores'),
    path('stores/create/', view=stores.AddStore.as_view(), name='add_stores'),
    path('stores/edit/<int:pk>/', view=stores.UpdateStore.as_view(), name='edit_stores'),
    path('stores/detail/<int:pk>', view=stores.DetailStore.as_view(), name='detail_stores'),
    path('stores/delete/<int:pk>/', view=stores.DeleteStores.as_view(), name='delete_stores'),

    # Kitchens Management urls
    path('kitchens/', view=kitchens.KitchensIndex.as_view(), name='kitchens_index'),
    path('kitchens/get/', view=kitchens.GetKitchens.as_view(), name='get_kitchens'),
    path('kitchens/create/', view=kitchens.AddKitchen.as_view(), name='add_kitchens'),
    path('kitchens/edit/<int:pk>/', view=kitchens.UpdateKitchen.as_view(), name='edit_kitchens'),
    path('kitchens/detail/<int:pk>', view=kitchens.DetailKitchen.as_view(), name='detail_kitchens'),
    path('kitchens/delete/<int:pk>/', view=kitchens.DeleteKitchen.as_view(), name='delete_kitchens'),

    # Category Management urls

    path('categories/', view=categories.CategoryIndex.as_view(), name='categories'),
    path('categories/get/', view=categories.CategoryGet.as_view(), name='get_category'),
    path('categories/create/', view=categories.AddCategory.as_view(), name='add_category'),
    path('categories/edit/<int:pk>/', view=categories.UpdateCategory.as_view(),
         name='edit_category'),
    path('categories/delete/<int:pk>/', view=categories.DeleteCategory.as_view(),
         name='delete_category'),

    # Ajax request for fetching kitchen based on store
    path('get-store-kitchens/', view=categories.GetStoreKitchen.as_view(), name='get_store_kitchens'),

    # Items Management urls
    path('items/', view=items.ItemsIndex.as_view(), name='items_index'),
    path('items/get/', view=items.GetItems.as_view(), name='get_items'),
    path('items/create/', view=items.AddItem.as_view(), name='add_items'),
    path('items/edit/<int:pk>/', view=items.UpdateItem.as_view(), name='edit_items'),
    path('items/detail/<int:pk>', view=items.DetailItem.as_view(), name='detail_items'),
    path('items/delete/<int:pk>/', view=items.DeleteItems.as_view(), name='delete_items'),

    # Ajax request for fetching kitchen based on store
    path('get-kitchens/', view=items.GetStoreKitchens.as_view(), name='get_kitchens_by_store'),
    path('get-categories/', view=items.GetKitchenCategory.as_view(), name='get_categories_by_kitchen'),

    # Orders Management urls
    path('allorder/', view=orders.AllOrders.as_view(), name='all_order'),
    path('allorder/get/', view=orders.GetOrders.as_view(), name='get_orders'),
    path('takeorder/', view=orders.Orders.as_view(), name='take_order'),
    path('getuser/', view=orders.GetUsers.as_view(), name='get-user'),
    path('update-username/', view=orders.UpdateUserName.as_view(), name='update_username'),
    path('finditems/', view=orders.FindItems.as_view(), name='find_items'),
    path('itemdetails/', view=orders.GetItemDetails.as_view(), name='get_item_details'),
    path('saveorder/', view=orders.SaveOrder.as_view(), name='save_order'),
    path('recent-order/', view=orders.GetRecentOrder.as_view(), name='get_recent_order'),
    path('re-order/', view=orders.Reorder.as_view(), name='re_order'),
    path('vieworder/<int:pk>/', view=orders.OrderDetail.as_view(), name='view_order'),
    path('allorder/update-order/', view=orders.UpdateOrder.as_view()),
    path('orders/bill/<int:pk>/', view=orders.OrderBill.as_view(), name='order_bill'),
    path('orders/kot/<int:pk>/', view=orders.OrderKOT.as_view(), name='order_kot'),

    # Discounts  Management urls
    path('discounts/', view=discount.DiscountsIndex.as_view(), name='discount_index'),
    path('discounts/create/', view=discount.AddDiscount.as_view(), name='add_discount'),
    path('discounts/get/', view=discount.GetDiscounts.as_view(), name='get_discount'),
    path('discounts/edit/<int:pk>/', view=discount.UpdateDiscount.as_view(), name='edit_discount'),
    path('discounts/delete/<int:pk>/', view=discount.DeleteDiscount.as_view(), name='delete_discount'),

    # Taxes Management urls
    path('taxes/', view=tax.TaxIndex.as_view(), name='taxes_index'),
    path('taxes/get/', view=tax.GetTax.as_view(), name='get_taxes'),
    path('taxes/create/', view=tax.AddTax.as_view(), name='add_taxes'),
    path('taxes/edit/<int:pk>/', view=tax.UpdateTax.as_view(), name='edit_taxes'),
    path('taxes/delete/<int:pk>/', view=tax.DeleteTax.as_view(), name='delete_taxes'),

    # User Management urls
    path('users/', view=user.UsersIndex.as_view(), name='users_index'),
    path('users/get/', view=user.GetUsers.as_view(), name='get_users'),
    path('user/deactivate/<int:pk>/', view=user.DeactivateUser.as_view(), name='user_deactivate'),

    # Feedback urls
    path('order-feedback/', view=feedback.OrderFeedbackIndex.as_view(), name='order_feedback_index'),
    path('order-feedback/get/', view=feedback.GetOrderFeedback.as_view(), name='get_order_feedback'),
    path('kitchen-feedback/', view=feedback.KitchenFeedbackIndex.as_view(), name='kitchen_feedback_index'),
    path('kitchen-feedback/get/', view=feedback.GetKitchenFeedback.as_view(), name='get_kitchen_feedback'),

    # Financial year urls
    path('financial-year/', view=fyear.FinancialYearAdd.as_view(), name='financial_year'),

    # notification Urls
    path('notifications/', view=notifications.NotificationIndex.as_view(), name='notifications'),
    path('notifications/get/', view=notifications.GetNotification.as_view(), name='get_notifications'),
    path('notifications/create/', view=notifications.CreateNotification.as_view(), name='get_notifications'),
    path('notifications/send/', view=notifications.SendNotification.as_view(), name='send_notifications'),

    # Ajax request for fetching order on kitchen based
    # path('get-order/', view=dashboard.GetKitchenData.as_view(), name='get_order_by_kitchen'),

    # Kitchen Timings On/Off urls
    path('kitchen-timings/', view=time.TimingKitchen.as_view(), name='get_kitchen_timings'),
    path('update-kitchen-status/', view=time.UpdateKitchenStatus.as_view(), name='update_kitchen_status'),

    # Store Timings On/Off urls
    path('store-timing/', view=time.TimingStore.as_view(), name='get_store_timings'),
    path('update-store-status/', view=time.UpdateStoreStatus.as_view(), name='update_store_status'),

    # Dashboard AJAX
    path('get_filter_orders/', view=dashboard.GetFilterOrder.as_view(), name='get_filter_orders'),
    path('get_kitchen_order_filter/', view=dashboard.GetKitchenOrderFilter.as_view(), name='get_kitchen_order_filter'),

    # Offer for Users
    path('promo-code/', view=promocode.PromoCodeIndex.as_view(), name='promo_code_index'),
    path('promo-code/get/', view=promocode.GetPromoCode.as_view(), name='get_promo_code'),
    path('promo-code/create/', view=promocode.AddPromoCode.as_view(), name='add_promo_code'),
    path('promo-code/update/<int:pk>/', view=promocode.UpdatePromoCode.as_view(), name='edit_promo_code'),
    path('promo-code/delete/<int:pk>/', view=promocode.DeletePromoCode.as_view(), name='delete_promo_code'),

    # delivery boy management
    path('delivery-boy/', delivery.DeliveryIndex.as_view(), name='delivery_index'),
    path('delivery-boy/create/', delivery.AddDelivery.as_view(), name='add_delivery'),
    path('delivery-boy/get/', delivery.GetDelivery.as_view(), name='get_delivery'),
    path('delivery-boy/profile/<int:pk>', delivery.DeliveryProfile.as_view(), name='detail_delivery'),
    path('delivery-boy/edit/<int:pk>/', delivery.UpdateDelivery.as_view(), name='edit_delivery'),
    path('delivery-boy/delete/<int:pk>/', delivery.DeactivateDelivery.as_view(), name='delete_delivery'),

    # Manager Points of Users
    path('manage-points/', managepoints_views.ManagePointIndex.as_view(), name='manage_points'),
    path('update-wallet/', managepoints_views.UpdateWallet.as_view(), name='updatewallet'),
    # csv file handler
    path('csv-file/', items.ImportCsvView.as_view(), name='csv_upload'),
]
