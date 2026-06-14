from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os
import glob
import shutil
import tempfile
import platform
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import ttk

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH)

config = {"run_at": None, "browser": "Chrome"}


# ── Profile auto-detection ────────────────────────────────────────────────────

def detect_firefox_profile():
    system = platform.system()
    if system == "Darwin":
        base = os.path.expanduser("~/Library/Application Support/Firefox/Profiles")
    elif system == "Windows":
        base = os.path.join(os.environ.get("APPDATA", ""), "Mozilla", "Firefox", "Profiles")
    else:
        base = os.path.expanduser("~/.mozilla/firefox")

    profiles = glob.glob(os.path.join(base, "*.default-release")) or \
               glob.glob(os.path.join(base, "*default*")) or \
               glob.glob(os.path.join(base, "*"))
    return profiles[0] if profiles else ""


def detect_chrome_profile():
    system = platform.system()
    if system == "Darwin":
        return os.path.expanduser("~/Library/Application Support/Google/Chrome")
    elif system == "Windows":
        return os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "User Data")
    else:
        return os.path.expanduser("~/.config/google-chrome")



def _copy_chromium_profile(src_user_data: str, prefix: str) -> str:
    """Copy a Chromium-family profile to a temp dir, skipping lock/cache files."""
    tmp = tempfile.mkdtemp(prefix=prefix)
    src_default = os.path.join(src_user_data, "Default")
    dst_default = os.path.join(tmp, "Default")
    if os.path.isdir(src_default):
        shutil.copytree(src_default, dst_default,
                        ignore=shutil.ignore_patterns(
                            "*.lock", "lockfile", "SingletonLock",
                            "SingletonCookie", "SingletonSocket",
                            "Cache", "Code Cache", "GPUCache",
                            "Crashpad", "*.log",
                        ))
    return tmp


# ── Driver factory ────────────────────────────────────────────────────────────

def build_driver(browser: str) -> webdriver.Remote:
    if browser == "Firefox":
        profile_path = detect_firefox_profile()
        opts = FirefoxOptions()
        if profile_path:
            opts.add_argument("-profile")
            opts.add_argument(profile_path)
            print(f"Firefox profile: {profile_path}")
        return webdriver.Firefox(options=opts)

    elif browser == "Chrome":
        profile_path = detect_chrome_profile()
        opts = ChromeOptions()
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--remote-debugging-port=0")
        opts.add_argument("--disable-extensions")
        opts.add_argument("--disable-gpu")

        if profile_path and os.path.isdir(profile_path):
            tmp_profile = _copy_chromium_profile(profile_path, "chrome_bot_")
            opts.add_argument(f"--user-data-dir={tmp_profile}")
            opts.add_argument("--profile-directory=Default")
            print(f"Chrome temp profile: {tmp_profile}  (copied from {profile_path})")
        else:
            print("Chrome: no profile found, launching fresh session")

        return webdriver.Chrome(options=opts)

    elif browser == "Safari":
        # Safari uses the system session automatically — no profile arg needed.
        # Requires: Safari > Develop > Allow Remote Automation  (one-time setup)
        return webdriver.Safari()

    else:
        raise ValueError(f"Unknown browser: {browser}")


# ── GUI ───────────────────────────────────────────────────────────────────────

def launch_gui():
    root = tk.Tk()
    root.title("USask Registration Bot")
    root.resizable(False, False)
    root.configure(bg="#2b2b2b")

    pad = {"padx": 20, "pady": 8}
    label_opts = {"bg": "#2b2b2b", "fg": "#ffffff"}
    entry_opts  = {"bg": "#3c3f41", "fg": "#ffffff", "insertbackground": "#ffffff"}

    # NSID
    tk.Label(root, text="NSID:", **label_opts).grid(row=0, column=0, sticky="w", **pad)
    email_var = tk.StringVar(value=os.environ.get("USASK_EMAIL", ""))
    tk.Entry(root, textvariable=email_var, width=30, **entry_opts).grid(row=0, column=1, **pad)

    # Password
    tk.Label(root, text="Password:", **label_opts).grid(row=1, column=0, sticky="w", **pad)
    pass_var = tk.StringVar(value=os.environ.get("USASK_PASSWORD", ""))
    tk.Entry(root, textvariable=pass_var, show="*", width=30, **entry_opts).grid(row=1, column=1, **pad)

    # Run time
    tk.Label(root, text="Run at (HH:MM, 24h):", **label_opts).grid(row=2, column=0, sticky="w", **pad)
    time_var = tk.StringVar(value="16:15")
    tk.Entry(root, textvariable=time_var, width=30, **entry_opts).grid(row=2, column=1, **pad)

    # Browser selector
    tk.Label(root, text="Browser:", **label_opts).grid(row=3, column=0, sticky="w", **pad)
    browser_var = tk.StringVar(value=os.environ.get("USASK_BROWSER", "Firefox"))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Dark.TCombobox",
        fieldbackground="#3c3f41",
        background="#3c3f41",
        foreground="#ffffff",
        selectbackground="#3c3f41",
        selectforeground="#ffffff",
        arrowcolor="#ffffff",
    )
    browser_menu = ttk.Combobox(
        root,
        textvariable=browser_var,
        values=["Firefox", "Chrome", "Safari"],
        state="readonly",
        width=27,
        style="Dark.TCombobox",
    )
    browser_menu.grid(row=3, column=1, **pad)

    # Status label
    status_var = tk.StringVar()
    tk.Label(root, textvariable=status_var, fg="#4ec94e", bg="#2b2b2b").grid(
        row=4, column=0, columnspan=2, pady=4
    )

    def save_and_start():
        email    = email_var.get().strip()
        password = pass_var.get().strip()
        run_time = time_var.get().strip()
        browser  = browser_var.get().strip()

        try:
            hour, minute = map(int, run_time.split(":"))
        except ValueError:
            status_var.set("Invalid time — use HH:MM")
            return

        with open(ENV_PATH, "w") as f:
            f.write(f'USASK_EMAIL="{email}"\n')
            f.write(f'USASK_PASSWORD="{password}"\n')
            f.write(f'USASK_BROWSER="{browser}"\n')

        os.environ["USASK_EMAIL"]    = email
        os.environ["USASK_PASSWORD"] = password
        os.environ["USASK_BROWSER"]  = browser

        run_at = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        if datetime.now() >= run_at:
            run_at += timedelta(days=1)
        config["run_at"]  = run_at
        config["browser"] = browser

        status_var.set(f"Saved! {browser} · will run at {run_at.strftime('%H:%M')}")
        root.after(1500, root.destroy)

    tk.Button(
        root, text="Save & Start", command=save_and_start,
        bg="#4a90d9", fg="#ffffff",
        activebackground="#357abd", activeforeground="#ffffff",
    ).grid(row=5, column=0, columnspan=2, pady=12)

    root.mainloop()


launch_gui()

if config["run_at"] is None:
    raise SystemExit("No run time set — exiting.")

run_at  = config["run_at"]
browser = config["browser"]

# print(f"Waiting until {run_at.strftime('%Y-%m-%d %H:%M:%S')} to start  [browser: {browser}]...")
# while datetime.now() < run_at:
#     time.sleep(1)
# print("Starting now.")

# ── Helpers ───────────────────────────────────────────────────────────────────

MAX_RETRIES = 3

def attempt_login(driver, wait, email, password):
    """Try to log in via CAS. Returns True if login was attempted, False if already logged in."""
    try:
        idLogin = wait.until(EC.presence_of_element_located((By.ID, "username")))
    except Exception:
        print("No login page detected — already logged in via profile.")
        return False

    # Clear fields before typing (important on retry)
    idLogin.clear()
    idLogin.send_keys(email)

    passLogin = driver.find_element(By.ID, "password")
    passLogin.clear()
    passLogin.send_keys(password)
    driver.find_element(By.NAME, "submit").click()
    return True


def login_with_retry(driver, wait, email, password, max_retries=MAX_RETRIES):
    """Attempt login, retrying up to max_retries times if an error banner appears."""
    for attempt in range(1, max_retries + 1):
        print(f"Login attempt {attempt}/{max_retries}...")
        attempted = attempt_login(driver, wait, email, password)

        if not attempted:
            return  # already logged in, nothing to verify

        # Wait briefly for the page to respond
        time.sleep(3)

        # Check for known CAS error messages
        error_selectors = [
            ".alert-danger",
            "#msg.errors",
            ".form-element.form-error",
            "[class*='error']",
        ]
        failed = False
        for sel in error_selectors:
            try:
                err = driver.find_element(By.CSS_SELECTOR, sel)
                if err.is_displayed() and err.text.strip():
                    print(f"  Login failed (attempt {attempt}): {err.text.strip()[:120]}")
                    failed = True
                    break
            except Exception:
                pass

        # If we're now past the login page, we succeeded
        if not failed:
            try:
                driver.find_element(By.ID, "username")
                # Still on login page but no visible error — might be loading, wait a bit
                time.sleep(2)
            except Exception:
                print(f"  Login succeeded on attempt {attempt}.")
                return

        if attempt < max_retries:
            print(f"  Retrying in 2 seconds...")
            time.sleep(2)
            # Reload the login page for a clean retry
            driver.get("https://banner.usask.ca/StudentRegistrationSsb/ssb/registration")
            time.sleep(2)
            try:
                pl = wait.until(EC.element_to_be_clickable((By.ID, "register")))
                pl.click()
            except Exception:
                pass
        else:
            raise RuntimeError(
                f"Login failed after {max_retries} attempts. "
                "Check your NSID/password and try again."
            )


# ── Launch browser & automate registration ────────────────────────────────────

driver = build_driver(browser)
driver.get("https://banner.usask.ca/StudentRegistrationSsb/ssb/registration")

wait = WebDriverWait(driver, 15)

planLink = wait.until(EC.element_to_be_clickable((By.ID, "register")))
planLink.click()

load_dotenv()
login_with_retry(driver, wait, os.environ["USASK_EMAIL"], os.environ["USASK_PASSWORD"])

time.sleep(99999)

print(f"Waiting until {run_at.strftime('%Y-%m-%d %H:%M:%S')} to start  [browser: {browser}]...")
while datetime.now() < run_at:
    time.sleep(1)
print("Starting now.")

choice = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_txt_term .select2-choice")))
choice.click()

searchBox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#select2-drop .select2-input")))
searchBox.send_keys("2026 Fall Term")
result = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='select2-drop']//li[contains(., '2026 Fall Term')]")))
result.click()

button = wait.until(EC.element_to_be_clickable((By.ID, "term-go")))
button.click()

button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Plans']")))
button.click()

button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-all-button.add-section-button.add-section-plan-button")))
button.click()

# Dismiss the notification-center-shim overlay if it's blocking the button
try:
    shim = driver.find_element(By.CSS_SELECTOR, ".notification-center-shim")
    driver.execute_script("arguments[0].remove();", shim)
    print("Removed notification-center-shim overlay")
except Exception:
    pass  # shim not present, no action needed

button = wait.until(EC.presence_of_element_located((By.ID, "saveButton")))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
time.sleep(0.5)
driver.execute_script("arguments[0].click();", button)
print("Clicked saveButton")
time.sleep(100)
