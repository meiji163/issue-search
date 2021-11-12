# GitHub Issue Searcher
A (possibly overkill) algorithm to find similar issues in a GitHub repository with semantic search.  
This can be useful in a large repository for identifying duplicate or relevant issues.

## Dependencies 
- [GitHub CLI](https://github.com/cli/cli)
- python>=3.8
- [sentence_transformers](https://github.com/UKPLab/sentence-transformers)
- torch>=1.10

## Usage
Download your repo's issues and fine-tune the model
```
# example with cli/cli 
$ ./download.sh -R cli/cli 

# this takes a long time without a GPU!
$ ./train.py -R cli/cli
```

Now you can perform a query with an issue ID.   
(The first query computes embeddings of all issues and may take a while)
```
$ gh issue list -R cli/cli -L 3
Showing 3 of 390 open issues in cli/cli

#4715  Excuting "gh browse gh browse -c -R owner/repo" inside another repo workspace... 
#4713  gh cs: add ssh --config flag                                                                                              
#4712  consider add ability to follow job logs (trailing)                                                                        

$ ./issue-search -R cli/cli 4713
#4713  gh cs: add ssh --config flag
#2179  support .ssh/config Include directives
# 837  support SSH in `gh repo create`
#1720  Login using default SSH key
#4217  Support for SSH config file
#4124  ssh-key add to support multiple hosts
```

## TODO
- [ ] pipeline for adding new issues
- [ ] remove inference dependencies
    - ideally only need the embedding vectors
- [ ] package into a gh-extension
- [ ] support query for new issues
