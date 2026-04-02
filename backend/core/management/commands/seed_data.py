from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import DeliveryOrder, DeliveryDriver, DeliveryRoute
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusDelivery with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusdelivery.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if DeliveryOrder.objects.count() == 0:
            for i in range(10):
                DeliveryOrder.objects.create(
                    order_id=f"Sample {i+1}",
                    customer_name=f"Sample DeliveryOrder {i+1}",
                    customer_phone=f"+91-98765{43210+i}",
                    pickup_address=f"Sample pickup address for record {i+1}",
                    delivery_address=f"Sample delivery address for record {i+1}",
                    status=random.choice(["pending", "assigned", "picked_up", "in_transit", "delivered", "failed"]),
                    amount=round(random.uniform(1000, 50000), 2),
                    assigned_driver=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 DeliveryOrder records created'))

        if DeliveryDriver.objects.count() == 0:
            for i in range(10):
                DeliveryDriver.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    phone=f"+91-98765{43210+i}",
                    email=f"demo{i+1}@example.com",
                    vehicle_type=random.choice(["bike", "car", "van", "truck"]),
                    license_number=f"Sample {i+1}",
                    status=random.choice(["available", "on_delivery", "off_duty"]),
                    deliveries_today=random.randint(1, 100),
                    rating=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 DeliveryDriver records created'))

        if DeliveryRoute.objects.count() == 0:
            for i in range(10):
                DeliveryRoute.objects.create(
                    name=f"Sample DeliveryRoute {i+1}",
                    driver_name=f"Sample DeliveryRoute {i+1}",
                    stops=random.randint(1, 100),
                    total_distance_km=round(random.uniform(1000, 50000), 2),
                    estimated_time_mins=random.randint(1, 100),
                    status=random.choice(["planned", "active", "completed"]),
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 DeliveryRoute records created'))
