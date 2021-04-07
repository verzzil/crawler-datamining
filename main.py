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
            if len(self.pages) > 1000:
                return True
            self.__get_all_links_from_page(page)
        return False

    def start_with_nesting(self):
        counter = 0
        for page in self.pages:
            self.__get_all_links_from_page(page)
            for sub_page in page.child_pages:
                self.__get_all_links_from_page(sub_page)
                # for sub_sub_page in sub_page.child_pages:
                #     self.__get_all_links_from_page(sub_sub_page)
            self.write_to_file()
            counter += 1
            print(counter)
        return False

    def write_to_file(self):
        with open("data.txt", "w", encoding="utf-8") as file:
            for page in self.pages:
                file.write(page.url + "\nCHILDREN: " + page.get_str_children() + "\n\n\n ------------------------\n")

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
    crawler = Crawler('https://keddr.com/')
    crawler.start_with_nesting()

    crawler.write_to_file()

    data = crawler.get_dict_from_pages()

    print(data)
