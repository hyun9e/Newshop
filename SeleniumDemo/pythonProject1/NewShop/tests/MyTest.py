import time
# import pytest
from package import cart_mangement as cm

class Test_CartManagement:
    def test_add_items_to_cart(self):
        cm.get_homepage()
        cm.add_items_to_cart()
        time.sleep(2)
        cm.driver.quit()

    # def test_order(self):
    #     time.sleep(2)
    #     cm.driver.quit()



