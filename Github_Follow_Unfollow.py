import customtkinter as ctk
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Global variables
driver = None
lock = threading.Lock()  # Thread lock to manage access to shared resources

# Function to initialize the WebDriver (Chrome)
def initialize_webdriver():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Open in maximized mode
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (often required for headless mode)
    chrome_options.add_argument("--window-size=1920x1080")  # Set window size to ensure elements are visible
    chrome_options.add_argument("--no-sandbox")  # Add sandboxing
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    service = Service(executable_path="C:/Drivers/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to handle the GitHub login
def github_login(username, password):
    with lock:
        driver.get("https://github.com/login")
        
        wait = WebDriverWait(driver, 20)
        username_field = wait.until(EC.presence_of_element_located((By.ID, "login_field")))
        username_field.send_keys(username)
        
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)
        
        sign_in_button = wait.until(EC.element_to_be_clickable((By.NAME, "commit")))
        sign_in_button.click()
        
        time.sleep(5)
        
        try:
            wait.until(EC.url_contains("github.com/"))
            log_widget.insert(ctk.END, "Login successful.\n")
        except:
            log_widget.insert(ctk.END, "Login might not be successful. Check credentials.\n")
            raise

# Generic function to handle following/unfollowing users across multiple pages
def handle_buttons(page_url, action):
    with lock:
        try:
            page_number = int(page_number_entry.get().strip())  # Get starting page number from user input
        except ValueError:
            log_widget.insert(ctk.END, "Invalid page number. Please enter a valid number.\n")
            return
        
        while True:
            current_page_url = f"{page_url}&page={page_number}"
            driver.get(current_page_url)
            
            wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
            try:
                try:
                    popup = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='flash flash-full flash-error ']//div[contains(text(), \"You can't perform that action at this time.\")]")
                    ))
                    if popup:
                        log_widget.insert(ctk.END, "Action limit reached. Closing WebDriver.\n")
                        driver.quit()
                        return False
                except:
                    pass

                if action == "follow":
                    buttons = wait.until(EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "input.btn.btn-sm[aria-label^='Follow']")
                    ))
                else:
                    buttons = wait.until(EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "input.btn.btn-sm[aria-label^='Unfollow']")
                    ))

                if not buttons:
                    log_widget.insert(ctk.END, f"No more {action} buttons found on page {page_number}. Stopping.\n")
                    break

                for i, button in enumerate(buttons):
                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        wait.until(EC.element_to_be_clickable(button))
                        button.click()
                        log_widget.insert(ctk.END, f"Clicked button {i + 1} on page {page_number}: {button.get_attribute('aria-label')}\n")
                        time.sleep(1)
                    except Exception as e:
                        log_widget.insert(ctk.END, f"Failed to click button {i + 1} on page {page_number}: {e}\n")
                        break
                
                log_widget.insert(ctk.END, f"Completed {action} actions on page {page_number}.\n")
                page_number += 1

            except Exception as e:
                log_widget.insert(ctk.END, f"Error occurred: {e}\n")
                break

        return True

# Function to start the follow/unfollow process based on user input
def start_process(action):
    threading.Thread(target=run_process, args=(action,)).start()

def run_process(action):
    with lock:
        initialize_webdriver()
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        page_url = url_entry.get().strip()
        
        if not username or not password or not page_url:
            log_widget.insert(ctk.END, "Please enter all required fields: Username, Password, and URL.\n")
            return
        
        try:
            github_login(username, password)
            handle_buttons(page_url, action)
        finally:
            driver.quit()
            log_widget.insert(ctk.END, "Process completed. WebDriver closed.\n")

# GUI setup and button bindings using customtkinter
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("GitHub Follow/Unfollow Automation")
root.geometry("635x600")

# Frame for content
frame = ctk.CTkFrame(root)
frame.pack(expand=True, fill=ctk.BOTH, padx=20, pady=20)

# Title Label
title_label = ctk.CTkLabel(frame, text="GitHub Follow/Unfollow Automation", font=ctk.CTkFont(size=20, weight="bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

# Username Entry
username_label = ctk.CTkLabel(frame, text="Username/Email:", font=ctk.CTkFont(size=14))
username_label.grid(row=1, column=0, pady=5, padx=10, sticky="e")

username_entry = ctk.CTkEntry(frame, width=400)
username_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

# Password Entry
password_label = ctk.CTkLabel(frame, text="Password:", font=ctk.CTkFont(size=14))
password_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")

password_entry = ctk.CTkEntry(frame, show="*", width=400)
password_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

# URL Entry
url_label = ctk.CTkLabel(frame, text="Page URL:", font=ctk.CTkFont(size=14))
url_label.grid(row=3, column=0, pady=5, padx=10, sticky="e")

url_entry = ctk.CTkEntry(frame, width=400)
url_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

# Page Number Entry
page_number_label = ctk.CTkLabel(frame, text="Starting Page Number:", font=ctk.CTkFont(size=14))
page_number_label.grid(row=4, column=0, pady=5, padx=10, sticky="e")

page_number_entry = ctk.CTkEntry(frame, width=400)
page_number_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")

# Follow and Unfollow buttons with custom colors
btn_follow = ctk.CTkButton(frame, text="Follow Users", command=lambda: start_process("follow"), fg_color="#997cc4", hover_color="#6e4ca1")
btn_follow.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

btn_unfollow = ctk.CTkButton(frame, text="Unfollow Users", command=lambda: start_process("unfollow"), fg_color="#997cc4", hover_color="#6e4ca1")
btn_unfollow.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Log area
log_widget = ctk.CTkTextbox(frame, wrap="word", height=10)
log_widget.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

# Adjust the grid configuration
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(7, weight=1)

# Start the GUI event loop
root.mainloop()
