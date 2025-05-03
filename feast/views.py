# from django.shortcuts import render,redirect
# from .models import CustomUser
# from django.contrib import messages
# from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.decorators import login_required
# import os
# Create your views here.

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import localdate
from datetime import datetime
from django.utils.timezone import now
from django.db.models import Sum
from .models import User, Order
from datetime import time
from django.utils.timezone import localtime
from django.http import JsonResponse
# views.py

# from django.contrib.auth import get_user_model
# from django.db.utils import IntegrityError

# from django.contrib.auth import get_user_model

# def create_college_user():
#     User = get_user_model()
#     if not User.objects.filter(username='college').exists():
#         User.objects.create_user(
#             username='college',
#             password='college123',
#             user_type='college_admin',  # Make sure this matches your model's choices
#             college='ABC College'
#         )


def add_student(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('student_added_success')  # Redirect to your students list
    else:
        form = SignUpForm()
    return render(request, 'add_student.html', {'form': form})

@login_required
def add_college_user(request):
    if request.method == 'POST':
        form = CollegeUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'College Admin user created successfully!')
            return redirect('college_user_added_success')  # Your target URL
    else:
        form = CollegeUserSignUpForm()
    return render(request, 'add_college_user.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')  # Redirect to your home page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('welcome')
login_required

def home_view(request):
    if request.user.is_superuser:
        return render(request, 'admin_home.html')  # Superuser dashboard
    elif request.user.user_type == 'college_admin':
        return render(request, 'college_home.html')  # College dashboard
    else:
        return render(request, 'student_home.html')  # Student dashboard

def welcome_view(request):
    user=request.user
    # print('user',request.user)
    return render(request,'welcome.html',{'user':user})


def menu_list(request):
    menu_items = Menu.objects.all()
    return render(request, 'menu_list.html', {'menu_items': menu_items})

# def add_menu_item(request):
#     if request.method == 'POST':
#         form = MenuForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('menu_list')
#     else:
#         form = MenuForm()
#     return render(request, 'add_menu.html', {'form': form})

def add_menu_item(request):
    days = Menu.DAYS_OF_WEEK
    categories = Menu.CATEGORY_CHOICES
    item_map = {
        'breakfast': ['Dosa', 'Idli', 'Poori', 'Upma', 'Puttu'],
        'lunch': ['Rice and Curry', 'Sambar', 'Meals', 'Chicken Fry'],
        'snacks': ['Egg Baji', 'Banana Fry', 'Samosa'],
        'dinner': ['Biriyani', 'Chapathi', 'Parotta']
    }

    if request.method == 'POST':
        day = request.POST.get('day')
        for category in item_map:
            for item in item_map[category]:
                price = request.POST.get(f'{category}_{item}_price')
                if price:
                    # Check if it already exists (update)
                    existing = Menu.objects.filter(day=day, category=category, name=item).first()
                    if existing:
                        existing.price = price
                        existing.save()
                    else:
                        Menu.objects.create(day=day, category=category, name=item, price=price)
        return redirect('menu_list')

    # menu_items = Menu.objects.all()
    menu_items = Menu.objects.all().order_by('day', 'category')

    # context = {
    #     'days': days,
    #     'categories': categories,
    #     'item_map': item_map,
    #     'menu_items': menu_items,
    # }
    context = {
    'days': days,
    'categories': categories,
    'item_map': item_map,
    'menu_items': menu_items,
    'category_items': [(category[0], item_map[category[0]]) for category in categories],
}

    return render(request, 'add_menu.html', context)

def delete_menu_item(request, item_id):
    item = get_object_or_404(Menu, id=item_id)
    item.delete()
    return redirect('menu_list')


@login_required
def buy_menu_item(request, item_id):
    menu_item = get_object_or_404(Menu, id=item_id)
    
    # Create an order record
    order = Order.objects.create(
        student=request.user,
        menu_item=menu_item,
        total_price=menu_item.price  # Assuming quantity = 1

    )

    return redirect('view_orders')  # Redirect to expense tracking


@login_required


def view_expense(request):
    today = localdate()
    current_month = today.month
    current_year = today.year

    # Daily expense
    daily_expense = Order.objects.filter(
        student=request.user, order_date=today
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Monthly expense
    monthly_expense = Order.objects.filter(
        student=request.user,
        order_date__year=current_year,
        order_date__month=current_month
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Expenses per day for the current month
    daily_expenses = Order.objects.filter(
        student=request.user,
        order_date__year=current_year,
        order_date__month=current_month
    ).values('order_date').annotate(
        total=Sum('total_price')
    ).order_by('order_date')  # Sorting by date

    return render(request, 'expense.html', {
        'daily_expense': daily_expense,
        'monthly_expense': monthly_expense,
        'daily_expenses': daily_expenses,  # List of {'order_date': date, 'total': amount}
    })


@login_required
def order_food(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.student = request.user  # Assign the logged-in student
            order.total_price = order.menu_item.price * order.quantity  # Calculate total cost
            order.save()
            return redirect('view_orders')  # Redirect to the orders page
    else:
        form = OrderForm()

    menu_items = Menu.objects.all()
    return render(request, 'order_food.html', {'form': form, 'menu_items': menu_items})

### **View Orders for the Current Day**
@login_required
def view_orders(request):
    today_orders = Order.objects.filter(student=request.user, order_date=now().date())
    return render(request, 'view_orders.html', {'orders': today_orders})

### owner side stdent details
@login_required
def canteen_student_details(request):
    if request.user.user_type != 'canteen_owner':
        return render(request, 'error.html', {'message': 'Access Denied'})

    students = User.objects.filter(user_type='student')

    student_expenses = []
    for student in students:
        total_expense = Order.objects.filter(student=student).aggregate(Sum('total_price'))['total_price__sum'] or 0
        student_expenses.append({'student': student, 'total_expense': total_expense})

    return render(request, 'student_details.html', {'student_expenses': student_expenses})




def select_in_option(request):
    if request.method == "POST":
        current_time = localtime(now()).time()

        if not (18 <= current_time.hour <= 21):
            messages.error(request, "You can only select the 'IN' option between 6 PM and 9 PM.")
            return redirect("home")

        student = request.user  # Assuming authenticated student

        if student.selected_in_today:
            messages.warning(request, "You have already selected 'IN' for today.")
            return redirect("home")

        # ✅ Mark 'IN' as selected
        student.selected_in_today = True  

        # ✅ Add ₹95 to the student's expense
        student.expense += 95  
        student.save()

        messages.success(request, "You are IN! ₹95 has been added to your expense.")

        return redirect("home")  

    return JsonResponse({"error": "Invalid request"}, status=400)



def student_added_success(request):
    return render(request, 'student_added_success.html')

def college_user_added_success(request):
    return render(request, 'college_user_added_success.html')


# def view_students(request):
#     if not hasattr(request.user, 'user_type'):
#         messages.error(request, "Invalid user type.")
#         return redirect('home')

#     if request.user.user_type != 'canteen_owner':
#         messages.error(request, "You do not have permission to view this page.")
#         return redirect('student_list')

#     students = User.objects.filter(user_type='student')
#     return render(request, '#', {'students': students})


from django.core.paginator import Paginator

def view_students(request):
    # if request.user.user_type != 'student || college_admin':
    if request.user.user_type != 'student' and request.user.user_type != 'college_admin':
        messages.error( "You do not have permission to view this page.")
        return redirect('home')

    student_list = User.objects.filter(user_type='student')
    paginator = Paginator(student_list, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {'page_obj': page_obj})

