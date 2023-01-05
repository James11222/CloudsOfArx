import CloudsOfArx.scrape as scrape
import CloudsOfArx.create_image as create_image
import CloudsOfArx.main as CloudsOfArx
import os

def test_tprint():
    try:
        if CloudsOfArx.test_print() == True:
            assert True
        else:
            assert False
    except:
        assert False

def test_clipping_mask():
    try:
        test_dir_path = os.path.realpath(__file__)[:-13]
        image_file = test_dir_path + 'BlackHole_Example.png'
        mask, image = create_image.create_image_mask(image_file)

        if mask.shape == image.shape:
            assert True
        else:
            assert False
    except:
        assert False

