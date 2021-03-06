import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    import operator
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    word_id_log_l = []
    # loop through ids 
    for word_id in range(0, len(test_set.get_all_Xlengths())):
        # get the X, lengths to score the model
        X, lengths = test_set.get_item_Xlengths(word_id)
        prob = {}
        # iterate through the models dict to map the score
        for word, model in models.items():
            try:
                prob[word] =  model.score(X, lengths)
            except:
                continue
        if prob:
            # add the scores to the probabilities list
            probabilities.append(prob)
            # get best guessed word
            best_guess_word = max(list(prob.items()), 
                                  key=operator.itemgetter(1))[0]
            guesses.append(best_guess_word)

    return probabilities, guesses
