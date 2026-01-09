"""
Datetime formatting and parsing 
    - Convert datetime to string (formatting)
    - Convert string to datetime (parising)
    - use safe, automation friendly formats
"""

from datetime import datetime

def main():
    # get datetime object 
    now_dt = datetime.now()
    
    #log friendly human readable 
    log_fmt = "%Y-%m-%d %H:%M:%S"
    log_str = now_dt.strftime(log_fmt)
    
    # File name safe (no spaces, no colons)
    file_fmt = "%Y%m%d_%H%M%S"
    file_str = now_dt.strftime(file_fmt)
    
    # iso 8601 (machine + humbam friendly)
    iso_str = now_dt.isoformat(timespec="seconds")
    
    print("Original datetime :", now_dt)
    print("log datetime :", log_str)
    print("File datetime :", file_str)
    print("ISO format :", iso_str)
    
    print("-"*50)
    
    # parsing the string-> datetime
    parsed_log = datetime.strptime(log_str, log_fmt)
    parsed_iso = datetime.fromisoformat(iso_str)
    
    print("Parsed from log: ", parsed_log)
    print("Parsed from ISO:", parsed_iso)
    
    
if __name__ == "__main__":
    main()