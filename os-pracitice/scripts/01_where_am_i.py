import os 

def main():
    # where python is 
    cwd = os.getcwd()
    
    # absolute path of this scipt file 
    script_path = os.path.abspath(__file__)
    
    print(__file__) # sometimes this ones give you relative path 
    print(script_path)
    
    # directory containing this script
    script_dir = os.path.dirname(script_path)
    script_other = os.path.dirname(__file__)
    
    print("Current working directory: ")
    print(cwd)
    print()
    
    print("script path :: ")
    print(script_path)
    print()

    print("scirpt directory")
    print(script_dir)
    print()
    
    print("other way of directory name :")
    print(script_other)
    
    
    
if __name__ == "__main__":
    main()