from app.rules.rule_engine import RuleEngine


class ValidationAgent:

    def __init__(self):
        self.rule_engine = RuleEngine()

    def validate(self, authorization, retrieved_rules):
        payer_rules_text = "\n\n".join(
            rule["document"]
            for rule in retrieved_rules
        )

        result = self.rule_engine.validate(
            authorization,
            payer_rules_text
        )

        return result