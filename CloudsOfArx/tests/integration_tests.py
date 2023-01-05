import CloudsOfArx
import os


def test_secret_token():
    try:
        token = os.environ.get("secrets.ADS_API_TOKEN_TEST")
        print(token)
        if token[0] == 'z':
            assert True
        else:
            assert False

    except:
        assert False
    

# def test_wordcloud():
#     try:
#         CloudsOfArx.create_wordcloud()
