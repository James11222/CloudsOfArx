import CloudsOfArx
import os


def test_secret_token():
    try:
        token = os.environ.get("ADS_KEY")
        if token[0] == 'z':
            assert True
        else:
            assert False

    except:
        assert False
    

def test_wordcloud():
    try:
        ADS_API_KEY = os.environ.get("ADS_KEY")
        flag = CloudsOfArx.create_wordcloud(ADS_API_KEY, 'Sunseri, James', test_case=True)
        if flag == True:
            assert True
        else:
            assert False
    except:
        assert False
