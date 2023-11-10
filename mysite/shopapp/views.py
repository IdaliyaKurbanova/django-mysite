from timeit import default_timer
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from typing import List, Dict, Any


def shop_index(request: HttpRequest):
    products: List[tuple] = [('lipstick', 599, 0, 0),
                ('eyeshadows', 999, 20, datetime.strptime("Nov 15 2023 1:33PM", "%b %d %Y %I:%M%p")),
                ('powder', 1199, 0, 0),
                ('perfume', 2599, 0, 0),
                ('eyeliner', 49, 0, 0),
                ]
    product_names: List[str] = [item[0] for item in products]
    context: Dict[str, Any] = {
        'launch_time': default_timer(),
        'products': products,
        'product_names': product_names,
    }
    return render(request, 'shopapp/shopapp-index.html', context=context)
