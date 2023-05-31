from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import datetime, os
from selenium.webdriver.support.ui import Select

login_fansly = os.environ.get('login_fansly')
password_fansly = os.environ.get('password_fansly')


def posting(l: list, hours: int):
    """ Запуск браузера, открытие целевого профиля и сопутствующие клики по элементам
        dic - Словарь с данными
        hours - количество часов, для отложенного удаления постов  """

    options = Options()
    service = Service('geckodriver.exe')
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Укажите путь к бинарному файлу Firefox
    browser = webdriver.Firefox(service=service, options=options)
    browser.maximize_window()
    browser.get('https://fansly.com/')
    sleep(2)

    enter_button = browser.find_element("xpath", "/html/body/app-root/div/div[3]/app-age-gate-modal/div/div/div["
                                                 "4]/div/div[2]")
    enter_button.click()
    sleep(2)

    login_input = browser.find_element("xpath",
                                       "/html/body/app-root/div/div[1]/div/app-landing-page/div/div[1]/div[2]/div[1]/div[2]/div[1]/div/input")
    login_input.send_keys(login_fansly)
    pssword_input = browser.find_element("xpath",
                                         "/html/body/app-root/div/div[1]/div/app-landing-page/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/input")
    pssword_input.send_keys(password_fansly)
    sleep(2)

    login_button = browser.find_element(By.CLASS_NAME, "btn.outline-blue.large.margin-top-1")
    login_button.click()
    sleep(4)

    later_button = browser.find_element(By.CLASS_NAME, "btn.margin-top-2")
    later_button.click()
    sleep(8)

    for i in l:
        """ Цикл кликов по различным элементам, для того чтобы поочередно постить сохраненные данные
            key - Текст для поста
            value - Путь к изображению на устройстве """

        text_for_post = browser.find_element("xpath",
                                             "/html/body/app-root/div/div[1]/div/app-feed-route/div[1]/div/div/app-post-creation/div[1]/div[2]/div[2]/textarea")
        text_for_post.send_keys(i[0])
        sleep(2)
        pre_upload_button = browser.find_element("xpath",
                                                 "/html/body/app-root/div/div[1]/div/app-feed-route/div[1]/div/div/app-post-creation/div[2]/div[1]/div/div[1]/i")
        pre_upload_button.click()
        sleep(2)
        upload_button = browser.find_element("xpath",
                                             "/html/body/app-root/div/div[1]/div/app-feed-route/div[1]/div/div/app-post-creation/div[2]/div[1]/div/div[2]/div[1]/i")
        upload_button.click()
        sleep(2)

        app = Application(backend="win32").connect(title='File Upload')
        sleep(1)
        file_dialog = app['File Upload']
        sleep(1)
        file_name_edit = file_dialog.Edit
        sleep(1)
        file_name_edit.set_text(i[1])
        sleep(1)
        send_keys("{ENTER}")
        sleep(1)
        trash_button = browser.find_element("xpath", "/html/body/app-root/div/div[3]/app-account-media-upload/div/div["
                                                     "2]/div[2]/app-account-media-permission-flags-editor/div[2]/div/div[1]/i")
        trash_button.click()
        sleep(1)

        upload_button = browser.find_element("xpath",
                                             "/html/body/app-root/div/div[3]/app-account-media-upload/div/div[3]/div[2]/div[3]")
        upload_button.click()
        sleep(4)

        del_timer_button = browser.find_element("xpath",
                                                "/html/body/app-root/div/div[1]/div/app-feed-route/div[1]/div/div/app-post-creation/div[2]/div[3]/div/i[1]")
        del_timer_button.click()
        sleep(1)

        # Работа с временем и установкой отложенного удаления поста
        current_time = datetime.datetime.now()
        delta = datetime.timedelta(hours=hours)
        new_time = current_time + delta
        new_hours = new_time.hour
        new_hours_formatted = str(new_hours).zfill(2)

        if new_time.day != current_time.day:
            # Если прибавляя часы к дате мы окажемся в следующем дне, выбираем следующий день:
            current_element = browser.find_element("xpath", "//td[@class='current-month-day is-selected is-today']")
            next_element = current_element.find_element("xpath",
                                                        "./following-sibling::td | ./following-sibling::tr[1]//td")
            next_element.click()
            sleep(1)

        # Дальше выставление времени удаления в селекторе часов
        select_element = browser.find_element(By.CLASS_NAME, "form-select")
        select = Select(select_element)
        select.select_by_visible_text(new_hours_formatted)
        sleep(1)

        confirm_button = browser.find_element("xpath",
                                              "/html/body/app-root/div/div[3]/app-post-expiry-modal/div/div[3]/div[2]")
        confirm_button.click()
        sleep(2)

        post_button = browser.find_element("xpath",
                                           "/html/body/app-root/div/div[1]/div/app-feed-route/div[1]/div/div/app-post-creation/div[2]/div[9]")
        post_button.click()
        sleep(3)

    browser.quit()
