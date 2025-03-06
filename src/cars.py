import pandas as pd
from typing import Tuple, Dict
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
                 delta=0.1,
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

    def gamma(self, t):
        return 1 / ((1 + self.delta) ** (t - 1))

    def cols_from_attrs(self):
        return [attr for attr in self.__dict__.keys()][3:]

    def calculate_mean_vals(self, table):
        cols = self.cols_from_attrs()
        translated_dict_of_cols = {CARS_FEAT[col]: col for col in cols}
        filtered_table = self.smgr_select_type(table)[translated_dict_of_cols.keys()]
        filtered_table.rename(columns=translated_dict_of_cols, inplace=True)
        return filtered_table[cols].mean().round(2)

    @staticmethod
    def N_K(table1, table2, coeff="N"):
        if coeff == "N":
            table_comparison = table1 > table2
        elif coeff == "K":
            table_comparison = table1 < table2
        n_k = table_comparison.values.sum()
        table_comparison = table_comparison.iloc[0, :]
        try:
            table1 = table1.iloc[0, :]
        except pd.errors.IndexingError:
            pass
        if n_k == 0:
            n_k = 1
        masked_table1 = table1[~table_comparison].to_dict()
        return n_k, masked_table1

    @staticmethod
    def inside_sum_sign(gamma, val1, val2):
        return round(gamma * val1 / val2, 2)

    @staticmethod
    def is_time_bound(attr_name: str):
        return True if 'life' or 'period' in attr_name else False

    def get_gammas_sum(self, values: Dict, valid=False):
        gammas = []
        for k, v in values.items():
            if self.is_time_bound(k):
                gammas.append(self.gamma(v))
            else:
                gammas.append(1)
        return sum(gammas)

    def equation_member(self, values, smgr_dict, coeff):
        sum_member = []
        for k, v in values.items():
            gamma = self.gamma(v) if self.is_time_bound(k) else 1
            sum_member.append(
                self.inside_sum_sign(gamma, v, smgr_dict[k])
            )
        return round(sum(sum_member) / coeff, 2)

    def p_inn_valid(self, table):
        _, _, N, K = self.compare_features(table)
        entered_table_feats = self.df_from_attrs()
        _, greater_values = self.N_K(table, entered_table_feats, coeff="N")
        _, smaller_values = self.N_K(table, entered_table_feats, coeff="K")
        greater_gammas = self.get_gammas_sum(greater_values)
        smaller_gammas = self.get_gammas_sum(smaller_values)
        p_inn_valid = round(greater_gammas / N + smaller_gammas / K, 2)
        print(f"p_inn_valid: {p_inn_valid}")
        return p_inn_valid

    def p_inn(self, table):
        greater_values, smaller_values, N, K = self.compare_features(table)
        smgr_dict = table.to_dict()
        N_member = self.equation_member(greater_values, smgr_dict, N)
        K_member = self.equation_member(smaller_values, smgr_dict, K)
        p_inn = N_member + K_member
        print(f"p_inn: {p_inn}")
        return p_inn

    def is_innovative(self, table):
        return self.p_inn(table) / self.p_inn_valid(table)

    def df_from_attrs(self):
        return pd.DataFrame(self.__dict__, index=[0]).iloc[:, 3:]

    def compare_features(self, table: pd.DataFrame) -> Tuple[Dict, Dict, int, int]:
        entered_table_feats = self.df_from_attrs()
        total_feats = entered_table_feats.shape[1]
        if total_feats == len(table):
            N, greater_values = self.N_K(entered_table_feats, table, coeff="N")
            K, smaller_values = self.N_K(entered_table_feats, table, coeff="K")
            return greater_values, smaller_values, N, K
        else:
            print("ERROR")

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


smgr = pd.read_excel("СМГР1.xlsx")
car = Car("19-1273",
          77,
          23,
          26,
          2,
          13,
          25,
          107,
          0.1,
          5)

smgr_df = car.calculate_mean_vals(smgr)
print(car.is_innovative(smgr_df))

