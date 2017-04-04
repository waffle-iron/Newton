from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

IXL_ACCOUNTS = [('atrost', '1'), ('kcyphers', '1'), ('smackinnon', '1'), ('tdasilva', '1')]
MYON_ACCOUNTS = [('atrost', '123')]
KIDSAZ_accounts = [('atrost', 'keebo333')]
IXL_LEVEL_DOWNLOADS = ['C', 'D', 'E', ]
IXL_LEVEL_NUMBERS = ['1', '2', '3', ]


def set_browser():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)  # custom location
    profile.set_preference('browser.download.dir',
                           '/Users/alexandertrost/PycharmProjects/newton/brain/scripts/csvdownloads')
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    # profile.set_preference('browser.download.dir',os.getcwd())
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    browser = webdriver.Firefox(firefox_profile=profile)
    return browser


def ixl_login(i):
    browser = set_browser()
    browser.get('https://www.ixl.com/signin/btwa/')
    assert "IXL" in browser.title
    try:
        username = browser.find_element_by_id('siusername')
        print('username {}'.format(username.tag_name))
        password = browser.find_element_by_id('sipassword')
        print('password {}'.format(password.tag_name))
        button = browser.find_element_by_id('custom-signin-button')
        print('button {}'.format(button.tag_name))
        username.send_keys(IXL_ACCOUNTS[i][0])
        password.send_keys(IXL_ACCOUNTS[i][1])
        password.submit()
    except:
        print("Login fields not found")
    return browser


def myon_login(i):
    browser = set_browser()
    # browser.get('https://www.myon.com/login/index.html')
    todays_date = str(date.today())
    browser.get(
        'https://myon.com/api/reports/facultyReports.json:lexileByStudent?begin_date=2016-08-05&end_date=' + todays_date + '&download=true')

    assert "myON" in browser.title
    try:
        building = browser.find_element_by_id('buildingText')
        building.send_keys("Booker T Washington")
    except:
        print("couldn't find building")
    time.sleep(1)
    try:
        building.send_keys(Keys.ENTER)
    except:
        print("Couldn't hit enter")

    try:
        username = browser.find_element_by_name('username')
        username.send_keys(MYON_ACCOUNTS[i][0])
    except:
        print("Couldn't find username")
    try:
        password = browser.find_element_by_name('password')
        password.send_keys(MYON_ACCOUNTS[i][1])
        password.submit()
    except:
        print("couldn't find password")
    return browser


def download_myon_report(browser):
    time.sleep(2)
    todays_date = str(date.today())
    browser.get(
        'https://myon.com/api/reports/facultyReports.json:lexileByStudent?begin_date=2016-08-05&end_date=' + todays_date + '&download=true')
    time.sleep(3)


def scrape_ixl_scoregrid(browser):
    browser.get('https://www.ixl.com/analytics/score-grid#grade=1')
    time.sleep(2)
    download_ixl_report(browser)
    browser.get('https://www.ixl.com/contact')
    browser.get('https://www.ixl.com/analytics/score-grid#grade=2')
    time.sleep(2)
    download_ixl_report(browser)
    browser.get('https://www.ixl.com/contact')
    browser.get('https://www.ixl.com/analytics/score-grid#grade=3')
    time.sleep(2)
    download_ixl_report(browser)

    time.sleep(3)


def download_ixl_report(browser):
    try:
        download_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "img-export")))
        print('download button found: {}'.format(download_button.tag_name))
        download_button.click()
        download_button.click()
    except:
        print('no download button found.')
    time.sleep(2)
    try:
        export_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "submit-button")))
        print('export button found: {}'.format(export_button.tag_name))
        time.sleep(1)
        export_button.click()
    except:
        print('no export button found.')
    time.sleep(2)


def get_ixl_stats(browser, i):
    browser.get('https://www.ixl.com/analytics/students-quickview')
    time.sleep(8)
    student_names = browser.find_elements_by_class_name( "student-name-column")
    last_practiced = browser.find_elements_by_class_name('last-active')
    questions = browser.find_elements_by_class_name('questions-num')
    time_spent = browser.find_elements_by_class_name('time-spent')
    results_list = []
    for j in range(len(student_names)):
        current_student = [student_names[j].text, last_practiced[j].text, questions[j].text, time_spent[j].text]
        results_list.append(current_student)
    write_ixl_stats_to_csv(results_list, i)


def write_ixl_stats_to_csv(results_list, i):
    outputFile = open('/Users/alexandertrost/PycharmProjects/newton/brain/scripts/csvdownloads/{}-ixlstats.csv'.format(
        IXL_ACCOUNTS[i][0]), 'w', newline='')
    outputWriter = csv.writer(outputFile)
    for row in results_list:
        outputWriter.writerow([row[0], row[1], row[2], row[3]])
    outputFile.close()


def full_ixl_scrape(i):  # Scrapes ALL relevant information from IXL for one teacher.
    browser = ixl_login(i)  # i is the # associated with the teacher in the list IXL ACCOUNTS
    scrape_ixl_scoregrid(browser)
    get_ixl_stats(browser, i)
    browser.quit()


def full_myon_scrape(i):
    browser = myon_login(i)
    download_myon_report(browser)
    browser.quit()


def run_all_teachers():  # The biggest function. Runs everything for the whole school.
    for i in range(len(IXL_ACCOUNTS)):
        full_ixl_scrape(i)
    for i in range(len(MYON_ACCOUNTS)):
        full_myon_scrape(i)

if __name__ == '__main__':
    run_all_teachers()