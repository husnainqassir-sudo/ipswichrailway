from django.contrib import admin
from django.urls import path
from railway.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', nav, name="nav"),
    path('about/', About, name="about"),
    path('contact/', contact, name="contact"),
    path('login/', Login_customer, name="login_customer"),
    path('register_customer/', Register_customer, name="register_customer"),
    path('search_train/', Search_Train, name="search_train"),

    # Booking URLs (no user_id in URL)
    path('book_detail/<int:train_id>/', Book_detail, name="book_detail"),
    path('delete_passenger/<int:passenger_id>/<int:train_id>/', Delete_passenger, name="delete_passenger"),
    path('card_detail/<int:total>/<int:train_id>/', Card_Detail, name="card_detail"),

    # User dashboard
    path('dashboard/', Dashboard, name="dashboard"),
    path('log_out/', Logout, name="log_out"),
    path('my_booking/', my_booking, name="my_booking"),
    path('delte_my_booking/<int:pid>/', delte_my_booking, name="delte_my_booking"),

    # Admin dashboard
    path('dashboard2/', admindashboard, name="admindashboard"),
    path('addtrain/', Add_train, name="add_train"),
    path('addroute/', add_route, name="add_route"),
    path('edittrain/<int:pid>/', edit, name="edittrain"),
    path('editroute/<int:pid>/', Edit_route, name="editroute"),
    path('delete/<int:pid>/', delete, name="delete"),
    path('delete_route/<int:pid>/', delete_route, name="delete_route"),

    # View trains/routes/bookings
    path('viewtrain/', view_train, name="view_train"),
    path('availableroute/', displayroute, name="availableroute"),
    path('viewbookings/', viewbookings, name="viewbookings"),
    path('deletebooking/<int:pid>/', deletebooking, name="deletebooking"),
    path('view_ticket/<int:pid>/', view_ticket, name="view_ticket"),
    path('change_image/<int:pid>/', change_image, name="change_image"),

    # Registered users management
    path('view_regusers/', view_regusers, name="view_regusers"),
    path('delete_user/<int:pid>/', delete_user, name="delete_user"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)