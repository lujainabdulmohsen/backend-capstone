from django.urls import path
from .views import (
    AgencyList,
    ServiceList,
    ServiceDetail,
    ServiceRequestList,
    ServiceRequestDetail,
    PayServiceRequestView,
    CreateUserView,
    LoginView,
    VerifyUserView,
    MyBankAccountView,
    ChangePasswordView
)

urlpatterns = [
    path('agencies/', AgencyList.as_view(), name='agency-list'),
    path('services/', ServiceList.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetail.as_view(), name='service-detail'),
    path('service-requests/', ServiceRequestList.as_view(), name='service-request-list'),
    path('service-requests/<int:pk>/', ServiceRequestDetail.as_view(), name='service-request-detail'),
    path('service-requests/<int:pk>/pay/', PayServiceRequestView.as_view(), name='service-request-pay'),
    path('users/signup/', CreateUserView.as_view(), name='signup'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('bank-account/', MyBankAccountView.as_view(), name='my-bank-account'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
