
from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm, AudioBookForm, UpdateUserForm 
from . models import AudioBook
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
# Create your views here.

def homepage(request):
  
  return render(request, 'collection/index.html')

def register(request):
  form = CreateUserForm()
  
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    
    if form.is_valid():
      form.save()
  
      return redirect('my-login')
    
  context = {'RegistrationForm': form}
  
  
  return render(request, 'collection/register.html', context) 

def my_login(request):
  form = LoginForm()
  
  if request.method == 'POST':
    form = LoginForm(request, data=request.POST)
    
    if form.is_valid():
      username = request.POST.get('username')
      password = request.POST.get('password')
      
      user = authenticate(request, username=username, password=password)
      
      if user is not None:
        auth.login(request, user)
        return redirect('book-list')
      
  context = {'LoginForm': form}  
  
  return render(request, 'collection/my-login.html', context) 


def user_logout(request):
  auth.logout(request)
  return redirect('')


# CRUD --------------------------

@login_required(login_url='my-login')
def book_list(request):
  current_user = request.user.id
  audioBook = AudioBook.objects.all().filter(user=current_user)
  
  context = {'AllAudioBooks': audioBook}
  
  return render(request, 'collection/crud/book-list.html', context) 

@login_required(login_url='my-login')
def create_audio_book(request):
  form = AudioBookForm()
  
  if request.method == 'POST':
    form = AudioBookForm(request.POST, request.FILES)
    
    if form.is_valid():
      # form.save()
      audioBook = form.save(commit=False) # post to database, but don't save it yet
      audioBook.user = request.user # assigning thought request to logged in user
      audioBook.save() # now save to database bc it is assigned to current user
      # messages.success(request, "Thought Created!")
      return redirect('book-list')
    
  context = {"AudioBookForm": form}
  
  return render(request, 'collection/crud/create-audio-book.html', context) 
  
  # UPDATE need id or pk
@login_required(login_url='my-login')
def update_audio_book(request, pk):
  try:
    audioBook = AudioBook.objects.get(id=pk, user=request.user)
  except:
    return redirect('book-list')
  
  if request.method == 'POST':
    form = AudioBookForm(request.POST or None, request.FILES or None, instance=audioBook)
    
    if form.is_valid():
      if 'book_image' in form.cleaned_data:
        if not form.cleaned_data['book_image']:
           form.instance.book_image = 'books/audio-book.png'
      
        form.save()
        return redirect('book-list')
  else:
    form = AudioBookForm(instance=audioBook)

  context = {'UpdateAudioBookForm': form}
  
  return render(request, 'collection/crud/update-audio-book.html', context ) 
  
  
# Delete Audio Book:
@login_required(login_url='my-login')
def delete_audio_book(request, pk):
  try:
    audioBook = AudioBook.objects.get(id=pk, user=request.user)
  except:
    return redirect('book-list')
  
  if request.method == 'POST':
    audioBook.delete()
    
    return redirect('book-list')
  
  return render(request, 'collection/crud/delete-audio-book.html') 
  
  
# ------ PROFILE MANAGEMENT ------------------

@login_required(login_url='my-login')
def profile_management(request):
  form = UpdateUserForm(instance=request.user)
  
  if request.method == 'POST':
    form = UpdateUserForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      return redirect('book-list')
  
  context = { 'UserUpdateForm': form }
  
  return render(request, 'collection/profile-management.html', context) 


@login_required(login_url='my-login')
def delete_account(request):
  if request.method == 'POST':
    deleteUser = User.objects.get(username=request.user)
    deleteUser.delete()
    return redirect('')

  return render(request, 'collection/delete-account.html') 