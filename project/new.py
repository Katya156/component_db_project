import re
x = 'Д26.72х42.5'
print(bool(re.search('.+х', x)))