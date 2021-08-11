import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from foodapp.models import Restaurant, Dishes, OrderPlaced


@login_required
def restaurants(request):
    return render(request, "restaurants.html")


@csrf_protect
def get_restaurants(request):
    if request.method == 'GET':
        # data = json.loads(request.body)
        restaurant = Restaurant.objects.all()
        names = []
        for rest in restaurant:
            names.append({'id': rest.id, 'name': rest.rest_name, 'address': rest.rest_address})

        send_data = {
            "status": "success",
            "data": names,
        }
        return_data = json.dumps(send_data)
        return JsonResponse(return_data, safe=False)
    else:
        send_data = {
            "status": "error",
            "message": "Method not allowed",
        }
        return_data = json.dumps(send_data)
        return JsonResponse(return_data, safe=False)


@csrf_protect
def get_dishes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rest_id = data['restId']
        rest = Restaurant.objects.get(id=rest_id)
        dishes = Dishes.objects.filter(rest_name=rest)
        names = []

        for dish in dishes:
            names.append({'id': dish.id, 'dishName': dish.dish_name, 'price': dish.price})

        send_data = {
            "status": "success",
            "data": names,
        }
        return_data = json.dumps(send_data)
        return JsonResponse(return_data, safe=False)
    else:
        send_data = {
            "status": "error",
            "message": "Method not allowed",
        }
        return_data = json.dumps(send_data)
        return JsonResponse(return_data, safe=False)


@csrf_protect
def place_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rest_id = data['selectedRestaurant']
        total_price = data['totalPrice']
        selected_dishes = data['selectedDishes']
        rest = Restaurant.objects.get(id=rest_id)
        try:
            orders = OrderPlaced.objects.all().order_by('-id')[0]
        except IndexError:
            orders = None
        if orders:
            order_id = orders.order_id + 1
        else:
            order_id = 1
        for dish_id in selected_dishes:
            dish = Dishes.objects.get(id=dish_id)
            OrderPlaced.objects.create(order_id=order_id, user=request.user, rest_name=rest, dish=dish,
                                       total_price=total_price)
        send_data = {
            "status": "success",
            "orderPlaced": True
        }
        return_data = json.dumps(send_data)
        return JsonResponse(return_data, safe=False)
    else:
        send_data = {
            "status": "error",
            "message": "Method not allowed",
            "orderPlaced": False
        }
        return_data = json.dumps(send_data)
        return JsonResponse(return_data, safe=False)


@csrf_protect
def my_orders(request):
    return render(request, "my-orders.html")


@csrf_protect
def get_my_orders(request):
    if request.method == 'GET':
        orders = OrderPlaced.objects.filter(user=request.user)
        data = []
        for order in orders:
            data.append({'dishName': order.dish.dish_name, 'Price': order.dish.price,
                         'restaurantName': order.rest_name.rest_name, 'dateOrdered': order.date.strftime('%d-%m-%Y')})
        send_data = {
            "data": data,
            "orderPlaced": True
        }
        return_data = json.dumps(send_data)
        return JsonResponse(return_data, safe=False)
    else:
        send_data = {
            "status": "error",
            "message": "Method not allowed",
            "orderPlaced": False
        }
        return_data = json.dumps(send_data)
        return JsonResponse(return_data, safe=False)
