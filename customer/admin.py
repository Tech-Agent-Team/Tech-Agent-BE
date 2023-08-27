# from django.contrib import admin

# # Register your models here.
# from .models import CustomerProfile
# # Register your models here.

# admin.site.register(CustomerProfile)

from django import forms
from django.contrib import admin
from .models import CustomerProfile

class CustomerProfileAdminForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = '__all__'  # Include all fields from CustomerProfile

    # Add additional fields from CustomUser for display
    email = forms.EmailField(label='Email', required=False, disabled=True)
    phone = forms.CharField(label='Phone', max_length=255, required=False, disabled=True)
    location = forms.CharField(label='Location', max_length=255, required=False, disabled=True)

class CustomerProfileAdmin(admin.ModelAdmin):
    form = CustomerProfileAdminForm
    # Define other admin options as needed

admin.site.register(CustomerProfile, CustomerProfileAdmin)

