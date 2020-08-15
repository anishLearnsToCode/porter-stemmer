import subprocess
import slate3k as slate

with open('resume.pdf') as resume:
    doc = slate.PDF(resume)




# def pdf_to_text(filepath):
#     print('Getting text content for {}...'.format(filepath))
#     process = subprocess.Popen(['pdf2txt.py', filepath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     stdout, stderr = process.communicate()
#
#     if process.returncode != 0 or stderr:
#         raise OSError('Executing the command for {} caused an error:\nCode: {}\nOutput: {}\nError: {}'.format(filepath, process.returncode, stdout, stderr))
#
#     return stdout.decode('utf-8')
#
#
# pdf_to_text("C:\\Users\anish\projects\nlp\porter-stemmer\resume.pdf")
