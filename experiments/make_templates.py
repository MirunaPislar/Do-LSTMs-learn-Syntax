from templates import TenseAgreementTemplates, CoordinationTemplates
from terminals import TenseAgreementTerminals, CoordinationTerminals
import argparse
import os
import pandas as pd
import random

parser = argparse.ArgumentParser(
    description="Create targeted syntactic templates.")

parser.add_argument("--filename", type=str, default="data/my_template.tab",
                    help="Path where to save the templates.")
parser.add_argument("--type", type=str, default="tense",
                    help="Type of template to construct. "
                         "Choose between coord or tense.")
args = parser.parse_args()


class MakeAgreementTemplate:
    def __init__(self):
        if args.type == "coord":
            self.terminals = CoordinationTerminals().terminals
            self.rules = CoordinationTemplates().rules
        elif args.type == "tense":
            self.terminals = TenseAgreementTerminals().terminals
            self.rules = TenseAgreementTemplates().rules
        else:
            raise ValueError("Unknown template name %s. Please, choose"
                             " between coord or tense." % args.type)

    @staticmethod
    def switch_tense(words, preterms_idx):
        valid_verb_switches = {
            "presBe": {"sg": ["will", "did", "has"],
                       "pl": ["will", "did", "have"]},
            "past": {"sg": ["is", "was"],
                     "pl": ["are", "were"]},
            "future": {"sg": ["is"],
                       "pl": ["are"]}}

        new_words = []
        my_number = preterms_idx.split("_")[-1]
        my_tense = preterms_idx.split("_")[-2]
        valid_verbs = valid_verb_switches[my_tense][my_number]

        for word in words:
            splits = word.split()
            sampled_verb = random.choice(valid_verbs)
            if len(splits) > 1:
                new_words.append(" ".join(sampled_verb + splits[1:]))
            else:
                new_words.append(sampled_verb)
        return new_words

    @staticmethod
    def switch_number(words, preterms_idx):
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

    def make_variable_sentences(self, preterms, match):
        base_sent = [self.terminals[p] for p in preterms]
        grammatical = base_sent[:]
        ungrammatical = self.switch_numbers(grammatical, match[1], preterms)
        return [grammatical, ungrammatical]


class MakeTestCase:
    def __init__(self, template, test_case):
        self.template = template
        self.test_case = test_case
        self.sent_templates = self.get_rules()

    def get_rules(self):
        sent_templates = {"pattern": [], "sent": [], "sent_alt": []}
        preterminals, templates = self.template.rules[self.test_case]
        if templates is not None:
            sentences = self.template.make_variable_sentences(
                preterminals, templates["match"])
            grammatical = list(self.expand_sent(sentences[0]))
            ungrammatical = list(self.expand_sent(sentences[1]))
            for i in range(len(grammatical)):
                sent_templates["pattern"].append(self.test_case)
                sent_templates["sent"].append(grammatical[i])
                sent_templates["sent_alt"].append(ungrammatical[i])
        return sent_templates

    def expand_sent(self, sent, partial="", switch_ds=False):
        if len(sent) == 1:
            for word in sent[0]:
                if switch_ds:
                    splits = partial.split(" ")
                    no = splits[0]
                    the = splits[3]
                    splits = partial.split()
                    partial_one = " ".join([x for x in splits[1:3]])
                    partial_two = " ".join([x for x in splits[4:]])
                    yield " ".join([the, partial_one, no, partial_two, word])
                elif word not in partial:
                    yield partial + word
                else:
                    yield "None"
        else:
            for word in sent[0]:
                for x in self.expand_sent(
                        sent=sent[1:],
                        partial=partial + word + " ",
                        switch_ds=switch_ds):
                    if x != "None":
                        yield x


def main():
    if os.path.isfile(args.filename):
        os.remove(args.filename)

    test_cases = MakeAgreementTemplate()
    for case in test_cases.rules.keys():
        sentences = MakeTestCase(test_cases.rules, case)
        df = pd.DataFrame.from_dict(sentences.sent_templates)
        if os.path.isfile(args.filename):
            df.to_csv(
                args.filename, mode="a", header=False, index=False, sep="\t")
        else:
            df.to_csv(
                args.filename, mode="a", header=True, index=False, sep="\t")


if __name__ == "__main__":
    main()
