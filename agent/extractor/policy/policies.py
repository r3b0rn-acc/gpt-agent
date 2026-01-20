from agent.extractor.policy.base import Policy, PolicyTarget, PolicyItems


class ExcludeHiddenPolicy(Policy):
    def apply(self, target: PolicyTarget, items: PolicyItems) -> PolicyItems:
        if target != "inputs":
            return items
        return [item for item in items if item.input_type != "hidden"]


class HrefNecessaryPolicy(Policy):
    def apply(self, target: PolicyTarget, items: PolicyItems) -> PolicyItems:
        if target != "links":
            return items
        return [item for item in items if item.href]


__all__ = ["ExcludeHiddenPolicy", "HrefNecessaryPolicy"]
