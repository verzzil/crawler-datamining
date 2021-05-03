import random
import re

import numpy as np

pages = []
di = {}
i = 0

with open('news.sportbox.ru.txt', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        splitted_data = re.split(r"(\d):", line)
        parent_page_url = splitted_data[0].rstrip()
        parent_page_id = int(splitted_data[1])
        parent_page_children_urls = splitted_data[2].split(", ")

        di.update(
            {
                parent_page_url: parent_page_children_urls
            }
        )

        if parent_page_url not in pages:
            pages.append(parent_page_url)

matrix_shape = len(pages)

probably_matrix = np.zeros(shape=(matrix_shape, matrix_shape), dtype=float)

i = 0
for parent, children in di.items():
    for child in children:
        try:
            probably_matrix[i][pages.index(child)] += 1 / len(children)
        except ValueError:
            probably_matrix[i][random.randint(0, matrix_shape - 1)] += 1 / len(children)
    i += 1

b = 0.85
v = np.full(shape=matrix_shape, fill_value=1 / matrix_shape, dtype=float)
e = np.ones(shape=matrix_shape)
const = ((1 - b) / matrix_shape) * e
probably_matrix = probably_matrix.T

for i in range(20):
    # if i == 19:
    #     print(v)
    v = probably_matrix.dot(v) * b + const

v.sort()
print("top 5:", v[-5: -1])
print("sum pageRank:", sum(v))
