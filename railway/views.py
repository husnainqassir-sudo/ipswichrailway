from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from railway.models import *
from django.shortcuts import render, redirect, get_object_or_404

from .models import Add_Train, Passenger


# ------------------ NAVIGATION ------------------ #
def nav(request):
    return render(request, 'carousel.html')

def About(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


# ------------------ CUSTOMER AUTH ------------------ #
def Register_customer(request):
    if request.method == "POST":
        n = request.POST['uname']
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        a = request.POST['add']
        m = request.POST['mobile']
        g = request.POST.get('male')
        d = request.POST['birth']
        p = request.POST['pwd']

        if User.objects.filter(username=n).exists():
            messages.error(request, "Username already taken.")
            return redirect('register_customer')

        if User.objects.filter(email=e).exists():
            messages.error(request, "Email already registered.")
            return redirect('register_customer')

        try:
            dob = datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('register_customer')

        user = User.objects.create_user(username=n, password=p, email=e, first_name=f, last_name=l)
        Register.objects.create(user=user, add=a, mobile=m, gender=g, dob=dob)

        messages.success(request, "Registration successful!")
        return redirect('login_customer')

    return render(request, "register_customer.html")


def Login_customer(request):
    error = error2 = error3 = False
    if request.method == "POST":
        n = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=n, password=p)
        if user:
            login(request, user)
            if user.is_staff:
                error2 = True
            else:
                error = True
        else:
            error3 = True

    return render(request, 'login_customer.html', {'error': error, 'error2': error2, 'error3': error3})


def Logout(request):
    logout(request)
    return redirect('nav')


# ------------------ TRAIN SEARCH ------------------ #
@login_required(login_url='login_customer')
def Search_Train(request):
    trains = Add_Train.objects.all()
    passengers = Passenger.objects.filter(user=request.user)

    if request.method == "POST":

        print("TRAIN ID:", request.POST.get('train_id'))
        print("ROUTE ID:", request.POST.get('route_id'))

        train_id = request.POST.get('train_id')
        route_id = request.POST.get('route_id')




        # ✅ SAFETY CHECK
        if not train_id or not route_id:
            messages.error(request, "Please select train and route")
            return redirect('search_train')

        train = get_object_or_404(Add_Train, id=train_id)
        route_obj = get_object_or_404(Add_route, id=route_id)

        Passenger.objects.create(
            user=request.user,
            train=train,
            name=request.POST.get('name'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            route=route_obj.route,
            fare=route_obj.fare
        )

        messages.success(request, "Passenger added successfully")
        return redirect('search_train')

    return render(request, 'search_train.html', {
        'trains': trains,
        'passengers': passengers
    })
# ------------------ DASHBOARD ------------------ #
@login_required(login_url='login_customer')
def Dashboard(request):
    return render(request, 'dashboard.html')


# ------------------ BOOKINGS ------------------ #
@login_required(login_url='login_customer')
def my_booking(request):
    user = request.user

    pro = Passenger.objects.filter(user=user)
    book = Book_ticket.objects.filter(user__user=user)

    return render(request, 'my_booking.html', {
        'user': user,
        'pro': pro,
        'book': book
    })

@login_required(login_url='login_customer')
def view_ticket(request, pid):
    book = Book_ticket.objects.filter(id=pid).first()
    return render(request, 'view_ticket.html', {'book': book})


@login_required(login_url='login_customer')
def Delete_passenger(request, passenger_id, train_id):
    Passenger.objects.filter(id=passenger_id, user__user=request.user).delete()
    messages.info(request, "Passenger Deleted Successfully")
    return redirect('book_detail', train_id=train_id)


@login_required(login_url='login_customer')
def Card_Detail(request, total, train_id):
    user = request.user
    user_instance = get_object_or_404(Register, user=user)
    train = get_object_or_404(Add_Train, id=train_id)
    passengers = Passenger.objects.filter(user=user_instance, train=train)

    if request.method == "POST":
        passengers.update(status="set")
        return redirect('my_booking')

    context = {
        'user': user_instance,
        'data2': train,
        'pro': passengers,
        'total': total
    }
    return render(request, 'card_detail.html', context)
@login_required(login_url='login_customer')
def delte_my_booking(request, pid):
    Passenger.objects.filter(id=pid).delete()
    return redirect('my_booking')


# ------------------ TRAIN MANAGEMENT ------------------ #
@login_required(login_url='login_customer')
def Add_train(request):
    error = False
    if request.method == "POST":
        Add_Train.objects.create(
            trainname=request.POST['busname'],
            train_no=request.POST['bus_no'],
            from_city=request.POST['fcity'],
            to_city=request.POST['tcity'],
            departuretime=request.POST['dtime'],
            arrivaltime=request.POST['atime'],
            trevaltime=request.POST['ttime'],
            distance=request.POST['dis'],
            img=request.FILES.get('img')
        )
        error = True
    return render(request, 'add_train.html', {'error': error})


@login_required(login_url='login_customer')
def view_train(request):
    data = Add_Train.objects.all()
    return render(request, "view_train.html", {"data": data})


@login_required(login_url='login_customer')
def add_route(request):
    error = False
    trains = Add_Train.objects.all()
    if request.method == "POST":
        train = Add_Train.objects.filter(id=request.POST['bus']).first()
        if train:
            Add_route.objects.create(
                train=train,
                route=request.POST['route'],
                distance=request.POST['dis'],
                fare=request.POST['fare']
            )
            error = True
    return render(request, 'add_route.html', {'data': trains, 'error': error})


@login_required(login_url='login_customer')
def Edit_route(request, pid):
    error = False
    route_obj = Add_route.objects.filter(id=pid).first()
    trains = Add_Train.objects.all()
    if request.method == "POST" and route_obj:
        train = Add_Train.objects.filter(id=request.POST['bus']).first()
        if train:
            route_obj.train = train
            route_obj.route = request.POST['route']
            route_obj.fare = request.POST['fare']
            route_obj.distance = request.POST['dis']
            route_obj.save()
            error = True
    return render(request, 'editroute.html', {'data': route_obj, 'data2': trains, 'error': error})


@login_required(login_url='login_customer')
def delete_route(request, pid):
    Add_route.objects.filter(id=pid).delete()
    return redirect('availableroute')


@login_required(login_url='login_customer')
def displayroute(request):
    routes = Add_route.objects.all()
    trains = Add_Train.objects.all()
    return render(request, "availableroute.html", {'data': routes, 'data2': trains})


# ------------------ BOOKING DETAIL ------------------ #
@login_required(login_url='login_customer')
def Book_detail(request, train_id):
    train = get_object_or_404(Add_Train, id=train_id)
    routes = Add_route.objects.filter(train=train)

    if request.method == "POST":
        route_obj = get_object_or_404(Add_route, id=request.POST.get('route_id'))

        Passenger.objects.create(
            user=request.user,
            train=train,
            name=request.POST.get('name'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            route=route_obj.route,
            fare=route_obj.fare
        )

        messages.success(request, "Passenger Added Successfully")
        return redirect('book_detail', train_id=train.id)

    tickets = Passenger.objects.filter(user=request.user, train=train)
    total = tickets.aggregate(total=Sum('fare'))['total'] or 0

    return render(request, 'book_detail.html', {
        'data2': train,
        'routes': routes,
        'pro': tickets,
        'total': total
    })
# ------------------ BOOKING VIEWS ------------------ #
@login_required(login_url='login_customer')
def viewbookings(request):
    book = Book_ticket.objects.all()
    return render(request, 'viewbookings.html', {'book': book})


@login_required(login_url='login_customer')
def deletebooking(request, pid):
    Passenger.objects.filter(id=pid).delete()
    return redirect('viewbookings')


# ------------------ TRAIN EDIT ------------------ #
@login_required(login_url='login_customer')
def edit(request, pid):
    error = False
    train = Add_Train.objects.filter(id=pid).first()
    if request.method == "POST" and train:
        train.trainname = request.POST['busname']
        train.train_no = request.POST['bus_no']
        train.from_city = request.POST['fcity']
        train.to_city = request.POST['tcity']
        train.departuretime = request.POST['dtime']
        train.arrivaltime = request.POST['atime']
        train.trevaltime = request.POST['ttime']
        train.distance = request.POST['dis']
        train.save()
        error = True
    return render(request, 'edittrain.html', {'data': train, 'error': error})


@login_required(login_url='login_customer')
def delete(request, pid):
    Add_Train.objects.filter(id=pid).delete()
    return redirect('view_train')


# ------------------ ADMIN ------------------ #
@login_required(login_url='login_customer')
def admindashboard(request):
    return render(request, 'admindashboard.html')


@login_required(login_url='login_customer')
def change_image(request, pid):
    train = Add_Train.objects.filter(id=pid).first()
    error = ""
    if request.method == "POST" and train:
        try:
            train.img = request.FILES['newpic']
            train.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'change_image.html', {'error': error, 'train': train})


@login_required(login_url='login_customer')
def view_regusers(request):
    data = Register.objects.filter(user__is_staff=False)
    return render(request, "view_regusers.html", {'data': data})


@login_required(login_url='login_customer')
def delete_user(request, pid):
    User.objects.filter(id=pid).delete()
    return redirect('view_regusers')