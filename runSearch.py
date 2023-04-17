'''
Script to use the search software to simply run the search
'''

from classes.search import Search

def main():

    s = Search('sampleData/test.xml')

    s.search()

    print(s.goodLocs)
if __name__ == '__main__':
    main()
