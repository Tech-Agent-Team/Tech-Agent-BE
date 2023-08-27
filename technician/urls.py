from django.urls import path

from .views import CustomerSignUpView
from accounts.views import TechnicianOnlyView
# from technician.views import techn
urlpatterns=[
    # path('signup/customer/', CustomerSignUpView.as_view()),
    path('signup/', CustomerSignUpView.as_view()),
    path('dashboard/', TechnicianOnlyView.as_view(), name='Technician-dashboard'),
    # path('login/',CustomAuthToken.as_view(), name='auth-token'),
    # path('logout/', LogoutView.as_view(), name='logout-view'),
    # path('freelance/dashboard/', FreelanceOnlyView.as_view(), name='freelance-dashboard'),
    # path('client/dashboard/', ClientOnlyView.as_view(), name='client-dashboard'),
]