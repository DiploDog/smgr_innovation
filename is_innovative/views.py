import os
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CarTypeForm, CarForm, PlatformForm, TankForm, IsothermicForm
from src.car_info import CARS_CODE
from src.cars import Car, Platform, Tank, Isothermic, smgr


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
        request.session["car_type"] = car_type
        return redirect("values")
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


def values(request):
    car_type = request.session.get("car_type")
    # Выбор нужной формы
    if car_type in ("13", "43"):
        form_class = PlatformForm
    elif car_type in ("15", "45"):
        form_class = TankForm
    elif car_type == "16":
        form_class = IsothermicForm
        erreport_path = "./Отчет_об_ошибке.txt"
        try:
            with open("./Коэффициент_изотерм.txt", mode="r") as f:
                number = f.readline()
                try:
                    heatTcoeff = float(number)
                except ValueError as e:
                    with open(erreport_path, mode="a") as err:
                        err.write(str(e))

        except FileNotFoundError as e:
            if os.path.exists(erreport_path):
                os.remove(erreport_path)
            with open(erreport_path, mode="w") as err:
                err.write(str(e))

        smgr["Коэффициент теплопередачи кузова"] = heatTcoeff
    else:
        form_class = CarForm

    if request.method == "POST":
        form = form_class(request.POST)

        if form.is_valid():
            # Получаем очищенные данные из формы
            cleaned_data = form.cleaned_data

            # Создаем объект Car и передаем данные
            class_name = form_class.__name__
            match class_name:
                case "PlatformForm": car = Platform
                case "TankForm": car = Tank
                case "IsothermicForm": car = Isothermic
                case _: car = Car

            car = car(**cleaned_data)
            smgr_df = car.calculate_mean_vals(smgr)
            print(smgr_df)
            result = car.is_innovative(smgr_df)

            # Сохраняем результат в сессии
            request.session["calculation_result"] = result

            # Перенаправляем на страницу результата
            return redirect("result")

    else:  # GET-запрос, рендерим пустую форму
        form = form_class(
            initial={
                "car_type": car_type,
                "release": datetime.datetime.now().year
            }
        )

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


def result(request):
    # Получаем результат из сессии
    result = round(float(request.session.get("calculation_result", "Результаты отсутствуют")), 3)
    if result < 1.05:
        class_ = "не инновационным"
    else:
        class_ = "инновационным"
    car_type = request.session.get("car_type")
    return render(
        request,
        template_name="result.html",
        context={
            "result": result,
            "header": "Результат расчета",
            "title": "Результат расчета",
            "car_type": car_type,
            "class_": class_,
            "href": "/car-type"
        },
    )