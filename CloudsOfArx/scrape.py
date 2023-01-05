import ads
from operator import itemgetter
from bs4 import BeautifulSoup
import requests
import re

def clean_results(papers_dict):
    """
    A function to remove any unwanted publications from the scraped papers from NASA ADS.

    papers_dict: [dict] - dictionary of scraped meta data for research papers by the desired author.

    returns [dict] - cleaned version of papers_dict
    """
    first_author_papers = []
    for paper in papers_dict:
        if paper['pub'] != 'GRB Coordinates Network':
            first_author_papers.append(paper)

    return first_author_papers

def get_papers(ADS_TOKEN, author, orcid=None):
    """
    A function to scrape NASA ADS for first-author papers of a given author.

    ADS_TOKEN: [string] - a token necessary to use the NASA ADS API.
    author: [string] - first-author whose work is desired string format 'LastName, FirstName'
    orcid: [string] - optional parameter to remove degeneracies between authors with the same name.

    returns [dict] - a dictionary populated with the papers by the author.
    """

    # CONFIGURE ADS
    ads.config.token = ADS_TOKEN
        
    if orcid is not None:
        papers = list(
            ads.SearchQuery(
                first_author=author,
                orcid=orcid,
                fl=[
                    "id",
                    "title",
                    "author",
                    "doi",
                    "year",
                    "pubdate",
                    "pub",
                    "volume",
                    "page",
                    "identifier",
                    "doctype",
                    "citation_count",
                    "bibcode"], max_pages=100))
    else:
        papers = list(
            ads.SearchQuery(
                first_author=author,
                fl=[
                    "id",
                    "title",
                    "author",
                    "doi",
                    "year",
                    "pubdate",
                    "pub",
                    "volume",
                    "page",
                    "identifier",
                    "doctype",
                    "citation_count",
                    "bibcode"], max_pages=100))
        
    dicts = []
    for paper in papers:
        aid = [
            ":".join(t.split(":")[1:])
            for t in paper.identifier
            if t.startswith("arXiv:")
        ]
        for t in paper.identifier:
            if len(t.split(".")) != 2:
                continue
            try:
                list(map(int, t.split(".")))
            except ValueError:
                pass
            else:
                aid.append(t)
        try:
            page = int(paper.page[0])
        except (ValueError, TypeError):
            page = None
            if paper.page is not None and paper.page[0].startswith("arXiv:"):
                aid.append(":".join(paper.page[0].split(":")[1:]))
        dicts.append(
            dict(
                doctype=paper.doctype,
                year=paper.year,
                pubdate=paper.pubdate,
                doi=paper.doi[0] if paper.doi is not None else None,
                pub=paper.pub,
                volume=paper.volume,
                page=page,
                arxiv=aid[0] if len(aid) else None,
                citations=(
                    paper.citation_count
                    if paper.citation_count is not None
                    else 0
                ),
                url="https://ui.adsabs.harvard.edu/abs/" + paper.bibcode,
            )
        )
    papers_dict = sorted(dicts, key=itemgetter("pubdate"), reverse=True)
    cleaned_papers_dict = clean_results(papers_dict)

    return cleaned_papers_dict


def compile_abstracts(first_author_papers):
    """
    A function to compile all the abstracts from the desired first-author papers to be 
    used in the word cloud. We use beautifulsoup to parse through the NASA ADS abstract page
    to find the desired abstracts. 

    first_author_papers: [dict] - dictionary of scraped meta data for research papers by the desired author.

    returns [string] - a string of all the text within the desired abstracts.
    """

    abstracts = []
    for i in range(len(first_author_papers)):
        #retrieve the ADS abstract page
        URL = first_author_papers[i]['url']
        
        # scrape the ADS abstract page
        page = requests.get(URL)
        
        #parse the page and pull out only the abstract text (excluding inline latex)
        soup = BeautifulSoup(page.content, 'html.parser')
        abstract = soup.p.string
        pattern = r'\$(.*?)\$'
        formatted_abstract = re.sub(pattern, '', abstract[21:-20])
        abstracts.append(formatted_abstract)

    #turn the list of abstracts into one long string
    total_abstract_string = ''
    for abstract in abstracts:
        total_abstract_string += abstract + ' '
        
    return total_abstract_string

    