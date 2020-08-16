from porter_stemmer import PorterStemmer

stemmer = PorterStemmer()
resume = open('resume.txt', 'r').read()
print(stemmer.stem_document(resume))
