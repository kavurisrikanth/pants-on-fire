import os
import time

import pandas as pd

from general import candidates_path_2012, candidates_path_2016, candidates_path, get_fn, statements_path

from bs4 import BeautifulSoup
from requests import get

# ********************************************************
# Scraping candidate data


def scrape_candidates():
    scrape_candidates_2012()
    scrape_candidates_2016()
    scrape_candidates_2020()


def scrape_candidates_2012():
    if os.path.exists(candidates_path_2012):
        return

    df = pd.DataFrame(columns=['Name', 'Party', 'Title'])

    scrape_candidates_2012_mini(df, 'Barack Obama', '44th President of the United States', True)
    scrape_candidates_2012_mini(df, 'Joseph R. Biden Jr.', 'Former vice president; former senator from Delaware', True)

    scrape_candidates_2012_mini(df, 'Mitt Romney', '70th Governor of Massachusetts', False)
    scrape_candidates_2012_mini(df, 'Paul Ryan', 'U.S. Representative from Wisconsin', False)
    scrape_candidates_2012_mini(df, 'Ron Paul', 'U.S. Representative from Texas', False)
    scrape_candidates_2012_mini(df, 'Fred Karger', 'Political consultant and gay rights activist from California', False)
    scrape_candidates_2012_mini(df, 'Newt Gingrich', 'former U.S. Speaker of the House of Representatives, from Georgia', False)
    scrape_candidates_2012_mini(df, 'Rick Santorum', 'former senator from Pennsylvania', False)
    scrape_candidates_2012_mini(df, 'Buddy Roemer', 'former governor of Louisiana', False)
    scrape_candidates_2012_mini(df, 'Rick Perry', 'Governor of Texas', False)
    scrape_candidates_2012_mini(df, 'Jon Huntsman, Jr.', 'former U.S.ambassador to China and former governor of Utah', False)
    scrape_candidates_2012_mini(df, 'Michele Bachmann', 'U.S.Representative from Minnesota', False)
    scrape_candidates_2012_mini(df, 'Gary Johnson', 'former governor of New Mexico', False)
    scrape_candidates_2012_mini(df, 'Herman Cain', 'businessman from Georgia', False)
    scrape_candidates_2012_mini(df, 'Thaddeus McCotter', 'U.S.Representative from Michigan', False)
    scrape_candidates_2012_mini(df, 'Tim Pawlenty', 'former governor of Minnesota', False)

    df.to_csv(candidates_path_2012, index=False)


def scrape_candidates_2012_mini(df: pd.DataFrame, name: str, title: str, d: bool = True):
    party = 'Democrat' if d else 'Republican'
    df.loc[len(df)] = [name, party, title]


def scrape_candidates_2016():
    if os.path.exists(candidates_path_2016):
        return

    url = 'https://www.nytimes.com/interactive/2016/us/elections/2016-presidential-candidates.html'

    response = get(url)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    df = pd.DataFrame(columns=['Name', 'Party', 'Title'])

    # First, get the front-runners
    d = scrape_candidates_2016_mini(html_soup, True)
    df.loc[len(df)] = d

    d = scrape_candidates_2016_mini(html_soup, False)
    df.loc[len(df)] = d

    # Now examine the candidates who dropped out.
    dropouts = html_soup.find('div', {'class': 'g-timeline'})
    dropouts = dropouts.find_all('div', {'class': 'g-candidate'})
    for d in dropouts:
        profile = d.find('div', {'class': 'g-profile'})
        name = profile.find('h2', {'class': 'g-name'}).text
        name = ' '.join(name.split(' ')[:-1])
        party = profile.find('span', {'class': 'g-party'}).text
        party = 'Democrat' if party == 'd' else 'Republican'
        title = profile.find('div', {'class': 'g-title'}).text

        print('name: {}, party: {}, title: {}'.format(name, party, title))
        df.loc[len(df)] = [name, party, title]

    df.to_csv(candidates_path_2016, index=False)


def scrape_candidates_2016_mini(soup: BeautifulSoup, d: bool = True) -> list:
    c = 'g-democrats' if d else 'g-republicans'
    party = 'Democrat' if d else 'Republican'

    candidates = soup.find('div', {'class': c})
    frontrunner = candidates.find('div', {'class': 'g-running'})
    name = frontrunner.find('h3', {'class': 'g-name'}).text
    title = frontrunner.find('p', {'class': 'g-summary'}).text

    # dropped_out = []
    #
    # candidates = candidates.find('div', {'class': 'g-out'})
    # candidates = candidates.find_all('div', {'class': 'g-candidate'})
    # for c in candidates:
    #     dropped_out.append(c.find('h3', {'class': 'g-name'}).text)

    return [name, party, title]


def scrape_candidates_2020():
    """
    Get the list of candidates running for President. For the purposes of ease, we will only
    focus on candidates who have declared.
    :return: Nothing; the data is written to a CSV file.
    """

    if os.path.exists(candidates_path):
        return

    url = 'https://www.nytimes.com/interactive/2019/us/politics/2020-presidential-candidates.html'

    response = get(url)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    running = html_soup.find('div', class_='g-item g-running g-category')
    c_divs = running.find_all('div', class_='g-item g-cand')

    df = pd.DataFrame(columns=['Name', 'Age', 'Party', 'Title'])

    for c in c_divs:
        # Get name, age, party, title
        name, age = c.find('div', class_='g-name').text.split(', ')
        title = c.find('div', class_='g-title').text
        party = c.find('div', class_='g-small-note').text

        print('name: ' + str(name) + ', age: ' + str(age) + ', title: ' + str(title) + ', party: ' + str(party))

        df.loc[len(df)] = [name, age, party, title]

    df.to_csv(candidates_path, index=False)


# ********************************************************
# Scraping candidate statements from PolitiFact.


def get_statements_by_name(name: str) -> list:
    base_url = 'https://www.politifact.com'
    search_url = base_url + '/search/?q='

    # Get the name into the required format for search.
    altered_name = name.replace('.', '').replace(' ', '+')
    '''
    print()
    print('Original name: {}'.format(name))
    print('Final name: {}'.format(altered_name))
    print('URL: {}'.format(search_url + altered_name))
    '''

    # Do a GET.
    response = get(search_url + name)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # Get the list of names the search yields.
    people = html_soup.find('div', {'id': 'people'})

    # For now, assume that the search will yield results. We'll add methods for otherwise
    # later.
    if people is None:
        print('returning')
        return []

    # Find the first list item.
    likely = people.find('li')

    '''
    # The text being printed is the name of the candidate. Ideally, we would compare
    # this name to the name we're given and check if they are likely to be the same (how?)
    print(likely.find('span').text)
    print()
    '''

    # Get the URL we need to go to for statements.
    candidate_url = likely.find('a')
    if candidate_url is None:
        return []
    candidate_url = candidate_url['href']

    candidate_url = base_url + candidate_url + 'statements/by'
    # print('Target URL: {}'.format(candidate_url))

    return get_statements_from_url(candidate_url)


def get_statements_from_url(url: str) -> list:
    ans = []
    page = 2
    next_exists = True
    next_url = url

    while next_exists:
        response = get(next_url)
        html_soup = BeautifulSoup(response.text, 'html.parser')

        statements = html_soup.find_all('div', {'class': 'scoretable__item'})
        if statements is None:
            continue

        for s in statements:
            # get statement text
            text = s.find('p', {'class': 'statement__text'})
            if text is None:
                continue
            text = text.find('a', {'class': 'link'})
            if text is None:
                continue

            text = text.text
            text = text.replace('\n', '')
            # print('text: {}'.format(text))

            # Get statement truthiness
            verdict = s.find('div', {'class': 'meter'})
            if verdict is None:
                continue
            verdict = verdict.find('img')
            if verdict is None:
                continue

            verdict = verdict['alt']
            # print('verdict: {}'.format(verdict))

            # Get statement date
            date = s.find('p', {'class': 'statement__edition'})
            if date is None:
                continue

            date = date.find('span', {'class', 'article__meta'})
            if date is None:
                continue

            date = date.text
            if date is None:
                continue

            if date[:2] == 'on':
                # Remove the word "on"
                date = date[3:]

            date_split = date.split(', ', 1)
            if 'day' in date_split[0]:
                date = date_split[1]
            date_split = date.split(' ')
            date_split[1] = date_split[1][:-3]
            date = ' '.join(date_split)

            ans.append({
                'text': text,
                'verdict': verdict,
                'date': date
            })

        next_link = html_soup.find('a', {'class': 'step-links__next'})
        if next_link is None:
            next_exists = False
        else:
            next_url = url + '/?page=' + str(page)
            page += 1
            time.sleep(1)

    return ans


def get_statements_mini(candidate_names: list):
    for n in candidate_names:
        # print('***')

        fn = get_fn(n)
        filename = os.path.join(statements_path, fn + '.csv')
        if os.path.exists(filename):
            print('Scraping already done for {}. Skipping.'.format(n))
            continue

        print('Candidate name: {}'.format(n))
        statements = get_statements_by_name(n)
        df = pd.DataFrame(statements)

        df = df.replace({
            'True': 0,
            'No Flip': 0,
            'Mostly True': 1,
            'Half-True': 2,
            'Half Flip': 2,
            'Mostly False': 3,
            'False': 4,
            'Full Flop': 4,
            'Pants on Fire!': 5
        })
        df.to_csv(filename, index=False)

        # print('Name: {}'.format(n))
        # print(df.head())
        # print('***')
        print('Done')
        time.sleep(1.5)

# ********************************************************
# Putting it all together


def get_statements():
    scrape_candidates()

    print("Scraping candidates' statements")
    df_candidates = pd.read_csv(candidates_path, header=0)
    get_statements_mini(list(df_candidates['Name']))

    df_candidates = pd.read_csv(candidates_path_2012, header=0)
    get_statements_mini(list(df_candidates['Name']))

    df_candidates = pd.read_csv(candidates_path_2016, header=0)
    get_statements_mini(list(df_candidates['Name']))

    print('Statement scraping finished.')