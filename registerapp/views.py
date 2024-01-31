from django.shortcuts import render,redirect
from.forms import AddForm
from .models import table
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login as log,logout
from django.contrib.auth.models import User, auth

# Create your views here.

#create form to add to data base
def register(request):
    form=AddForm()
    if request.method=="POST":
        form=AddForm(request.POST,request.FILES)
        if form.is_valid(): 
            form.save()
        
    return render(request,"register.html",{'form':form})

def login(request):
    return render(request,"login.html")

#view added data
def view(request):
    cr=table.objects.all()
    return render(request,"view.html",{'cr':cr})

#detailed view
def detailview(request,pk):
    cr=table.objects.get(id=pk)
    return render(request,"detailedview.html",{'cm':cr})

#update
def update(request,pk):
    cr=table.objects.get(id=pk)
    form2=AddForm(instance=cr)
    if request.method =="POST":
        form2=AddForm(request.POST,instance=cr)
        if form2.is_valid:
            form2.save()
            return redirect("view")
    return render(request,"update.html",{'form2':form2})

# deleteform
def delete(request,pk):
    cr=table.objects.get(id=pk)
    cr.delete()
    return redirect("view") 


#for login checking
def userlog(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        cr=table.objects.filter(email=email,password=password)
        e="error credentials"
        if cr:
            user_details=table.objects.get(email=email,password=password)

            # for session
            id=user_details.id
            firstname=user_details.firstname
            lastname=user_details.lastname
            phone=user_details.phone 
            gender=user_details.gender 

            request.session['id']=id
            request.session['firstname']=firstname
            request.session['lastname']=lastname
            request.session['phone']=phone
            request.session['gender']=gender

            return redirect('welcome')
        else:
            return render(request,'login.html',{'e':e})
        
    else:
        return render(request,'register.html')
    
def welcome(request):
    id=request.session['id']
    firstname=request.session['firstname']
    lastname=request.session['lastname']
    return render(request,"welcome.html",{'id':id,'firstname':firstname,'lastname':lastname})

def logoutuser(request):
    logout(request)
    return redirect('login')

def adminlog(request):
    return render(request,"adminlogin.html")

def alog(request):
    if request.method=='POST':
        # e="error credentials"
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            username=user.username
            password=user.password
            email=user.email

            request.session['username']=username
            request.session['password']=password
            request.session['email']=email
            return redirect('welcomeadmin')
        else:
             return redirect('adminlog')
        
    else:
        return redirect('view')

def welcomeadmin(request):
    username=request.session['username']
    password=request.session['password']
    email=request.session['email']
    return render(request,"welcomeadmin.html",{'username':username,'password':password,'email':email})

def logoutadmin(request):
    logout(request)
    return redirect('adminlog')