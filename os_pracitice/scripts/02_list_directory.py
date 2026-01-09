import os


"""
    list directory contents using full paths.

"""

def main():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    
    dir_path = os.path.join(scripts_dir, "..", "playground", "data")
    dir_path = os.path.abspath(dir_path)
    
    if not os.path.exists(dir_path):
        print("Data directory not exist")
        return 
    
    for name in os.listdir(dir_path):
        print(name)
    
    


if __name__ == "__main__":
    main()