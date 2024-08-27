import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# For chrome config: disable notification and maximize window
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# For login exceptions
from selenium.common.exceptions import NoSuchElementException

from my_module import find_by_xpath,find_and_click_by_xpath,wait_for_presence_xpath, wait_until_clickable_xpath

option = Options()
option.add_argument("--disable-notifications")
option.add_argument("start-maximized")

# Initiate Chrome WebDriver (Open Chrome)
driver = webdriver.Chrome(options=option)
# Define Impliticity wait time
wait = WebDriverWait(driver, 10)


# Initialize WebDriver if needed, rediredt to homepage_url
def get_homepage():
    global driver
    if driver is None or not driver.session_id:
        driver = webdriver.Chrome(options=option)
    homepage_url = "https://newshop.vn/"
    driver.get(homepage_url)


# Quit driver. Set driver to None after quitting to ensure reinitialization
def quit_driver():
    time.sleep(2)
    global driver
    if driver is not None:
        driver.quit()
        driver = None



# Check to see if user logged in
def is_login_successful():
    try:
        # wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Đăng xuất")))
        driver.find_element(By.PARTIAL_LINK_TEXT, "Đăng xuất")
        return True
    except NoSuchElementException:
        return False


# Log in
def login(username, password):
    print(f'Tài khoản: {username} \nMật khẩu: {password}')
    wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Đăng nhập"))).click()

    login_username_field_xpath = "(//input[@name='email'])[2]"
    login_username_field = wait.until(ec.visibility_of_element_located(
        (By.XPATH, login_username_field_xpath)))
    login_username_field.clear()
    login_username_field.send_keys(username)
    print("Đã nhập tk")

    login_password_field_xpath = "(//input[@name='password'])[1]"
    login_password_field = find_by_xpath(login_password_field_xpath)
    login_password_field.clear()
    login_password_field.send_keys(password)
    print("Đã nhập mk")
    login_password_field.send_keys(Keys.ENTER)

    if is_login_successful():
        print("Đăng Nhập thành công!")
        return True
    else:
        print('Đăng nhập thất bại, sai tài khoản/mật khẩu!')


# Log out
def logout():
    if is_login_successful():
        driver.find_element(By.LINK_TEXT, "Đăng xuất").click()
    print("Đăng Xuất thành công!")


# Check to see if user's password has changed
def is_password_changed():
    cases = {
        "//div[contains(@class,'alert') and contains(@class,'alert-success')]":
            True,
        "//li[contains(text(),'Mật khẩu xác nhận không trùng.')]":
            "Mật khẩu xác nhận không trùng.",
        "//li[contains(text(),'Mật khẩu cần phải lớn hơn 8 ký tự.')]":
            "Mật khẩu cần phải lớn hơn 8 ký tự.",
        "//li[contains(text(),'Mật khẩu là bắt buộc')]":
            "Mật khẩu là bắt buộc"
    }

    for key, value in cases.items():
        try:
            e = find_by_xpath(key)
            if isinstance(value, str):
                print(e.text)
                return False
            return value

        except NoSuchElementException:
            continue
    print("Lỗi không xác định")
    return False


# Change user's password
def change_password(newpassword):
    if is_login_successful():
        driver.find_element(By.LINK_TEXT, "Tài khoản").click()
        driver.find_element(By.LINK_TEXT, "Đổi mật khẩu").click()
    # Input new password
    new_password_field = wait_for_presence_xpath("//input[@name='password']")
    new_password_field.send_keys(newpassword)

    # Confirm new password
    new_password_confirmation = find_by_xpath(
            "//input[@name='password_confirmation']")
    new_password_confirmation.send_keys(newpassword+'1')
    new_password_confirmation.send_keys(Keys.ENTER)
    if is_password_changed():
        print('Đổi mật khẩu thành công!')
    else:
        print('Mật khẩu/Mật khẩu xác nhận không hợp lệ!')
    # Không trùng, dưới 8 kí tự, bỏ trống


def main():
    login('ntwolf23@gmail.com','dat12345')
