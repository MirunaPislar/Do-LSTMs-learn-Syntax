
class CoordinationTemplates:
    def __init__(self):
        self.rules = {
            "simple_2NPs_coord_pos":
                (["PropN1", "AND", "PropN2", "MV", "DOT"],
                 {"match": ([0, 2], [3]), "vary": []}),
            "simple_2NPs_coord_neg":
                (["PropN1", "AND", "PropN2", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2], [3]), "vary": []}),
            "simple_2NPs_coord_interr":
                (["INTERR_MOD", "PropN1_lower", "AND", "PropN2", "MV", "QUEST_MARK"], 
                 {"match": ([1, 3], [0]), "vary": []}),


            "simple_3NPs_coord_pos":
                (["PropN1", "COMMA", "PropN2", "AND", "PropN3", "MV", "DOT"],
                 {"match": ([0, 1, 3], [4]), "vary": []}),
            "simple_3NPs_coord_neg":
                (["PropN1", "COMMA", "PropN2", "AND", "PropN3", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 1, 3], [4]), "vary": []}),
            "simple_3NPs_coord_interr":
                (["INTERR_MOD", "PropN1_lower", "COMMA", "PropN2", "AND", "PropN3", "MV", "QUEST_MARK"],
                 {"match": ([1, 2, 4], [0]), "vary": []}),


            "first_expanded_2NPs_coord_pos":
                (["ExpNP", "AND", "PropN1", "MV", "DOT"],
                 {"match": ([0, 2], [3]), "vary": []}),
            "first_expanded_2NPs_coord_neg":
                (["ExpNP", "AND", "PropN1", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2], [3]), "vary": []}),
            "first_expanded_2NPs_coord_interr":
                (["INTERR_MOD", "ExpNP_lower", "AND", "PropN1", "MV", "QUEST_MARK"],
                 {"match": ([1, 3], [0]), "vary": []}),


            "second_expanded_2NPs_coord_pos":
                (["PropN1", "AND", "ExpNP_lower", "MV", "DOT"],
                 {"match": ([0, 2], [3]), "vary": []}),
            "second_expanded_2NPs_coord_neg":
                (["PropN1", "AND", "ExpNP_lower", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2], [3]), "vary": []}),
            "second_expanded_2NPs_coord_interr":
                (["INTERR_MOD", "PropN1_lower", "AND", "ExpNP_lower", "MV", "QUEST_MARK"],
                 {"match": ([1, 3], [0]), "vary": []}),


            "both_expanded_2NPs_coord_pos":
                (["ExpNP", "AND", "ExpNP2", "MV", "DOT"],
                 {"match": ([0, 2], [3]), "vary": []}),
            "both_expanded_2NPs_coord_neg":
                (["ExpNP", "AND", "ExpNP2", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2], [3]), "vary": []}),
            "both_expanded_2NPs_coord_interr":
                (["INTERR_MOD", "ExpNP_lower", "AND", "ExpNP2", "MV", "QUEST_MARK"],
                 {"match": ([1, 3], [0]), "vary": []}),


            "first_expanded_3NPs_coord_pos":
                (["ExpNP", "COMMA", "PropN1", "AND", "PropN3", "MV", "DOT"],
                 {"match": ([0, 1, 3], [4]), "vary": []}),
            "first_expanded_3NPs_coord_neg":
                (["ExpNP", "COMMA", "PropN1", "AND", "PropN3", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 1, 3], [4]), "vary": []}),
            "first_expanded_3NPs_coord_interr":
                (["INTERR_MOD", "ExpNP_lower", "COMMA", "PropN1", "AND", "PropN3", "MV", "QUEST_MARK"],
                 {"match": ([1, 2, 4], [0]), "vary": []}),


            "last_expanded_3NPs_coord_pos":
                (["PropN1", "COMMA", "PropN3", "AND", "ExpNP_lower", "MV", "DOT"],
                 {"match": ([0, 1, 3], [4]), "vary": []}),
            "last_expanded_3NPs_coord_neg":
                (["PropN1", "COMMA", "PropN3", "AND", "ExpNP_lower", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 1, 3], [4]), "vary": []}),
            "last_expanded_3NPs_coord_interr":
                (["INTERR_MOD", "PropN1_lower", "COMMA", "PropN3", "AND", "ExpNP_lower", "MV", "QUEST_MARK"],
                 {"match": ([1, 2, 4], [0]), "vary": []}),


            "both_expanded_3NPs_coord_pos":
                (["ExpNP", "COMMA", "ExpNP2", "AND", "PropN3", "MV", "DOT"],
                 {"match": ([0, 1, 3], [4]), "vary": []}),
            "both_expanded_3NPs_coord_neg":
                (["ExpNP", "COMMA", "ExpNP2", "AND", "PropN3", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 1, 3], [4]), "vary": []}),
            "both_expanded_3NPs_coord_interr":
                (["INTERR_MOD", "ExpNP_lower", "COMMA", "ExpNP2", "AND", "PropN3", "MV", "QUEST_MARK"],
                 {"match": ([1, 2, 4], [0]), "vary": []}),
        }
