from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse
from .aes import encryption,decryption,check_password
from .aes_ocr import ocr_encryption
from datetime import datetime
from .models import User,BlockChain,File
from .page_count import check_page_count
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'blockchain/index.html', {})

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_conformation = request.POST.get('password_confirm')
        email = request.POST.get('email')
        if(password != password_conformation):
            messages.error(request, "Confirm Passowrd does not match original password")
            return redirect('blockchain:signup')
        else:
            if(User.objects.filter(username=username).exists()):
                messages.error(request, "Username already exists, try to signin or choose different username")
                return redirect('blockchain:signup')
            else:
                try:
                    user = User.objects.create_user(
                        username=username, password=password, email=email)
                    user.save()
                except:
                    messages.error(request, "Email already exists")
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
            messages.error(request, "Username or Password Incorrect")
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
            file2 = request.FILES['user_file']
            print(file.name)
            if file.name.endswith('.txt'):
                (salt, iv, hashed_password, ciphertext) = encryption(file,file_password)
                block = BlockChain(user=request.user,salt=salt,iv=iv,file_password=hashed_password,cipher_text=ciphertext)
                block.save()
                file_model = File(user=request.user, file_name=file.name, block=block)
                file_model.save()
                return redirect('blockchain:home')
            elif file.name.endswith('.pdf'):
                (salt, iv, hashed_password, ciphertext) = ocr_encryption(file,file_password)
                block = BlockChain(user=request.user,salt=salt,iv=iv,file_password=hashed_password,cipher_text=ciphertext)
                block.save()
                file_model = File(user=request.user, file_name=file.name, block=block)
                file_model.save()
                return redirect('blockchain:home')
            else:
                messages.error(request, "Please Upload a valid file type txt/pdf")
                return redirect('blockchain:user_file_upload')
        return redirect('blockchain:user_file_upload')
    return render(request,'blockchain/file_upload.html',{})

@login_required
def user_files(request):
    user_files = File.objects.filter(user=request.user)
    return render(request,'blockchain/user_files.html',{'user_files':user_files})

@login_required
def file_details(request,pk = None):
    crrt_pass = False
    count = 0
    file = File.objects.get(pk=pk)
    block = file.block
    text = ''
    if request.method == "POST":
        file_enter_password = request.POST.get('password')
        if(check_password(block.file_password,file_enter_password)):
            text = decryption(block.salt, block.iv, block.cipher_text, file_enter_password)
            text = text.decode('utf-8')
            crrt_pass = True
        else:
            messages.error(request, "Incorrect password please try again")
            count = 1
    return render(request,'blockchain/input_password.html',{'text':text,'crrt_pass':crrt_pass,'pk':pk,'count':count})
