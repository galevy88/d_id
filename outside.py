from cloudwatch_logger import CloudWatchLogger
import logging
if __name__ == '__main__':
    try:
        # Deliberately raising an exception
        raise Exception("This is a simulated exception for testing.")

    except Exception as e:
        # Logging the exception using CloudWatchLogger
        CloudWatchLogger.log(f"An exception occurred: {e}", level=logging.ERROR)
