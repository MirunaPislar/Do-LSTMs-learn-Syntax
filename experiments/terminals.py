
class CoordinationTerminals:
    def __init__(self):
        self.terminals = {
            "PropN1":
                ["Sam",
                 "Jane",
                 "The girl",
                 "A woman",
                 "This woman",
                 ],
            "PropN1_lower":
                ["Sam",
                 "Jane",
                 "the girl",
                 "a woman",
                 "this woman",
                 ],
            "PropN2":
                ["Tom",
                 "Sarah",
                 "the boy",
                 "a man",
                 "this man",
                 ],
            "PropN3":
                ["a pupil",
                 "my uncle",
                 "John",
                 ],
            "ExpNP":
                ["Her teacher 's son",
                 "A complete stranger",
                 "The rich man she loves",
                 "The boy she sees on television every Tuesday",
                 "The guy who works for her company",
                 "Tom ( the captain of the basketball team )",
                 "Sarah ( the French lady living on the third floor )",
                 ],
            "ExpNP_lower":
                ["her teacher 's son",
                 "a complete stranger",
                 "the rich man she loves",
                 "the boy she sees on television every Tuesday",
                 "the guy who works for her company",
                 "Tom ( the captain of the basketball team )",
                 "Sarah ( the French lady living on the third floor )",
                 ],
            "ExpNP2":
                ["one of his best friends",
                 "the girl who cooks the best soup in this town",
                 "the woman wearing a bracelet on her right wrist",
                 "Bill ( a cousin who recently returned from Africa )",
                 ],
            "AND":
                ["and",
                 ],
            "NEG_MOD":
                ["do not",
                 ],
            "INTERR_MOD":
                ["Do",
                 ],
            "MV":
                ["take dancing classes",
                 "like fishing",
                 "eat dinner with some friends",
                 "drink a beer in the pub tonight",
                 "love animals with fur",
                 "find it difficult to concentrate",
                 ],
            "obv_MV":
                ["take dancing classes together",
                 "share 50 friends on Facebook",
                 "eat dinner with some common friends",
                 "get along very well",
                 "get back together",
                 "know each other since 2010",
                 ],
            "DOT":
                [". <eos>",
                 ],
            "QUEST_MARK":
                ["? <eos>",
                 ],
            "COMMA":
                [",",
                 ],
        }
