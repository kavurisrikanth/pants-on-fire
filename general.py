import datetime
import os

cwd = os.path.join(os.getcwd(), 'data')
candidates_path = os.path.join(cwd, 'candidates.csv')
candidates_path_2012 = os.path.join(cwd, 'candidates_2012.csv')
candidates_path_2016 = os.path.join(cwd, 'candidates_2016.csv')
statements_path = os.path.join(cwd, 'statements')


def fact_check():
    if not os.path.exists(candidates_path):
        raise ModuleNotFoundError('File {} does not exist.'.format(candidates_path))

    p = Politifact()
    obama = p.statements().people('Barack Obama')

    for line in obama:
        print(line)
        print(line.ruling)


def alter_name(name: str) -> str:
    # Take care of cases like Beto O'Rourke
    # and convert name to lowercase.
    name = name.lower().replace("'", '')

    # Split by space
    pieces = name.split(' ')

    # Return the name in the Politifact URL format.
    ans = '-'.join(pieces)
    return ans


def get_datetime(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, '%B %d %Y')


def get_fn(n: str) -> str:
    return n.replace('.', '').replace(',', '').replace(' ', '_')