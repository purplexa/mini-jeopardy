import unittest
import datetime

from ..jservice import Clue, Category, JService

# TODO: don't rely on the public api since it could change


class ClueTestCase(unittest.TestCase):
    sample_clue = {
        'id': 616,
        'answer': 'Diane Keaton',
        'question': "Though this actress' cat is named for Buster Keaton, she's really no relation",
        'value': 300,
        'airdate': '1984-09-14T12:00:00.000Z',
        'created_at': '2014-02-11T22:47:34.721Z',
        'updated_at': '2014-02-11T22:47:34.721Z',
        'category_id': 11,
        'game_id': None,
        'invalid_count': None,
        'category': {
            'id': 11,
            'title': 'trivia',
            'created_at': '2014-02-11T22:47:19.531Z',
            'updated_at': '2014-02-11T22:47:19.531Z',
            'clues_count': 50
        }
    }

    def test_from_response(self):
        clue = Clue.from_response(ClueTestCase.sample_clue)
        self.assertIsInstance(clue, Clue)
        self.assertEqual(getattr(clue, 'cid', None),
                         ClueTestCase.sample_clue['id'])
        for attribute in ['answer', 'question', 'value', 'airdate', 'category_id', 'game_id', 'invalid_count']:
            self.assertEqual(getattr(clue, attribute, None),
                             ClueTestCase.sample_clue[attribute])

    def test_is_final_jeopardy(self):
        clue_false = Clue.from_response(ClueTestCase.sample_clue)
        self.assertFalse(clue_false.is_final_jeopardy())
        clue_true = Clue.from_response(
            dict(ClueTestCase.sample_clue, value=None))
        self.assertTrue(clue_true.is_final_jeopardy())


class CategoryTestCase(unittest.TestCase):
    sample_category = {
        "id": 11531,
        "title": "mixed bag",
        "clues_count": 5
    }

    def test_from_response(self):
        category = Category.from_response(CategoryTestCase.sample_category)
        self.assertEqual(getattr(category, 'cid', None),
                         CategoryTestCase.sample_category['id'])
        for attribute in ['title', 'clues_count']:
            self.assertEqual(getattr(category, attribute, None),
                             CategoryTestCase.sample_category[attribute])

    @unittest.skip('unimplemented')
    def test_get_clues(self):
        pass


class JServiceTestCase(unittest.TestCase):
    sample_category = {
        "id": 11531,
        "title": "mixed bag",
        "clues_count": 5
    }

    def test_clues(self):
        jservice = JService('http://jservice.io/api')
        min_date = datetime.datetime(year=2009, month=1, day=1)
        max_date = datetime.datetime(year=2009, month=12, day=31)
        category_id = JServiceTestCase.sample_category['id']
        clues = jservice.clues(
            min_date=min_date, max_date=max_date, category=category_id)
        for clue in clues:
            airdate = datetime.datetime.fromisoformat(clue.airdate.rstrip('Z'))
            self.assertGreaterEqual(airdate, min_date)
            self.assertLessEqual(airdate, max_date)
            self.assertEqual(clue.category.cid, category_id)

    @unittest.skip('unimplemented')
    def test_random(self):
        pass

    def test_categories(self):
        jservice = JService('http://jservice.io/api')
        categories1 = jservice.categories(count=3)
        self.assertEqual(len(categories1), 3)
        for category in categories1:
            self.assertIsInstance(category, Category)
        categories2 = jservice.categories(count=1, offset=3)
        self.assertEqual(len(categories2), 1)
        category = categories2[0]
        self.assertIsInstance(category, Category)
        categories1_ids = [c.cid for c in categories1]
        self.assertNotIn(category.cid, categories1_ids)

    @unittest.skip('unimplemented')
    def test_category(self):
        pass

    def test_find_category_by_title(self):
        jservice = JService('http://jservice.io/api')
        category = jservice.find_category_by_title(
            JServiceTestCase.sample_category['title'])
        self.assertIsInstance(category, Category)
        self.assertEqual(category.cid, JServiceTestCase.sample_category['id'])
        self.assertEqual(
            category.title, JServiceTestCase.sample_category['title'])
        self.assertEqual(category.clues_count,
                         JServiceTestCase.sample_category['clues_count'])

    def test_get_n_clues(self):
        jservice = JService('http://jservice.io/api')
        clues1 = jservice.get_n_clues(n=3, final_jeopardy=True)
        self.assertEqual(len(clues1), 3)
        for clue in clues1:
            self.assertIsNone(clue.value)
        clues2 = jservice.get_n_clues(
            n=2, final_jeopardy=False, category=JServiceTestCase.sample_category['title'])
        self.assertEqual(len(clues2), 2)
        for clue in clues2:
            self.assertIsNotNone(clue.value)
            self.assertEqual(clue.category.cid,
                             JServiceTestCase.sample_category['id'])
