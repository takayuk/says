import sys

table = {}

with file(sys.argv[1]) as opened:
    for line in opened:
        token = line.strip().split("\t")

        userid, photoid, datetaken = token[0], token[1], int(token[2])

        if not userid in table:
            table[userid] = []

        table[userid].append((photoid, datetaken))
       

for u in table:
    #print(table[u])

    s = sorted(table[u], key=lambda x:x[1])
    print(s)
