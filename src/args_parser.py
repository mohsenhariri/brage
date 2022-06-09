import argparse

parser = argparse.ArgumentParser(description="Dataset")

parser.add_argument("-id", type=str, default=None, metavar="N", help="Dataset")
id = parser.parse_args().id
