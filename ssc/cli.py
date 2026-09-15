import argparse
from ssc.links import validate_links
from ssc.links.saver import save_to_csv


def main():
    parser = argparse.ArgumentParser(description='Simple Site Checker')
    parser.add_argument('-links', action='store_true',
                        help='Check all links on the page')
    parser.add_argument('-src', action='store_true',
                        help='Check availability of loaded resources (images, scripts, styles)')
    parser.add_argument('-url', required=True,
                        help='URL of the webpage to check')
    parser.add_argument('-auth', help='Path to cookie file or raw cookie string for authentication')
    parser.add_argument('-skip-strict', action='store_true',
                        help='Skip validation for strict anti-bot domains (e.g. LinkedIn, Twitter)')
    parser.add_argument('-res', help='Save results to CSV file')

    args = parser.parse_args()

    if args.links or args.src:
        results = validate_links(args.url, auth_input=args.auth, skip_strict=args.skip_strict, check_links=args.links, check_src=args.src)

        if args.res:
            save_to_csv(results, args.res)
            print(f'Results saved to {args.res}')


if __name__ == "__main__":
    main()
