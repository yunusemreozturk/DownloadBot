"""
Eğitim amaçlı yapılmıştır.
"""
import os
import shutil
import pyautogui
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  # en yeni google drive almamıza yarıyor
from selenium.webdriver.common.keys import Keys  # belirli tuşlara basabilmemiz olanak sağlar
import time
from os import walk


class Download:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    count = 0

    def login(self):
        username = 'username'
        password = 'password'
        url = 'https://1milyonistihdam.hmb.gov.tr/ozgecmis/login'

        self.driver.get(url)

        time.sleep(2)

        username_login = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[1]/div/div/form/div[1]/input')
        username_login.send_keys(username)

        time.sleep(2)

        pass_login = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[1]/div/div/form/div[2]/input[1]')
        pass_login.send_keys(password)

        username_login.send_keys(Keys.ENTER)

        time.sleep(2)

        self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]/div/div/div/div/a').click()

    def get_link(self, url):
        href_list = []
        name_list = []

        if self.count == 0:
            self.login()
            time.sleep(1)

        self.driver.maximize_window()
        time.sleep(1)

        self.count += 1

        self.driver.get(url)
        time.sleep(1)

        name = self.driver.find_element_by_css_selector('div.col-md-6.col-xs-12.hero-info h2').text

        href_rows = self.driver.find_elements_by_css_selector('div.course-play-icon a')
        with open(f'href-name.txt', 'w', encoding='utf-8') as file:
            for item in href_rows:
                if str(item.get_attribute('href')) != 'None':
                    href_list.append(str(item.get_attribute('href')))
                    print(href_list[-1])
                    file.write(str(href_list[-1]) + '\n')

        name_rows = self.driver.find_elements_by_css_selector('div.cbp_tmlabel a h4')
        with open(f'name.txt', 'w', encoding='utf-8') as file:
            for item in name_rows:
                name_list.append(str(item.text))
                print(name_list[-1])
                file.write(str(name_list[-1]) + '\n')

        return name_list, href_list, name

    @staticmethod
    def check_file(path, name):
        dirnames = []

        for (dirpath, dirnames, filenames) in walk(path):
            break

        if name in dirnames:
            return True
        elif name not in dirnames:
            return False

    @staticmethod
    def get_file_name(path):
        filenames = []

        for (dirpath, dirnames, filenames) in walk(path):
            break

        return filenames

    @staticmethod
    def delete_letters(name_list):
        new_list = []
        disallowed_characters = ['Ç', 'ç', 'ğ', 'Ğ', 'Ö', 'ö', 'Ş', 'ş', 'ı', 'İ', 'Ü', 'ü', '?', '!', ',', '#', '/',
                                 '\\', "'", ':', ';']

        for item in name_list:
            for character in disallowed_characters:
                item = item.replace(character, '')
            new_list.append(item)

        return new_list

    def bot(self, name_list, href_list, lesson_name):
        f = []

        self.driver.minimize_window()

        if not self.check_file(f'C:\\Users\\Genos\\Downloads\\Video', lesson_name):
            os.makedirs(f'C:\\Users\\Genos\\Downloads\\Video\\{lesson_name}')

        time.sleep(1)

        for name_item, href_item in zip(name_list, href_list):
            name_item = name_item.strip()
            name = name_item + '.mp4'

            pyautogui.click(430, 65)
            pyautogui.write(href_item)

            time.sleep(1)

            pyautogui.press('enter')

            time.sleep(12)

            pyautogui.click(1773, 971, duration=0.5)
            pyautogui.click(1641, 574, duration=0.5)
            pyautogui.click(925, 499, clicks=3)
            pyautogui.write(name)
            pyautogui.click(959, 614)

            while name not in f:
                f = self.get_file_name(f"C:\\Users\\Genos\\Downloads\\Video")

                time.sleep(8)

            source = f'C:\\Users\\Genos\\Downloads\\Video\\{name}'
            destination = f'C:\\Users\\Genos\\Downloads\\Video\\{lesson_name}'

            shutil.move(source, destination)

            pyautogui.click(1837, 969)

        os.remove(f'href-name.txt')
        os.remove(f'name.txt')


list1 = [
    'https://www.btkakademi.gov.tr/portal/course/blokzincir-ve-kripto-paralar-10569#!/about',
    'https://www.btkakademi.gov.tr/portal/course/buyuk-veri-uygulamalar--10925#!/about']

object = Download()

for item in list1:
    name_list, href_name, name = object.get_link(item)
    new_list = object.delete_letters(name_list)

    object.bot(new_list, href_name, name)
