from django.shortcuts import render,redirect

from django.views.generic import View
from django import forms
from budget.models import Transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# fields are automatically populated
# save()
class TransactionForm(forms.ModelForm):

    class Meta:
        model=Transaction
        #fields="__all__"
        # fileds=[]
        exclude=("created_date",)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]


class LoginForm(forms.Form):

    username=forms.CharField()
    password=forms.CharField()




# transactions => list
# url:localhost:8000/transactions/all/
# method:get
        
        

class TransactionListView(View):
    def get(self,request,*args,**kwargs):
        qs=Transaction.objects.all()
        return render(request,"transaction_list.html",{"data":qs})




# view for creating new transaction
# url:localhost:8000/transactions/add/
# method:get,post


class TransactionCreateView(View):

    def get(self,request,*args,**kwargs):
        form=TransactionForm()
        return render(request,"transaction_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TransactionForm(request.POST)

        if form.is_valid():
            # data=form.cleaned_data
            # Transaction.objects.create(**data)
            form.save()
            return redirect("transaction-list")
        else:
            return render(request,"transaction_add.html",{"form":form})




# transactions detail
# url:localhost:8000/transactions/{id}/
# method:get
        
class TransactionDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Transaction.objects.get(id=id)
        return render(request,"transaction_detail.html",{"data":qs})



# transactions delete
# url:localhost:8000/transactions/{id}/remove/
# method get

class TransactionDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Transaction.objects.filter(id=id).delete()
        return redirect("transaction-list")


# transactin update
# url:localhost:8000/transactions/{id}/change/
# method:get,post

class TransacationUpateView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        transaction_object=Transaction.objects.get(id=id)        
        form=TransactionForm(instance=transaction_object)
        return render(request,"transaction_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        transaction_object=Transaction.objects.get(id=id) 
        data=request.POST
        form=TransactionForm(data,instance=transaction_object) 
        if form.is_valid():
            form.save()
            return redirect("transaction-list")
        else:
            return render(request,"transaction_edit.html",{"form":form})


# signup
#url:localhost:8000/signup/
# method:get,post
        
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()#password encrypt
            User.objects.create_user(**form.cleaned_data)
            print("created")
            return redirect("signup")
        else:
            print("failed")
            return render(request,"register.html",{"form":form})


# signin
# url:localhost:8000/signin/
# method:get,post
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                print("credentials are valid")
                login(request,user_object)
                # 
                # request.user =>anonymous user (user has no session)
                return redirect("transaction-list")
        print("invalid")
        return render(request,"login.html",{"form":form})




class SignOutView(View):

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
  
            