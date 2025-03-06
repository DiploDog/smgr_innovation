from django import forms
from src.car_info import CARS_CODE


class CarTypeForm(forms.Form):
    car_type = forms.CharField(
        label="Модель вагона",
        widget=forms.Select(choices=CARS_CODE,
                            attrs={'class': 'form-control form-label'})
    )


class MotherForm(forms.Form):
    delta = forms.FloatField(label="Коэфф. отдаления получения эффекта, Δ", initial=0.1)
    effect_year = forms.IntegerField(label="Год наступления эффекта")
    car_type = forms.CharField(label="Модель вагона")
    carrying_capacity = forms.FloatField(label="Грузоподъемность, т")
    tare_weight = forms.FloatField(label="Масса тары, т")
    car_service_life = forms.IntegerField(label="Срок службы вагона, лет")
    depot_repair_period = forms.IntegerField(label="Срок деповского ремонта, лет")
    major_repair_period = forms.IntegerField(label="Срок капитального ремонта, лет")
    axial_load = forms.FloatField(label="Нагрузка на ось, тс")

    def __init__(self, *args, **kwargs):
        super(MotherForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})


class CarForm(MotherForm):
    body_volume = forms.FloatField(label="Объем кузова, куб. м")

    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})


class PlatformForm(MotherForm):
    floor_area = forms.FloatField(label="Площадь пола, кв. м")

    def __init__(self, *args, **kwargs):
        super(PlatformForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})


class TankForm(MotherForm):
    tank_volume = forms.FloatField(label="Объем котла, куб. м")

    def __init__(self, *args, **kwargs):
        super(TankForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})
