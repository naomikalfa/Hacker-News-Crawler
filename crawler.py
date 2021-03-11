from bs4 import BeautifulSoup
from colorama import Fore
import requests

ROOT_URL = 'https://news.ycombinator.com/'
HN_LINK_URL = 'https://news.ycombinator.com/item?id='


def fetch_page(url, greater_than):

    high_comment_articles = []

    page = requests.get(url)
    articles = page.content

    soup = BeautifulSoup(articles, 'html.parser')

    titles = soup.find_all('tr', class_='athing')
    subtext_list = soup.find_all('td', class_='subtext')
    links = soup.find_all('a', 'href', class_='storylink')
    hn_links = soup.find_all('tr', class_='athing')

    for title, subtext, link, hn_link in zip(titles, subtext_list, links, hn_links):

        string_soup = subtext.text
        strained_soup = string_soup.split('|')
        finer_sieve = strained_soup[-1]
        comments_soup = finer_sieve.split()
        comments_strained = comments_soup[0]

        link_soup = link
        link_string_soup = str(link_soup)
        strained_links = link_string_soup.split('href=')
        fine_links = strained_links[1]
        finer_links = fine_links.split('>')
        finest_links = finer_links[0]

        refined_links = finest_links.replace('"', '')

        hn_link_soup = hn_link['id']
        hn_link_strained = HN_LINK_URL + hn_link_soup

        def scrub_integers(strained_comments):

            strained_comments = strained_comments.replace('discuss', '').replace('hide', '').replace(' ', '')

            if strained_comments == '':
                strained_comments = '0'

            return strained_comments

        clean = scrub_integers(comments_strained)
        int_stripped_and_strained = int(clean)
        fresh_comment_soup = int_stripped_and_strained

        if fresh_comment_soup > greater_than:
            high_comment_articles.append([title.text, refined_links, hn_link_strained, fresh_comment_soup])

    return high_comment_articles


greater_than = 100
pages_to_search = 30
stack = []

for i in range(pages_to_search):
    stack.extend(fetch_page(ROOT_URL + '/news?p=' + str(i), greater_than))

for article in stack:
    print(Fore.LIGHTBLUE_EX + article[0])
    print(Fore.BLUE + '    ' + article[1])
    print(Fore.CYAN + '    ' + article[2])
    print(Fore.YELLOW + '    ' + 'comments:', article[3], '\n')
    
print(Fore.RED + '∴ We searched through', pages_to_search, 'pages on', Fore.LIGHTRED_EX + 'HN & sifted through',
      pages_to_search * 30, Fore.LIGHTMAGENTA_EX + 'links & found a total', Fore.MAGENTA + 'of', len(stack),
      'articles with >', Fore.BLUE + str(greater_than), 'comments - - Happy reading! ∴', '\n')
