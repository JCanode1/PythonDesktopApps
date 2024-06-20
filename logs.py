import logging

logging_mode = True
# Initialize the logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Set the logging level according to your needs

# Define a file handler
try:
    file_handler = logging.FileHandler('log.txt')
    file_handler.setLevel(logging.DEBUG)  # Set the log level for file output
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except FileNotFoundError:
    logger.addHandler(logging.StreamHandler())  # Fallback to console output if log file not found
    logger.error("Log File not found")

def log(logMSG):
    if logging_mode:  # Assuming logging_mode is defined somewhere
        logger.debug(logMSG)  # Log the message at DEBUG level
    else:
        pass
