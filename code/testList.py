dict={}
item=['qdaka','wdda','edfd','rdada']
item_2=['qdadddaka','wdadadda','edaddfd','rdddada']
i=0
for it in item:
	dict[it]=item_2[i]
	i=i+1

print dict

itemTest =  "qdaka"
itemTest_2 ="dhakdaldja"
dict[itemTest_2]='adkdha'
print dict
if itemTest in dict:
	print "yes"
list = []
for x in xrange(0,10):
	list.append([])
	print x
	temp = x
	temp_2 =x*x
	list[x].append(temp)
	list[x].append(temp_2)
print list
print list[0][-1]
print list[2][-1]
print list[-1]

string = 'ajdhakdhdj'
if '.' in string:
	print "yes. there is a dot string"
string_2 = "dakf.dkakd"
if '.' in string_2:
	print "yes. there is a dot string_2"