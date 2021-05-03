import re

import requests
from bs4 import BeautifulSoup


class Page:
    def __init__(self, url: str, id: int, children=[]):
        self.url: str = url
        self.child_pages = children
        self.id = id

    def __eq__(self, other):
        return other.url == self.url

    def __hash__(self):
        return self.url.__hash__()

    def __str__(self):
        return "url: " + url + " id: " + id

    def add_children(self, page):
        self.child_pages.append(page)

    def get_str_children(self):
        return ', '.join(map(lambda page: page.url, self.child_pages))


class Crawler:
    def __init__(self, url_init_page: str):
        self.init_page = Page(url_init_page, 1)
        self.pages = [self.init_page]

        self.set_of_pages = set()
        self.set_of_pages.add(url_init_page)
        self.url = url_init_page

    def write_to_file(self):
        with open(self.url[8:-1] + ".txt", "w", encoding="utf-8") as file:
            for page in self.pages:
                if len(page.child_pages) != 0:
                    file.write(
                        page.url + " " + str(page.id) + ":" + page.get_str_children() + "\n")

    def start(self):
        for page in self.pages:
            if page.id == 4:
                return True
            self.__get_all_links_from_page_with_nesting(page)
        return False

    def __get_all_links_from_page_with_nesting(self, page: Page):
        try:
            request = requests.get(page.url).text
            soup = BeautifulSoup(request, 'html.parser')
        except Exception:
            return
        for link in soup.findAll('a'):
            if 'href' in link.attrs:

                if '#' in link.attrs['href'] or \
                        'javascript:void' in link.attrs['href'] or \
                        re.match(r'\S*[^/]*\.[^./]*$', link.attrs['href']):
                    continue

                if not link.attrs['href'].startswith('http'):
                    if link.attrs['href'].startswith('//'):
                        new_page = Page("https://" + link.attrs['href'][2:], page.id + 1)
                    else:
                        new_page = Page(page.url[:len(page.url) - 1] + link.attrs['href'], page.id + 1)
                    page.add_children(new_page)
                else:
                    new_page = Page(link.attrs['href'], page.id + 1)
                    page.add_children(new_page)

                if not new_page.url in self.set_of_pages:
                    self.pages.append(new_page)
                    self.set_of_pages.add(new_page.url)

            self.write_to_file()

    def get_dict_from_pages(self):
        result = {}
        for page in self.pages:
            if result.get(page.url) is None:
                result.update(
                    {
                        page.url: list(
                            map(lambda pg: pg.url, page.child_pages)
                        )
                    }
                )
        return result


if __name__ == '__main__':
    url = input()
    crawler = Crawler(url)
    print(crawler.start())

    crawler.write_to_file()

    # data = crawler.get_dict_from_pages()
    #
    # print(data)
