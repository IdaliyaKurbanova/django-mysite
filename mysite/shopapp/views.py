from timeit import default_timer
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def shop_index(request: HttpRequest):
    products = [('lipstick', 599, 0, 0),
                ('eyeshadows', 999, 20, datetime.strptime("Nov 15 2023 1:33PM", "%b %d %Y %I:%M%p")),
                ('powder', 1199, 0, 0),
                ('perfume', 2599, 0, 0),
                ('eyeliner', 49, 0, 0),
                ]
    product_names = [item[0] for item in products]
    context = {
        'launch_time': default_timer(),
        'products': products,
        'product_names': product_names,
    }
    return HttpResponse("Hello, world!")
    # return render(request, 'shopapp/shopapp-index.html', context=context)
