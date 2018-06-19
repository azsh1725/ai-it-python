import requests
import pandas as pd
import re
import os
import sys

lang_test = sys.argv[1]
output_for_correct = "correct.txt"
output_for_wrong = "wrong.txt"
aibotbench_url = "http://ai2.aibotbench.com/ai"
rus_test = "pattern-matching-it-rus.txt"
eng_test = "pattern-matching-it.txt"
cols_for_test = ["quest", "answer"]

if lang_test == "en":
    df = pd.read_csv(eng_test, sep=";", header=None, names=cols_for_test)
    print("en")
elif lang_test == "ru":
    df = pd.read_csv(rus_test, sep=";", header=None, names=cols_for_test)
    print("ru")

correct = 0
wrong = 0

if os.path.exists(output_for_wrong):
    os.remove(output_for_wrong)

if os.path.exists(output_for_correct):
    os.remove(output_for_correct)

for index, row in df.iterrows():
    resp = requests.post(aibotbench_url, params={"lang": lang_test}, json={"text": row[cols_for_test[0]]}).json()
    resp = re.sub(u"\u0301", "", resp["text"])
    # print(resp)
    if len(re.findall(row[cols_for_test[1]].lower(), resp.lower())) >= 1:
        correct += 1
        with open(output_for_correct, "a", encoding="utf-8") as correct_out:
            correct_out.write("Question to ai: {}\n".format(row[cols_for_test[0]]))
            correct_out.write("ai answer: {}\n".format(resp.lower()))
            correct_out.write("pattern to match: {}\n".format(row[cols_for_test[1]]))
    else:
        wrong += 1
        with open(output_for_wrong, "a", encoding="utf-8") as wrong_out:
            wrong_out.write("Question to ai: {}\n".format(row[cols_for_test[0]]))
            wrong_out.write("ai answer: {}\n".format(resp.lower()))
            wrong_out.write("pattern to match: {}\n".format(row[cols_for_test[1]]))

print("Total number of questions: {}".format(df.shape[0]))
print("# of correct answers: {}".format(correct))
print("# of wrong answers: {}".format(wrong))
print("Success rate: {}%".format(round(correct / df.shape[0] * 100, 2)))
print("Failure rate: {}%".format(round(wrong / df.shape[0] * 100, 2)))
