from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Initialize WebDriver (Chrome in this example)
driver = webdriver.Chrome()
driver.get("https://www.cheapoair.com/")

def set_city(city_name,key_):
    try:
        # Wait for input to be present (up to 10 seconds)
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, key_))
        )
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", input_field)
        
        # Clear existing value
        input_field.clear()
        time.sleep(0.5)  # Brief pause
        
        for char in city_name:
            print(char)
            input_field.send_keys(char)
        # Method 1: Simulate typing (works for most sites)
        # input_field.send_keys(Keys.CONTROL + "a")
        time.sleep(2)  # Allow time for dropdown to appear
        
        # Trigger Enter key to select first dropdown option
        input_field.send_keys(Keys.ARROW_DOWN, Keys.ENTER)
        
        # Method 2: JavaScript alternative (use if Method 1 doesn't work)
        # driver.execute_script(f"""
        #     const input = document.getElementById('fs_originCity_0');
        #     input.value = "{city_name}";
        #     input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        #     input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        # """)
        
        print(f"Successfully set origin city to: {city_name}")
        
    except Exception as e:
        print(f"Error setting city: {str(e)}")
        # Consider adding screenshot for debugging:
        # driver.save_screenshot("error_screenshot.png")
def select_and_verify_date_return(driver, input_id, date_label):
    """
    Selects a return date from the calendar and verifies it's selected.
    
    Args:
        driver: Selenium WebDriver instance.
        input_id: ID of the input field that triggers the calendar (e.g., "fs_returnDate_0").
        date_label: The aria-label of the date to select (e.g., "29 July 2025").
    """
    wait = WebDriverWait(driver, 10)
    
    # Open the calendar
    date_input = wait.until(EC.presence_of_element_located((By.ID, input_id)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", date_input)
    date_input.click()
    
    # Wait for calendar to fully load
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "calendar")))
    
    # Select the date
    date_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//span[@aria-label='{date_label}']"))
    )
    date_element.click()
    
    # More flexible verification - check if date is selected (might have different classes for return)
    # selected_date = wait.until(EC.presence_of_element_located(
    #     (By.XPATH, f"//span[@aria-label='{date_label}' and contains(@class, 'bg-blue') and contains(@class, 'is--return')]"))
    # )
    print(f"✅ Successfully selected and verified return date: {date_label}")
    return date_element
def set_travelers(driver, adults=1, seniors=0, children=0):
    """
    Sets the number of travelers in the CheapOair traveler selection dialog
    
    Args:
        driver: Selenium WebDriver instance
        adults: Number of adults (16-64)
        seniors: Number of seniors (65+)
        children: Number of children (2-15)
    """
    wait = WebDriverWait(driver, 15)
    
    try:
        print("👥 Opening traveler selection dialog...")
        # Open traveler dialog
        traveler_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "travellerButtonFlights"))
        )
        ActionChains(driver).move_to_element(traveler_btn).pause(0.5).click().perform()
        
        # Wait for dialog to fully load
        wait.until(EC.visibility_of_element_located(
            (By.ID, "travellerDialogBox"))
        )
        time.sleep(0.5)
        
        # Set number of adults
        print(f"👨‍👩‍👧 Setting adults to {adults}...")
        current_adults = int(driver.find_element(By.ID, "lbladults").text)
        for _ in range(adults - current_adults):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addADULTS")))
            btn.click()
            time.sleep(random.uniform(0.2, 0.4))
        
        # Set number of seniors
        print(f"👵 Setting seniors to {seniors}...")
        current_seniors = int(driver.find_element(By.ID, "lblseniors").text)
        for _ in range(seniors - current_seniors):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addSENIORS")))
            btn.click()
            time.sleep(random.uniform(0.2, 0.4))
        
        # Set number of children
        print(f"🧒 Setting children to {children}...")
        current_children = int(driver.find_element(By.ID, "lblchild").text)
        for _ in range(children - current_children):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addCHILD")))
            btn.click()
            time.sleep(random.uniform(0.2, 0.4))
        
        # Close the dialog
        print("✅ Applying traveler selections...")
        done_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "closeFlightDialog"))
        )
        done_btn.click()
        
        # Verify selection in the main button
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#travellerButtonFlights .travelers-count__number"), 
            str(adults + seniors + children))
        )
        print(f"✅ Successfully set travelers: {adults} adults, {seniors} seniors, {children} children")
        return True
        
    except Exception as e:
        print(f"❌ Failed to set travelers: {str(e)}")
        return False
def click_search_flights(driver):
    """
    Clicks the 'Search Flights' button
    
    Args:
        driver: Selenium WebDriver instance
    """
    wait = WebDriverWait(driver, 15)
    
    try:
        print("🛫 Clicking 'Search Flights' button...")
        # Locate the button by its ID
        search_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "searchNow"))
        )
        
        # Scroll into view (if needed)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search_btn)
        
        # Click using JavaScript for reliability
        driver.execute_script("arguments[0].click();", search_btn)
        print("✅ Successfully clicked 'Search Flights' button")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to click search button: {str(e)}")
        return False
def reak_time_flight(driver):
        wait = WebDriverWait(driver, 15)
        stpos = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".stop__number.pt-1.stop__number-0"))
        )
        duration=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "stop__trip-duration"))
        )



        airline=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "trip__airline--name"))
        )
# Example usage:
# set_city_field("fs_originCity_0","tunis")
set_city("tunis","fs_originCity_0")
set_city("france","fs_destCity_0")
select_and_verify_date_return(driver,"fs_departDate_0","25 July 2025")
select_and_verify_date_return(driver,"fs_returnDate_0","29 July 2025")
# set_date_field("fs_departDate_0", "28-06-2025")
# select_date_from_calendar(driver, "2025-07-15")  # Selects July 15, 2025
# Keep browser open for 10 seconds to see result
set_travelers(driver, adults=2, seniors=1, children=1)
click_search_flights(driver)

time.sleep(60)
driver.quit()