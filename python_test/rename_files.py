from hmac import new
import os 




script_dir = os.path.dirname(os.path.abspath(__file__))

for i, fname in enumerate(os.listdir(script_dir), start = 1):
    if fname.endswith(".txt"):
        modified_name = f"modified_{i}.txt"
        old_path = os.path.join(script_dir, fname)
        new_path = os.path.join(script_dir, modified_name)
        os.rename(old_path, new_path)
        print(f"{fname} | {modified_name}")

        
print("**Successfully renamed the file names")
    

