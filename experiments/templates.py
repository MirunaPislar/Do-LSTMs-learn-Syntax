
class CoordinationTemplates:
    def __init__(self):
        self.rules = {
            "simple_2NPs_coord_aff":
                (["PropN1", "AND", "PropN2", "MV", "DOT"],
                 {"match": ([0, 2], [3])}),
            "simple_2NPs_coord_neg":
                (["PropN1", "AND", "PropN2", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2], [3])}),
            "simple_2NPs_coord_interr":
                (["INTERR_MOD", "PropN1_lower", "AND", "PropN2", "MV", "QUEST_MARK"],
                 {"match": ([1, 3], [0])}),

            "simple_3NPs_coord_aff":
                (["PropN1", "COMMA", "PropN2", "AND", "PropN3", "MV", "DOT"],
                 {"match": ([0, 2, 4], [5])}),
            "simple_3NPs_coord_neg":
                (["PropN1", "COMMA", "PropN2", "AND", "PropN3", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2, 4], [5])}),
            "simple_3NPs_coord_interr":
                (["INTERR_MOD", "PropN1_lower", "COMMA", "PropN2", "AND", "PropN3", "MV", "QUEST_MARK"],
                 {"match": ([1, 3, 5], [0])}),

            "first_expanded_2NPs_coord_aff":
                (["ExpNP", "AND", "PropN1_lower", "MV", "DOT"],
                 {"match": ([0, 2], [3])}),
            "first_expanded_2NPs_coord_neg":
                (["ExpNP", "AND", "PropN1_lower", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2], [3])}),
            "first_expanded_2NPs_coord_interr":
                (["INTERR_MOD", "ExpNP_lower", "AND", "PropN1_lower", "MV", "QUEST_MARK"],
                 {"match": ([1, 3], [0])}),

            "second_expanded_2NPs_coord_aff":
                (["PropN1", "AND", "ExpNP_lower", "MV", "DOT"],
                 {"match": ([0, 2], [3])}),
            "second_expanded_2NPs_coord_neg":
                (["PropN1", "AND", "ExpNP_lower", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2], [3])}),
            "second_expanded_2NPs_coord_interr":
                (["INTERR_MOD", "PropN1_lower", "AND", "ExpNP_lower", "MV", "QUEST_MARK"],
                 {"match": ([1, 3], [0])}),

            "both_expanded_2NPs_coord_aff":
                (["ExpNP", "AND", "ExpNP2", "MV", "DOT"],
                 {"match": ([0, 2], [3])}),
            "both_expanded_2NPs_coord_neg":
                (["ExpNP", "AND", "ExpNP2", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2], [3])}),
            "both_expanded_2NPs_coord_interr":
                (["INTERR_MOD", "ExpNP_lower", "AND", "ExpNP2", "MV", "QUEST_MARK"],
                 {"match": ([1, 3], [0])}),

            "first_expanded_3NPs_coord_aff":
                (["ExpNP", "COMMA", "PropN1_lower", "AND", "PropN3", "MV", "DOT"],
                 {"match": ([0, 2, 4], [5])}),
            "first_expanded_3NPs_coord_neg":
                (["ExpNP", "COMMA", "PropN1_lower", "AND", "PropN3", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2, 4], [5])}),
            "first_expanded_3NPs_coord_interr":
                (["INTERR_MOD", "ExpNP_lower", "COMMA", "PropN1_lower", "AND", "PropN3", "MV", "QUEST_MARK"],
                 {"match": ([1, 3, 5], [0])}),

            "last_expanded_3NPs_coord_aff":
                (["PropN1", "COMMA", "PropN3", "AND", "ExpNP_lower", "MV", "DOT"],
                 {"match": ([0, 2, 4], [5])}),
            "last_expanded_3NPs_coord_neg":
                (["PropN1", "COMMA", "PropN3", "AND", "ExpNP_lower", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2, 4], [5])}),
            "last_expanded_3NPs_coord_interr":
                (["INTERR_MOD", "PropN1_lower", "COMMA", "PropN3", "AND", "ExpNP_lower", "MV", "QUEST_MARK"],
                 {"match": ([1, 3, 5], [0])}),

            "both_expanded_3NPs_coord_aff":
                (["ExpNP", "COMMA", "ExpNP2", "AND", "PropN3", "MV", "DOT"],
                 {"match": ([0, 2, 4], [5])}),
            "both_expanded_3NPs_coord_neg":
                (["ExpNP", "COMMA", "ExpNP2", "AND", "PropN3", "NEG_MOD", "MV", "DOT"],
                 {"match": ([0, 2, 4], [5])}),
            "both_expanded_3NPs_coord_interr":
                (["INTERR_MOD", "ExpNP_lower", "COMMA", "ExpNP2", "AND", "PropN3", "MV", "QUEST_MARK"],
                 {"match": ([1, 3, 5], [0])}),
        }


class TenseAgreementTemplates:
    def __init__(self):
        self.rules = {

            # Present tense agreement AFFIRMATIVE with the main verb BE.
            # e.g. Sam is angry , and Fred is too . <eos>
            "tense_agr_presBe_sg_sg_aff":
                (["NP1_sg", "presBe_sg", "BE_action", "COMMA", "AND", "NP2_sg", "presBe_sg", "TOO", "DOT"],
                 {"match": ([5], [6])}),
            "tense_agr_presBe_sg_pl_aff":
                (["NP1_sg", "presBe_sg", "BE_action", "COMMA", "AND", "NP2_pl", "presBe_pl", "TOO", "DOT"],
                 {"match": ([5], [6])}),
            "tense_agr_presBe_pl_sg_aff":
                (["NP1_pl", "presBe_pl", "BE_action", "COMMA", "AND", "NP2_sg", "presBe_sg", "TOO", "DOT"],
                 {"match": ([5], [6])}),
            "tense_agr_presBe_pl_pl_aff":
                (["NP1_pl", "presBe_pl", "BE_action", "COMMA", "AND", "NP2_pl", "presBe_pl", "TOO", "DOT"],
                 {"match": ([5], [6])}),

            # Present tense agreement NEGATIVE with the main verb BE.
            # e.g. Sam is not angry , but Fred is . <eos>
            "tense_agr_presBe_sg_sg_1neg":
                (["NP1_sg", "presBe_sg", "NOT", "BE_action", "COMMA", "BUT", "NP2_sg", "presBe_sg", "DOT"],
                 {"match": ([6], [7])}),
            "tense_agr_presBe_sg_pl_1neg":
                (["NP1_sg", "presBe_sg", "NOT", "BE_action", "COMMA", "BUT", "NP2_pl", "presBe_pl", "DOT"],
                 {"match": ([6], [7])}),
            "tense_agr_presBe_pl_sg_1neg":
                (["NP1_pl", "presBe_pl", "NOT", "BE_action", "COMMA", "BUT", "NP2_sg", "presBe_sg", "DOT"],
                 {"match": ([6], [7])}),
            "tense_agr_presBe_pl_pl_1neg":
                (["NP1_pl", "presBe_pl", "NOT", "BE_action", "COMMA", "BUT", "NP2_pl", "presBe_pl", "DOT"],
                 {"match": ([6], [7])}),

            # Present tense agreement NEGATIVE with the main verb BE.
            # e.g. Sam is angry , but Fred is not . <eos>
            "tense_agr_presBe_sg_sg_2neg":
                (["NP1_sg", "presBe_sg", "BE_action", "COMMA", "BUT", "NP2_sg", "presBe_sg", "NOT", "DOT"],
                 {"match": ([5], [6])}),
            "tense_agr_presBe_sg_pl_2neg":
                (["NP1_sg", "presBe_sg", "BE_action", "COMMA", "BUT", "NP2_pl", "presBe_pl", "NOT", "DOT"],
                 {"match": ([5], [6])}),
            "tense_agr_presBe_pl_sg_2neg":
                (["NP1_pl", "presBe_pl", "BE_action", "COMMA", "BUT", "NP2_sg", "presBe_sg", "NOT", "DOT"],
                 {"match": ([5], [6])}),
            "tense_agr_presBe_pl_pl_2neg":
                (["NP1_pl", "presBe_pl", "BE_action", "COMMA", "BUT", "NP2_pl", "presBe_pl", "NOT", "DOT"],
                 {"match": ([5], [6])}),

            # Past tense agreement AFFIRMATIVE.
            # e.g. Sam laughed , and Fred did too . <eos>
            "tense_agr_past_sg_sg_aff":
                (["NP1_sg", "PAST_action", "COMMA", "AND", "NP2_sg", "DID_past_sg", "TOO", "DOT"],
                 {"match": ([4], [5])}),
            "tense_agr_past_sg_pl_aff":
                (["NP1_sg", "PAST_action", "COMMA", "AND", "NP2_pl", "DID_past_pl", "TOO", "DOT"],
                 {"match": ([4], [5])}),
            "tense_agr_past_pl_sg_aff":
                (["NP1_pl", "PAST_action", "COMMA", "AND", "NP2_sg", "DID_past_sg", "TOO", "DOT"],
                 {"match": ([4], [5])}),
            "tense_agr_past_pl_pl_aff":
                (["NP1_pl", "PAST_action", "COMMA", "AND", "NP2_pl", "DID_past_pl", "TOO", "DOT"],
                 {"match": ([4], [5])}),

            # Past tense agreement NEGATIVE.
            # e.g. Sam did not laugh , but Fred did . <eos>
            "tense_agr_past_sg_sg_neg":
                (["NP1_sg", "DID_past_sg", "NOT", "INFINITIVE_action", "COMMA", "BUT", "NP2_sg", "DID_past_sg", "DOT"],
                 {"match": ([6], [7])}),
            "tense_agr_past_sg_pl_neg":
                (["NP1_sg", "DID_past_sg", "NOT", "INFINITIVE_action", "COMMA", "BUT", "NP2_pl", "DID_past_pl", "DOT"],
                 {"match": ([6], [7])}),
            "tense_agr_past_pl_sg_neg":
                (["NP1_pl", "DID_past_pl", "NOT", "INFINITIVE_action", "COMMA", "BUT", "NP2_sg", "DID_past_sg", "DOT"],
                 {"match": ([6], [7])}),
            "tense_agr_past_pl_pl_neg":
                (["NP1_pl", "DID_past_pl", "NOT", "INFINITIVE_action", "COMMA", "BUT", "NP2_pl", "DID_past_pl", "DOT"],
                 {"match": ([6], [7])}),

            # Future tense agreement AFFIRMATIVE.
            # e.g. Sam will laugh , and Fred will too . <eos>
            "tense_agr_future_sg_sg_aff":
                (["NP1_sg", "WILL_future_sg", "INFINITIVE_action", "COMMA", "AND", "NP2_sg", "WILL_future_sg", "TOO", "DOT"],
                 {"match": ([5], [6])}),
            "tense_agr_future_sg_pl_aff":
                (["NP1_sg", "WILL_future_sg", "INFINITIVE_action", "COMMA", "AND", "NP2_pl", "WILL_future_pl", "TOO", "DOT"],
                 {"match": ([5], [6])}),
            "tense_agr_future_pl_sg_aff":
                (["NP1_pl", "WILL_future_pl", "INFINITIVE_action", "COMMA", "AND", "NP2_sg", "WILL_future_sg", "TOO", "DOT"],
                 {"match": ([5], [6])}),
            "tense_agr_future_pl_pl_aff":
                (["NP1_pl", "WILL_future_pl", "INFINITIVE_action", "COMMA", "AND", "NP2_pl", "WILL_future_pl", "TOO", "DOT"],
                 {"match": ([5], [6])}),

            # Future tense agreement NEGATIVE.
            # e.g. Sam will not laugh , but Fred will . <eos>
            "tense_agr_future_sg_sg_neg":
                (["NP1_sg", "WILL_future_sg", "NOT", "INFINITIVE_action", "COMMA", "BUT", "NP2_sg", "WILL_future_sg", "DOT"],
                 {"match": ([6], [7])}),
            "tense_agr_future_sg_pl_neg":
                (["NP1_sg", "WILL_future_sg", "NOT", "INFINITIVE_action", "COMMA", "BUT", "NP2_pl", "WILL_future_pl", "DOT"],
                 {"match": ([6], [7])}),
            "tense_agr_future_pl_sg_neg":
                (["NP1_pl", "WILL_future_pl", "NOT", "INFINITIVE_action", "COMMA", "BUT", "NP2_sg", "WILL_future_sg", "DOT"],
                 {"match": ([6], [7])}),
            "tense_agr_future_pl_pl_neg":
                (["NP1_pl", "WILL_future_pl", "NOT", "INFINITIVE_action", "COMMA", "BUT", "NP2_pl", "WILL_future_pl", "DOT"],
                 {"match": ([6], [7])}),

            # Present tense agreement AFFIRMATIVE with the main verb BE and INVERSION.
            # e.g. Sam is angry , and so is Fred . <eos>
            "tense_agr_with_inv_presBe_sg_sg_aff":
                (["NP1_sg", "presBe_sg", "BE_action", "COMMA", "AND_aff", "presBe_sg", "NP2_sg", "DOT"],
                 {"match": ([6], [5])}),
            "tense_agr_with_inv_presBe_sg_pl_aff":
                (["NP1_sg", "presBe_sg", "BE_action", "COMMA", "AND_aff", "presBe_pl", "NP2_pl", "DOT"],
                 {"match": ([6], [5])}),
            "tense_agr_with_inv_presBe_pl_sg_aff":
                (["NP1_pl", "presBe_pl", "BE_action", "COMMA", "AND_aff", "presBe_sg", "NP2_sg", "DOT"],
                 {"match": ([6], [5])}),
            "tense_agr_with_inv_presBe_pl_pl_aff":
                (["NP1_pl", "presBe_pl", "BE_action", "COMMA", "AND_aff", "presBe_pl", "NP2_pl", "DOT"],
                 {"match": ([6], [5])}),

            # Present tense agreement NEGATIVE with the main verb BE and INVERSION.
            # e.g. Sam is not angry , and neither is Fred . <eos>
            "tense_agr_with_inv_presBe_sg_sg_neg":
                (["NP1_sg", "presBe_sg", "NOT", "BE_action", "COMMA", "AND_neg", "presBe_sg", "NP2_sg", "DOT"],
                 {"match": ([7], [6])}),
            "tense_agr_with_inv_presBe_sg_pl_neg":
                (["NP1_sg", "presBe_sg", "NOT", "BE_action", "COMMA", "AND_neg", "presBe_pl", "NP2_pl", "DOT"],
                 {"match": ([7], [6])}),
            "tense_agr_with_inv_presBe_pl_sg_neg":
                (["NP1_pl", "presBe_pl", "NOT", "BE_action", "COMMA", "AND_neg", "presBe_sg", "NP2_sg", "DOT"],
                 {"match": ([7], [6])}),
            "tense_agr_with_inv_presBe_pl_pl_neg":
                (["NP1_pl", "presBe_pl", "NOT", "BE_action", "COMMA", "AND_neg", "presBe_pl", "NP2_pl", "DOT"],
                 {"match": ([7], [6])}),

            # Past tense agreement AFFIRMATIVE with INVERSION.
            # e.g. Sam laughed , and so did Fred . <eos>
            "tense_agr_with_inv_past_sg_sg_aff":
                (["NP1_sg", "PAST_action", "COMMA", "AND_aff", "DID_past_sg", "NP2_sg", "DOT"],
                 {"match": ([5], [4])}),
            "tense_agr_with_inv_past_sg_pl_aff":
                (["NP1_sg", "PAST_action", "COMMA", "AND_aff", "DID_past_pl", "NP2_pl", "DOT"],
                 {"match": ([5], [4])}),
            "tense_agr_with_inv_past_pl_sg_aff":
                (["NP1_pl", "PAST_action", "COMMA", "AND_aff", "DID_past_sg", "NP2_sg", "DOT"],
                 {"match": ([5], [4])}),
            "tense_agr_with_inv_past_pl_pl_aff":
                (["NP1_pl", "PAST_action", "COMMA", "AND_aff", "DID_past_pl", "NP2_pl", "DOT"],
                 {"match": ([5], [4])}),

            # Past tense agreement NEGATIVE with INVERSION.
            # e.g. Sam did not laugh , and neither did Fred . <eos>
            "tense_agr_with_inv_past_sg_sg_neg":
                (["NP1_sg", "DID_past_sg", "NOT", "INFINITIVE_action", "COMMA", "AND_neg", "DID_past_sg", "NP2_sg", "DOT"],
                 {"match": ([7], [6])}),
            "tense_agr_with_inv_past_sg_pl_neg":
                (["NP1_sg", "DID_past_sg", "NOT", "INFINITIVE_action", "COMMA", "AND_neg", "DID_past_pl", "NP2_pl", "DOT"],
                 {"match": ([7], [6])}),
            "tense_agr_with_inv_past_pl_sg_neg":
                (["NP1_pl", "DID_past_pl", "NOT", "INFINITIVE_action", "COMMA", "AND_neg", "DID_past_sg", "NP2_sg", "DOT"],
                 {"match": ([7], [6])}),
            "tense_agr_with_inv_past_pl_pl_neg":
                (["NP1_pl", "DID_past_pl", "NOT", "INFINITIVE_action", "COMMA", "AND_neg", "DID_past_pl", "NP2_pl", "DOT"],
                 {"match": ([7], [6])}),

            # Future tense agreement AFFIRMATIVE with INVERSION.
            # e.g. Sam will laugh , and so will Fred . <eos>
            "tense_agr_with_inv_future_sg_sg_aff":
                (["NP1_sg", "WILL_future_sg", "INFINITIVE_action", "COMMA", "AND_aff", "WILL_future_sg", "NP2_sg", "DOT"],
                 {"match": ([6], [5])}),
            "tense_agr_with_inv_future_sg_pl_aff":
                (["NP1_sg", "WILL_future_sg", "INFINITIVE_action", "COMMA", "AND_aff", "WILL_future_pl", "NP2_pl", "DOT"],
                 {"match": ([6], [5])}),
            "tense_agr_with_inv_future_pl_sg_aff":
                (["NP1_pl", "WILL_future_pl", "INFINITIVE_action", "COMMA", "AND_aff", "WILL_future_sg", "NP2_sg", "DOT"],
                 {"match": ([6], [5])}),
            "tense_agr_with_inv_future_pl_pl_aff":
                (["NP1_pl", "WILL_future_pl", "INFINITIVE_action", "COMMA", "AND_aff", "WILL_future_pl", "NP2_pl", "DOT"],
                 {"match": ([6], [5])}),

            # Future tense agreement NEGATIVE with INVERSION.
            # e.g. Sam did not laugh , and neither did Fred . <eos>
            "tense_agr_with_inv_future_sg_sg_neg":
                (["NP1_sg", "WILL_future_sg", "NOT", "INFINITIVE_action", "COMMA", "AND_neg", "WILL_future_sg", "NP2_sg", "DOT"],
                 {"match": ([7], [6])}),
            "tense_agr_with_inv_future_sg_pl_neg":
                (["NP1_sg", "WILL_future_sg", "NOT", "INFINITIVE_action", "COMMA", "AND_neg", "WILL_future_pl", "NP2_pl", "DOT"],
                 {"match": ([7], [6])}),
            "tense_agr_with_inv_future_pl_sg_neg":
                (["NP1_pl", "WILL_future_pl", "NOT", "INFINITIVE_action", "COMMA", "AND_neg", "WILL_future_sg", "NP2_sg", "DOT"],
                 {"match": ([7], [6])}),
            "tense_agr_with_inv_future_pl_pl_neg":
                (["NP1_pl", "WILL_future_pl", "NOT", "INFINITIVE_action", "COMMA", "AND_neg", "WILL_future_pl", "NP2_pl", "DOT"],
                 {"match": ([7], [6])}),

            # Present tense agreement AFFIRMATIVE with the main verb BE.
            # e.g. Sam is angry , is n't he ? <eos>
            "tense_agr_tags_presBe_sg_aff":
                (["NP1_sg", "presBe_sg", "BE_action", "COMMA", "presBe_sg", "NT", "HE", "QUEST_MARK"],
                 {"match": ([0], [4])}),
            "tense_agr_tags_presBe_pl_aff":
                (["NP1_pl", "presBe_pl", "BE_action", "COMMA", "presBe_pl", "NT", "THEY", "QUEST_MARK"],
                 {"match": ([0], [4])}),

            # Present tense agreement NEGATIVE with the main verb BE.
            # e.g. Sam is n't angry , is he ? <eos>
            "tense_agr_tags_presBe_sg_neg":
                (["NP1_sg", "presBe_sg", "NT", "BE_action", "COMMA", "presBe_sg", "HE", "QUEST_MARK"],
                 {"match": ([0], [5])}),
            "tense_agr_tags_presBe_pl_neg":
                (["NP1_pl", "presBe_pl", "NT", "BE_action", "COMMA", "presBe_pl", "THEY", "QUEST_MARK"],
                 {"match": ([0], [5])}),

            # Past tense agreement AFFIRMATIVE.
            # e.g. Sam laughed , did n't he ? <eos>
            "tense_agr_tags_past_sg_aff":
                (["NP1_sg", "PAST_action", "COMMA", "DID_past_sg", "NT", "HE", "QUEST_MARK"],
                 {"match": ([0], [3])}),
            "tense_agr_tags_past_pl_aff":
                (["NP1_pl", "PAST_action", "COMMA", "DID_past_pl", "NT", "THEY", "QUEST_MARK"],
                 {"match": ([0], [3])}),

            # Past tense agreement NEGATIVE.
            # e.g. Sam did n't laugh , did he ? <eos>
            "tense_agr_tags_past_sg_neg":
                (["NP1_sg", "DID_past_sg", "NT", "INFINITIVE_action", "COMMA", "DID_past_sg", "HE", "QUEST_MARK"],
                 {"match": ([0], [5])}),
            "tense_agr_tags_past_pl_neg":
                (["NP1_pl", "DID_past_pl", "NT", "INFINITIVE_action", "COMMA", "DID_past_pl", "THEY", "QUEST_MARK"],
                 {"match": ([0], [5])}),

            # Future tense agreement AFFIRMATIVE.
            # e.g. Sam will laugh , will n't he ? <eos>
            "tense_agr_tags_future_sg_aff":
                (["NP1_sg", "WILL_future_sg", "INFINITIVE_action", "COMMA", "WILL_future_sg", "NT", "HE", "QUEST_MARK"],
                 {"match": ([0], [4])}),
            "tense_agr_tags_future_pl_aff":
                (["NP1_pl", "WILL_future_pl", "INFINITIVE_action", "COMMA", "WILL_future_pl", "NT", "THEY", "QUEST_MARK"],
                 {"match": ([0], [4])}),

            # Future tense agreement NEGATIVE.
            # e.g. Sam will n't laugh , will he ? <eos>
            "tense_agr_tags_future_sg_neg":
                (["NP1_sg", "WILL_future_sg", "NT", "INFINITIVE_action", "COMMA", "WILL_future_sg", "HE", "QUEST_MARK"],
                 {"match": ([0], [5])}),
            "tense_agr_tags_future_pl_neg":
                (["NP1_pl", "WILL_future_pl", "NT", "INFINITIVE_action", "COMMA", "WILL_future_pl", "THEY", "QUEST_MARK"],
                 {"match": ([0], [5])}),
        }
