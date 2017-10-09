import sys, os
import re

#Command Line Argument
if len(sys.argv) < 2:
    sys.exit("Usage: %s filename" % sys.argv[0])

filename = sys.argv[1]

if not os.path.exists(filename):
    sys.exit("ERROR: File '%s' not found" % sys.argv[1])

#Dictionary
PlayerList = {} #name: (bat, hit, avg)

#Helper Function
def avgnum(hitnum,batnum):
    if batnum != 0:
        avg = round(float(hitnum)/float(batnum),3)
    else:
        avg = 0
    return avg

#Parse readings
regex = re.compile(r"(?P<name>\w+ \w+)\sbatted\s(?P<batnum>\d+)\stimes\swith\s(?P<hitnum>\d+)\shits\sand\s(\d+)\sruns")

with open(filename) as f:
    for line in f:
        players = regex.match(line)
        
        if players != None:
            name = players.group('name')
            batnum = int(players.group('batnum'))
            hitnum = int(players.group('hitnum'))
            avg = avgnum(hitnum,batnum)

            if batnum != None and hitnum != None:
                newscore = (batnum, hitnum, avg)

            if name != None:
                if name not in PlayerList:
                    PlayerList[name] = newscore
                else:
                    if name in PlayerList:
                        newbatnum = PlayerList[name][0] + batnum
                        newhitnum = PlayerList[name][1] + hitnum
                        newavg = avgnum(newhitnum,newbatnum)
                        PlayerList[name] = (newbatnum, newhitnum, newavg)

#Sorting in list
player_average = []

for player, stats in PlayerList.items():
    bat, hit, avg = stats
    player_average.append( [player, avg] )

avgs = sorted(player_average, key=lambda v: v[1], reverse = True)

for player, avg in avgs:
    print ('%s: %0.3f' % (player, avg))
