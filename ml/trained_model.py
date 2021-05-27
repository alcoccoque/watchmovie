import pandas as pd
import pickle
from os.path import join, dirname, realpath
def load():
    """
    load the nlp model and vectorizer from disk
    """
    filename = join(dirname(realpath(__file__)), 'nlp_model.pkl')
    clf = pickle.load(open(filename, 'rb'))

    transform = join(dirname(realpath(__file__)), 'tranform.pkl')
    vectorizer = pickle.load(open(str(transform), 'rb'))

    return filename, clf, vectorizer


# converting list of string to list (eg. "["abc","def"]" to ["abc","def"])
def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["', '')
    my_list[-1] = my_list[-1].replace('"]', '')
    return my_list


def get_suggestions():
    """
    suggest yo user film title based on first characters
    """
    data = pd.read_csv(join(dirname(realpath(__file__)), 'main_data.csv'))
    return list(data['movie_title'].str.capitalize())
