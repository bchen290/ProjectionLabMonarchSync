import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ProjectionLab():
    API = "projectionlabPluginAPI"

    def __init__(self, url="https://app.projectionlab.com", timeout=30) -> None:
        self._email = os.getenv("PROJECTIONLAB_EMAIL")
        self._password = os.getenv("PROJECTIONLAB_PASSWORD")
        self._plugin_key = os.getenv("PROJECTIONLAB_PLUGIN_API_KEY")

        options = Options()
        options.add_argument("--headless=new")
        options.add_experimental_option("detach", True)
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get(url)

        # Email login. Google login potentially possible if you export your user data dir
        WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "firebaseui-idp-password"))).click()
        WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "firebaseui-id-email"))).send_keys(os.getenv("PROJECTIONLAB_EMAIL"))
        WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "firebaseui-id-submit"))).click()
        WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "firebaseui-id-password"))).send_keys(os.getenv("PROJECTIONLAB_PASSWORD"))
        WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "firebaseui-id-submit"))).click()

        WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.ID, "current-finances-section")))
    
    def preprocess_options(self, options):
        options = {} if options is None else options
        options["key"] = self._plugin_key
        return options
    

    def updateAccount(self, accountId: str, data: dict, options: dict = None):
        options = self.preprocess_options(options)
        return self.driver.execute_script(f"return window.{self.API}.updateAccount({accountId}, {json.dumps(data)}, {json.dumps(options)})")


    def exportData(self, options: dict = None):
        options = self.preprocess_options(options)
        return self.driver.execute_script(f"return window.{self.API}.exportData({json.dumps(options)})")
    