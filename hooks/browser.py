import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def open_chrome(context, url, **kwargs):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

    driver.get(url)
    # Load cookies from the file
    try:
        with open("cookies.json", "r") as file:
            all_cookies = json.load(file)
        # Add each cookie to the browser
        for cookie in all_cookies:
            driver.add_cookie(cookie)
        
        # Load Local Storage and Session Storage from files
        with open("local_storage.json", "r") as file:
            local_storage = json.load(file)

        # Set Local Storage and Session Storage data
        for key, value in local_storage.items():
            driver.execute_script(f"window.localStorage['{key}'] = '{value}';")

        with open("session_storage.json", "r") as file:
            session_storage = json.load(file)

        for key, value in session_storage.items():
            driver.execute_script(f"window.sessionStorage['{key}'] = '{value}';")
    except Exception as e:
        print(e)
        pass

    driver.get(url)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


    context['driver'] = driver

def close_chrome(context, **kwargs):
    driver = context.get('driver', None)

    # Get all cookies
    all_cookies = driver.get_cookies()

    # Save cookies to a file
    with open("cookies.json", "w") as file:
        json.dump(all_cookies, file)
    
    # Get Local Storage
    local_storage = driver.execute_script("return window.localStorage;")
    with open("local_storage.json", "w") as file:
        json.dump(local_storage, file)

    # Session Storage
    session_storage = driver.execute_script("return window.sessionStorage;")
    with open("session_storage.json", "w") as file:
        json.dump(session_storage, file)

    
    if driver is not None:
        driver.quit()