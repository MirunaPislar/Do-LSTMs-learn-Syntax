
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


class TenseAgreementTerminals:
    def __init__(self):
        self.terminals = {
            "NP1_sg":
                ["Sam",
                 "The boy",
                 "Her father",
                 "A person in the audience",
                 "The guy we met yesterday on the bus",
                 "The boy with blue eyes that everyone admires",
                 "The inventor who was in the news",
                 "The ambassador known for some dirty businesses",
                 ],
            "NP2_sg":
                ["she",
                 "Jane",
                 "my friend Carl",
                 "every person in the room",
                 "everyone invited",
                 ],
            "NP1_pl":
                ["My parents",
                 "The students",
                 "The girls",
                 "All the women in New York",
                 "Some friends of my father-in-law",
                 "A few acquaintances born in a Western country",
                 "A dozen little girls with brown hair",
                 "The kids she sees every day at lunchtime",
                 ],
            "NP2_pl":
                ["they",
                 "their relatives",
                 "a few neighbours",
                 "some strangers on the street",
                 "the others",
                 ],
            "presBe_sg":
                ["is",
                 ],
            "presBe_pl":
                ["are",
                 ],
            "BE_action":
                ["angry",
                 "busy",
                 "away",
                 "unlikely to win the lottery",
                 "tired from running",
                 "sick of washing the dishes",
                 "very determined to read all the evolutionary biology books in the library",
                 "eager to start writing the homework on linear algebra",
                 ],
            "INFINITIVE_action":
                ["laugh",
                 "cheat",
                 "watch TV",
                 "get tired from running",
                 "think about the human condition",
                 "complain about life \'s misery",
                 "read all the evolutionary biology books in the library",
                 "write the homework on linear algebra",
                 ],
            "PAST_action":
                ["laughed",
                 "cheated",
                 "watched TV",
                 "got tired from running",
                 "thought about the human condition",
                 "complained about life \'s misery",
                 "read all the evolutionary biology books in the library",
                 "wrote the homework on linear algebra",
                 ],
            "HE":
                ["he",
                 ],
            "THEY":
                ["they",
                 ],
            "DID_past_sg":
                ["did",
                 ],
            "DID_past_pl":
                ["did",
                 ],
            "WILL_future_sg":
                ["will",
                 ],
            "WILL_future_pl":
                ["will",
                 ],
            "AND_aff":
                ["and so",
                 ],
            "AND_neg":
                ["and neither",
                 ],
            "AND":
                ["and",
                 ],
            "BUT":
                ["but",
                 ],
            "TOO":
                ["too",
                 ],
            "NOT":
                ["not",
                 ],
            "NT":
                ["n\'t",
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
