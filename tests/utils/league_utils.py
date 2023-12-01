from app.domain.model.league import League


def build_league(id="L001", name="LN001", races=[], ranking=[], runners=[]):
    return League(
        id=id,
        name=name,
        races=races,
        ranking=ranking,
        participants=runners
        )
