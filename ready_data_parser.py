import re
import networkx as nx
import matplotlib.pyplot as plt

pages = []
set_pages = set()

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

        # current_page = Page(
        #     parent_page_url,
        #     parent_page_id,
        #     list(
        #         map(
        #             lambda child_url: Page(child_url, parent_page_id + 1),
        #             parent_page_children_urls
        #         )
        #     )
        # )
        #
        # pages.append(current_page)
        # if i == 10:
        #     break
        # i+=1


graph = nx.Graph()

for parent in di.keys():
    graph.add_node(parent)
for parent, children in di.items():
    for child in children:
        graph.add_edge(parent, child)
    print("checkpoint")

print("ready")

plt.figure(figsize=(100,100))
nx.draw(graph, font_weight='bold', node_size=13)
print("graph")
plt.show()
