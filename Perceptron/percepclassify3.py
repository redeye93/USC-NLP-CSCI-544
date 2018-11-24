import sys
import string

FAKE = "Fake"
TRUE = "True"
NEG = "Neg"
POS = "Pos"


class Percepclassify:

    def __init__(self, model_path, file_path):
        # Open the model trained
        file = open(model_path, encoding='utf8')

        # Parse the model from string to the dict
        model = file.read()
        file.close()

        model = eval(model)
        weight_vector_c1 = model["weight_c1"]
        weight_vector_c2 = model["weight_c2"]
        bias_c1 = model["bias_c1"]
        bias_c2 = model["bias_c2"]

        translator = str.maketrans('', '', string.punctuation)

        # Stop Words
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

        file = open('percepoutput.txt', 'w', encoding='utf8')

        # Loop over all the sentences
        for sentence in open(file_path, encoding='utf8'):
            s_words = sentence.translate(translator).split(" ")
            y1 = 0
            y2 = 0

            # Loop from the fourth word of the sentence which marks the beginning of the sentence
            for word in s_words[1:]:
                word = word.lower()
                # word = word.replace("\n", "")

                # The word should not be in stop words
                if word not in stop_words:
                    y1 += weight_vector_c1.get(word, 0)
                    y2 += weight_vector_c2.get(word, 0)

            if y1 + bias_c1 > 0:
                y1 = TRUE
            else:
                y1 = FAKE

            if y2 + bias_c2 > 0:
                y2 = POS
            else:
                y2 = NEG

            # Write the key
            file.write(s_words[0] + " " + y1 + " " + y2 + "\n")

        file.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Insufficient number of arguments')
        exit(1)
    else:
        hmm = Percepclassify(sys.argv[1], sys.argv[2])
