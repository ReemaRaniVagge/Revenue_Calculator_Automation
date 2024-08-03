from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def main():
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.fitpeo.com")
        
        driver.maximize_window()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Revenue Calculator"))
        ).click()

        # Scroll Down
        slider_section = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".slider"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", slider_section)
        
        # Adjusting the Slider
        slider = driver.find_element(By.CSS_SELECTOR, ".slider input[type='range']")
        move_slider(driver, slider, 820)

        # Verify slider value
        slider_value = driver.find_element(By.CSS_SELECTOR, ".slider-value")
        assert slider_value.get_attribute("value") == "820", "Slider value is not set to 820"

        # Update the Text Field
        text_field = driver.find_element(By.CSS_SELECTOR, ".slider-text")
        text_field.clear()
        text_field.send_keys("560")
        text_field.send_keys(Keys.RETURN)

        # Validate Slider Value updates
        time.sleep(2)  # wait for slider to update
        assert slider_value.get_attribute("value") == "560", "Slider value did not update to 560"

        # Select CPT Codes
        cpt_codes = ["99091", "99453", "99454", "99474"]
        for code in cpt_codes:
            checkbox = driver.find_element(By.CSS_SELECTOR, f"input[value='CPT-{code}']")
            if not checkbox.is_selected():
                checkbox.click()

        # Validate Total Recurring Reimbursement
        reimbursement_text = driver.find_element(By.CSS_SELECTOR, ".total-reimbursement")
        assert reimbursement_text.text == "$110700", "Total Recurring Reimbursement is incorrect"

        print("All test cases passed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def move_slider(driver, slider, value):
    action = ActionChains(driver)
    action.click_and_hold(slider).move_by_offset(value, 0).release().perform()

if __name__ == "__main__":
    main()
