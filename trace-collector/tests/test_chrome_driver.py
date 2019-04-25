import unittest
from selenium import webdriver


class ChromeDriverTestCase(unittest.TestCase):
    def setUp(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def test_load_google(self):
        self.driver.get("https://www.google.com")
        self.assertEqual(self.driver.title, "Google")


if __name__ == "__main__":
    unittest.main()
