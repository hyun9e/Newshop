import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# For chrome config: disable notification and maximize window
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
# For hover function
from selenium.webdriver.common.action_chains import ActionChains
# For login exceptions
from selenium.common.exceptions import NoSuchElementException

option = Options()
option.add_argument("--disable-notifications")
option.add_argument("start-maximized")

# Initiate Chrome Driver/Open Chrome
driver = webdriver.Chrome(options=option)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)


def get_homepage():
    homepage_url = "https://newshop.vn/"
    driver.get(homepage_url)


# Find an element by XPATH
def find_by_xpath(element_path):
    return driver.find_element(By.XPATH, element_path)


# Find an element by XPATH and Click it
def find_and_click_by_xpath(element_path):
    find_by_xpath(element_path).click()


def hover_by_xpath(element_path):
    elem = actions.move_to_element(find_by_xpath(element_path))
    elem.perform()


# Wait for an element to be clickable
def wait_until_clickable_xpath(element_path):
    wait.until(ec.element_to_be_clickable(
        (By.XPATH, element_path))).click()


def wait_for_presence_xpath(element_path):
    return wait.until(ec.presence_of_element_located(
        (By.XPATH, element_path)))


# Adding items to cart
def add_items_to_cart():
    # Sách Văn Học Category
    find_and_click_by_xpath("//a[@id='menu-item-95']")

    # Random number of items to add
    number_of_items_to_add = random.randint(1, 10)  # Maximun items displayed per page: 24
    print("Đang thêm sản phẩm vào giỏ hàng %d lần!" % number_of_items_to_add)

    # Add x item(s) to the cart
    # for i in range(1, number_of_items_to_add+1):
    for i in range(1,number_of_items_to_add+1):
        # 1.1 Random add item with position.X from 0->24 counting from left to right
        position = random.randint(1, 24)

        # 1.2 Add item to cart
        item_xpath = f"(//span[@class='button-buy-now '])[{position}]"
        hover_by_xpath(item_xpath)
        find_and_click_by_xpath(item_xpath)

        # 1.3 Close the Cart pop-up screen and continue the loop
        continue_shopping_button = "//span[contains(text(),'Tiếp tục mua hàng')]"
        wait_until_clickable_xpath(continue_shopping_button)

    # 2. Cart report
    # 2.1 Open cart
    cart_button_xpath = "//a[contains(@class,'get-cart-box')]"
    wait_until_clickable_xpath(cart_button_xpath)

    # 2.2 Read cart details
    print(find_by_xpath("//div[contains(text(),'Giỏ hàng của bạn')]").get_attribute("innerText"))
    print("Tạm tính:", driver.find_element(By.CLASS_NAME, "cart-total").text)


def is_login_successful():
    try:
        # wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Đăng xuất")))
        driver.find_element(By.PARTIAL_LINK_TEXT, "Đăng xuất")
        return True
    except NoSuchElementException:
        return False


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


def logout():
    if is_login_successful():
        driver.find_element(By.LINK_TEXT, "Đăng xuất").click()
    print("Đăng Xuất thành công!")


# def is_password_changed():
#     try:
#         find_by_xpath("//div[contains(@class,'alert') and contains(@class,'alert-success')]")
#         return True
#     except NoSuchElementException:
#         try:
#             e = find_by_xpath("//li[contains(text(),'Mật khẩu xác nhận không trùng.')]")
#             print(e.text)
#             return False
#         except NoSuchElementException:
#             try:
#                 e = find_by_xpath("//li[contains(text(),'Mật khẩu cần phải lớn hơn 8 ký tự.')]")
#                 print(e.text)
#                 return False
#             except NoSuchElementException:
#                 try:
#                     e = find_by_xpath("//li[contains(text(),'Mật khẩu là bắt buộc')]")
#                     print(e.text)
#                     return False
#                 except NoSuchElementException:
#                     print("Lỗi không xác định")
#                     return False





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

def is_checkout_login_successful():
    try:
        find_by_xpath("//div[contains(text(),'* Đăng nhập để thanh toán tiện lợi hơn')]")
        return True
    except NoSuchElementException:
        return False

def proceed_to_checkout():
    get_homepage()
    cart_button_xpath = "//a[contains(@class,'get-cart-box')]"
    wait_until_clickable_xpath(cart_button_xpath)
    wait_until_clickable_xpath("//span[contains(text(),'Tiến hành thanh toán')]")

    is_checkout_login_successful()
    name = 'Nguyen Dat'
    email = 'exampleee@gmail.com'
    phone = '0123456789'
    find_and_click_by_xpath("//button[@type='submit']")
    find_by_xpath("//input[@placeholder='Họ và Tên']").send_keys(name)
    find_by_xpath("//input[@placeholder='Email']").send_keys(email)
    find_by_xpath("//input[@placeholder='Số điện thoại']").send_keys(phone)
    find_by_xpath("//input[@placeholder='Nhập lại số điện thoại']").send_keys(phone)
    find_by_xpath("//input[@placeholder='Nhập lại số điện thoại']").send_keys(phone)
    # adress = "(//li[@class ='el-select-dropdown__item'])[24]"
    # adress = "//li[@class='el-select-dropdown__item']/span[text()='Hà Nội']"
    address = "//span[contains(text(),'Hà Nội')]"
    address_2 = "//span[contains(text(),'Quận Bắc Từ Liêm')]"
    address_3 = "//span[contains(text(),'Phường Minh Khai')]"
    address_detail = "//input[@placeholder='Nhập số nhà, tên đường']"
    find_and_click_by_xpath(address)
    find_and_click_by_xpath(address_2)
    find_and_click_by_xpath(address_3)
    find_and_click_by_xpath(address_detail)






def main():
    # Open Newshop homepage
    get_homepage()
    # add_items_to_cart()

    proceed_to_checkout()


    # username = 'ntwolf23@gmail.com'
    # password = 'dat12345'
    # login(username, password)
    # change_password(password)
    # logout()
    time.sleep(2)
    driver.quit()


if __name__ == "__main__":
    main()
