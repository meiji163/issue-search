#!/usr/bin/env python
import argparse
parser = argparse.ArgumentParser(description = "fine tune SBERT on a repository's issues")
parser.add_argument("--repo","-R", dest="repo", required=True)
args = parser.parse_args()

import torch
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, evaluation, losses, util
from sentence_transformers.readers import InputExample
import json

from issim.utils import *  

if __name__ == "__main__":
    repo = args.repo
    data_path = "data/{}-issues.json".format(repo.replace('/','-'))
    with open(data_path,'r') as file:
        issues = json.load(file)

    dupls = find_duplicates(issues, repo)
    links = find_links(issues, repo)
    links.update(dupls)

    idx = id_to_idx(issues)

    samples = []
    eval1, eval2, eval_labels = [], [], []
    for id_tuple in links:
        try:
            id1, id2 = id_tuple
            issue1, issue2 = issues[ idx[id1] ], issues[ idx[id2] ] 
            body1, body2 = content(issue1), content(issue2)
            samples.append(InputExample(texts=[body1, body2], label=1))
            samples.append(InputExample(texts=[body2, body1], label=1))

            eval1.append(body1)
            eval2.append(body2)
            eval_labels.append(1)
        except KeyError as e:
            # issue not found
            continue

    bs = 16
    epochs = 4 

    #model_name = "all-MiniLM-L12-v2"
    model_name = "multi-qa-MiniLM-L6-cos-v1"

    model = SentenceTransformer(model_name)
    if torch.cuda.is_available():
        model.to("cuda")

    # add special tokens
    word_embedding = model._first_module()
    tokens = ["gh","pr","graphQL","ssh","WSL","CLI","repo","stdin","stderr","tty","amd64","arm64"]
    word_embedding.tokenizer.add_tokens(tokens, special_tokens=True)
    word_embedding.auto_model.resize_token_embeddings(len(word_embedding.tokenizer))

    dataloader = DataLoader(samples, shuffle=True, batch_size=bs)
    loss = losses.MultipleNegativesRankingLoss(model)
    evaluator = evaluation.BinaryClassificationEvaluator(eval1,eval2,eval_labels)

    model_path = "data/{}-model".format(repo.replace('/','-'))

    model.fit(
        train_objectives=[(dataloader, loss)],
        evaluator=evaluator,
        epochs=epochs,
        warmup_steps=1000,
        output_path=model_path,
    )

    evaluator(model, output_path=model_path) 
