import argparse
parser = argparse.ArgumentParser(
    description = "Search for similar issues in a GitHub repository."
                  "Supply the issue ID and the repo with the `-R` flag.")
parser.add_argument("-R", dest="repo", required=True)
parser.add_argument("-L", dest="limit", default=8, type=int)
parser.add_argument("issue", type=int)

import os
import logging 
from .doc2vec import *
from .utils import *
from .gh import * 
from .__init__ import DATA_PATH 

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

if __name__ == "__main__":
    args = parser.parse_args()
    repo = args.repo

    repo_prefix = repo.replace('/','-')
    issue_path = os.path.join(DATA_PATH, f"{repo_prefix}-issues.json")
    vec_path = os.path.join(DATA_PATH,f"{repo_prefix}-vecs.pkl")

    if not os.path.exists(issue_path):
        logging.info("downloading issues")
        data = get_issues(repo, 1000)
        with open(issue_path, 'w') as f:
            f.write(data)
        del data

    with open(issue_path, 'r') as f:
        issues = json.load(f)

    if not os.path.exists(vec_path):
        logging.info("computing issue vectors") 

        docs = [ tokenize( content(issue) ) for issue in issues ]
        d2v = issue2vec(issues)
        logging.info("saving issue vectors")
        d2v.save(vec_path)
    else:
        d2v = Doc2Vec.load(vec_path)

    selected = None
    for issue in issues:
        if issue["number"] == args.issue:
            selected = issue 
    if selected is None:
        raise RuntimeError("issue not found")

    tokens = tokenize( content(selected) )
    vec = d2v.infer_vector(tokens)
    sims = d2v.dv.most_similar([vec], topn=args.limit)

    for i, score in sims:
        issue_id = issues[i]["number"]
        print(f"\t#{issue_id}: {score:.3f}")

