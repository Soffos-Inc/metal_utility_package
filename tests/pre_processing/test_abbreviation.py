import typing as t
from unittest import TestCase

from metal.pre_processing.abbreviation import Abbreviation


class AbbreviationTests(TestCase):

    class TestData(t.NamedTuple):
        text: str
        known: t.List[str] = []
        unknown: t.List[str] = []

    def assert_abbreviations(self, *datas: TestData):
        for data in datas:
            known_abbreviations, unknown_abbreviations = Abbreviation.from_text(data.text)

            expected_known_abbreviations = []
            for known_abbreviation in data.known:
                index = data.text.index(known_abbreviation)
                expected_known_abbreviations.append(Abbreviation(
                    text=known_abbreviation,
                    span=(index, index + len(known_abbreviation))
                ))
            self.assertListEqual(known_abbreviations, expected_known_abbreviations)

            expected_unknown_abbreviations = []
            for unknown_abbreviation in data.unknown:
                index = data.text.index(unknown_abbreviation)
                expected_unknown_abbreviations.append(Abbreviation(
                    text=unknown_abbreviation,
                    span=(index, index + len(unknown_abbreviation))
                ))
            self.assertListEqual(unknown_abbreviations, expected_unknown_abbreviations)

    def test_from_text(self):
        text = 'Prof. John has a Ph.D. in computer science and is experienced in OOP.'
        known_abbreviations, unknown_abbreviations = Abbreviation.from_text(text)
        self.assertListEqual(known_abbreviations, [
            Abbreviation(text='Prof.', span=(0, 5)),
            Abbreviation(text='Ph.D.', span=(17, 22)),
        ])
        self.assertListEqual(unknown_abbreviations, [
            Abbreviation(text='OOP.', span=(65, 69))
        ])

    def test_from_text__known__mixed_periods(self):
        for text in ['Ph.D.', 'PhD.', 'PhD']:
            known_abbreviations, _ = Abbreviation.from_text(text)
            self.assertListEqual(known_abbreviations, [
                Abbreviation(text=text, span=(0, len(text)))
            ])

    def test_from_text__unkown__start_boundaries(self):
        self.assert_abbreviations(
            self.TestData(text='ABC blah blah.', unknown=['ABC']),  # start of paragraph.
            self.TestData(text='blah.\nABC blah.', unknown=['ABC']),  # start of new paragraph.
            self.TestData(text='blah. ABC blah.', unknown=['ABC']),  # start of sentence.
            self.TestData(text='blah.ABC blah.')  # invalid start of sentence.
        )

    def test_from_text__unkown__end_boundaries(self):
        self.assert_abbreviations(
            self.TestData(text='blah blah ABC', unknown=['ABC']),  # end of sentence: 0 punct.
            self.TestData(text='blah blah ABC.', unknown=['ABC.']),  # end of sentence: 1 punct.
            self.TestData(text='blah blah ABC..', unknown=['ABC.']),  # end of sentence: 2+ puncts.
            self.TestData(text='blah ABC. Blah', unknown=['ABC']),  # end + new sentence.
            self.TestData(text='blah ABC.Blah'),  # end + invalid new sentence.
            self.TestData(text='blah ABC. blah', unknown=['ABC.']),  # middle of sentence.
            self.TestData(text='blah ABC.blah')  # invalid in middle of sentence.
        )

    def test_from_text__unknown__mixed_casing(self):
        self.assert_abbreviations(
            self.TestData(text='ABC blah blah', unknown=['ABC']),  # all caps.
            self.TestData(text='AbC blah blah', unknown=['AbC']),  # start and end caps.
            self.TestData(text='aBC blah blah'),  # end caps.
            self.TestData(text='ABc blah blah'),  # start caps.
            self.TestData(text='abc blah blah')  # no caps.
        )

    def test_from_text__unknown__mixed_periods(self):
        self.assert_abbreviations(
            self.TestData(text='blah A.B.C. blah', unknown=['A.B.C.']),
            self.TestData(text='blah AB.C. blah', unknown=['AB.C.']),
            self.TestData(text='blah A.BC. blah', unknown=['A.BC.']),
            self.TestData(text='blah A.B.C blah', unknown=['A.B.C']),
            self.TestData(text='blah ABC. blah', unknown=['ABC.']),
            self.TestData(text='blah AB.C blah', unknown=['AB.C']),
            self.TestData(text='blah A.BC blah', unknown=['A.BC']),
            self.TestData(text='blah ABC blah', unknown=['ABC'])
        )
