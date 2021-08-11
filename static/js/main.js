let selectedDishes = [];

function getCookie(name) {  //Function to get Cookie
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {   //For cross site protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)); // these HTTP methods do not require CSRF protection
}

function showRestaurants() {
    let csrfToken = getCookie('csrftoken');    // For CSRF verification
    let sendData = JSON.stringify({});
    document.getElementById('heading').innerText = 'Pick a Restaurant';
    sessionStorage.clear();
    sessionStorage.setItem('totalPrice', '0');
    document.getElementById('dishes-parent-container').style.display = 'none';
    document.getElementById('restaurant-container').style.display = 'flex';
    document.getElementById("restaurant-container").innerHTML = ``;
    $.ajax({
        method: "GET",
        beforeSend: function (request, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                request.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        url: "/restaurants/get-restaurants",
        data: sendData,
        dataType: "json",
        success: function (data) {
            let returnData = JSON.parse(data);
            // console.log(returnData);
            returnData.data.forEach(rest => {
                // console.log(rest);
                document.getElementById("restaurant-container").innerHTML += `
                    <div class="col-sm-4 mb-4" id="restaurant-${rest.id}">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title">${rest.name}</h5>
                                <p class="card-text">${rest.address}</p>
                                <button class="btn btn-primary" onclick="showDishes(${rest.id})">Order Now</button>
                            </div>
                        </div>
                    </div>`;
            })
        }
    });
}

function showDishes(restId) {
    sessionStorage.setItem('selectedRestaurant', restId);
    let csrfToken = getCookie('csrftoken');    // For CSRF verification
    let sendData = JSON.stringify({'restId': restId});
    document.getElementById('restaurant-container').style.display = 'none';
    document.getElementById('heading').innerText = 'Create your Order';
    $.ajax({
        method: "POST",
        beforeSend: function (request, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                request.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        url: "/restaurants/get-dishes",
        data: sendData,
        dataType: "json",
        success: function (data) {
            let returnData = JSON.parse(data);
            // console.log(returnData);
            let restaurant_container = document.getElementById("dishes-container");
            restaurant_container.innerHTML = ``;
            returnData.data.forEach(dish => {
                // console.log(dish);
                sessionStorage.setItem(dish.id, JSON.stringify(dish));
                restaurant_container.innerHTML += `
                <div class="col-md-12 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${dish.dishName}</h5>
                            <hr/>
                            <div style="float: right;">
                                <button class="btn btn-primary" onclick="selectDish(${dish.id})">
                                    <i class="uil uil-rupee-sign"></i>${dish.price}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>`;
            })
            document.getElementById('dishes-parent-container').style.display = 'flex';
        }
    });
}

function selectDish(dishId) {
    let selectedItems = document.getElementById('selected-items');
    if (selectedDishes.length === 0) {
        selectedItems.innerHTML = ``;
    }
    selectedDishes.push(dishId);
    let selectedDish = JSON.parse(sessionStorage.getItem(dishId));
    sessionStorage.setItem('totalPrice', (parseInt(sessionStorage.getItem('totalPrice')) + selectedDish.price).toString());
    selectedItems.innerHTML += `
        <div class="card text-center mb-2" id="dish-${dishId}">
            <div class="card-body">
                <div class="row">
                    <div class="col-8">
                        <h6 class="card-title">${selectedDish.dishName}</h6>
                    </div>
                    <div class="col-2 text-end">
                        <span style="cursor: pointer;" onclick="removeDish(${dishId})"><i class="uil uil-trash-alt"></i></span>
                    </div>
                    <div class="col-2 text-end">
                        <h6><i class="uil uil-rupee-sign"></i>${selectedDish.price}</h6>
                    </div>
                </div>
            </div>
        </div>`;
    updateTotalPrice();
}

function removeDish(dishId) {
    $('#dish-' + dishId).remove();
    selectedDishes.splice(dishId, 1);
    if (selectedDishes.length === 0) {
        let selectedItems = document.getElementById('selected-items');
        selectedItems.innerHTML = `No items selected`;
    }
    let selectedDish = JSON.parse(sessionStorage.getItem(dishId));
    sessionStorage.setItem('totalPrice', (parseInt(sessionStorage.getItem('totalPrice')) - selectedDish.price).toString());
    updateTotalPrice();
}

function updateTotalPrice() {
    document.getElementById('total-price').innerHTML = `<i class="uil uil-rupee-sign"></i>${sessionStorage.getItem('totalPrice')}`;
}

function placeOrder() {
    let csrfToken = getCookie('csrftoken');    // For CSRF verification
    let sendData = JSON.stringify({
        'totalPrice': sessionStorage.getItem('totalPrice'),
        'selectedDishes': selectedDishes,
        'selectedRestaurant': parseInt(sessionStorage.getItem('selectedRestaurant'))
    });
    document.getElementById('restaurant-container').style.display = 'none';
    document.getElementById('heading').innerText = 'Create your Order';
    $.ajax({
        method: "POST",
        beforeSend: function (request, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                request.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        url: "/restaurants/place-order",
        data: sendData,
        dataType: "json",
        success: function (data) {
            let returnData = JSON.parse(data);
            // console.log(returnData);
            if (returnData.orderPlaced) {
                // console.log("order success");
                sessionStorage.clear();
                selectedDishes = []
                showRestaurants();
                toastr.options = {
                    "positionClass": "toast-top-center",
                };
                toastr.success('Your order placed successfully !');
            }
        }
    });
}
