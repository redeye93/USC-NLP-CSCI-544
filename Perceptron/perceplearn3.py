import sys
import string

FAKE = "Fake"
TRUE = "True"
NEG = "Neg"
POS = "Pos"


class Perceplearn:

    def __init__(self, file_path):

        weight_vector_c1 = dict()
        bias_c1 = 0
        weight_vector_c2 = dict()
        bias_c2 = 0
        weight_vector_average_c1 = dict()
        bias_average_c1 = 0
        weight_vector_average_c2 = dict()
        bias_average_c2 = 0
        sentence_list = []
        output_list = []

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

            # Get the first classifier and set the expected output
            c1 = s_words[1]
            if c1 == FAKE:
                y1 = -1
            else:
                y1 = 1

            # Get the second classifier and check whether it has an entry in the classifier dict
            c2 = s_words[2]
            if c2 == POS:
                y2 = 1
            else:
                y2 = -1

            # Push the output to the list
            output_list.append([y1, y2])
            # Initialize the sentence list
            sentence_list.append(dict())

            # Loop from the fourth word of the sentence which marks the beginning of the sentence
            for word in s_words[3:]:
                word = word.lower()
                # word = word.replace("\n", "")

                # The word should not be in stop words
                if word not in stop_words:
                    # Update the word count in that sentence
                    sentence_list[len(sentence_list) - 1][word] = sentence_list[len(sentence_list) - 1].get(word, 0) + 1

        index_c1 = 0
        index_c2 = 0
        modify1 = True
        modify2 = True

        while modify1 or modify2:
            modify1 = False
            modify2 = False

            for idx, sentence in enumerate(sentence_list):
                y1 = y2 = 0
                for word in sentence.keys():
                    # Calculate the classifier output
                    y1 += weight_vector_c1.get(word, 0) * sentence[word]
                    y2 += weight_vector_c2.get(word, 0) * sentence[word]

                if (y1 + bias_c1) * output_list[idx][0] <= 0:
                    modify1 = True
                    for word in sentence.keys():
                        weight_vector_c1[word] = weight_vector_c1.get(word, 0) + \
                                                 output_list[idx][0] * sentence[word]
                        weight_vector_average_c1[word] = weight_vector_average_c1.get(word, 0) + \
                                                         output_list[idx][0] * sentence[word] * (idx + 1)

                    bias_c1 += output_list[idx][0]
                    bias_average_c1 += (idx + 1) * output_list[idx][0]

                if (y2 + bias_c2) * output_list[idx][1] <= 0:
                    modify2 = True
                    for word in sentence.keys():
                        weight_vector_c2[word] = weight_vector_c2.get(word, 0) + \
                                                 output_list[idx][1] * sentence[word]
                        weight_vector_average_c2[word] = weight_vector_average_c2.get(word, 0) + \
                                                         output_list[idx][1] * sentence[word] * (idx + 1)

                    bias_c2 += output_list[idx][1]
                    bias_average_c2 += (idx + 1) * output_list[idx][1]

            if modify1:
                index_c1 += 1

            if modify2:
                index_c2 += 1

        for word in weight_vector_average_c1.keys():
            weight_vector_average_c1[word] = weight_vector_c1[word] - \
                                             weight_vector_average_c1[word]/(index_c1*len(sentence_list))

        bias_average_c1 = bias_c1 - bias_average_c1/(index_c1*len(sentence_list))

        for word in weight_vector_average_c2.keys():
            weight_vector_average_c2[word] = weight_vector_c2[word] - \
                                             weight_vector_average_c2[word]/(index_c2*len(sentence_list))

        bias_average_c2 = bias_c2 - bias_average_c2/(index_c2*len(sentence_list))

        content = dict()
        content["weight_c1"] = weight_vector_c1
        content["bias_c1"] = bias_c1
        content["weight_c2"] = weight_vector_c2
        content["bias_c2"] = bias_c2

        # Write the model
        file = open('vanillamodel.txt', 'w', encoding='utf8')
        file.write(str(content))
        file.close()

        content = dict()
        content["weight_c1"] = weight_vector_average_c1
        content["bias_c1"] = bias_average_c1
        content["weight_c2"] = weight_vector_average_c2
        content["bias_c2"] = bias_average_c2

        # Write the model
        file = open('averagedmodel.txt', 'w', encoding='utf8')
        file.write(str(content))
        file.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Insufficient number of arguments')
        exit(1)
    else:
        percep = Perceplearn(sys.argv[1])
