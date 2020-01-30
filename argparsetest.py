import argparse

parser = argparse.ArgumentParser(
        prefix_chars="-", fromfile_prefix_chars="@")
parser.add_argument('-f', '--foo', action='append')
parser.add_argument('--if', action='store_true')
print parser.parse_args('-f 42 --foo 34 --if '.split())
print parser.parse_args('-f 42 --foo 34 '.split())

