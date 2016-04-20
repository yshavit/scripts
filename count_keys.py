#!/usr/bin/python

import json
import re
import sys

MAX_EXAMPLE_LEN = 50

if len(sys.argv) == 1:
    import os
    me = os.path.basename(sys.argv[0])
    sys.stderr.write('''%s file.js [file.js...]

    Reads all of the files, which must be json objects or json lists of objects,
    and reports about their top-level keys.

    Keys are reported first by how common they are, and then alphabetically.
    For each key, this script reports how many objects had that key, as well as
    an example value. The example is prefaced with a note of which file, and
    which object within that file, the example came from. Both are 1-indexed.
''' % me)
    exit(1)

key_counts = {}
key_examples = {}
errs = 0

total_objs_count = 0
for fidx, f in enumerate(sys.argv[1:]):
    fidx += 1
    print 'reading file %d: %s.' % (fidx, f)
    with open(f) as f_handle:
        objs = json.load(f_handle)
        if type(objs) == dict:
            objs = [objs]
        objs_count = 0
        for o in objs:
            objs_count += 1
            total_objs_count += 1
            if type(o) != dict:
                errs += 1
                continue
            for k, v in o.iteritems():
                if k in key_counts:
                    key_counts[k] += 1
                else:
                    key_counts[k] = 1
                if k not in key_examples:
                    if len(v) > MAX_EXAMPLE_LEN:
                        v = '%s...' % v[:MAX_EXAMPLE_LEN]
                    key_examples[k] = '%s:%s - %s' % (fidx, objs_count, v)

print 'Read %d object%s.' % (total_objs_count,
                             '' if total_objs_count == 1 else 's')
print ''

items = sorted(key_counts.items(), key=lambda (k, v): (-v, k))
max_key_len = max(len('key'), max(map(lambda (k, v): len(k), items)))
max_count_len = max(map(lambda (k, v): len(str(v)), items))
max_example_len = max(map(len, key_examples.values()))
format_str = '%%-%ds | %%-%ds  | %%s' % (max_key_len, max_count_len)

header = format_str % ('Key', '#', 'Example')
print header
header = re.sub('[^|]', '-', header).replace('|', '+')
header += '-' * (max_example_len - len('Example'))
print header

for k, v in items:
    print format_str % (k, v, key_examples[k])
