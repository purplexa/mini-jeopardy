# TODO: add docstrings
# TODO: implement

class JService:

    def __init__(self, endpoint):
        pass

    def clues(self, value, category, min_date, max_date):
        pass

    def random(self, count):
        pass

    def categories(self, count):
        pass

    def category(self, id):
        pass

    def find_category_by_title(self, title):
        pass

    def get_n_clues(self, n, final_jeopardy, **filters):
        pass


class Category:

    def __init__(self, cid, title, clues_count):
        self.id = cid
        self.title = title
        self.clues_count = clues_count

    def get_clues(self, jservice):
        pass


class Clue:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.answer = kwargs['answer']
        self.question = kwargs['question']
        self.value = kwargs['value']
        self.airdate = kwargs['airdate']
        self.category_id = kwargs['category_id']
        self.game_id = kwargs['game_id']
        self.invalid_count = kwargs['invalid_count']
        self.category = kwargs['category']

    def is_final_jeopardy(self):
        self.value == None

    
