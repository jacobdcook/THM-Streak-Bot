import os
import time
import random
import configparser
from urllib import request
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pydub
import speech_recognition


def change_type():
    """Convert audio from mp3 to wav format for speech recognition"""
    try:
        sound = pydub.AudioSegment.from_mp3(f"{os.getcwd()}/recapchasound/sample.wav")
        sound.export(f"{os.getcwd()}/recapchasound/sample.wav", format="wav")
    except Exception as e:
        with open("tryhackmebot.log", 'a') as f:
            print(f"[!] Error converting audio: {e}")
            f.write(f"[!] Error converting audio: {e}\n")


def recapcha(driver):
    """Solve reCAPTCHA challenge using audio recognition"""
    time.sleep(random.uniform(1,3))
    with open("tryhackmebot.log", 'a') as f:
        print("[+] Attempting to Solve Recaptcha")
        f.write("[+] Attempting to Solve Recaptcha\n")

    try:
        # Find and switch to the reCAPTCHA iframe
        frames = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(frames)
        
        time.sleep(random.uniform(1,3))
        driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()
        
        time.sleep(random.uniform(1,3))
        driver.switch_to.default_content()
        
        # Switch to the audio challenge
        try:
            frames = driver.find_element(By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']")
            driver.switch_to.frame(frames)
            
            # Click the audio button
            audio_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))
            )
            audio_button.click()

            time.sleep(random.uniform(1,3))
            
            # Click the play button
            play_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[starts-with(@class, 'rc-button')]"))
            )
            play_button.click()

            time.sleep(random.uniform(1,3))
            
            # Get the audio source
            src = driver.find_element(By.XPATH, "//a[contains(text(), 'Download')]").get_attribute("href")
            os.makedirs("recapchasound", exist_ok=True)
            request.urlretrieve(src, f"{os.getcwd()}/recapchasound/sample.wav")
            change_type()

            # Use speech recognition to solve the CAPTCHA
            sample_audio = speech_recognition.AudioFile(f"{os.getcwd()}/recapchasound/sample.wav")
            recognize = speech_recognition.Recognizer()
            with sample_audio as source:
                audio = recognize.record(source)
            
            key = recognize.recognize_google(audio)
            with open("tryhackmebot.log", 'a') as f:
                print(f"[+] Recaptcha Passcode: {key}")
                f.write(f"[+] Recaptcha Passcode: {key}\n")

            # Input the recognized text
            driver.find_element(By.ID, "audio-response").send_keys(key.lower())
            time.sleep(random.uniform(1,3))
            driver.find_element(By.ID, "recaptcha-verify-button").click()
            
        except (ElementNotInteractableException, NoSuchElementException, TimeoutException) as e:
            with open("tryhackmebot.log", 'a') as f:
                print(f"[!] Error with reCAPTCHA challenge: {e}")
                f.write(f"[!] Error with reCAPTCHA challenge: {e}\n")
            pass
        
    except Exception as e:
        with open("tryhackmebot.log", 'a') as f:
            print(f"[!] Error solving reCAPTCHA: {e}")
            f.write(f"[!] Error solving reCAPTCHA: {e}\n")
    
    # Return to main content
    driver.switch_to.default_content()


def login_form(driver):
    """Handle the login form for TryHackMe"""
    config = configparser.ConfigParser()
    config.read("account.conf")
    try:
        driver.get("https://tryhackme.com/login")
        time.sleep(random.uniform(3,6))
        
        # Enhanced error handling for finding elements
        try:
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "form-control"))
            )
            email_field.send_keys(config["account"]["mail"])
            
            time.sleep(random.uniform(1,3))
            
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.send_keys(config["account"]["pass"])
            
            # Handle reCAPTCHA
            recapcha(driver)
            
            time.sleep(random.uniform(1,3))
            
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
            )
            login_button.click()
            
        except (NoSuchElementException, TimeoutException) as e:
            with open("tryhackmebot.log", 'a') as f:
                print(f"[!] Error finding login elements: {e}")
                f.write(f"[!] Error finding login elements: {e}\n")
            raise Exception("Login form elements not found")

        # Verify successful login
        time.sleep(5)  # Wait for login to complete
        if "dashboard" in driver.current_url:
            with open("tryhackmebot.log", 'a') as f:
                print("[+] You Are Logged In!")
                f.write("[+] You Are Logged In!\n")
        else:
            with open("tryhackmebot.log", 'a') as f:
                print("[!] Login failed, retrying...")
                f.write("[!] Login failed, retrying...\n")
            login_form(driver)
            
    except KeyboardInterrupt:
        with open("tryhackmebot.log", 'a') as f:
            print("[!] Process interrupted by user")
            f.write("[!] Process interrupted by user\n")
        pass
        
    except Exception as e:
        with open("tryhackmebot.log", 'a') as f:
            print(f"[!] Something Went Wrong: {e}")
            f.write(f"[!] Something Went Wrong: {e}\n")
            print("[+] Trying Again...")
            f.write("[+] Trying Again...\n")
        login_form(driver)
