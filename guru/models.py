import numpy as np
import warnings

from django.db import models
from django.db.models import Max

class PriceRecord(models.Model):
    stock = models.CharField(max_length=50)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.stock} - {self.date}"


class StockStats(models.Model):
    stock = models.CharField(max_length=50, unique=True)
    most_recent_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_difference_30days = models.DecimalField(max_digits=10, decimal_places=4)
    price_difference_6months = models.DecimalField(max_digits=10, decimal_places=4)
    price_difference_1year = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f"Stats for {self.price_records.stock}"

    def get_difference(self, price_records, days=30):
        interval_length = int(days * 22 / 30)
        most_recent_id = price_records.latest('date').id

        try:
            current_record = price_records.get(id=most_recent_id)
            previous_record = price_records.get(id=most_recent_id - interval_length)

            date_diff = abs((current_record.date - previous_record.date).days)
            if date_diff > days * 1.1:
                warnings.warn(f"Encountered date inconsistency while calculating price difference for {self.stock}"
                            f"\ninterval length = {days} days"
                            f"\ncurrent_date = {current_record.date}"
                            f"\nprevious_date = {previous_record.date}", UserWarning)

            return (current_record.price - previous_record.price) / previous_record.price
        except price_records.model.DoesNotExist:
            warnings.warn(f"Price difference ({days} days) for {self.stock} could not be calculated.", UserWarning)
            return np.nan

    def save(self, *args, **kwargs):
        price_records = PriceRecord.objects.filter(stock=self.stock)
        self.most_recent_price = price_records.latest('date').price
        self.price_difference_30days = self.get_difference(price_records, 30)
        self.price_difference_6months = self.get_difference(price_records, 180)
        self.price_difference_1year = self.get_difference(price_records, 365)

        super().save(*args, **kwargs)