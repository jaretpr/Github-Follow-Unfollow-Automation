import tkinter as tk
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Global variable for WebDriver (initialized only when needed)
driver = None

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
    driver.get("https://github.com/login")
    
    # Wait for the login page to load and locate the username and password fields
    wait = WebDriverWait(driver, 20)
    
    # Enter username
    username_field = wait.until(EC.presence_of_element_located((By.ID, "login_field")))
    username_field.send_keys(username)
    
    # Enter password
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(password)
    
    # Click the "Sign in" button
    sign_in_button = wait.until(EC.element_to_be_clickable((By.NAME, "commit")))
    sign_in_button.click()
    
    # Debugging: Print current URL to verify successful login
    time.sleep(5)  # Allow time for redirection
    print("Current URL after login:", driver.current_url)
    
    # Alternative wait: Check if URL contains the dashboard page path
    try:
        wait.until(EC.url_contains("github.com/"))
        print("Login successful, now on the GitHub home/dashboard page.")
        log_widget.insert(tk.END, "Login successful.\n")
    except:
        print("Login might not be successful. Current URL:", driver.current_url)
        log_widget.insert(tk.END, "Login might not be successful. Check credentials.\n")
        raise

# Generic function to handle following/unfollowing users across multiple pages
def handle_buttons(page_url, action):
    page_number = 1
    while True:
        current_page_url = f"{page_url}&page={page_number}"
        driver.get(current_page_url)
        
        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        try:
            # Check if the "You can't perform that action at this time." popup appears
            try:
                popup = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='flash flash-full flash-error ']//div[contains(text(), \"You can't perform that action at this time.\")]")
                ))
                if popup:
                    log_widget.insert(tk.END, "Action limit reached. Closing WebDriver.\n")
                    driver.quit()  # Close the WebDriver
                    return False  # Exit the function
            except:
                pass  # Continue if the popup is not found

            if action == "follow":
                # Look for Follow buttons
                buttons = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "input.btn.btn-sm[aria-label^='Follow']")
                ))
            else:
                # Look for Unfollow buttons
                buttons = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "input.btn.btn-sm[aria-label^='Unfollow']")
                ))

            # If no buttons are found, assume we are done with all pages
            if not buttons:
                log_widget.insert(tk.END, f"No more {action} buttons found on page {page_number}. Stopping.\n")
                break

            # Click each button one by one
            for i, button in enumerate(buttons):
                try:
                    # Scroll to the button to ensure it is visible
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    # Wait for the button to be clickable
                    wait.until(EC.element_to_be_clickable(button))
                    # Click the button
                    button.click()
                    log_widget.insert(tk.END, f"Clicked button {i + 1} on page {page_number}: {button.get_attribute('aria-label')}\n")
                    time.sleep(1)  # Adjust the delay as needed
                except Exception as e:
                    log_widget.insert(tk.END, f"Failed to click button {i + 1} on page {page_number}: {e}\n")
                    break
            
            log_widget.insert(tk.END, f"Completed {action} actions on page {page_number}.\n")
            page_number += 1  # Move to the next page
            
        except Exception as e:
            print(f"Error on the page: {e}")
            log_widget.insert(tk.END, f"Error occurred: {e}\n")
            break

    return True

# Function to start the follow/unfollow process based on user input
def start_process(action):
    # Initialize the WebDriver when the user clicks the button
    initialize_webdriver()
    
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    page_url = url_entry.get().strip()
    
    if not username or not password or not page_url:
        log_widget.insert(tk.END, "Please enter all required fields: Username, Password, and URL.\n")
        return
    
    try:
        # Perform login
        github_login(username, password)
        
        # Handle follow/unfollow process
        handle_buttons(page_url, action)

    finally:
        driver.quit()
        log_widget.insert(tk.END, "Process completed. WebDriver closed.\n")

# GUI setup and button bindings
root = tk.Tk()
root.title("GitHub Follow/Unfollow Automation")
root.geometry("635x500")  # Window size
root.configure(bg='#2d2d30')

# Layout management
frame = tk.Frame(root, padx=20, pady=20, bg='#2d2d30')
frame.pack(expand=True, fill=tk.BOTH)

# Label
title_label = tk.Label(frame, text="GitHub Follow/Unfollow Automation", font=("Arial", 16, "bold"), fg="white", bg="#2d2d30")
title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

# Username Entry
username_label = tk.Label(frame, text="Username/Email:", font=("Arial", 12), fg="white", bg="#2d2d30")
username_label.grid(row=1, column=0, pady=5, padx=10, sticky="e")

username_entry = tk.Entry(frame, font=("Arial", 12), width=40)
username_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w", ipady=5, ipadx=5)

# Password Entry
password_label = tk.Label(frame, text="Password:", font=("Arial", 12), fg="white", bg='#2d2d30')
password_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")

password_entry = tk.Entry(frame, font=("Arial", 12), width=40, show="*")
password_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w", ipady=5, ipadx=5)

# URL Entry
url_label = tk.Label(frame, text="Page URL:", font=("Arial", 12), fg="white", bg="#2d2d30")
url_label.grid(row=3, column=0, pady=5, padx=10, sticky="e")

url_entry = tk.Entry(frame, font=("Arial", 12), width=40)
url_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w", ipady=5, ipadx=5)

# Button styles with light red color
button_style = {"font": ("Arial", 12), "padx": 5, "pady": 5, "bg": "#eb3a34", "fg": "white", "relief": tk.RAISED, "borderwidth": 2}

# Follow and Unfollow buttons
btn_follow = tk.Button(frame, text="Follow Users", command=lambda: start_process("follow"), **button_style)
btn_follow.grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

btn_unfollow = tk.Button(frame, text="Unfollow Users", command=lambda: start_process("unfollow"), **button_style)
btn_unfollow.grid(row=5, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

# Log area
log_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=10, font=("Arial", 10), bg="#1e1e1e", fg="white", borderwidth=2, relief=tk.RAISED)
log_widget.grid(row=6, column=0, columnspan=2, pady=5, padx=5, sticky="nsew")

# Prevent unwanted resizing
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(6, weight=1)

# Start the GUI event loop
root.mainloop()
