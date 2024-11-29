import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # get the real date time, .log = extension

log_path=os.path.join(os.getcwd(), "logs")#get the path from this loggers file and add logs to create new folder in this path
os.makedirs(log_path, exist_ok=True)#Create a folder names "logs" in env path

LOG_FILEPATH=os.path.join(log_path, LOG_FILE) #LOG_FILE is the actual time

#logger - to note the debugging with real time 
logging.basicConfig(level=logging.INFO,
        filename=LOG_FILEPATH,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)