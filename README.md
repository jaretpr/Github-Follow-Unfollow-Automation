# GitHub Follow/Unfollow Automation Tool

This tool provides a GUI for automating the process of following or unfollowing users on GitHub. It uses Python's `tkinter` for the GUI and Selenium WebDriver for interacting with GitHub's website. The tool allows you to log in to your GitHub account and perform follow or unfollow actions on users in bulk based on the provided profile URL.

## Features

- **Automated GitHub Login**: Log in to your GitHub account with your username and password.
- **Follow/Unfollow Users**: Follow or unfollow users in bulk from a specified GitHub profile's followers or following list.
- **Headless Mode**: The Selenium WebDriver runs in headless mode, meaning it operates in the background without opening a visible browser window.
- **Scrollable Log**: View the log of actions performed in the application after the WebDriver session is closed.

## Prerequisites

- Python 3.x
- `tkinter` (usually included with Python)
- Selenium (`pip install selenium`)
- Chrome WebDriver (Download from [here](https://sites.google.com/chromium.org/driver/) and specify the correct path)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/github-follow-unfollow-automation.git
   cd github-follow-unfollow-automation

2. **Install Dependencies**:
   ```bash
   pip install selenium

3. **Download Chrome Webdriver**:
   Download the Chrome WebDriver matching your Chrome browser version from here.
   Place the WebDriver in a known directory and update the executable_path in the code accordingly.

## Usage
1. **Run the Script**
   ```bash
   Github_Follow_Unfollow.py

3. **Use the Tool**
**Username/Email:** Enter your GitHub username or email.
**Password:** Enter your GitHub password.
**Page URL:** Enter the URL of the GitHub profile whose followers/following you want to interact with (e.g., https://github.com/someuser/followers).
**Follow Users:** Click this button to follow all users on the specified page.
**Unfollow Users:** Click this button to unfollow all users on the specified page.
**Logs:** The tool will display logs of actions performed in the application after the WebDriver session is closed.

## Important Notes
- Non-Responsive Window: When the Selenium WebDriver starts running, the GUI may appear unresponsive because Selenium has taken over control. You can monitor the progress through the logs in the tool.
- Rate Limiting: GitHub may temporarily block actions if you perform too many in a short period. The tool will handle this by stopping the process if a limit is reached.

## Example
1. Enter your GitHub credentials.
2. Provide a profile URL like https://github.com/someuser/followers.
3. Click "Follow Users" to follow all users on that profile's follower list.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Disclaimer
This tool is intended for educational purposes only. Use responsibly and respect GitHub's Terms of Service.
