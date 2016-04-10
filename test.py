import re
import mysql.connector

TEST = '			<$META_LINK$> '
print (TEST + '\n\n')

TEST = re.sub('^(\s*)<\$META_LINK\$>.*$','\g<1><link href="" rel="canonical">\n\g<1><$META_LINK$>',TEST)

print (TEST + '\n\n')
