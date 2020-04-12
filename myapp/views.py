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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
        if request.user.is_authenticated:
            return redirect("list")
        else:
            return render(request, 'home.html')
def labeltool(request, transwalk_ASRid):
    if request.user.is_authenticated:
        item = TransWalk.objects.get(pk=transwalk_ASRid)
        if request.method == 'POST' and item.IsOpenFlag == False:
            messages.error(request, "Session Expired !!!")
            return redirect("list")
        if request.method != 'POST':
            item.click_timestamp = datetime.now()
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
            prev_counter_value = int(item.Trans_Counter)
            if item.Transcribers_Checked:
                prev_transcriber_checked = str(item.Transcribers_Checked)
                item.Transcribers_Checked = prev_transcriber_checked+ " | " +str(request.user)
            else:
                item.Transcribers_Checked = str(request.user)
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
            messages.info(request, "Transcription Saved")
            return redirect("/list")

        elif request.method == 'POST' and 'Submission_Cancelled' in request.POST:
            print("IsOpenFlag is now false")
            item.IsOpenFlag = False
            item.save()
            messages.warning(request, "Transcription Cancelled")
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
        Max_timeout = 1800
        time = datetime.now()
        timestamp = datetime.timestamp(time)
        global test_counter
        test_counter = 3
        all_Items_list = TransWalk.objects.all()

        for things in all_Items_list:
            if things.click_timestamp is not None:
                thingstimestamp = datetime.timestamp(things.click_timestamp)
                if (timestamp-thingstimestamp)>Max_timeout:
                    things.IsOpenFlag= False
                    things.save()
        paginator = Paginator(all_Items_list, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)



        context = {
                    'all_items' : page_obj,
                    'test_counter' : test_counter
                  }
        return render(request, 'list.html', context)
    else:
        return redirect("login") 


def register(request):
    if request.user.is_authenticated:
        messages.error(request, "Please Logout Then Register")
        return redirect("/list")
    elif request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if first_name and last_name and username and email and password1 and password2 :
            if len(username) >=4:
                if len(password1) >= 6:
                    if password1 == password2:
                        if User.objects.filter(username=username).exists():
                            messages.error(request, "Username Already Exists")
                            #return redirect("/register")            
                        else:
                            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name,last_name=last_name)
                            user.save()
                            messages.success(request, f"New account created: {username}")
                            return redirect("/login")
                    else:
                        messages.error(request, "Password Not Matching!")
                        #return redirect("/register")
                else:
                    messages.error(request, "Password Must be Atleast 6 Characters Long")
                    #return redirect("/register")
            else:
                messages.error(request, "Username must be atleast 4 Characters Long")
                #return redirect("/register")
        else:
            messages.error(request, "None Of The Fields Can Be Empty")
    return render(request,"register.html")

def login_request(request):
    if request.user.is_authenticated:
        messages.error(request, "Please Logout Then Login Again")
        return redirect("/list")
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You are now logged in as {username}")
            return redirect("/list")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request,"login.html")

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

def account(request):
    return render(request, template_name = "account.html")