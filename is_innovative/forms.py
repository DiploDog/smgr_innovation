from django import forms
from src.car_info import CARS_CODE


class CarTypeForm(forms.Form):
    car_type = forms.CharField(
        label="Модель вагона",
        widget=forms.Select(choices=CARS_CODE,
                            attrs={'class': 'form-control form-label'})
    )


class MotherForm(forms.Form):
    delta = forms.FloatField(label="Коэфф. отдаления получения эффекта, Δ", initial=0.1, step_size=0.01)
    car_type = forms.CharField(label="Модель вагона")
    carrying_capacity = forms.FloatField(label="Грузоподъемность, т", step_size=0.1)
    tare_weight = forms.FloatField(label="Масса тары, т", step_size=0.1)
    car_service_life = forms.IntegerField(label="Срок службы вагона, лет")
    depot_repair_period = forms.IntegerField(label="Срок деповского ремонта, лет")
    major_repair_period = forms.IntegerField(label="Срок капитального ремонта, лет")
    axial_load = forms.FloatField(label="Нагрузка на ось, тс", step_size=0.1)

    def __init__(self, *args, **kwargs):
        super(MotherForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})


class CarForm(MotherForm):
    body_volume = forms.FloatField(label="Объем кузова, куб. м", step_size=0.1)

    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})


class PlatformForm(MotherForm):
    floor_area = forms.FloatField(label="Площадь пола, кв. м", step_size=0.1)

    def __init__(self, *args, **kwargs):
        super(PlatformForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})


class TankForm(MotherForm):
    tank_volume = forms.FloatField(label="Объем котла, куб. м", step_size=0.1)

    def __init__(self, *args, **kwargs):
        super(TankForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})


class IsothermicForm(CarForm):
    heat_transfer_coeff = forms.FloatField(label="Коэффициент теплопередачи кузова", step_size=0.01)
    mean_heat_transfer_coeff = forms.FloatField(label="Средний коэффициент теплопередачи кузова", step_size=0.01)

    def __init__(self, *args, **kwargs):
        super(IsothermicForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})