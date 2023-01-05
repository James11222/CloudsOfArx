import CloudsOfArx.scrape as scrape
import CloudsOfArx.create_image as create_image
import CloudsOfArx.main as CloudsOfArx

def test_tprint():
    try:
        if CloudsOfArx.test_print() == True:
            assert True
        else:
            assert False
    except:
        assert False
