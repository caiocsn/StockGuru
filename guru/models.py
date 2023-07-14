from django.db import models
from django.db.models import Avg

class PriceRecord(models.Model):
    stock = models.CharField(max_length=50)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.stock} - {self.date}"


class StockStats(models.Model):
    stock = models.CharField(max_length=50)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Stats for {self.price_records.stock}"

    def save(self, *args, **kwargs):
        price_records = PriceRecord.objects.filter(stock=self.stock)
        average_price = price_records.aggregate(Avg('price'))['price__avg']
        self.average_price = average_price
        super().save(*args, **kwargs)