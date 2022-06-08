from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import RegisterUserForm,LoginUserForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login
from .models import Category,Product


def homepage(request):
    categorys = Category.objects.all()
    return render(request, 'blog/homepage.html',{'categorys':categorys})

def get_categorys(request,category_slug):
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'blog/get_categorys.html',{'products':products})

def basket(request,id_prod):
    tovars = Product.objects.filter(id = id_prod).values_list('id','name','price','description','image')
    amount = 1
    tovar_id = tovars[0][0]
    tovar_name = tovars[0][1]
    tovar_price = int(tovars[0][2])
    tovar_description = tovars[0][3]
    tovar_image = tovars[0][4]
    a = 0
    if request.session.get('basket'):
        add = request.session['basket']
        all_sum = request.session["sumbaskett"] + int(tovar_price)
        request.session["sumbaskett"] = int(all_sum)
        for i in add:
                if int(i[0]) == int(id_prod):
                    a = a + 1 
                    i[5] = i[5] + 1
                    break
        if a == 0: 
            add.append([tovar_id,tovar_name,tovar_price,tovar_image,tovar_description,amount])
    else:
        request.session["basket"]=[]
        request.session["sumbaskett"]=0
        add = request.session['basket']
        add.append([tovar_id,tovar_name,tovar_price,tovar_image,tovar_description,amount])
        b = request.session["sumbaskett"] + int(tovar_price)
        request.session["sumbaskett"] = int(b)
    return redirect('/show_basket')

def show_basket(request):
    basketall = request.session['basket']
    sum =  request.session["sumbaskett"]
    return render(request, 'blog/show_basket.html',{'basketall':basketall,'sum':sum})

def delete_basket(request):
    id = request.GET.get('id')
    spisok_basket = request.session["basket"]
    sum_basket = request.session["sumbaskett"]
    a = 0
    for i in spisok_basket:
        dellcount = int(i[5])
        dellprice = int(i[2])
        dellsum = int(dellprice)*int(dellcount)
        if int(i[0]) == int(id):
            sum_basket = sum_basket - dellsum
            del spisok_basket[a]
        a = a + 1
    request.session["add"] = spisok_basket
    request.session["sumbaskett"] = sum_basket
    return redirect("/show_basket")

def udateplus(request):
    amount = request.GET.get('amount')
    id = request.GET.get('id')
    all_sum = request.session["sumbaskett"]
    if int(amount) <= int(9):
        amount = int(amount) + int(1)
        spisok_basket = request.session["basket"]
        for i in spisok_basket:
            if i[0] == int(id):
                all_sum = int(all_sum) + int(i[2])
                i[5] = amount
        request.session["basket"] = spisok_basket
        request.session["sumbaskett"] = all_sum 
    return redirect("/show_basket")

def udateminus(request):
    amount = request.GET.get('amount')
    id = request.GET.get('id')
    all_sum = request.session["sumbaskett"]
    if int(amount) > int(1):
        amount = int(amount) - int(1)
        print(amount)
        spisok = request.session["basket"]
        for i in spisok:
            if i[0] == int(id):
                all_sum = int(all_sum) - int(i[2])
                i[5] = amount
                request.session["sumbaskett"] = all_sum
        request.session["basket"] = spisok
    return redirect("/show_basket")


    
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_success_url(self):
        return reverse_lazy('homepage')


def logout_user(request):
    logout(request)
    return redirect('login')