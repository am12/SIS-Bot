import atexit
import datetime
import sys
from tokenize import String
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass

def click_button(browser, button_id: String, wait_duration: int = 20):
    staleElement = True
    while staleElement:
        try:
            submit = WebDriverWait(browser, wait_duration).until(
                EC.element_to_be_clickable((By.ID, button_id))
            )
            submit.click()
            staleElement = False
        except:
            staleElement = True

def dismiss_warnings(browser, prompt_type: String):
    try:
        click_button(browser, f'ctl00_contentPlaceHolder_rb{prompt_type}Yes')
        click_button(browser, 'ctl00_contentPlaceHolder_cmdContinue')
        return True
    except:
        return False

def button_exists(browser, button_id: String):
    try:
        browser.find_element(By.ID, button_id)
        return True
    except:
        return False

def exit_browser():
    print("Exiting the browser...")
    browser.quit()

try:
    usernameStr = sys.argv[1]
    isgrad = len(sys.argv) >= 3 and sys.argv[2] == 'grad'
except BaseException:
    print("\nError: This script should be run with the following (valid) flags:\n python bot.py <jhed@jh.edu>\n")
    sys.exit(-1)

passwordStr = getpass()

browser = webdriver.Chrome()
atexit.register(exit_browser)  # Ensure browser quits on exit

try:
    browser.get("https://sis.jhu.edu/sswf/")
    
    click_button(browser, 'linkSignIn')

    username = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.NAME, 'loginfmt')))
    username.send_keys(usernameStr)

    click_button(browser, 'idSIButton9')

    password = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.NAME, 'passwd')))
    password.send_keys(passwordStr)

    click_button(browser, 'idSIButton9')

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "aspnetForm")))

    browser.get("https://sis.jhu.edu/sswf/SSS/EnrollmentCart/SSS_EnrollmentCart.aspx?MyIndex=88199")

    click_button(browser, 'SelectAllCheckBox')

    register_str = 'ctl00_contentPlaceHolder_cmdSubmit' if isgrad else 'ctl00_contentPlaceHolder_ibEnroll'
    register = browser.find_element(By.ID, register_str)

    # Wait until it's 7 O'clock
    while True:
        hr = datetime.datetime.now().time().hour
        if hr >= 7:
            click_button(browser, register_str, 0)
            if button_exists(browser, 'ctl00_contentPlaceHolder_cmdSubmit'):
                click_button(browser, 'ctl00_contentPlaceHolder_cmdSubmit')

            warning = True
            while warning:
                warning = False
                warning |= dismiss_warnings(browser, 'Waitlist')
                warning |= dismiss_warnings(browser, 'Override')
                warning |= dismiss_warnings(browser, 'Approval')
except KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting gracefully.")
finally:
    browser.quit()
