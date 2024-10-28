# checks links in markdown files and prints results
# results are temp stored so the user can decide to implement them or not
import re

test_link = "[test](https://test.com)"

# grab github readme string
readme_link = re.compile(r'\[(.*?)\)')
print(readme_link.match(test_link))