import sys
import string


class NBLearn:

    def __init__(self, file_path):
        # Dictionaries for the two classifiers and the word
        classifier1 = dict({})
        classifier2 = dict({})
        words = dict({})

        # Count key and Word Count
        count_key = "$*$count$*$"
        word_count = "$*$word$*$"

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

        # Loop over all the sentences
        for sentence in open(file_path, encoding='utf8'):
            s_words = sentence.translate(translator).split(" ")

            # Get the first classifier and check whether it has an entry in the classifier dict
            c1 = s_words[1]
            if classifier1.get(c1, None) is None:
                classifier1[c1] = dict({count_key: 1, word_count: 0})
            else:
                classifier1[c1][count_key] += 1

            # Get the second classifier and check whether it has an entry in the classifier dict
            c2 = s_words[2]
            if classifier2.get(c2, None) is None:
                classifier2[c2] = dict({count_key: 1, word_count: 0})
            else:
                classifier2[c2][count_key] += 1

            # Loop from the fourth word of the sentence which marks the beginning of the sentence
            for word in s_words[3:]:
                word = word.lower()

                # The word should not be in stop words
                if word not in stop_words:
                    classifier1[c1][word_count] += 1
                    classifier1[c1][word] = classifier1[c1].get(word, 0) + 1

                    classifier2[c2][word_count] += 1
                    classifier2[c2][word] = classifier2[c2].get(word, 0) + 1

                    # Unique word entry
                    words[word] = words.get(word, 0) + 1

        # Consolidate the data in one array
        content = [classifier1, classifier2, words]

        # Write the model
        file = open('nbmodel.txt', 'w', encoding='utf8')
        file.write(str(content))
        file.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Insufficient number of arguments')
        exit(1)
    else:
        hmm = NBLearn(sys.argv[1])
