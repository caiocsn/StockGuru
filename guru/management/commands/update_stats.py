from django.core.management.base import BaseCommand
from guru.models import PriceRecord, StockStats
from django.db.models import Avg

class Command(BaseCommand):
    help = 'Create StockStats objects for each unique stock value in PriceRecord'

    def handle(self, *args, **options):
        unique_stocks = PriceRecord.objects.values_list('stock', flat=True).distinct()

        for stock in unique_stocks:
            stock_stats = StockStats.objects.create(stock=stock)
            stock_stats.save()

        self.stdout.write(self.style.SUCCESS('StockStats objects created successfully for each unique stock value.'))
