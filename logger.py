import logging

#filename='app.log', filemode='w'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

if __name__ == '__main__':
    print("LOGGER module started")
else:
    LOGGER = logging.getLogger(__name__)