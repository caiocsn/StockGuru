from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import PriceRecord, StockStats


@require_http_methods(['GET'])
def stock_records_view(request, stock):
    stock_records = PriceRecord.objects.filter(stock=stock).order_by('date')
    context = {'stock': stock, 'stock_records': stock_records}
    return render(request, 'guru/stock_records.html', context)

@require_http_methods(['GET'])
def stock_stats_grid(request):
    stock_stats = StockStats.objects.all()
    context = {'stock_stats_list': stock_stats}
    return render(request, 'guru/stock_stats_grid.html', context)