from datetime import datetime
import time


fb_time = "05/24/2021 12:55 AM"
epoch = int(time.mktime(time.strptime(fb_time, "%m/%d/%Y %I:%M %p")))


print(epoch)
