import os
import sys
import datetime
from login import *
from keepstreak import *
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def main():
    # Configure Firefox options for headless operation in GitHub Actions
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    firefox_options.set_preference("media.volume_scale", "0.0")
    firefox_options.set_preference("dom.push.enabled", False)
    
    # Set MOZ_HEADLESS environment variable
    os.environ['MOZ_HEADLESS'] = '1'
    
    # Configure and initialize the WebDriver with appropriate logging
    driver = webdriver.Firefox(
        service=Service(
            GeckoDriverManager(path=os.getcwd()).install(), 
            log_path=os.path.join(os.getcwd(), 'geckodriver.log')
        ), 
        options=firefox_options
    )
    
    # Set implicit wait time
    driver.implicitly_wait(10)
    
    # Clear terminal output
    os.system("clear")

    # Initialize log file
    with open("tryhackmebot.log", 'a') as f:
        print("[+] Starting...")
        date = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        f.write(f"{date}\n")
        f.write("[+] Starting...\n")

    # Log in to TryHackMe
    login_form(driver)
    
    # Maintain the streak
    keep_streak(driver)

    # Close the log file and quit the WebDriver
    with open("tryhackmebot.log", 'a') as f:
        print("[+] Closing...")
        f.write("[+] Closing...\n\n")

    driver.quit()


if __name__ == "__main__":
    main()
