import CloudsOfArx
import os

def test_secret_token():
    token = os.environ.get("ADS_KEY")
    flag = token[0] == 'z'
    assert flag
    
def test_wordcloud():
    ADS_API_KEY = os.environ.get("ADS_KEY")
    flag = CloudsOfArx.create_wordcloud(ADS_API_KEY, 'Sunseri, James', test_case=True)
    assert flag
