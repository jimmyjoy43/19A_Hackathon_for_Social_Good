import re

with open ('output_got.csv', 'r' ) as f:
    content = f.read()
content_new = re.sub(';\s', r'-', content, flags = re.M)

output_file = open("output_got_mod.csv", "w")

output_file.write(content_new)