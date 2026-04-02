import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import DeliveryOrder, DeliveryDriver, DeliveryRoute


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['deliveryorder_count'] = DeliveryOrder.objects.count()
    ctx['deliveryorder_pending'] = DeliveryOrder.objects.filter(status='pending').count()
    ctx['deliveryorder_assigned'] = DeliveryOrder.objects.filter(status='assigned').count()
    ctx['deliveryorder_picked_up'] = DeliveryOrder.objects.filter(status='picked_up').count()
    ctx['deliveryorder_total_amount'] = DeliveryOrder.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['deliverydriver_count'] = DeliveryDriver.objects.count()
    ctx['deliverydriver_bike'] = DeliveryDriver.objects.filter(vehicle_type='bike').count()
    ctx['deliverydriver_car'] = DeliveryDriver.objects.filter(vehicle_type='car').count()
    ctx['deliverydriver_van'] = DeliveryDriver.objects.filter(vehicle_type='van').count()
    ctx['deliverydriver_total_rating'] = DeliveryDriver.objects.aggregate(t=Sum('rating'))['t'] or 0
    ctx['deliveryroute_count'] = DeliveryRoute.objects.count()
    ctx['deliveryroute_planned'] = DeliveryRoute.objects.filter(status='planned').count()
    ctx['deliveryroute_active'] = DeliveryRoute.objects.filter(status='active').count()
    ctx['deliveryroute_completed'] = DeliveryRoute.objects.filter(status='completed').count()
    ctx['deliveryroute_total_total_distance_km'] = DeliveryRoute.objects.aggregate(t=Sum('total_distance_km'))['t'] or 0
    ctx['recent'] = DeliveryOrder.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def deliveryorder_list(request):
    qs = DeliveryOrder.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(order_id__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'deliveryorder_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def deliveryorder_create(request):
    if request.method == 'POST':
        obj = DeliveryOrder()
        obj.order_id = request.POST.get('order_id', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.customer_phone = request.POST.get('customer_phone', '')
        obj.pickup_address = request.POST.get('pickup_address', '')
        obj.delivery_address = request.POST.get('delivery_address', '')
        obj.status = request.POST.get('status', '')
        obj.amount = request.POST.get('amount') or 0
        obj.assigned_driver = request.POST.get('assigned_driver', '')
        obj.save()
        return redirect('/deliveryorders/')
    return render(request, 'deliveryorder_form.html', {'editing': False})


@login_required
def deliveryorder_edit(request, pk):
    obj = get_object_or_404(DeliveryOrder, pk=pk)
    if request.method == 'POST':
        obj.order_id = request.POST.get('order_id', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.customer_phone = request.POST.get('customer_phone', '')
        obj.pickup_address = request.POST.get('pickup_address', '')
        obj.delivery_address = request.POST.get('delivery_address', '')
        obj.status = request.POST.get('status', '')
        obj.amount = request.POST.get('amount') or 0
        obj.assigned_driver = request.POST.get('assigned_driver', '')
        obj.save()
        return redirect('/deliveryorders/')
    return render(request, 'deliveryorder_form.html', {'record': obj, 'editing': True})


@login_required
def deliveryorder_delete(request, pk):
    obj = get_object_or_404(DeliveryOrder, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/deliveryorders/')


@login_required
def deliverydriver_list(request):
    qs = DeliveryDriver.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(vehicle_type=status_filter)
    return render(request, 'deliverydriver_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def deliverydriver_create(request):
    if request.method == 'POST':
        obj = DeliveryDriver()
        obj.name = request.POST.get('name', '')
        obj.phone = request.POST.get('phone', '')
        obj.email = request.POST.get('email', '')
        obj.vehicle_type = request.POST.get('vehicle_type', '')
        obj.license_number = request.POST.get('license_number', '')
        obj.status = request.POST.get('status', '')
        obj.deliveries_today = request.POST.get('deliveries_today') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.save()
        return redirect('/deliverydrivers/')
    return render(request, 'deliverydriver_form.html', {'editing': False})


@login_required
def deliverydriver_edit(request, pk):
    obj = get_object_or_404(DeliveryDriver, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.phone = request.POST.get('phone', '')
        obj.email = request.POST.get('email', '')
        obj.vehicle_type = request.POST.get('vehicle_type', '')
        obj.license_number = request.POST.get('license_number', '')
        obj.status = request.POST.get('status', '')
        obj.deliveries_today = request.POST.get('deliveries_today') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.save()
        return redirect('/deliverydrivers/')
    return render(request, 'deliverydriver_form.html', {'record': obj, 'editing': True})


@login_required
def deliverydriver_delete(request, pk):
    obj = get_object_or_404(DeliveryDriver, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/deliverydrivers/')


@login_required
def deliveryroute_list(request):
    qs = DeliveryRoute.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'deliveryroute_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def deliveryroute_create(request):
    if request.method == 'POST':
        obj = DeliveryRoute()
        obj.name = request.POST.get('name', '')
        obj.driver_name = request.POST.get('driver_name', '')
        obj.stops = request.POST.get('stops') or 0
        obj.total_distance_km = request.POST.get('total_distance_km') or 0
        obj.estimated_time_mins = request.POST.get('estimated_time_mins') or 0
        obj.status = request.POST.get('status', '')
        obj.date = request.POST.get('date') or None
        obj.save()
        return redirect('/deliveryroutes/')
    return render(request, 'deliveryroute_form.html', {'editing': False})


@login_required
def deliveryroute_edit(request, pk):
    obj = get_object_or_404(DeliveryRoute, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.driver_name = request.POST.get('driver_name', '')
        obj.stops = request.POST.get('stops') or 0
        obj.total_distance_km = request.POST.get('total_distance_km') or 0
        obj.estimated_time_mins = request.POST.get('estimated_time_mins') or 0
        obj.status = request.POST.get('status', '')
        obj.date = request.POST.get('date') or None
        obj.save()
        return redirect('/deliveryroutes/')
    return render(request, 'deliveryroute_form.html', {'record': obj, 'editing': True})


@login_required
def deliveryroute_delete(request, pk):
    obj = get_object_or_404(DeliveryRoute, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/deliveryroutes/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['deliveryorder_count'] = DeliveryOrder.objects.count()
    data['deliverydriver_count'] = DeliveryDriver.objects.count()
    data['deliveryroute_count'] = DeliveryRoute.objects.count()
    return JsonResponse(data)
