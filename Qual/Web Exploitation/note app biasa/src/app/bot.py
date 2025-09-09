from flask import Blueprint, request, jsonify
from .auth import login_required
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from time import sleep


bot_bp = Blueprint('bot', __name__)

def read_note(note_id):
    driver = None
    try:
        service = FirefoxService(executable_path="/usr/local/bin/geckodriver")

        profile = FirefoxProfile()
        profile.set_preference("dom.disable_open_during_load", False)
        
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.profile = profile

        driver = webdriver.Firefox(service=service, options=options)

        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        # login as admin
        driver.get("http://localhost:5001/auth/login")
        sleep(2)
        username = driver.find_element("name", "username")
        password = driver.find_element("name", "password")
        username.send_keys("admin")
        password.send_keys("SecUr3ADM00NP4$$")
        driver.find_element("xpath", "//button[@type='submit']").click()
        
        driver.get("http://localhost:5001/notes/view/" + note_id)
        sleep(5)
        
    except Exception as e:
        print(f"Error during Selenium operation with Firefox: {e}")
        if driver:
            try:
                driver.quit()
            except Exception as qe:
                print(f"Error quitting driver during exception: {qe}")
        return False
    finally:
        if driver:
            try:
                driver.quit()
                print("Firefox driver quit successfully in finally block.")
            except Exception as e_finally:
                print(f"Error quitting Firefox driver in finally block: {e_finally}")
    return True

@bot_bp.route('/report', methods=['POST'])
@login_required
def report():
    data = request.get_json()
    if not data or 'note_id' not in data:
        return jsonify({"error": "Invalid request"}), 400
    note_id = data.get('note_id')
    
    if not note_id:
        return jsonify({"error": "Note ID is required"}), 400
    
    if read_note(note_id):
        return jsonify({"message": "Bot operation completed successfully"}), 200
    else:
        return jsonify({"error": "Bot operation failed"}), 500


