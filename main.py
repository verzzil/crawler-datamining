import requests
from bs4 import BeautifulSoup


class Page:
    def __init__(self, url: str):
        self.url: str = url
        self.child_pages = []

    def __eq__(self, other):
        if other.url == self.url:
            return True
        return False

    def __hash__(self):
        return self.url.__hash__()

    def add_children(self, page):
        self.child_pages.append(page)

    def get_str_children(self):
        return ', '.join(map(lambda page: page.url, self.child_pages))


class Crawler:
    def __init__(self, url_init_page: str):
        self.pages = [Page(url_init_page)]
        self.html_of_init_page = requests.get(url_init_page)

    def start(self):
        for page in self.pages:
            if len(self.pages) > 4:
                return True
            self.__get_all_links_from_page(page)
        return False

    def write_to_file(self):
        with open("data.txt", "w", encoding="utf-8") as file:
            for page in self.pages:
                file.write(str(page.url) + "\t" + page.get_str_children() + "\n")

    def __get_all_links_from_page(self, page: Page):
        request = requests.get(page.url).text
        soup = BeautifulSoup(request, 'html.parser')
        for link in soup.findAll('a'):
            if 'href' in link.attrs:

                if '#' in link.attrs['href'] or \
                        'javascript:void' in link.attrs['href']:
                    continue

                if not link.attrs['href'].startswith('http'):
                    new_page = Page(page.url[:len(page.url) - 1] + link.attrs['href'])
                    page.add_children(new_page)
                    self.pages.append(new_page)
                else:
                    new_page = Page(link.attrs['href'])
                    page.add_children(new_page)
                    self.pages.append(new_page)


if __name__ == '__main__':
    crawler = Crawler('https://keddr.com/novosti1/')
    crawler.start()

    crawler.write_to_file()
