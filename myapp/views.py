from django.shortcuts import render, redirect
from .models import TransWalk, TransIndiv
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from django import forms
from django.contrib.auth.models import User
from datetime import datetime



def home(request):
        if request.user.is_authenticated:
            return redirect("list")
        else:
            return render(request, 'home.html')
def labeltool(request, transwalk_ASRid):
    if request.user.is_authenticated:    
        item = TransWalk.objects.get(pk=transwalk_ASRid)
        global test_counter
        print("Test counter value is " + str(test_counter))
        if  request.method != 'POST' and item.IsOpenFlag == True:
            messages.info(request, "File Already In Progress")
            return redirect("list")
        elif request.method != 'POST' and item.Trans_Counter == test_counter:
            messages.info(request, "File Already Submitted")
            return redirect("list")
        elif item.IsOpenFlag == False:
            item.IsOpenFlag = True
        audiolink = item.Audio_File_Link
        text_output = item.Transcripted_Text
        item.save()
        submitbutton = "None"
        if request.method == 'POST' and 'Submitted' in request.POST:
            text_update = request.POST.get('text_update')
            item.Transcripted_Text = text_update
  #          r = TransIndiv(ASRid = item, audio_file_link = item.Audio_File_Link, Text_Indiv = text_update, audio_duration = item.audio_duration, Transcribed_By = request.user)
  #          r.save()
            prev_counter_value = int(item.Trans_Counter)
            prev_transcriber_checked = str(item.Transcribers_Checked)
            item.Transcribers_Checked = prev_transcriber_checked+ " | " +str(request.user)
            item.Trans_Counter = prev_counter_value + 1
            item.IsOpenFlag = False
            item.Updated_At = datetime.now()
            indiv_submit = item.transindiv_set.create   (asrid = int(item.ASRid),
                                                        audio_file_link = item.Audio_File_Link,
                                                        Text_Indiv = text_update,
                                                        audio_duration = item.audio_duration,
                                                        Transcribed_By = str(request.user),
                                                        counter_left = int(test_counter - (int(item.Trans_Counter))))
            indiv_submit.save()
            item.save()
            submitbutton = request.POST.get('Submit')
            return redirect("/list")

        elif request.method == 'POST' and 'Submission_Cancelled' in request.POST:
            print("IsOpenFlag is now false")
            item.IsOpenFlag = False
            item.save()
            return redirect("/list")

        context = {  
                        'submitbutton': submitbutton,
                        'audiolink' : audiolink,
                        'text_output' : text_output
                  }
                  
        
        return render(request, 'createpost.html', context)
    else:
        return redirect("login")                                                                                                                                                       
    

def audioList(request):
    if request.user.is_authenticated:
        global test_counter
        test_counter = 3
        all_Items = TransWalk.objects.all()
        context = {
                    'all_items' : all_Items,
                    'test_counter' : test_counter
                  }
        return render(request, 'list.html', context)
    else:
        return redirect("login") 


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("/list")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "register.html",
                  context={"form":form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/list")
               # return render(request ,template_name = "list.html" )
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")

def account(request):
    return render(request, template_name = "account.html")