from porter_stemmer import PorterStemmer


def number_of_words(document):
    count = 0
    for line in document.split('\n'):
        count += len(line.split())
    return count


def unique_words(document):
    words = set()
    for line in document.split('\n'):
        for word in line.split():
            words.add(word)
    return len(words)


stemmer = PorterStemmer()
resume = open('assets/resume.txt', 'r').read()
number_words_resume = number_of_words(resume)
number_unique_words_in_resume = unique_words(resume)
number_unique_words_stemmed_resume = unique_words(stemmer.stem_document(resume))

print('Number of Words in Resume:', number_words_resume)
print('Number Of Unique Words In Resume:', number_unique_words_in_resume)
print('Number of Unique Words after Stemming:', number_unique_words_stemmed_resume)
