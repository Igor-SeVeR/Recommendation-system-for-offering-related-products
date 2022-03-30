import numpy as np
from utils import check_integer_values
from gensim.models import KeyedVectors
from config import PATH_TO_SAVE_DATA, WORD2VEC_FILE_NAME, STOCKCODE_FILE_NAME


# =========== TECHNICAL FUNCTIONS ===========


def aggregate_vectors(model, products):
    product_vec = []

    for prod in products:
        try:
            product_vec.append(model[prod])
        except KeyError:
            continue

    if not product_vec:
        all_vects = model[model.wv.vocab]
        i = np.random.randint(len(all_vects))
        return all_vects[i]

    res = np.mean(product_vec, axis=0)

    return res


def similar_products(model, products, n=7):
    products_dict = np.load(PATH_TO_SAVE_DATA + STOCKCODE_FILE_NAME,
                            allow_pickle='TRUE').item()

    cart_vec = aggregate_vectors(model, products)

    # получим наиболее похожие продукты для входного вектора
    N = len(products) + n + 1
    prods_sorted = model.similar_by_vector(cart_vec, topn=N)[1:]

    res = []
    count = 0
    for prod in prods_sorted:
        if count == n:
            break

        cur_id = prod[0]
        cur_description = products_dict[prod[0]][0]
        cur_confidence = prod[1]

        if cur_id in products:
            continue

        new_out = (cur_id, cur_description, cur_confidence)
        res.append(new_out)
        count += 1
    return res


# ============ MAIN PART ============


def get_recommendations(json):
    # loading model
    model = KeyedVectors.load(PATH_TO_SAVE_DATA + WORD2VEC_FILE_NAME, mmap='r')

    products = json['product_list']
    n = check_integer_values(n=json['n'])

    res = similar_products(model, products, n=n)
    return {'recommendation': res}
