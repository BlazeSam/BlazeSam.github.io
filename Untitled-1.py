from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time

driver = webdriver.Chrome()
driver.get('https://banner.usask.ca/StudentRegistrationSsb/ssb/registration')
#driver.get('https://cas.usask.ca/cas')

#idLogin = driver.find_element(By.ID, "username")
#idLogin.send_keys('zqd984')

#passLogin = driver.find_element(By.ID, 'password')
#passLogin.send_keys('Blazefire4ever')

#submit = driver.find_element(By.NAME, 'submit')

#submit.click()
time.sleep(1000)
#driver.quit()

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