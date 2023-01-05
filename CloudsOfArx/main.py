import CloudsOfArx.scrape as scrape
import CloudsOfArx.create_image as create_image

def create_wordcloud(ADS_TOKEN, author, image_file=None, orcid=None, save_name=None, test_case=False):
    """
    A function to create a wordcloud image out of the abstracts of an author's first-authored papers.

    ADS_TOKEN: [string] - a token necessary to use the NASA ADS API.
    author: [string] - first-author whose work is desired string format 'LastName, FirstName'
    image_file: [string] - the string representing the file location of the image desired.
    orcid: [string] - optional parameter to remove degeneracies between authors with the same name.
    save_name: [string] - optional parameter to change the save name of the wordcloud image.

    returns: None
    """
    #format the abstracts of the first-authored papers
    first_author_papers = scrape.get_papers(ADS_TOKEN, author, orcid)
    abstract_string = scrape.compile_abstracts(first_author_papers)

    #generate the wordcloud image
    create_image.create_wordcloud(abstract_string, image_file, test_case, save_name)

    print("Your wordcloud creation was succesful!")
    return True


def test_print():
    print("This package is working!")
    return True

