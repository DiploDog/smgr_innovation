from django.views.generic import TemplateView
from django.urls import re_path, path, include
from is_innovative import views


urlpatterns = [
    path("", views.index, {"header": "Проверка инновационности вагона"}),
    path("postuser/", views.postuser),
    #path("values/", views.calculation),
    path("values/", views.calculation),
    path("about/",
         TemplateView.as_view(template_name="about.html"),
         {"header": "О приложении"},
         name="about",
         ),
]
