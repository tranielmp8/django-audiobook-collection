# these come with django already just need to import them
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django import forms 
from django.forms import ModelForm 
from django.forms.widgets import PasswordInput, TextInput
from . models import AudioBook

# USER MODEL
class CreateUserForm(UserCreationForm):
  
  class Meta:
    model = User 
    fields = ['username', 'email', 'password1', 'password2']
    
  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError("This email address is already registered.")
    return email

# LOGIN MODEL   
class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=TextInput())
  password = forms.CharField(widget=PasswordInput())
  
class AudioBookForm(ModelForm):
  
  class Meta:
    model = AudioBook
    fields = ['title', 'author', 'description', 'book_image', 'is_favorite', 'listen_date',]
    exclude = ['user',]
    
    
# UPDATE USER INFO
class UpdateUserForm(forms.ModelForm):
  password = None
  
  class Meta:
    model = User 
    fields = ['username', 'email',]
    exclude = ['password1', 'password2',]