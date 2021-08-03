from django.urls import path, include, re_path

from api.v1.views.payment_view import TransactionN
from api.v1.views.user_views import UserListViews, UserProfileEdit, UserWalletView, UserDetailView, UserProfilePic, \
    UserMobileUpdateVerify, WalletListView, CardLogView, CardDetails,CardDelete
from api.v1.views.auth_views import GetUserApiView, LoginApiView, LogoutApiView

from rest_framework.documentation import include_docs_urls

from api.v1.views.banner_view import BannerView, KitchenBannerView, PromoCodeView, PromoDetailView
from api.v1.views.address_views import AddressCreateView, AddressUpdateView, AddressDelete, AddressListing
from api.v1.views.store_view import StoreListingView, StoreDetailView, StoreDistanceView, StoreFilterView, StoreSearch
from api.v1.views.kitchen_view import KitchenDetailView, KitchenFeedbackView, KitchenSearchView, KitchenDetailCatView,kitchenStatusView
from api.v1.views.order_view import OrderFeedbackView, OrderPlaceView, OrderListView, OrderDetailView, OrderTrack, \
    OrderTrackStatusBasis
# from api.v1.views.payment_view import GenerateChecksum, VerifyChecksum, TransactionDetail, PaytmTransactionInit, \
#     TransactionStatus, TransactionP
from api.v1.views.item_view import ItemDetailView, ItemFeedbackView
from api.v1.views.category_view import CategoryListView
from api.v1.views.page_view import AboutUsView, ContactUsView, Privacy, TermOfUse, Cancellation, FaqsView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

from api.v1.views.payment_view import TransactionP, TransactionDetail, TransactionStatus, \
    PaytmTransactionInit, VerifyChecksum, GenerateChecksum

urlpatterns = [
    # user related  api
    path('docs/', include_docs_urls(title='PKB')),
    path('users/', UserListViews.as_view(), name='users'),
    # url(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', GetUserApiView.as_view(), name='signup'),
    path('auth/verify-otp/', LoginApiView.as_view(), name='verify-otp'),
    path('user/profile-update/', UserProfileEdit.as_view(), name='edit-profile'),
    path('user/add-address/', AddressCreateView.as_view(), name='add-address'),
    path('user/update-address/', AddressUpdateView.as_view(), name='update-address'),
    path('user/delete-address/', AddressDelete.as_view(), name='delete-address'),
    path('user/wallet/', UserWalletView.as_view(), name='user-wallet'),
    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("user/profile-pic/", UserProfilePic.as_view(), name='profile-pic'),
    path('mobile-update-otp/', UserMobileUpdateVerify.as_view(), name='mobile-otp'),
    path('address-list/', AddressListing.as_view(), name='address-list'),
    path('log-out/', LogoutApiView.as_view(), name='auth_logout'),

    # promo banner api
    path('banners/', BannerView.as_view(), name='banners'),
    path('kitchen-banners-list/<int:pk>/', KitchenBannerView.as_view(), name='kitchen_banners'),

    # promo code api
    path('promo-code/', PromoCodeView.as_view(), name='promo_code'),
    path('promo-detail/<int:pk>/', PromoDetailView.as_view(), name='promo-detail'),

    # store api
    path('stores/', StoreListingView.as_view(), name='stores'),
    path('stores/detail/<int:pk>/', StoreDetailView.as_view(), name='store_detail'),
    path('distance-search/', StoreDistanceView.as_view(), name='store-distance'),
    path('store-filter/', StoreFilterView.as_view(), name='store_filter'),
    path('store-search/', StoreSearch.as_view(), name='store-search'),

    # kitchen related api
    path('kitchen-detail/<int:pk>/', KitchenDetailView.as_view(), name='kitchen-detail'),
    path('kitchen-feedback/', KitchenFeedbackView.as_view(), name='kitchen-feedback'),
    path('global-search/', KitchenSearchView.as_view(), name='global-search'),
    path('kitchen-category/<int:pk>/', KitchenDetailCatView.as_view(), name='kitchen-category'),
    path('kitchen-status/<int:pk>/',kitchenStatusView.as_view(),name='kitchen-status'),

    # order api
    path('order-feedback/', OrderFeedbackView.as_view(), name='order-feedback'),
    path('order-place/', OrderPlaceView.as_view(), name='order-place'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('order-detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-track/<int:pk>/', OrderTrack.as_view(), name='order-track'),
    path('order-status-details/', OrderTrackStatusBasis.as_view(), name='order-status'),

    # items related api
    path('item-feedback/', ItemFeedbackView.as_view(), name='item-feedback'),
    path('item-detail/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),

    # category related api
    path('category-item/<int:pk>/', CategoryListView.as_view(), name='category-item'),

    # pkb term and use related api
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('privacy-policy/', Privacy.as_view(), name='privacy-policy'),
    path('term-use/', TermOfUse.as_view(), name='term-use'),
    path('cancellation-policy/', Cancellation.as_view(), name='cancellation'),
    path("TransactionN/", TransactionN.as_view(), name='TransactionN'),
    # payment related api
    path("checkout/", GenerateChecksum.as_view(), name="checkout"),
    # path("handlerequest/", HandleRequest.as_view(), name="handlerequest"),
    path('verifychecksum/', VerifyChecksum.as_view(), name='verifychecksum'),
    # path('mobile-update-otp/',UserMobileUpdateVerify.as_view(),name='mobile-otp'),
    path('transaction/', TransactionDetail.as_view(), name="transaction"),
    path('paytm_transaction_init/', PaytmTransactionInit.as_view(), name="paytm_transaction_init"),
    path('paytm_transaction_status/', TransactionStatus.as_view(), name="paytm_transaction_status"),

    path('transaction/', TransactionDetail.as_view(), name="transaction"),
    path('wallet_history/', WalletListView.as_view(), name="wallet_list"),
    path('card_add/', CardLogView.as_view(), name='card_log_add'),
    path('card_detail/', CardDetails.as_view(), name='card_details'),
    path("TransactionP/", TransactionP.as_view(), name='TransactionP'),
    path('card_delete/', CardDelete.as_view(), name='card_delete'),
    # # Faq's api
    path('faqs/', FaqsView.as_view(), name='faqs'),

]
