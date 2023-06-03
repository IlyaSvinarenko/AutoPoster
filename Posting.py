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
count_of_complete_posts = 0

def fansly_open(l: list, hours: int):
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
    posting_cycle(l, browser, hours)

def posting_cycle(l, browser, hours):
    global count_of_complete_posts
    try:
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

            dialog_window(file_path=i[1])
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
                next_element = current_element.find_element("xpath", "./following::td[1]")
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
            sleep(5)

            post_button = browser.find_element("xpath",
                                               "/html/body/app-root/div/div[1]/div/app-feed-route/div[1]/div/div/app-post-creation/div[2]/div[9]")
            post_button.click()
            count_of_complete_posts += 1
            print('count_of_complete_posts = 1')
            sleep(4)
        browser.quit()
        count_of_complete_posts = 0
    except:
        print('////////////////   Произошла ошибка в posting_cycle   //////////////')
        browser.refresh()
        sleep(8)
        posting_cycle(l[count_of_complete_posts], browser, hours)


def dialog_window(file_path):
    app = Application(backend="win32").connect(title='File Upload')
    sleep(1)
    file_dialog = app['File Upload']
    try:
        sleep(1)
        if file_dialog.exists():
            print('file_dialog.exists()file_dialog.exists()file_dialog.exists()')
        file_name_edit = file_dialog.Edit
        sleep(1)
        file_name_edit.set_text(file_path)
        sleep(1)
        file_dialog.type_keys("{ENTER}")
    except:
        print('////////////////   Произошла ошибка в dialog_window   //////////////')
        file_dialog.close()
        sleep(2)
        dialog_window(file_path)


# l = [['‼️𝙁𝙍𝙀𝙀 𝙉𝙐𝘿𝙀𝙎 𝙏𝙊𝘿𝘼𝙔 𝙊𝙉𝙇𝙔 fans.ly/pandabigbooty ‼️ 𝙈𝙔 𝘾𝙐𝙏𝙀 𝘽𝙇𝙊𝙉𝘿𝙀 𝘽𝙀𝙎𝙏𝙄𝙀 𝙒𝙄𝙏𝙃 𝙃𝙐𝙂𝙀 𝘽𝙐𝘽𝘽𝙇𝙀 𝘼𝙎𝙎 𝙄𝙎 𝙇𝙊𝙊𝙆𝙄𝙉𝙂 𝙁𝙊𝙍 𝘼  𝘿𝙄𝘾𝙆 𝙏𝙊 𝙋𝙇𝘼𝙔 𝙒𝙄𝙏𝙃 🍆👉🏻  fans.ly/pandabigbooty 👈🏻\n\n❤️𝙎𝙀𝙓𝙏𝙄𝙉𝙂 🥵𝘾𝙐𝙎𝙏𝙊𝙈 𝙍𝙀𝙌𝙐𝙀𝙎𝙏𝙎 💕𝙂𝙁𝙀 💦𝘿𝙄𝘾𝙆 𝙍𝘼𝙏𝙀𝙎 🔥𝙃𝙐𝙂𝙀 𝙑𝙄𝘿𝙀𝙊 𝙎𝙏𝙊𝙍𝙀😈𝙏𝘼𝘽𝙊𝙊🍑 𝙏𝙒𝙀𝙍𝙆 𝙌𝙐𝙀𝙀𝙉 🤩𝘿𝘼𝙈𝙉 𝙎𝙃𝙀’𝙎 𝙎𝙊 𝙆𝙄𝙉𝙆𝙔😈\n⭕️𝙁𝙊𝙇𝙇𝙊𝙒 𝙁𝙊𝙍 𝙁𝙍𝙀𝙀 𝙍𝙉! 𝘼𝙉𝘿 𝘿𝙈 𝙃𝙀𝙍 𝙁𝙊𝙍 𝙁𝙍𝙀𝙀 😙 fans.ly/pandabigbooty\n#slut #pawg #bigass #hugeass #bbw #curvy #tattoos #ass #bigboobs #fyp #phat #thick #thicc #twerk #gfe #sexting #custom #twerk #boobs #milf #booty #chubby #ass #submissive #alt #blonde', 'C:\\_Project\\AutoPoster\\images\\1618.jpg'], ['Wonder if you would punish me for being so naughty.💋\nI want you to tear my clothes off my body.👅\nFind me here ▶️ @RubyRoss 🥰 fansly.com/RubyRoss 🥰', 'C:\\_Project\\AutoPoster\\images\\1617.jpg'], ['FOLLOW THIS CUTE GIRL @LeaBonita and see her explicit content!🥰💦 fansly.com/LeaBonita 💦', 'C:\\_Project\\AutoPoster\\images\\1616.jpg'], ['I have been a really naughty girl today. I think I need to be punished!🤤😰\nCan I be your favorite naughty girl?😈 hmm come on daddy!👅💋\nText me @BlondyMyra 😍 fansly.com/BlondyMyra 😍', 'C:\\_Project\\AutoPoster\\images\\1615.jpg'], ["@MayaLaster wants to show you what's in her pussy 😱 @MayaLaster 🔥\nLoves to fuck herself in the ass and pussy,give passionate blowjobs 🤯.Makes the best sexing and cock appreciation 😍\nKeep the link to her hot content 👉🏻  https://fans.ly/subscriptions/giftcode/NDQ3MTAxNDAxNDc1MDY3OTA0OjE6MTo0ZTYyMWFkZDQz  ✅\n\nFansly\nFollow me for free on Fansly! <3\n\n#fyp #tattoo #dildo #sex #pussy #ass #sexting #custom #anal #teen #young", 'C:\\_Project\\AutoPoster\\images\\1614.jpg'], ["@Melissamell 🧡\nI will satisfy your many fantasies and desires\nStreaming on webcam and planning to stream on twitch - CS:GO and Retro Games\nI'm Kinky girl, but i love to chat before some dirty things, it giving more pleasure, you agree? 😏 26 years old naughty girl\nFree first week, to feel me fully 👇💋\nfans.ly/subscriptions/giftcode/NTIwMjcyMDIyMjQxMDMwMTQ0OjE6MTpkM2U0YTA4NjU5\n#fyp #bigtits #bigboobs #gamergirl", 'C:\\_Project\\AutoPoster\\images\\1613.jpg']]
# hours = 24
# fansly_open(l, hours)