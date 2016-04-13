import sys
import json

pretty = (len(sys.argv) > 1) and (sys.argv[1] == '--pretty')

d = dict()
d['format'] = 'TPC 0.1'
d['dimension'] = 2
d['attributes'] = [ 'sum', 'min' ]
d['timestamp'] = '2015-10-26T07:46:36.611Z'
d['description'] = 'An example TPC file'
d['optional'] = dict(what='Additional attributes',why='Are permitted')

points = [
    {'v': [1.0,1.0],
     'a': [2.0,1.0],
     't': ['positive'] },
    {'v': [1.0,2.0],
     'a': [3.0,1.0],
     't': ['positive', 'distinct'] },
    {'v': [-2.0,1.0],
     'a': [-1.0,-2.0],
     't': ['distinct'] },
    {'v': [-3.0,-3.0],
     'a': [-6.0,-3.0],
     't': [] } ]

d['points'] = points

if pretty:
    print(json.dumps(d, sort_keys=True,indent=4, separators=(',', ': ')))
else:
    print(json.dumps(d))
    
