import argparse
from . import qsf

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('format', choices=['qsf', 'csv'])
parser.add_argument('--replacements', nargs='*')
parser.add_argument('--skipids', nargs='*', default=[])

args = parser.parse_args()

replacements = []
if args.replacements:
    print('ASDF')
    print(args.replacements)
    replacements = [l.split('->') for l in args.replacements]
    print(replacements)

if args.format == 'qsf':
    survey = qsf.parse(file=args.file)
    with open('survey.html', 'w') as f:
        txt = str(survey.distribute(replacements=replacements, skipids=args.skipids))
        # this is a hack
        #txt = txt.replace('"', '').replace()
        txt = txt.replace("&quot;", "'")
        print(txt)
        f.write(txt)