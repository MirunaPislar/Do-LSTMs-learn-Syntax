from templates import TenseAgreementTemplates, CoordinationTemplates
from terminals import TenseAgreementTerminals, CoordinationTerminals
import argparse
import os
import random
import pandas as pd

parser = argparse.ArgumentParser(
    description="Create targeted syntactic templates.")

parser.add_argument("--filename", type=str, default="data/my_template.tab",
                    help="Name of the file in which to save the templates.")
parser.add_argument("--type", type=str, default="tense",
                    help="Type of template to construct. Choose from: "
                         "[coord, tense].")
# parser.add_argument("--seed", type=int, default=1121,
#                    help="Value of the random seed.")
args = parser.parse_args()


class MakeAgreementTemplate:
    def __init__(self):
        if args.type == "coord":
            self.terminals = CoordinationTerminals().terminals
            self.rules = CoordinationTemplates().rules
        elif args.type == "tense":
            self.terminals = TenseAgreementTerminals().terminals
            self.rules = TenseAgreementTemplates().rules
        self.verbs_of_tense = {
            "presBe": ["is", "are"],
            "pres": ["does", "do"],
            "presCont": ["has", "have"],
            "future": ["will"],
            "past": ["did", "had"],
            "pastCont": ["was", "were"]}
        self.verbs_of_number = {
            "sg": ["is", "was", "does", "did", "has", "will", "had"],
            "pl": ["are", "were", "do", "did", "have", "will", "had"]}

    def switch_tense(self, words, preterms_idx):
        new_words = []
        my_number = preterms_idx.split("_")[-1]
        my_tense = preterms_idx.split("_")[-2]

        possible_verbs = self.verbs_of_number[my_number]
        valid_verbs = []
        for tense, verbs in self.verbs_of_tense.items():
            if tense == my_tense:
                continue
            for verb in verbs:
                if verb in possible_verbs:
                    valid_verbs.append(verb)
        random.shuffle(valid_verbs)
        for word in words:
            splits = word.split()
            sampled_verb = random.choice(valid_verbs)
            if len(splits) > 1:
                new_words.append(" ".join(sampled_verb + splits[1:]))
            else:
                new_words.append(sampled_verb)
        return new_words

    def switch_number(self, words, preterms_idx):
        new_words = []
        is_verb = preterms_idx[-1] == "V"
        is_mod = len(preterms_idx) > 2 and preterms_idx[-3:] == "MOD"
        for word in words:
            splits = word.split()
            if splits[0] == "is":
                new_words.append(" ".join(["are"] + splits[1:]))
            elif splits[0] == "are":
                new_words.append(" ".join(["is"] + splits[1:]))
            elif splits[0] == "was":
                new_words.append(" ".join(["were"] + splits[1:]))
            elif splits[0] == "were":
                new_words.append(" ".join(["was"] + splits[1:]))
            elif splits[0] == "has":
                new_words.append(" ".join(["have"] + splits[1:]))
            elif splits[0] == "have":
                new_words.append(" ".join(["has"] + splits[1:]))
            elif is_mod:
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
            if args.type == "coord":
                new_sent[idx] = self.switch_number(new_sent[idx], preterms[idx])
            elif args.type == "tense":
                new_sent[idx] = self.switch_tense(new_sent[idx], preterms[idx])
            else:
                raise ValueError("Unknown value for template type: %s."
                                 "Choose between tense and coord." % args.type)
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
    if os.path.isfile(args.filename):
        os.remove(args.filename)

    argument_template = MakeAgreementTemplate()
    argument_test_cases = argument_template.rules.keys()\

    for case in argument_test_cases:
        sentences = MakeTestCase(argument_template, case)
        df = pd.DataFrame.from_dict(sentences.sent_templates)
        if os.path.isfile(args.filename):
            df.to_csv(args.filename, mode="a", header=False,
                      index=False, sep="\t")
        else:
            df.to_csv(args.filename, mode="a", index=False, sep="\t")


if __name__ == "__main__":
    main()
