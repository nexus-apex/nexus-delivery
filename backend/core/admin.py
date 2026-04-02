from django.contrib import admin
from .models import DeliveryOrder, DeliveryDriver, DeliveryRoute

@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ["order_id", "customer_name", "customer_phone", "status", "amount", "created_at"]
    list_filter = ["status"]
    search_fields = ["order_id", "customer_name", "customer_phone"]

@admin.register(DeliveryDriver)
class DeliveryDriverAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "vehicle_type", "license_number", "created_at"]
    list_filter = ["vehicle_type", "status"]
    search_fields = ["name", "phone", "email"]

@admin.register(DeliveryRoute)
class DeliveryRouteAdmin(admin.ModelAdmin):
    list_display = ["name", "driver_name", "stops", "total_distance_km", "estimated_time_mins", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "driver_name"]
