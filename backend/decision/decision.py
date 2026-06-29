from planning.planning import create_plan


def make_decision(message: str) -> str:
    """Decision layer for RIKAA Core.

    Flow: Planning → Decision → Return

    Currently a pass-through that returns the original message.
    Future implementations will add validation and routing logic
    here without modifying core, routes, or services.
    """
    planned = create_plan(message)
    return planned