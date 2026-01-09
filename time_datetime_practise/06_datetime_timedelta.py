"""
Datetime arithmatic with timedelta
    - Add and subtract time using timedelta 
    - Compute differences between datetimes
"""

from datetime import datetime, timedelta
import time

def main():
    # get date time 
    now_dt = datetime.now()
    
    one_day_later = now_dt + timedelta(days = 1)
    seven_days_later = now_dt + timedelta(days = 7)
    thirty_minutes_later = now_dt + timedelta(minutes=30)
    
    # time differences calculations
    diff = seven_days_later - now_dt
    
    print("Now                 :", now_dt)
    print("1 day ago            :", one_day_later)
    print("7 days from now      :", seven_days_later)
    print("30 minutes from now  :", thirty_minutes_later)
    print("-" * 50)
    
    print("Difference (timedelta)", diff)
    print("Difference in days   :", diff.days)
    print("Differnece in seconds    :", diff.total_seconds())
    
    
    
if __name__ == "__main__":
    main()
    