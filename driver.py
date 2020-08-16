from porter_stemmer import PorterStemmer

stemmer = PorterStemmer()
resume = open('assets/resume.txt', 'r').read()
print(stemmer.stem_document(resume))
