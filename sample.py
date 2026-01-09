#%% 
x = "i am good boy"

# %%
import time 
import os
print(time.time())

print(os.path.getmtime(__file__))
now = time.time()
created = os.path.getmtime(__file__)
print(f"differnece {now - created}")