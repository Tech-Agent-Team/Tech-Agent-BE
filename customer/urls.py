from django.urls import path

from .views import CustomerSignUpView
from accounts.views import CustomerOnlyView
# from technician.views import techn
urlpatterns=[
    path('signup/', CustomerSignUpView.as_view()),
    path('dashboard/', CustomerOnlyView.as_view(), name='customer-dashboard'),

    # path('signup/client/', ClientSignupView.as_view()),
    # path('login/',CustomAuthToken.as_view(), name='auth-token'),
    # path('logout/', LogoutView.as_view(), name='logout-view'),
    # path('freelance/dashboard/', FreelanceOnlyView.as_view(), name='freelance-dashboard'),
    # path('client/dashboard/', ClientOnlyView.as_view(), name='client-dashboard'),
]