import argparse
import ScrapLib

parser = argparse.ArgumentParser(description='Scraper for www.mangaworld.so')
parser.add_argument('url', metavar='url', help='first page url')
parser.add_argument('--pc', metavar='pathCBR', default='cbrfile\\',
                    help='Folder where app save the cbr files')
parser.add_argument('--ptf', metavar='pathTmpfile', default='tmpfile\\',
                    help='Folder where app save temporary the image files')

args = parser.parse_args()

ScrapLib.downloadCBR(args.url, args.pathCBR, args.pathTmpfile)

print('Download terminato')

