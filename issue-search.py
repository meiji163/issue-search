import json
import os
import pickle 
import logging

import argparse
parser = argparse.ArgumentParser(
    description = "Search for similar issues in a GitHub repository. Supply the issue ID and the repo with the `-R` flag.")
#parser.add_argument("--model","-m", dest="model")
parser.add_argument("-R", dest="repo", required=True)
parser.add_argument("issue", type=int)
args = parser.parse_args()

from sentence_transformers import SentenceTransformer, util, LoggingHandler
import torch
from dataloader import id_to_idx

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])

if __name__ == "__main__":
    repo = args.repo
    embedding_path = "./data/{}-embd.pkl".format(repo.replace('/','-'))
    issue_path = "./data/{}-issues.json".format(repo.replace('/','-'))
    with open(issue_path,'r') as f:
        issues = json.load(f)
    idx = id_to_idx(issues)

    if os.path.exists(embedding_path):
        logging.info("Load embeddings")
        with open(embedding_path, 'rb') as f:
            data = pickle.load(f)
            ids = data["ids"]
            embeddings = data["embeddings"]
    else:
        logging.info("Compute embeddings")
        model_path = "./data/{}-model".format(repo.replace('/','-'))
        model = SentenceTransformer(model_path)

        ids = [issue["number"] for issue in issues]
        embeddings = model.encode(issues, convert_to_tensor=True)
        with open(embedding_path, 'wb') as f: 
            pickle.dump({ "ids": ids, "embeddings": embeddings}, f)

    try:
        query = embeddings[ idx[args.issue] ]
    except KeyError:
        raise ValueError(f"Issue #{args.issue} not found")
    
    cos_sims = util.pytorch_cos_sim(query, embeddings)[0]
    top = torch.topk(cos_sims, k=10)

    for score, i in zip(top[0], top[1]):
        id = issues[i]["number"]
        title = issues[i]["title"]
        print(f"\033[32m#{id:>4}\033[0m {title}")
