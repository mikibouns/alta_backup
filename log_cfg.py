import logging

format = logging.Formatter('%(asctime)s %(levelname)-10s %(message)s')

# logging to a file
file_hand = logging.FileHandler('alta_backup.log')
file_hand.setLevel(logging.INFO)
file_hand.setFormatter(format)


# logging to stdout
# stdout_hand = logging.StreamHandler()
# file_hand.setLevel(logging.INFO)
# file_hand.setFormatter(format)


#top-level recorder
log = logging.getLogger('alta_backup')
log.setLevel(logging.INFO)
log.addHandler(file_hand)
# log.addHandler(stdout_hand)

if __name__ == '__main__':
    pass