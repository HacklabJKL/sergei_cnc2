#!/usr/bin/env python3

import sys
import json
import argparse

parser = argparse.ArgumentParser(description='''Create toolbit files for FreeCAD
Example usage: ./CreateTool.py 61 6x6x38x76''')
parser.add_argument('--carbide', '-c', action = 'store_const', dest = 'material', const = 'Carbide', default = 'HSS', help = 'Made out of carbide (default HSS)')
parser.add_argument('--flutes', '-f', dest = 'flutes', type=int, default = 2, help = 'Number of flutes in tool (default 2)')
parser.add_argument('--library', dest = 'library', default = 'Library/HacklabJKL.fctl', help = 'Library file to edit')
parser.add_argument('id', metavar = 'ID')
parser.add_argument('size', metavar = 'D1xD2xL1xL2')
args = parser.parse_args()

d1, d2, l1, l2 = map(float, args.size.split('x', 3))

bit = {
    'version': 2,
    'name': args.size,
    'shape': 'endmill.fcstd',
    'parameter': {
        'Chipload': '0.05 mm',
        'CuttingEdgeHeight': '%0.3f mm' % l1,
        'Diameter': '%0.3f mm' % d1,
        'Flutes': str(args.flutes),
        'Length': '%0.3f mm' % l2,
        'Material': args.material,
        'ShankDiameter': '%0.3f mm' % d2,
        'SpindleDirection': 'Forward'
    },
    'attribute': {}
}

open('Bit/' + args.size + '.fctb', 'w').write(json.dumps(bit, indent = 2))

library = json.loads(open(args.library).read())

library['tools'] = [x for x in library['tools'] if x.get('nr') != args.id]
library['tools'].append({
    'nr': args.id,
    'path': args.size + '.fctb'
})

library['tools'].sort(key = lambda x: x.get('nr'))

new = json.dumps(library, indent = 2)
open(args.library, 'w').write(new)

