import sys
import pandas as pd
import numpy as np
from tqdm import tqdm
from gensim.models import Word2Vec
from config import PATH_TO_SAVE_DATA, DATA_COLUMNS, \
    WORD2VEC_FILE_NAME, STOCKCODE_FILE_NAME,\
    WORD2VEC_FILE_NAME_TRAINED, STOCKCODE_FILE_NAME_TRAINED, DROP_DUPLICATES_COLUMNS


# =========== TECHNICAL FUNCTIONS ===========


def make_collab_matrix(df, products):
    N = len(products)
    res = np.zeros((N, N))
    prod_freq_dict = df[['InvoiceNo', 'StockCode']].groupby(['StockCode']).count().to_dict()['InvoiceNo']
    temp_df = df[['InvoiceNo', 'StockCode']]
    temp_df = temp_df.groupby('InvoiceNo').filter(lambda x: x.shape[0] != 1)

    for i in tqdm(range(N)):
        for j in range(i + 1, N):
            prod_i = products[i]
            prod_j = products[j]

            freq_prod_i = prod_freq_dict[prod_i]
            freq_prod_j = prod_freq_dict[prod_j]

            t= temp_df[(temp_df.StockCode == prod_i) | (temp_df.StockCode == prod_j)]
            ij_freq =t.groupby(['InvoiceNo']).filter(
                lambda x: x.StockCode.shape[0] == 2
            ).shape[0]

            res[i][j] = (2 * ij_freq) / (freq_prod_i + freq_prod_j)

    return res


# ============ MAIN PART ============


if __name__ == '__main__':
    print('Processing file, please wait...')

    path = sys.argv[1]
    parallel_train = sys.argv[2]
    extension = path.split('.')[-1]

    try:
        if extension == 'csv':
            df = pd.read_csv(path)
        elif extension == 'xlsx':
            df = pd.read_excel(path)
        else:
            print('Incorrect file extension: must be .csv or .xlsx')
            sys.exit(-1)
    except:
        print('Cannot read file.')
        sys.exit(-1)

    print('Processing data, please wait...')

    df.dropna(inplace=True)
    try:
        df = df[DATA_COLUMNS]
        df['StockCode'] = df['StockCode'].astype(str)
        df.drop_duplicates(subset=DROP_DUPLICATES_COLUMNS, keep='first', inplace=True)
    except:
        print('File format does not fit requirements. Try checking out column names.')
        sys.exit(-1)

    invoices = df['InvoiceNo'].unique().tolist()
    print('Unique transactions:', df['InvoiceNo'].unique().shape[0])
    products = df['StockCode'].unique().tolist()
    print('Unique products:', df['StockCode'].unique().shape[0])
    customers = df["CustomerID"].unique().tolist()
    print('Unique clients:', len(customers))

    df_temp = df[["StockCode", "Description"]]
    df_temp.drop_duplicates(inplace=True, subset='StockCode', keep="last")
    # StockCode - Description dict
    products_dict = df_temp.groupby('StockCode')['Description'].apply(list).to_dict()

    customer_purchases = []
    for i in tqdm(customers):
        customer_purchases.append(df[df["CustomerID"] == i]["StockCode"].tolist())
    print()

    model = Word2Vec(window=10, min_count=5, sg=1, hs=0,
                     negative=15,  # negative sampling
                     alpha=0.03, min_alpha=0.0007,
                     seed=14)
    model.build_vocab(customer_purchases, progress_per=200)
    model.train(customer_purchases, total_examples=model.corpus_count, epochs=10, report_delay=1)

    model.init_sims(replace=True)

    # saving model
    if parallel_train == 'False':
        model.wv.save(PATH_TO_SAVE_DATA + WORD2VEC_FILE_NAME)
        np.save(PATH_TO_SAVE_DATA + STOCKCODE_FILE_NAME, products_dict)
    else:
        model.wv.save(PATH_TO_SAVE_DATA + WORD2VEC_FILE_NAME_TRAINED)
        np.save(PATH_TO_SAVE_DATA + STOCKCODE_FILE_NAME_TRAINED, products_dict)
