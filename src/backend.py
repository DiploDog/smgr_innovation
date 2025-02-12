from urllib.request import urlretrieve
import pandas as pd
from car_info import CARS_CODE, CARS_CHARS
import os

class Car:

    smgr1_url = 'https://vs2.numeral.su/wp-content/uploads/%D0%A1%D0%9C%D0%93%D0%A01.xlsx'
    filename = 'СМГР1.xlsx'

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
                 effect_year):

        self.car_type = car_type
        self.delta = delta
        self.effect_year = effect_year

        self.new_carrying_capacity = carrying_capacity
        self.new_tare_weight = tare_weight
        self.new_car_service_life = car_service_life
        self.new_depot_repair_period = depot_repair_period
        self.new_major_repair_period = major_repair_period
        self.new_axial_load = axial_load
        self.new_body_volume = body_volume

        self.old_carrying_capacity = None
        self.old_tare_weight = None
        self.old_car_service_life = None
        self.old_depot_repair_period = None
        self.old_major_repair_period = None
        self.old_axial_load = None
        self.old_body_volume = None


    def calculate_gamma(self):
        gamma = 1 / ((1 + self.delta) ** self.effect_year)
        return gamma

    def download_smgr1(self):
        try:
            urlretrieve(self.smgr1_url, self.filename)
        except Exception as e:
            print(f'Неизвестная ошибка во время скачивания {self.filename}.\n'
                  f'Пожалуйста, проверьте соединение с интернетом, отключите VPN\n'
                  f'или посетите сайт https://numeral.su/smgr/')

    def __get_old_vals(self):
        try:
            smgr_df = pd.read_excel(self.filename)
            try:
                smgr_df = smgr_df[CARS_CHARS]
            except KeyError:
                print('Некорректный запрос к таблице.')
            return smgr_df[CARS_CHARS]
        except FileNotFoundError:
            print(f'Отсутствует файл {self.filename} папке innovative_car/src/')

    def calculate_mean_smgr(self):
        df = self.__get_old_vals().astype('float32')
        df_filtered_by_type = df[df['Шифр модели'].startswith(self.car_type[:2])]
        mean_vals = dict(df_filtered_by_type.mean())
        return mean_vals



print(pd.read_excel('СМГР1.xlsx').columns)