import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')


def get_author_id(name):
    params = {
        "engine": "google_scholar",
        "q": name,
        "api_key": API_KEY,
        "num": 1  # only the first result is needed
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    try:
        # Assuming the first organic result is the author's profile
        author_id = data["profiles"]["authors"][0]["author_id"]
        return author_id
    except Exception as e:
        try:
            author_id = data["organic_results"][0]["publication_info"]["authors"][0]["author_id"]
            return author_id
        except Exception as e:
            print(f'error on: {author_name}')


def get_most_cited_papers(author_name):
    params = {
        "engine": "google_scholar_author",
        "author_id": get_author_id(author_name),
        "api_key": API_KEY
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    if "articles" in data:
        return data["articles"][:15]
    else:
        return []


def get_articles(citation_id):
    params = {
        "engine": "google_scholar_author",
        "citation_id": citation_id,
        "view_op": "view_citation",
        "api_key": API_KEY
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    if "citation" in data:
        if "resources" in data["citation"]:
            return data["citation"]["resources"][0]["link"]
    else:
        return None


with open('./names.txt', 'r') as names:
    for name in names:
        author_name = name[:-1]
        print(f'action on: {author_name}')
        papers = get_most_cited_papers(author_name)
        i = 0
        os.mkdir(f"./reviewers/{author_name}")
        error = 0
        for paper in papers:
            cid = paper["citation_id"]
            link = get_articles(cid)
            if link:
                try:
                    r = requests.get(link, allow_redirects=True)
                    open(f'./reviewers/{author_name}/article{i}.pdf', 'wb').write(r.content)
                    i = i + 1
                except Exception as e:
                    error += 1
        if error > 2:
            print(f'error on: {author_name}')
