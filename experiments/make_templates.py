from templates import CoordinationTemplates
from terminals import CoordinationTerminals
import pandas as pd
import os
import sys


class MakeAgreementTemplate:
    def __init__(self):
        self.terminals = CoordinationTerminals().terminals
        self.rules = CoordinationTemplates().rules

    def switch_number(self, words, preterms_idx):
        new_words = []
        is_verb = preterms_idx[-1] == "V"
        is_mod = len(preterms_idx) > 2 and preterms_idx[-3:] == "MOD"
        for word in words:
            if is_mod:
                splits = word.split()
                if len(splits) > 1:
                    if splits[0][-2:] == "es":
                        new_words.append(" ".join([splits[0][:-2]] + splits[1:]))
                    else:
                        new_words.append(" ".join([splits[0] + "es"] + splits[1:]))
                else:
                    if word[-2:] == "es":
                        new_words.append(word[:-2])
                    else:
                        new_words.append(word + "es")
            elif is_verb:
                splits = word.split()
                if len(splits) > 1:
                    if splits[0][-1] == "s":
                        new_words.append(" ".join([splits[0][:-1]] + splits[1:]))
                    else:
                        new_words.append(" ".join([splits[0] + "s"] + splits[1:]))
                else:
                    if word[-1] == "s":
                        new_words.append(word[:-1])
                    else:
                        new_words.append(word + "s")
            elif word[-4:] == "self":
                new_words.append("themselves")
            else:
                new_words.append(word + "s")
        return new_words

    def get_case_name(self, preterms, match, vary):
        sent = ""
        for j in range(len(match)):
            for i in range(len(match[j])):
                sent += preterms[match[j][i]] + "_"
        if len(vary) > 0:
            for j in range(len(vary)):
                sent += preterms[vary[j]] + "_"
        return sent[:-1]

    def switch_numbers(self, base_sent, variables, preterms):
        new_sent = base_sent[:]
        for idx in variables:
            new_sent[idx] = self.switch_number(new_sent[idx], preterms[idx])
        return new_sent

    def make_variable_sentences(self, preterms, match, vary):
        all_sentences = {}
        base_sent = [self.terminals[p] for p in preterms]
        grammatical = base_sent[:]
        ungrammatical = self.switch_numbers(grammatical, match[1], preterms)
        all_sentences[self.get_case_name(preterms, match, vary)] = [grammatical, ungrammatical]
        return all_sentences


class MakeTestCase:
    def __init__(self, template, test_case):
        self.template = template
        self.test_case = test_case
        self.sent_templates = self.get_rules()

    def get_rules(self):
        sent_templates = {"pattern": [], "sent": [],
                          "sent_alt": []}
        preterminals, templates = self.template.rules[self.test_case]
        if templates is not None:
            sentences = self.template.make_variable_sentences(
                preterminals, templates["match"], templates["vary"])
            for k in sentences.keys():
                gram = list(self.expand_sent(sentences[k][0]))
                ungram = list(self.expand_sent(sentences[k][1]))
                for i in range(len(gram)):
                    sent_templates["pattern"].append(self.test_case)
                    # sent_templates["case_name"].append(k)
                    sent_templates["sent"].append(gram[i])
                    sent_templates["sent_alt"].append(ungram[i])
        return sent_templates

    def expand_sent(self, sent, partial="", switch_ds=False):
        if len(sent) == 1:
            for word in sent[0]:
                if switch_ds:
                    sp = partial.split(" ")
                    no = sp[0]
                    the = sp[3]
                    new_partial_one = " ".join([x for x in partial.split()[1:3]])
                    new_partial_two = " ".join([x for x in partial.split()[4:]])
                    yield " ".join([the, new_partial_one, no, new_partial_two, word])
                elif word not in partial:
                    yield partial + word
                else:
                    yield "None"
        else:
            for word in sent[0]:
                for x in self.expand_sent(
                        sent=sent[1:], partial=partial + word + " ",
                        switch_ds=switch_ds):
                    if x != "None":
                        yield x


def main():
    if len(sys.argv) != 2:
        raise ValueError("ERROR: more than one argument provided!"
                         "Correct usage: python make_templates.py [filename]")
    filename = "data/" + sys.argv[1] + ".txt"
    if os.path.isfile(filename):
        os.remove(filename)

    argument_template = MakeAgreementTemplate()
    argument_test_cases = argument_template.rules.keys()

    for case in argument_test_cases:
        sentences = MakeTestCase(argument_template, case)
        df = pd.DataFrame.from_dict(sentences.sent_templates)
        if os.path.isfile(filename):
            df.to_csv(filename, mode="a", header=False, index=False, sep="\t")
        else:
            df.to_csv(filename, mode="a", index=False, sep="\t")


if __name__ == "__main__":
    main()
