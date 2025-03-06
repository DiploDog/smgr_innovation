from django.shortcuts import render
from django.http import HttpResponse
from .forms import CarTypeForm, CarForm, PlatformForm, TankForm, MotherForm
from src.car_info import CARS_CODE


def index(request, header):
    return render(
        request,
        template_name="index.html",
        context={"href": "car-type/"}
    )


def about(request, header):
    return render(request, "about.html")


def select_car_type(request):
    if request.method == "POST":
        car_type = request.POST.get("car_type")
        if car_type in ("13", "43"):
            form = PlatformForm()
        elif car_type in ("15", "45"):
            form = TankForm()
        else:
            form = CarForm()

        form.initial = {"car_type": car_type}

        return render(
            request,
            template_name="values.html",
            context={
                "form": form,
                "header": f"Введите характеристики для {CARS_CODE[int(car_type)]}",
                "title": "Расчет инновационности вагона",
                "href": "values/",
            },

        )

    else:
        form = CarTypeForm()
        return render(
            request=request,
            template_name="values.html",
            context={
                "form": form,
                "header": f"Введите модель вагона",
                "title": "Определение модели вагона",
                "href": "car-type/"
            }
        )



def postuser(request):
    car_type = request.POST.get('car_type', None)
    carrying_capacity = request.POST.get('carrying_capacity', None)
    return HttpResponse(
        f"""
        car_type: {car_type}
        carrying_capacity: {carrying_capacity}
        """
    )


def calculation(request):
    if request.method == "POST":
        delta = request.POST.get("delta")
        effect_year = request.POST.get("effect_year")
        car_type = request.POST.get("car_type")
        carrying_capacity = request.POST.get("carrying_capacity")
        tare_weight = request.POST.get("tare_weight")
        car_service_life = request.POST.get("car_service_life")
        depot_repair_period = request.POST.get("depot_repair_period")
        major_repair_period = request.POST.get("major_repair_period")
        axial_load = request.POST.get("axial_load")
        body_volume = request.POST.get("body_volume")
        print(
            delta,
            effect_year,
            car_type,
            carrying_capacity,
            tare_weight,
            car_service_life,
            depot_repair_period,
            major_repair_period,
            axial_load,
            body_volume
        )
        return HttpResponse("Смотри в консоль")
    else:
        userform = UserForm()
        return render(request, "values.html", {"form": userform})