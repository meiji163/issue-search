import json
import re
from collections import defaultdict
from typing import Dict, Tuple, Set, List

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')

STOP_WORDS = set(stopwords.words('english'))
QUOTES = {'""',"'","''",'`','``','```'}
PUNCT = '!"#$%&\'()*+,./;<=>?@[\\]^_`{|}~ ' #keep '-' for flags and ':' for emojis

def tokenize(s: str) -> List[str]:
    tok = [ t.strip().lower() for t in word_tokenize(s)]
    def is_token(s):
        return len(s)>1 and len(s)<12 \
            and s not in STOP_WORDS\
            and s not in QUOTES
    tok = filter(is_token, tok)
    return list(tok)

def find_duplicates(issues: dict, repo: str) -> Set[Tuple[int,int]]: 
    dupl_re = re.compile(r"[dD]uplicate [oO]f #*(\d+)")
    url = r"https://github.com/" + repo + "/issues/"
    dupl_url_re = re.compile(f"[dD]uplicate [oO]f {url}(\d+)")

    duplicates = set() 
    for issue in issues:
        m1 = dupl_re.search(issue["body"])
        num = issue["number"]
        if m1:
            duplicates.add( (num, eval(m1.group(1))) )
            continue
        for comment in issue["comments"]:
            if not comment["isMinimized"]:
                m1 = dupl_re.search(comment["body"])
                m2 = dupl_url_re.search(comment["body"])
                if m1:
                    duplicates.add( (num, eval(m1.group(1))) )
                    break
                elif m2:
                    duplicates.add( (num, eval(m2.group(1))) )
                    break
    return duplicates

# note: these overlap with found duplicates
def find_links(issues: dict, repo: str) -> Set[Tuple[int,int]]:
    url = r"https://github.com/" + repo + "/issues/"
    url_re = re.compile(f"{url}(\d+)")

    links = set() 
    for issue in issues:
        num = issue["number"]
        m = url_re.search(issue["body"])
        if m:
            for n in url_re.findall(issue["body"]):
                links.add( (num, eval(n)) )
        for comment in issue["comments"]:
            if not comment["isMinimized"]:
                m = url_re.search(comment["body"])
                if m:
                    for n in url_re.findall(issue["body"]):
                        links.add( (num, eval(n)) )
    return links

def find_labels(issues: dict) -> Dict[str, List[int]]:
    labels = {}
    for idx, issue in enumerate(issues):
        for lbl in issue["labels"]:
            if lbl not in labels:
                labels[lbl] = []
            labels[lbl].append(idx)
    return label

def id_to_idx(issues: dict) -> Dict[int,int]:
    '''get index of a issue from its GitHub ID'''
    ids = [issue["number"] for issue in issues]
    return { num: idx for idx, num in enumerate(ids) }

def load_issues(path: str) -> dict:
    with open(path, 'r') as file:
        issues = json.load(f)
    return issues

def content(issue: dict, use_comments=True) -> str:
    bodys = [issue["title"], issue["body"]]
    if use_comments:
        for comment in issue["comments"]:
            if not comment["isMinimized"]:
                bodys.append(comment["body"])
    return "\n\n".join(bodys)
