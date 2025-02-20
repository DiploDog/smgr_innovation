from urllib.request import urlretrieve


class App:
    def __init__(self, smgr1_url, filename):
        self.smgr1_url = 'https://vs2.numeral.su/wp-content/uploads/%D0%A1%D0%9C%D0%93%D0%A01.xlsx'
        self.filename = 'СМГР1.xlsx'

    def download_smgr1(self):
        try:
            urlretrieve(self.smgr1_url, self.filename)
        except Exception as e:
            print(f'Неизвестная ошибка во время скачивания {self.filename}.\n'
                  f'Пожалуйста, проверьте соединение с интернетом, отключите VPN\n'
                  f'или посетите сайт https://numeral.su/smgr/')