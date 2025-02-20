import pandas as pd
from datetime import datetime, timedelta
from car_info import CARS_CODE, CARS_FEAT
import os


class Car:

    def __init__(self,
                 car_type,
                 carrying_capacity,
                 tare_weight,
                 car_service_life,
                 depot_repair_period,
                 major_repair_period,
                 axial_load,
                 body_volume,
                 delta,
                 effect_year=5):

        self.delta = delta
        self.effect_year = effect_year

        self.car_type = car_type
        self.carrying_capacity = carrying_capacity
        self.tare_weight = tare_weight
        self.car_service_life = car_service_life
        self.depot_repair_period = depot_repair_period
        self.major_repair_period = major_repair_period
        self.axial_load = axial_load
        self.body_volume = body_volume

    def extract_car_type_num(self):
        return self.car_type[:2]

    def calculate_gamma(self):
        gamma = 1 / ((1 + self.delta) ** (self.effect_year - 1))
        return gamma

    def cols_from_attrs(self):
        return [attr for attr in self.__dict__.keys()][2:]

    def calculate_mean_vals(self, table):
        cols = self.cols_from_attrs()
        filtered_table = self.smgr_select_type(table)
        return filtered_table[cols].mean().round(2)

    def compare_features(self, table: pd.DataFrame):
        entered_table_feats = pd.DataFrame(self.__dict__, index=[0]).iloc[:, 3:]
        total_feats = entered_table_feats.shape[1]
        if total_feats == table.shape[1]:
            increased_feats = (entered_table_feats > table).values.sum()
            decreased_feats = total_feats - increased_feats
            #TODO
    def smgr_select_type(
            self,
            table,
            col_type="Шифр модели",
            col_year="Год выпуска"
    ):
        begin_year = int(
            (
                datetime.today() - timedelta(
                    self.effect_year * 365
                         )
            ).year
        )
        car_type_extracted = self.extract_car_type_num()
        filtered_table = table[
            (table[col_type].str.startswith(
                car_type_extracted)) &
            (table[col_year] >= begin_year)
        ]
        return filtered_table

class Platform(Car):

    def __init__(self, car_type,
                 carrying_capacity,
                 tare_weight,
                 car_service_life,
                 depot_repair_period,
                 major_repair_period,
                 axial_load,
                 floor_area,
                 delta,
                 effect_year,
                 ):
        super().__init__(
            car_type,
            carrying_capacity,
            tare_weight,
            car_service_life,
            depot_repair_period,
            major_repair_period,
            axial_load,
            delta,
            effect_year
        )
        self.floor_area = floor_area


class Tank(Car):
    def __init__(self, car_type,
                 carrying_capacity,
                 tare_weight,
                 car_service_life,
                 depot_repair_period,
                 major_repair_period,
                 axial_load,
                 tank_volume,
                 delta,
                 effect_year,
                 ):
        super().__init__(
            car_type,
            carrying_capacity,
            tare_weight,
            car_service_life,
            depot_repair_period,
            major_repair_period,
            axial_load,
            delta,
            effect_year
        )
        self.tank_volume = tank_volume


class Isothermic(Car):
    def __init__(self, car_type,
                 carrying_capacity,
                 tare_weight,
                 car_service_life,
                 depot_repair_period,
                 major_repair_period,
                 axial_load,
                 body_volume,
                 delta,
                 effect_year,
                 heat_transfer_coeff
                 ):
        super().__init__(
            car_type,
            carrying_capacity,
            tare_weight,
            car_service_life,
            depot_repair_period,
            major_repair_period,
            body_volume,
            axial_load,
            delta,
            effect_year
        )
        self.heat_transfer_coeff = heat_transfer_coeff

#
car = Car(1,2,3,4,5,6,7,8,9,10)
car2 = Car(3,1,4,5,2,6,7,8,9,10)

print(
    (pd.DataFrame(car.__dict__, index=[0]).iloc[:,3:] >
    pd.DataFrame(car2.__dict__, index=[0]).iloc[:,3:]).values.sum()
)
# for attr in car.__dict__:
#     print(attr, car.__dict__[attr])

