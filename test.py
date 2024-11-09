import schedule
import time
def prrint(se) :
    print(se)
    
    
schedule.every().saturday.at("02:13").do(prrint, 'to')

while True:
    schedule.run_pending()
    time.sleep(1)