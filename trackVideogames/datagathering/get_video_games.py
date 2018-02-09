from igdb_api_python.igdb import igdb

igdb = igdb('b39ab80da1d9eac24dc7ae18954930c0')
result = igdb.games({'limit':50,'offset':10})

print "helo"

for game in result.body:
    print("Retrieved: " + game["name"]) 