import json

import spacy
import PyPDF2
import os


def extract_sections(file_path):
    text = ''
    # creating a pdf file object
    pdfFileObj = open(file_path, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    for i in range(5):
        pageObj = pdfReader.pages[i]
        text += pageObj.extract_text() + '\n'
    pdfFileObj.close()
    return text


nlp = spacy.load('en_core_web_sm')

score = {}


submissions = {}

reviewers_articles = {}

for dirpath, dirnames, filenames in os.walk("./submissions"):
    for submission in filenames:
        print(submission)
        sub_text = extract_sections(f'{dirpath}/{submission}')
        sub = nlp(sub_text)
        submissions[submission] = sub

for dirpath, dirnames, filenames in os.walk("./reviewers"):
    for reviewer in dirnames:
        print(reviewer)
        reviewers_articles[reviewer] = {}
        for dirpath_to_reviewer, _, articles in os.walk(f"./reviewers/{reviewer}"):
            for article in articles:
                try:
                    pdf_text = extract_sections(f'{dirpath_to_reviewer}/{article}')
                    pdf = nlp(pdf_text)
                    reviewers_articles[reviewer][article] = pdf
                except Exception:
                    pass
print(reviewers_articles)
for submission in submissions:
    print(submission)
    score[submission] = {}
    for reviewer in reviewers_articles:
        number_of_articles = len(reviewers_articles[reviewer])
        sum_similarity_score = 0
        for article in reviewers_articles[reviewer]:
            sum_similarity_score += submissions[submission].similarity(reviewers_articles[reviewer][article])
        score[submission][reviewer] = sum_similarity_score / number_of_articles

with open('./result.json', 'w') as result:
    result.write(json.dumps(score))