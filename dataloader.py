import json
import re

def find_duplicates(issues):
    dupl_re = re.compile(r"[dD]uplicate [oO]f #*(\d+)")
    dupl_url_re = re.compile(r"[dD]uplicate [oO]f https://github.com/cli/cli/issues/(\d+)")

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

if __name__ == "__main__":
    with open("issues.json",'r') as file:
        data = json.load(file)

    dupls = find_duplicates(data)
