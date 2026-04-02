from django.db import models

class DeliveryOrder(models.Model):
    order_id = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255, blank=True, default="")
    customer_phone = models.CharField(max_length=255, blank=True, default="")
    pickup_address = models.TextField(blank=True, default="")
    delivery_address = models.TextField(blank=True, default="")
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("assigned", "Assigned"), ("picked_up", "Picked Up"), ("in_transit", "In Transit"), ("delivered", "Delivered"), ("failed", "Failed")], default="pending")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    assigned_driver = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_id

class DeliveryDriver(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    vehicle_type = models.CharField(max_length=50, choices=[("bike", "Bike"), ("car", "Car"), ("van", "Van"), ("truck", "Truck")], default="bike")
    license_number = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("available", "Available"), ("on_delivery", "On Delivery"), ("off_duty", "Off Duty")], default="available")
    deliveries_today = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class DeliveryRoute(models.Model):
    name = models.CharField(max_length=255)
    driver_name = models.CharField(max_length=255, blank=True, default="")
    stops = models.IntegerField(default=0)
    total_distance_km = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estimated_time_mins = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("planned", "Planned"), ("active", "Active"), ("completed", "Completed")], default="planned")
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
