from django.urls import path
from .views import TechnicianSignUpView,homeTechnicianView,TechnicianAcceptedOrdersView,TechnicianCancelOrdersView,TechnicianProfileView
# from .views import TechnicianUpdateProfileView

from accounts.views import CustomUserUpdateProfileView
urlpatterns=[
    path('signup/', TechnicianSignUpView.as_view()),
    path('profile/<str:user_name>/', TechnicianProfileView.as_view(), name='Technician-dashboard'),
    path('profileupdate/', CustomUserUpdateProfileView.as_view()),
    # path('profileupdate/', CustomerUpdateProfileView.as_view(), name='customer-profile-update'),
    path('hometechnician/', homeTechnicianView.as_view(), name='Technician-home'),
    path('techacceptedlist/', TechnicianAcceptedOrdersView.as_view(), name='Technician-accepted'),
    path('cancelorder/<int:order_id>/', TechnicianCancelOrdersView.as_view(), name='Technician-cancel'),

]