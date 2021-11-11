import json
import re
from collections import defaultdict
from typing import List, Dict, Tuple, Set

def find_duplicates(issues: dict, repo: str) -> List[Tuple[int,int]]: 
    dupl_re = re.compile(r"[dD]uplicate [oO]f #*(\d+)")
    url = r"https://github.com/" + repo + "/issues/"
    dupl_url_re = re.compile(f"[dD]uplicate [oO]f {url}(\d+)")

    duplicates = []
    for issue in issues:
        m1 = dupl_re.search(issue["body"])
        num = issue["number"]
        if m1:
            duplicates.append( (num, eval(m1.group(1))) )
            continue
        for comment in issue["comments"]:
            if not comment["isMinimized"]:
                m1 = dupl_re.search(comment["body"])
                m2 = dupl_url_re.search(comment["body"])
                if m1:
                    duplicates.append( (num, eval(m1.group(1))) )
                    break
                elif m2:
                    duplicates.append( (num, eval(m2.group(1))) )
                    break
    return duplicates

# note: these overlap with found duplicates
def find_links(issues: dict, repo: str) -> List[Tuple[int,int]]:
    url = r"https://github.com/" + repo + "/issues/"
    url_re = re.compile(f"{url}(\d+)")

    links = defaultdict(set)
    for issue in issues:
        num = issue["number"]
        m = url_re.search(issue["body"])
        if m:
            for n in url_re.findall(issue["body"]):
                links[num].add( eval(n) )
        for comment in issue["comments"]:
            if not comment["isMinimized"]:
                m = url_re.search(comment["body"])
                if m:
                    for n in url_re.findall(issue["body"]):
                        links[num].add( eval(n) )
    pairs = []
    for iss1 in links:
        for iss2 in links[iss1]:
            pairs.append( (iss1, iss2) )
    return pairs


def id_to_idx(issues: dict) -> Dict[int,int]:
    '''get index of a issue from its GitHub ID'''
    ids = [issue["number"] for issue in issues]
    return { num: idx for idx, num in enumerate(ids) }

def content(issue: dict) -> str:
    bodys = [issue["title"], issue["body"]]
    for comment in issue["comments"]:
        if not comment["isMinimized"]:
            bodys.append(comment["body"])
    return "\n\n".join(bodys)

