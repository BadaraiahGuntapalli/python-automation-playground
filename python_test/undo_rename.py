import os 


for name in os.listdir("renamed"):
    os.rename(os.path.join("renamed", name), name)
    
    