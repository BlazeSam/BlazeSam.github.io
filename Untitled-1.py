from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
from datetime import datetime , timedelta
import time
import tkinter as tk

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH)

config = {"run_at": None}

def launch_gui():
    root = tk.Tk()
    root.title("USask Registration Bot")
    root.resizable(False, False)

    pad = {"padx": 20, "pady": 8}

    tk.Label(root, text="NSID:", fg="white").grid(row=0, column=0, sticky="w", **pad)
    email_var = tk.StringVar(value=os.environ.get("USASK_EMAIL", ""))
    tk.Entry(root, textvariable=email_var, width=30).grid(row=0, column=1, **pad)

    tk.Label(root, text="Password:", fg="white").grid(row=1, column=0, sticky="w", **pad)
    pass_var = tk.StringVar(value=os.environ.get("USASK_PASSWORD", ""))
    tk.Entry(root, textvariable=pass_var, show="*", width=30).grid(row=1, column=1, **pad)

    tk.Label(root, text="Run at (HH:MM, 24h):", fg="white").grid(row=2, column=0, sticky="w", **pad)
    time_var = tk.StringVar(value="16:15")
    tk.Entry(root, textvariable=time_var, width=30).grid(row=2, column=1, **pad)

    status_var = tk.StringVar()
    tk.Label(root, textvariable=status_var, fg="green").grid(row=3, column=0, columnspan=2, pady=4)

    def save_and_start():
        email    = email_var.get().strip()
        password = pass_var.get().strip()
        run_time = time_var.get().strip()

        try:
            hour, minute = map(int, run_time.split(":"))
        except ValueError:
            status_var.set("Invalid time — use HH:MM")
            return

        with open(ENV_PATH, "w") as f:
            f.write(f'USASK_EMAIL="{email}"\n')
            f.write(f'USASK_PASSWORD="{password}"\n')

        os.environ["USASK_EMAIL"] = email
        os.environ["USASK_PASSWORD"] = password

        run_at = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        if datetime.now() >= run_at:
            run_at += timedelta(days=1)
        config["run_at"] = run_at

        status_var.set(f"Saved! Will run at {run_at.strftime('%H:%M')}")
        root.after(1500, root.destroy)

    tk.Button(root, text="Save & Start", command=save_and_start).grid(row=4, column=0, columnspan=2, pady=12)
    root.mainloop()

launch_gui()

if config["run_at"] is None:
    raise SystemExit("No run time set — exiting.")

run_at = config["run_at"]
print(f"Waiting until {run_at.strftime('%Y-%m-%d %H:%M:%S')} to start...")
while datetime.now() < run_at:
    time.sleep(1)
print("Starting now.")

FIREFOX_PROFILE_PATH = "/Users/ayoyinkalafiaji/Library/Application Support/Firefox/Profiles/M0xoySU1.Profile 1"

options = Options()
options.add_argument("-profile")
options.add_argument(FIREFOX_PROFILE_PATH)

driver = webdriver.Firefox(options=options)
driver.get('https://banner.usask.ca/StudentRegistrationSsb/ssb/registration')

wait = WebDriverWait(driver, 15)

planLink = wait.until(EC.element_to_be_clickable((By.ID, "register")))
planLink.click()


# If not already logged in, you'll be redirected to CAS login — handle it here
try:
    load_dotenv()
    idLogin = wait.until(EC.presence_of_element_located((By.ID, "username")))
    idLogin.send_keys(os.environ["USASK_EMAIL"])
    passLogin = driver.find_element(By.ID, "password")

    WebDriverWait(driver, 15)
    passLogin.send_keys(os.environ["USASK_PASSWORD"])
    print(os.environ["USASK_PASSWORD"])
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 15)
except Exception:
    print("Already logged in via profile — proceeding")

#register classees
# button = wait.until(EC.element_to_be_clickable((By.ID, "register")))
# button.click()

choice = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_txt_term .select2-choice")))
choice.click()

searchBox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#select2-drop .select2-input")))
#searchBox.send_keys("2026 Fall Term")
searchBox.send_keys("2026 Summer Term")
result = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='select2-drop']//li[contains(., '2026 Summer Term')]")))
#result = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='select2-drop']//li[contains(., '2026 Fall Term')]")))
result.click()


button = wait.until(EC.element_to_be_clickable((By.ID, "term-go")))
button.click()

button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Plans']")))
#driver.find_element(By.CSS_SELECTOR, "[aria-label='Close']")
button.click()

button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-all-button.add-section-button.add-section-plan-button")))
button.click()


button = wait.until(EC.element_to_be_clickable((By.ID, "saveButton")))
button.click()
time.sleep(100)



# grid = [[1,1,1,1,1,1] for i in range(8)]
# print(len(grid), len(grid[0]))
# for i in range(len(grid)):
#     print(grid[i])


# for v in range(4):
#     print(v%4)
"""# def minJumps(nums):
#     if len(nums) <= 2:
#         return len(nums) - 1

#     maximum = max(nums) 
#     isPrime = [True] * (maximum + 1)
#     isPrime[0] = isPrime[1] = False
#     bucket = []
#     index = []
    
#     i = 2
#     while i * i <= maximum:
#         if isPrime[i]:
#             if i in nums:
#                 for val in range(i*i, maximum+1, i):
#                     isPrime[val] = False 
#         i += 1
    
#     for i in range(len(nums)):
#         if isPrime[nums[i]] and nums[i] not in bucket:
#             bucket.append(nums[i])
#             index.append(i)

#     # simple graph representation 
#     adjList = {} #we are storing the nodes as their index
    
#     for i in range(len(nums)):
#         if i == 0:
#             adjList[i] = [i+1]
#         elif i == len(nums) - 1:
#             adjList[i] = [i-1]
#         else:
#             adjList[i] = [i-1, i+1]
            
#         if i in index:
#             for val in range(len(nums)):
#                 if val != i:
#                     if nums[val] % nums[i] == 0:
#                         adjList[i].append(val)
#     print(adjList)
#     #BFS
    
#     #visited = [False] * len(nums)
#     visited = [[True] + [False]*(len(nums)-1) for i in range(len(nums) - 1)]
#     res = []
#     q = []
#     dist = [[0, 1] + [-1] * (len(nums)-2) for i in range(len(nums) - 1)]
#     optimum = -1

#     #visited[0] = True
#     res.append(0)
#     for i in adjList[0]:
#         q.append(i)
    
#     val = 0
#     while q:
        
#         curr = q.pop(0)
#         res.append(curr)
        
#         for x in adjList[curr]:
#             if not visited[x]:
#                 visited[x] = True
#                 if x == len(nums) - 1:
#                     dist[val][x] = dist[val][curr] + 1
#                     if optimum == -1:
#                         optimum = dist[val][x]
#                     elif dist[val][x] < optimum:
#                         optimum = dist[val][x]
#                 else: 
#                     dist[val][x] = dist[val][curr]+1#answer
#                 q.append(x)
#                 val += 1
                
#     print(dist)
#     return optimum

# v = [7,5,7]

# print(minJumps(v))"""