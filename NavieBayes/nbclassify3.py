import sys
from math import log10, inf
import string


class NBClassify:

    def __init__(self, file_path):
        # Open the model trained
        file = open('nbmodel.txt', encoding='utf8')

        stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as",
                      "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
                      "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further",
                      "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
                      "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in",
                      "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor",
                      "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over",
                      "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that",
                      "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
                      "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
                      "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what",
                      "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why",
                      "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
                      "yourself", "yourselves"]

        # Parse the model from string to the dict
        model = file.read()
        model = eval(model)
        classifier1 = model[0]
        classifier2 = model[1]
        words = model[2]
        file.close()

        # Set the count key and the word count
        count_key = "$*$count$*$"
        word_count = "$*$word$*$"

        translator = str.maketrans('', '', string.punctuation)

        file = open('nboutput.txt', 'w', encoding='utf8')

        # Iterate over all the sentences
        for sentence in open(file_path, encoding='utf8'):
            s_words = sentence.translate(translator).split(" ")

            # Set the probability dictionary for all the classes
            prob = dict({})

            # Calculate the total count of the occurrences of the classes
            total = 0
            for key in classifier1.keys():
                total += classifier1[key][count_key]

            # Classifier1 probability
            for key in classifier1.keys():
                prob[key] = log10(classifier1[key][count_key]/total)

            # Code to assign the class probability for 2nd classifier
            total = 0
            for key in classifier2.keys():
                total += classifier2[key][count_key]

            # Classifier2 probability
            for key in classifier2.keys():
                prob[key] = log10(classifier2[key][count_key]/total)

            # Iterate over all the words
            for word in s_words[1:]:
                word = word.lower()

                # Remove all the punctuations
                for p in [',', '!', '@', '#', '$', '%', '^', '&', '*', '.', '(', ')', '-', '_', '{', '}', '"', ':',
                          ';', '+', '=', '\\', '/', '\n', '?']:
                    word = word.replace(p, '')
                word = word.split('\'')[0]

                # The word should not be a stop word and should be from vocabulary
                if word not in stop_words and word in words.keys():
                    for key in classifier1.keys():
                        # The count of that word occurrence should be at least one - laplace smoothing
                        prob[key] += log10(
                            (classifier1[key].get(word, 0) + 1) / (classifier1[key][word_count] + len(words)))

                    for key in classifier2.keys():
                        # The count of that word occurrence should be at least one - laplace smoothing
                        prob[key] += log10(
                            (classifier2[key].get(word, 0) + 1) / (classifier2[key][word_count] + len(words)))

            # Loop over all the keys of the classifiers and store the max
            max1 = dict({"v": -inf, "k": None})
            for key in classifier1.keys():
                if max1["v"] < prob[key]:
                    max1["v"] = prob[key]
                    max1["k"] = key

            # Loop over all the keys of the classifiers and store the max
            max2 = dict({"v": -inf, "k": None})
            for key in classifier2.keys():
                if max2["v"] < prob[key]:
                    max2["v"] = prob[key]
                    max2["k"] = key

            # Write the key
            file.write(s_words[0] + " " + max1["k"] + " " + max2["k"] + "\n")

        # Close the file
        file.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Insufficient number of arguments')
        exit(1)
    else:
        hmm = NBClassify(sys.argv[1])
