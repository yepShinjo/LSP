from django.forms import ModelForm
from .models import auction, User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'password2']

class auctionForm(ModelForm):
    class Meta: # Model Meta is basically used to change the behavior of your model fields. why do class Meta right after the (ModelForm) ? cuz django documentation said so (:
        model = auction 
        fields = '__all__'
        exclude = ['host', 'participants', 'auction_status']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'