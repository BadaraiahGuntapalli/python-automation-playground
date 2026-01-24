"""
Datetime basics

    - understand datetime, date and time objects
    - extract calendar components

"""

from datetime import datetime, date

def main():
    # current date + time
    now_dt = datetime.now()
    
    # current date only
    today_date = date.today()
    
    # current time only 
    current_time = now_dt.time()
    
    print("Current datetime: ", now_dt)
    print("current date    :", today_date)
    print("current time    :", current_time)
    print("-"*50)
    
    # Accessing attributes
    print("Year         :", now_dt.year)
    print("Month        :", now_dt.month)
    print("Day          :", now_dt.day)
    print("Hour         :", now_dt.hour)
    print("Minute       :", now_dt.minute)
    print("Second       :", now_dt.second)
    
    
    
    
if __name__ == "__main__":
    main()
    
    