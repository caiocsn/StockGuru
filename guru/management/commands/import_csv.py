import pandas as pd
from django.core.management.base import BaseCommand
from guru.models import PriceRecord
from guru.serializers import PriceRecordSerializer

class Command(BaseCommand):
    help = 'Import data from a CSV file into PriceRecord'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        df = pd.read_csv(csv_file)
        
        df['name'] = 'PETR4'
        df['Close'] = df['Close'].round(2) 
        
        df = df.rename(columns={'name': 'stock', 'Date': 'date', 'Close': 'price'})
        
        records = df.to_dict(orient='records')
        serializer = PriceRecordSerializer(data=records, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
