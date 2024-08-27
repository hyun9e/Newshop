import pytest
from package import order as od

@pytest.fixture
def setup_and_teardown():
    # Setup code
    od.get_homepage()
    yield
    # Teardown code
    od.quit_driver()

def test_fully_order_info(setup_and_teardown):
    a = ["Fake Order","fakemail@gmail.com", "0123456789", "0123456789",
         "An Giang", "Huyện An Phú", "Thị Trấn An Phú", "Fake Adress" ]
    # Name - Email - Phone number - Confirm phone number - Adress: 1, 2, 3, details
    od.add_items_to_cart(1)
    if od.checkout(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]):
        print("Đặt hàng thành công")
    else:
        print("Đặt hàng thất bại, thông tin địa chỉ không hợp lệ")


def test_empty_order_info(setup_and_teardown):
    # Name - Email - Phone number - Confirm phone number - Adress: 1, 2, 3, details
    od.add_items_to_cart(1)
    if od.invalid_checkout("","","0","",""):
        print("Đặt hàng thành công")
    else:
        print("Đặt hàng thất bại, thông tin địa chỉ không hợp lệ")

def test_false_order_info(setup_and_teardown):
    od.add_items_to_cart(1)
    if od.invalid_checkout("1", "1", "0", "123", "2"):
        print("Đặt hàng thành công")
    else:
        print("Đặt hàng thất bại, thông tin địa chỉ không hợp lệ")

