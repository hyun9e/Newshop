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

# Initiate Chrome WebDriver (Open Chrome)
driver = webdriver.Chrome(options=option)
# Define Impliticity wait time
wait = WebDriverWait(driver, 10)
# For Hovering Function
actions = ActionChains(driver)

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



# Initialize WebDriver if needed, rediredt to homepage_url

# Find an element by XPATH
def find_by_xpath(element_path):
    return driver.find_element(By.XPATH, element_path)


# Find an element by XPATH and Click it
def find_and_click_by_xpath(element_path):
    find_by_xpath(element_path).click()


# Hover cursor to the element by XPATH
def hover_by_xpath(element_path):
    elem = actions.move_to_element(find_by_xpath(element_path))
    elem.perform()


# Wait for an element to be clickable
def wait_until_clickable_xpath(element_path):
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable(
        (By.XPATH, element_path))).click()


# Wait for the element presence
def wait_for_presence_xpath(element_path):
    return WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.XPATH, element_path)))

def is_element_xpath_exist(xpath):
    try:
        WebDriverWait(driver, 5).until(ec.presence_of_element_located(
            (By.XPATH, xpath)))
        return True
    except Exception:
        return False
        pass

# Return price_text as an integer
def sanitize_price(element_xpath_or_price_text):
    price_text = element_xpath_or_price_text
    # If input is element_xpath, convert to price_text
    if not element_xpath_or_price_text[0].isdigit():
        price_text = find_by_xpath(element_xpath_or_price_text).text
    # Remove 'đ' and '.' in price_text (ex: 67.500đ)
    cleaned_text = price_text.replace('đ', '').replace('.', '')
    return int(cleaned_text)


# Add n items to cart (Set n to blank or 0 to add a random number of items)
def add_items_to_cart(n):
    total_price_expected = 0
    # Sách Văn Học Category
    find_and_click_by_xpath("//a[@id='menu-item-95']")


    # Add a random number of items
    if n==0 or n=='':
        number_of_items_to_add = random.randint(1, 10)
    else:
        if n > 0:
            number_of_items_to_add = n
            print("Đang thêm %d sản phẩm (có thể trùng) vào giỏ hàng!" % number_of_items_to_add)
        else:
            print("Invalid number of items value!")
            exit()
    # Add n item(s) to the cart
    for i in range(1,number_of_items_to_add+1):
        # 1.1 Randomly add an item with position X from 1 to 24
        # counting from left to right, up to down
        # Maximum items displayed per category page: 24
        position = random.randint(1, 24)

        # 1.2 Add item to cart, Add price to total_price_expected
        item_xpath = f"(//span[@class='button-buy-now '])[{position}]"
        item_sale_price = f"(//div[@class='price-group']//span[@class='price sale-price'])[{position}]"

        hover_by_xpath(item_xpath)
        total_price_expected += sanitize_price(item_sale_price)
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
    cart_total_price = driver.find_element(By.CLASS_NAME, "cart-total").text
    print("Tạm tính:", cart_total_price)
    # print('total_price_expected:',total_price_expected)
    # print('cart_total_price: ',sanitize_price(cart_total_price))
    return total_price_expected == sanitize_price(cart_total_price)


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


def is_login_successful():
    try:
        # wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Đăng xuất")))
        driver.find_element(By.PARTIAL_LINK_TEXT, "Đăng xuất")
        return True
    except NoSuchElementException:
        return False


# Log out
def logout():
    if is_login_successful():
        driver.find_element(By.LINK_TEXT, "Đăng xuất").click()
    print("Đăng Xuất thành công!")




def is_checkout_login_successful():
    try:
        find_by_xpath("//div[contains(text(),'* Đăng nhập để thanh toán tiện lợi hơn')]")
        return True
    except NoSuchElementException:
        return False


def checkout(name,email,p1,p2,a1,a2,a3,a):
    get_homepage()
    cart_button_xpath = "//a[contains(@class,'get-cart-box')]"
    wait_until_clickable_xpath(cart_button_xpath)
    wait_until_clickable_xpath("//span[contains(text(),'Tiến hành thanh toán')]")

    # 99 sản phẩm
    items_quantity = find_by_xpath("//div[@class='el-input el-input--small']//input")
    items_quantity.clear()
    items_quantity.send_keys('99')
    # Email hoặc Số điện thoại
    find_by_xpath("//input[@placeholder='Email hoặc Số điện thoại']").send_keys('0123456789')
    # Tiếp tục
    find_and_click_by_xpath("//button[contains(text(), 'Tiếp tục')]")
    time.sleep(2)
    # 1. Họ và Tên
    find_by_xpath("//input[@placeholder='Họ và Tên']").send_keys(name)
    # 2. Email
    find_by_xpath("//input[@placeholder='Email']").send_keys(email)
    # 3. Số điện thoại
    phone_field = find_by_xpath("//input[@placeholder='Số điện thoại']")
        # phone_field.clear() error not working
    driver.execute_script("arguments[0].value = '';", phone_field)
    phone_field.send_keys(p1)
    # 4. Nhập lại điện thoại
    phone2_field = find_by_xpath("//input[@placeholder='Nhập lại số điện thoại']")
    phone2_field.clear()
    phone2_field.send_keys(p2)
    # 5. Tỉnh/Thành phố
    find_and_click_by_xpath("//input[@placeholder='Chọn Tỉnh / Thành phố']")
    wait_until_clickable_xpath(f"//span[text()='{a1}']")
    # 6. Quận / Huyện
    wait_for_presence_xpath("//label[contains(text(),'Quận/Huyện')]")
    wait_until_clickable_xpath("//input[@placeholder='Chọn Quận / Huyện']")
    wait_until_clickable_xpath(f"//span[text()='{a2}']")
    # 7. Xã/Phường
    wait_for_presence_xpath("//label[contains(text(),'Xã/Phường')]")
    wait_until_clickable_xpath("//input[@placeholder='Chọn Xã / Phường']")
    wait_until_clickable_xpath(f"//span[text()='{a3}']")
    # 8. Địa chỉ
    find_by_xpath("//input[@placeholder='Nhập số nhà, tên đường']").send_keys(a)
    find_and_click_by_xpath("//button//strong[contains(text(),'Tiếp tục')]")
    return is_element_xpath_exist("//div[contains(text(),'Phương thức thanh toán')]")

def invalid_checkout(name,email,p1,p2,a):
    get_homepage()
    cart_button_xpath = "//a[contains(@class,'get-cart-box')]"
    wait_until_clickable_xpath(cart_button_xpath)
    wait_until_clickable_xpath("//span[contains(text(),'Tiến hành thanh toán')]")

    # 99 sản phẩm
    items_quantity = find_by_xpath("//div[@class='el-input el-input--small']//input")
    items_quantity.clear()
    items_quantity.send_keys('99')
    # Email hoặc Số điện thoại
    first_mail_field =  find_by_xpath("//input[@placeholder='Email hoặc Số điện thoại']")
    if first_mail_field.get_attribute('value') == '':
        find_by_xpath("//input[@placeholder='Email hoặc Số điện thoại']").send_keys('0123456789')
    # Tiếp tục
    find_and_click_by_xpath("//button[contains(text(), 'Tiếp tục')]")
    time.sleep(2)
    # 1. Họ và Tên
    find_by_xpath("//input[@placeholder='Họ và Tên']").send_keys(name)
    # 2. Email
    find_by_xpath("//input[@placeholder='Email']").send_keys(email)
    # 3. Số điện thoại
    phone_field = find_by_xpath("//input[@placeholder='Số điện thoại']")
        # phone_field.clear() error not working
    driver.execute_script("arguments[0].value = '';", phone_field)
    phone_field.send_keys(p1)
    # 4. Nhập lại điện thoại
    phone2_field = find_by_xpath("//input[@placeholder='Nhập lại số điện thoại']")
    phone2_field.clear()
    phone2_field.send_keys(p2)
    # 8. Địa chỉ
    find_by_xpath("//input[@placeholder='Nhập số nhà, tên đường']").send_keys(a)
    find_and_click_by_xpath("//button//strong[contains(text(),'Tiếp tục')]")
    return is_element_xpath_exist("//div[contains(text(),'Phương thức thanh toán')]")

def main():
    # Open Newshop homepage
    get_homepage()
    add_items_to_cart(2)
    quit_driver()


if __name__ == "__main__":
    main()
