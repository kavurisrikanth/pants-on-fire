# Final project for DADV.
# Given the list of candidates running for President of the United States in 2020, list for each
# candidate the amount of time before Election Day (November 9th 2020) when the candidate
# begins making more dishonest statements than usual.

from plot import plot_truthiness
from scrape import get_statements

if __name__ == '__main__':
    get_statements()
    plot_truthiness()