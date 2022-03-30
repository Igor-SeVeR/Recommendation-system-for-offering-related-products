import redis

ACCESS_TOKEN_EXPIRE_HOURS = 24 * 7
ALGORITHM = "HS256"
DATA_COLUMNS = ['InvoiceNo', 'StockCode', 'Description', 'CustomerID']
DATABASE = redis.Redis(host='localhost', port=6379, db=0)
DROP_DUPLICATES_COLUMNS = ['InvoiceNo', 'StockCode', 'CustomerID']
HOST = '0.0.0.0'
PATH_TO_SAVE_DATA = './data/'
PORT = 8090
SECRET_KEY = "368265b264d270f7b9834cf3493354fdb8eba5970ae881b5793c3193e175fbb2"
STOCKCODE_FILE_NAME = 'stockcode_to_description_dict.npy'
STOCKCODE_FILE_NAME_HASHED = 'stockcode_to_description_dict_hashed.npy'
STOCKCODE_FILE_NAME_TRAINED = 'stockcode_to_description_dict_trained.npy'
WORD2VEC_FILE_NAME = 'word2vec-100.bin'
WORD2VEC_FILE_NAME_HASHED = 'word2vec-100_hashed.bin'
WORD2VEC_FILE_NAME_TRAINED = 'word2vec-100_trained.bin'
