from typing import List

import requests

# TODO: add docstrings
# TODO: implement

class Clue:

    def __init__(self, **kwargs):
        self.cid = kwargs['cid']
        self.answer = kwargs['answer']
        self.question = kwargs['question']
        self.value = kwargs['value']
        self.airdate = kwargs['airdate']
        self.category_id = kwargs['category_id']
        self.game_id = kwargs['game_id']
        self.invalid_count = kwargs['invalid_count']
        self.category = kwargs['category']

    @classmethod
    def from_response(cls, decoded_json):
        decoded_json['cid'] = decoded_json.pop('id', None)
        decoded_json['category'] = Category.from_response(decoded_json['category'])
        return cls(**decoded_json)

    def is_final_jeopardy(self) -> bool:
        self.value == None


class Category:

    def __init__(self, cid, title, clues_count):
        self.cid = cid
        self.title = title
        self.clues_count = clues_count

    @classmethod
    def from_response(cls, decoded_json):
        decoded_json['cid'] = decoded_json.pop('id', None)
        decoded_json = { k: v for k, v in decoded_json.items() if k in ['cid', 'title', 'clues_count']}
        return cls(**decoded_json)

    def get_clues(self, jservice) -> List[Clue]:
        pass


class JService:

    def __init__(self, endpoint):
        self.endpoint = endpoint.rstrip('/')

    def clues(self, value=None, category=None, min_date=None, max_date=None, offset=None) -> List[Clue]:
        # TODO: param validation
        params = dict(value=value, category=category, min_date=min_date, max_date=max_date, offset=offset)
        params = { k: v for k, v in params.items() if v is not None }
        r = requests.get(self._url('clues'), params=params)
        if r.status_code != requests.codes.ok:
            raise requests.exceptions.RequestException()
        # TODO: validate response
        return [Clue.from_response(x) for x in r.json()]

    def random(self, count) -> Clue:
        # TODO: implement
        pass

    def categories(self, count=100, offset=0) -> List[Category]:
        # TODO: validate count
        params = dict(count=count, offset=offset)
        r = requests.get(self._url('categories'), params=params)
        if r.status_code != requests.codes.ok:
            raise requests.exceptions.RequestException()
        # TODO: validate response
        return [Category.from_response(x) for x in r.json()]

    def category(self, cid) -> Category:
        # TODO: implement
        pass

    def find_category_by_title(self, title) -> Category:
        offset = 0
        while True:
            categories = self.categories(count=100, offset=offset)
            if not categories:
                return None
            for category in categories:
                if category.title and category.title.casefold() == title.casefold():
                    return category
            offset = offset + 100


    def get_n_clues(self, n, final_jeopardy=None, **filters) -> List[Clue]:
        category_id = None
        clues = []
        offset = 0
        if 'category' in filters:
            if isinstance(filters['category'], str) and not filters['category'].isdigit():
                category = self.find_category_by_title(filters.pop('category'))
                category_id = category.cid if category is not None else None
            else:
                category_id = filters.pop('category')
        while True:
            new_clues = self.clues(category=category_id, **filters)
            offset = offset + len(new_clues)

            if not new_clues:
                return None
            if final_jeopardy is True:
                new_clues = [clue for clue in new_clues if clue.value is None]
            if final_jeopardy is False:
                new_clues = [clue for clue in new_clues if clue.value is not None]

            clues.extend(new_clues)
            if len(clues) >= n:
                return clues[0:n]

    def _url(self, route) -> str:
        return '{}/{}'.format(self.endpoint, route)
