from django.views.generic import TemplateView
from django.urls import re_path, path, include
from is_innovative import views


urlpatterns = [
    path("", views.index, {"header": "Проверка инновационности вагона"}),
    path("car-type/", views.select_car_type, name="car-type"),
    path("values/", views.values, name="values"),
    path("result/", views.result, name="result"),
    path("about/",
         TemplateView.as_view(template_name="about.html"),
         {"header": "О приложении"},
         name="about",
         ),
]
