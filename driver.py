from porter_stemmer import PorterStemmer

if __name__ == '__main__':
    stemmer = PorterStemmer()
    resume = open('resume.txt', 'r').read()
    print(stemmer.stem_document(resume))
