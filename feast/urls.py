# from django.urls import path
# from .views import *



# urlpatterns = [
#         # Authentication Routes
#     path('signup/',signup_view, name='signup'),
#     path('signin/',signin_view, name='signin'),
#     path('signout/',signout_view, name='signout'),
    
    # Home Route
    # path('',home_view, name='home'),
    
    # Meal Selection Flow
    # path('categories/',meal_categories, name='meal_categories'),
    # path('categories/<int:category_id>/items/',menu_items, name='menu_items'),
    # path('order/<int:menu_item_id>/',order_meal, name='order_meal'),
    
    # Balance Management
    # path('balance/top-up/',top_up_balance, name='top_up'),
    # path('expenses/',expense_history, name='expense_history'),
# ]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.homeview, name='home'),
#     # path('signup/', views.student_signup, name='student_signup'),
#     # path('signup/success/', views.signup_success, name='signup_success'),
# ]

from django.urls import path
from . views import *

urlpatterns = [
    path('add_student/', add_student, name='add_student'),
    path('signin/', signin_view, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('', welcome_view, name='welcome'),
    path('menu/', menu_list, name='menu_list'),
    path('menu/add/', add_menu_item, name='add_menu_item'),
    path('menu/delete/<int:item_id>/', delete_menu_item, name='delete_menu_item'),
    path('menu/buy/<int:item_id>/', buy_menu_item, name='buy_menu_item'),
    path('expenses/', view_expense, name='view_expense'),
    path('order/', order_food, name='order_food'),
    path('orders/', view_orders, name='view_orders'),
    # path('admin_home/', home_view, name='home_view'),
    # path('student_home/', home_view, name='home_view'),
    path('students_details/', canteen_student_details, name='student_details'),
    # path("select-in/", select_in_option, name="select_in_option"),
    path("student_added_success/", student_added_success, name="student_added_success"),
    path("view_students/", view_students, name="view_students"),
    path('add-college-user/', add_college_user, name='add_college_user'),
    path('college_added_success/', add_college_user, name='college_user_added_success'),
    path('in-details/', in_details_view, name='in_details'),
    path('attendance/', attendance_view, name='attendance'),
    # path("calendar/", calendar_view, name="calendar"),
]