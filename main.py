import os
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv

load_dotenv()

EMAIL=os.getenv("EMAIL")
PASSWORD=os.getenv("PASSWORD")
GYM_URL = "https://appbrewery.github.io/gym/"
#just bunch of stuff I gotta call before opening the program
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
#Keep my loging even if I close the tab
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

#open the tab
driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)
wait = WebDriverWait(driver, 5)
log_dir = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "Home_heroButton__3eeI3"))
)

#internet resilience:
def retry(func, retries = 7, description = None):
    for i in range(retries):
        print(f"Trying {description}, Attempt: {i + 1}")
        try:
            return func()
        except TimeoutException:
            if i == retries - 1:
                raise
            time.sleep(1)
            driver.refresh()

# Function to book a class process that checks if the button text changed with retry
def attempt_booking(button):
    button.click()
    # Wait for button state to change - will time out if booking failed
    wait.until(lambda d: button.text in ["Booked", "Waitlisted"])

#automatically log in to the page
def login():
    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "login-button"))
                              )
    login_button.click()
    email_login = wait.until(
        EC.visibility_of_element_located((By.ID, "email-input"))
    )
    email_login.send_keys(EMAIL)
    password_login = driver.find_element(By.ID, "password-input")
    password_login.send_keys(PASSWORD)
    submit_pass_and_email_but = driver.find_element(By.ID, "submit-button")
    submit_pass_and_email_but.click()

    wait.until(
        EC.presence_of_element_located((By.ID, "schedule-page"))
    )

def get_my_bookings():

    my_booking_link = driver.find_element(By.ID, "my-bookings-link")
    my_booking_link.click()
    wait.until(EC.presence_of_element_located((By.ID, "my-bookings-page")))
    #find all card confirmed and on waiting list
    cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='-card-']")
    if not cards:
        raise TimeoutException("No cards found")
    return cards

def main():
    retry(login, description="login")
    #book next Tuesday class
    booking_classes = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[id^="class-card"]'))
    )

    #print output:
    new_classes_booked = 0
    new_waitlisted_joined = 0
    already_booked_waitlisted = 0

    for classes in booking_classes:
        day_classes = classes.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
        day_title = day_classes.find_element(By.TAG_NAME, "h2").text.lower()
        #check if it's a Tuesday
        if "tue" in day_title.lower() or "thu" in day_title.lower():
            #check if it's 6pm
            time_text = classes.find_element(By.CSS_SELECTOR, 'p[id^="class-time"]').text
            if "6:00 pm" in time_text.lower():
                #get the class name
                class_name = classes.find_element(By.CSS_SELECTOR, 'h3[id^="class-name"]').text
                #book class
                book_class = classes.find_element(By.CSS_SELECTOR, 'button[id^="book-button-"]')

                button = classes.find_element(By.CSS_SELECTOR, 'button[id^="book-button-"]')
                if book_class.text == "Booked":
                    book_class.click()
                    new_classes_booked += 1
                    print(f"Your {class_name} was successfully booked! for {day_title} at {time_text}")

                elif book_class.text == "Waitlisted":
                    book_class.click()
                    new_waitlisted_joined += 1
                    print(f"You successfully joined the waitlist for "
                          f"the class {class_name}, at {day_title} at {time_text}, we look forward to having you!")

                elif book_class.text == "Book Class":
                    retry(lambda: attempt_booking(button), description="book class")
                    new_classes_booked += 1

                elif book_class.text == "Join Waitlist":
                    retry(lambda: attempt_booking(button), description="join waitlist")
                    new_waitlisted_joined += 1


    # print(f"--- BOOKING SUMMARY ---"
    #       f"\nClasses booked:{new_classes_booked} "
    #       f"\nWaitlists joined: {new_waitlisted_joined} "
    #       f"\nAlready booked/waitlisted: {already_booked_waitlisted}"
    #       f"\nTotal {day_title}at {time_text} "
    #       f"classes processed: "
    #       f"{new_classes_booked + new_waitlisted_joined + already_booked_waitlisted}")
    print("\n")
    print(f"--- Total Tuesday/Thursday 6pm classes:"
              f" {new_classes_booked+new_waitlisted_joined+already_booked_waitlisted} ---")
    print("---- VERIFYING ON MY BOOKING PAGE ----")
    all_booked_classes = new_classes_booked+new_waitlisted_joined+already_booked_waitlisted


    all_cards = retry(get_my_bookings, description="get booking")
    verified_count = 0
    for card in all_cards:
        status = card.get_attribute("data-booking-status")
        day_text = card.find_element(By.CSS_SELECTOR, "div p").text.lower()
        booked_class = card.find_element(By.TAG_NAME, "h3").text.lower()

        if status == "confirmed" or status == "waitlisted":
            if ("thu" in day_text or "tue" in day_text) and "6:00 pm" in day_text:
                verified_count += 1
                print(f"Your {booked_class} is scheduled for {day_text}")

    if verified_count == all_booked_classes:
        print("✅ SUCCESS: All bookings verified!")
    else:
        print(f"MISMATCH: It's missing {all_booked_classes - verified_count} bookings.")


if __name__ == "__main__":
    main()