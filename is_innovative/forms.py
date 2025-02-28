from django import forms


class UserForm(forms.Form):
    delta = forms.FloatField(label="Коэфф. отдаления получения эффекта, Δ", initial=0.1)
    effect_year = forms.IntegerField(label="Год наступления эффекта")
    car_type = forms.CharField(label="Модель вагона", max_length=20)
    carrying_capacity = forms.FloatField(label="Грузоподъемность, т")
    tare_weight = forms.FloatField(label="Масса тары, т")
    car_service_life = forms.IntegerField(label="Срок службы вагона, лет")
    depot_repair_period = forms.IntegerField(label="Срок деповского ремонта, лет")
    major_repair_period = forms.IntegerField(label="Срок капитального ремонта, лет")
    axial_load = forms.FloatField(label="Нагрузка на ось, тс")
    body_volume = forms.FloatField(label="Объем кузова, куб. м")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})
