from django.urls import path
from .views import Customerordersfeed,CustomerProfileView ,CustomerSignUpView ,Customermyorders , Customerdeletorders , Customerordersdone,CustomerUpdateProfileView
from accounts.views import CustomerOnlyView

urlpatterns=[
    path('signup/', CustomerSignUpView.as_view()),
    path('profile/<str:user_name>/', CustomerProfileView.as_view(), name='customer-profile'),
    path('profileupdate/', CustomerUpdateProfileView.as_view(), name='customer-profile-update'),
    path('myorders/', Customermyorders.as_view(), name='customer-myorders'),
    path('deletorders/<int:order_id>/', Customerdeletorders.as_view(), name='customer-myorders'),
    path('ordersdone/<int:order_id>/', Customerordersdone.as_view(), name='customer-myorders'),
    path('feedback/<int:order_id>/', Customerordersfeed.as_view(), name='customer-myorders'),
    
]