import os

from config import PATH_TO_SAVE_DATA, \
    WORD2VEC_FILE_NAME, STOCKCODE_FILE_NAME,\
    WORD2VEC_FILE_NAME_TRAINED, STOCKCODE_FILE_NAME_TRAINED

if __name__ == '__main__':
    correct_files = True
    if not correct_files:
        print('Can not load files.')
        exit(0)

    try:
        file = open(PATH_TO_SAVE_DATA + WORD2VEC_FILE_NAME_TRAINED, 'r')
        file = open(PATH_TO_SAVE_DATA + STOCKCODE_FILE_NAME_TRAINED, 'r')
    except:
        print('Can not find new trained files. Aborting...')
        exit(0)

    # deleting files
    try:
        os.remove(PATH_TO_SAVE_DATA + WORD2VEC_FILE_NAME)
        os.remove(PATH_TO_SAVE_DATA + STOCKCODE_FILE_NAME)
        print('Previous files were successfully deleted -> renaming.')
    except:
        print('Previous files were not found -> renaming.')

    # renaming files
    try:
        os.rename(PATH_TO_SAVE_DATA + WORD2VEC_FILE_NAME_TRAINED, PATH_TO_SAVE_DATA + WORD2VEC_FILE_NAME)
        os.rename(PATH_TO_SAVE_DATA + STOCKCODE_FILE_NAME_TRAINED, PATH_TO_SAVE_DATA + STOCKCODE_FILE_NAME)
        print('Success!')
    except:
        print('Can not rename files. Check access rights.')
