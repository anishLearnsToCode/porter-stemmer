from porter_stemmer import PorterStemmer

stemmer = PorterStemmer()
resume = open('resume.txt', 'r').read()
# resume = open('do-not-go-gentle-into-that-good-night.txt', 'r').read()
print(stemmer.stem_document(resume))
