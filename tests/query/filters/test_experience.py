from nhlpy.api.query.filters.experience import ExperienceQuery


def test_is_rookie():
    experience = ExperienceQuery(is_rookie=True)
    assert experience.to_query() == "isRookie='1'"


def test_is_veteran():
    experience = ExperienceQuery(is_rookie=False)
    assert experience.to_query() == "isRookie='0'"
