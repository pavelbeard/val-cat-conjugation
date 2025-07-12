from api.schemas.verbs import VerbConjugation, VerbMode, VerbOut


fake_data = VerbOut(
    _id="test_id",
    infinitive="test",
    translation="test",
    conjugation=[
        VerbMode(
            tense="test_tense",
            conjugation=[
                VerbConjugation(
                    pronoun="p1",
                    forms=["f1"],
                    variation_types=None,
                    translation="f1",
                ),
                VerbConjugation(
                    pronoun="p2",
                    forms=["f2"],
                    variation_types=None,
                    translation="f2",
                ),
            ],
        ),
        VerbMode(
            tense="another_tense",
            conjugation=[
                VerbConjugation(
                    pronoun="p1",
                    forms=["f3"],
                    variation_types=None,
                    translation="f3",
                ),
                VerbConjugation(
                    pronoun="p2",
                    forms=["f4"],
                    variation_types=None,
                    translation="f4",
                ),
            ],
        ),
    ],
    created_at="2023-10-01T00:00:00Z",
)
