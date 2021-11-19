from sklearn.linear_model import SGDClassifier
import numpy as np

import os
import json
import logging 
from .doc2vec import *
from .utils import *
from .gh import * 
from .__init__ import DATA_PATH 

logging.basicConfig(format='%(asctime)s - %(message)s',

if __name__ == "__main__":
    repo_prefix = repo.replace('/','-')
    issue_path = os.path.join(DATA_PATH, f"{repo_prefix}-issues.json")
    vec_path = os.path.join(DATA_PATH,f"{repo_prefix}-vecs.pkl")

    with open(issue_path, 'w') as f:
        issues = json.load(f)
    idx = id_to_idx(issues)

    # classify bug label
    bugs = []
    for i, issue in enumerate(issues):
    for l in issues["labels"]:
        if l["name"] == "bug":
            bugs.append(i)

    clf = SGDClassifier(random_state=0, max_iter=1000, tol=1e-3)
    clf.fit(x_train, y_train)

