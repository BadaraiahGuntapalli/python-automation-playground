import os 

os.makedirs("renamed", exist_ok=True)

i = 1

for i, name in enumerate(os.listdir("."), start=1):
    if name.endswith(".txt"):
        new_name = f"file_{i}.txt"
        os.rename(name, os.path.join("renamed", new_name))
        print(f"{name} -> renamed/{new_name}")
        i += 1
        
print("**Successfully renamed the file names")
    