from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse
from .aes import encryption,decryption
from datetime import datetime
from .models import BlockChain,File

# Create your views here.


def index(request):
    return render(request, 'blockchain/home.html', {})

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_conformation = request.POST.get('password_confirm')
        email = request.POST.get('email')

        if(password != password_conformation):
            # messages.error(
            #     request, "Confirm Passowrd does not match original password")
            return redirect('blockchain:signup')
        else:
            if(User.objects.filter(username=username).exists()):
                # messages.error(
                #     request, "Username already exists, try to signin or choose different username")
                return redirect('blockchain:signup')
            else:
                try:
                    user = User.objects.create_user(
                        username=username, password=password, email=email)
                    user.save()
                except:
                    # messages.error(request, "Email already exists")
                    return redirect('blockchain:signup')
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('blockchain:home'))
    return render(request, 'blockchain/signup.html', {})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('blockchain:home'))
            else:
                return HttpResponse("Account not active")
        else:
            return redirect('blockchain:login')
    else:
        return render(request,'blockchain/login.html',{})

## logout view.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blockchain:home'))

@login_required
def user_file_upload(request):
    if request.method == "POST":
        file_password = request.POST.get('password')
        if 'user_file' in request.FILES:
            file = request.FILES['user_file']
            (salt, iv, hashed_password, ciphertext) = encryption(file,file_password)
            print(hashed_password)
            block = BlockChain(user=request.user,
                                salt=salt,
                                iv=iv,
                                file_password=hashed_password,
                                cipher_text=ciphertext)
            block.save()
            file_model = File(user=request.user, file_name=file.name, block=block)
            file_model.save()
            return redirect('blockchain:home')
        return redirect('blockchain:user_file_upload')
    return render(request,'blockchain/file_upload.html',{})
