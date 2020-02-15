import datetime

from lib.jservice import JService

# TODO: support command line options

def run():
    jservice = JService('http://www.jservice.io/api')
    min_date = datetime.datetime(year=1996, month=1, day=1)
    max_date = datetime.datetime(year=1996, month=12, day=31)
    category_name='science'
    clues = jservice.get_n_clues(n=5, final_jeopardy=False, min_date=min_date, max_date=max_date, category=category_name)
    clues.sort(key=lambda x: x.value)
    # TODO: handle bad data
    for clue in clues:
        print('Point Value: {:>4d}'.format(clue.value))
        print('Question: {}\n'.format(clue.question))

run()