import hashlib

import numpy as np
from gensim.models import KeyedVectors
from gensim.models.keyedvectors import Word2VecKeyedVectors
from config import PATH_TO_SAVE_DATA, WORD2VEC_FILE_NAME, STOCKCODE_FILE_NAME, \
    WORD2VEC_FILE_NAME_HASHED, STOCKCODE_FILE_NAME_HASHED

MAIN_FILES = {WORD2VEC_FILE_NAME: WORD2VEC_FILE_NAME_HASHED,
              STOCKCODE_FILE_NAME: STOCKCODE_FILE_NAME_HASHED}


def check_files(products_dict_path, model_path):
    try:
        products_dict_check = np.load(products_dict_path,
                                      allow_pickle='TRUE').item()
        if not isinstance(products_dict_check, dict):
            raise TypeError('Loaded file is incorrect')

        model_check = KeyedVectors.load(model_path,
                                        mmap='r')
        if not isinstance(model_check, Word2VecKeyedVectors):
            raise TypeError('Loaded file is incorrect')

    except FileNotFoundError:
        print('Saved model files do not exist.')
        return False

    except TypeError:
        print('Saved model files contain incorrect data.')
        return False

    except:
        print('Saved model files are not in correct format.')
        return False

    return True


def check_integer_values(**kwarg):
    out = []
    for name, val in kwarg.items():
        try:
            out.append(int(val))
        except:
            raise TypeError('Incorrect type of ' + name + ': must be integer')

    if len(out) > 1:
        return tuple(out)
    else:
        return out[0]


def hash_main_files():
    for main_file in MAIN_FILES.keys():
        # hashing file
        hash_md5 = hashlib.md5()
        with open(PATH_TO_SAVE_DATA + main_file, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        # saving file
        try:
            file = open(PATH_TO_SAVE_DATA + MAIN_FILES[main_file], 'w')
            file.write(hash_md5.hexdigest())
            file.close()
            print('Successfully hashed and saved %s' % main_file)
        except:
            print('Can not save hash and save file %s' % main_file)
            return False
    return True


def check_main_hashed_files():
    for main_file in MAIN_FILES.keys():
        # hashing file
        hash_md5 = hashlib.md5()
        with open(PATH_TO_SAVE_DATA + main_file, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        # checking hashes
        file_hash = ''
        try:
            file = open(PATH_TO_SAVE_DATA + MAIN_FILES[main_file], 'r')
            file_hash = file.read()
            file.close()
        except:
            print('Can not read file with hash %s' % MAIN_FILES[main_file])
            return False
        if file_hash != hash_md5.hexdigest():
            print('Hashes are not equal. '
                  'Files were changed. Restart the server.')
            return False
    return True
