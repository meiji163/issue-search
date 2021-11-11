from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, LoggingHandler, losses, util
from sentence_transformers.readers import InputExample
import json

from dataloader import *  

if __name__ == "__main__":
    with open("issues.json",'r') as file:
        issues = json.load(file)

    repo = "cli/cli"

    dupls = find_duplicates(issues, repo)
    lks = find_links(issues, repo)
    idx = id_to_idx(issues)

    samples = []
    for id_tuple in dupls + lks:
        try:
            id1, id2 = id_tuple
            issue1, issue2 = issues[ idx[id1] ], issues[ idx[id2] ] 
            body1, body2 = content(issue1), content(issue2)
            samples.append(InputExample(texts=[body1, body2], label=1))
            samples.append(InputExample(texts=[body2, body1], label=1))
        except KeyError as e:
            # issue not found
            continue

    bs = 4 
    epochs = 1 

    model = SentenceTransformer("stsb-distilbert-base")
    dataloader = DataLoader(samples, shuffle=True, batch_size=bs)
    loss = losses.MultipleNegativesRankingLoss(model)

    model.fit(
        train_objectives=[(dataloader, loss)],
        epochs=epochs,
        warmup_steps=1000,
        output_path="model_finetune",
    )

