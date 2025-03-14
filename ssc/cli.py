import argparse
from .links import validate_links
from .links.saver import save_to_csv


def main():
    parser = argparse.ArgumentParser(
        description='Simple Site Checker - Link Validation')
    parser.add_argument('-links', action='store_true',
                        help='Check all links on the page')
    parser.add_argument('-url', required=True,
                        help='URL of the webpage to check')
    parser.add_argument('-res', help='Save results to CSV file')

    args = parser.parse_args()

    if args.links:
        results = validate_links(args.url)

        if args.res:
            save_to_csv(results, args.res)
            print(f'Results saved to {args.res}')
