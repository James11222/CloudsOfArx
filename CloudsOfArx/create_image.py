import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude
from wordcloud import WordCloud, ImageColorGenerator


def create_image_mask(image_file=None):
    """
    A function which takes in an image and formats a mask to be used by the wordcloud.

    image_file: [string] - the string representing the file location of the image desired.

    returns: mask, original_image

    """
    if image_file is not None:
        # choose image we wish to use
        image = np.array(Image.open(path.join(image_file)))
        image = image[:,:,:3]
        
        # create mask white is "masked out" using edge detection
        mask = image
        mask[mask.sum(axis=2) == 0] = 255
        edges = np.mean([gaussian_gradient_magnitude(image[:, :, i] / 255., 2) for i in range(3)], axis=0)
        mask[edges > .08] = 255

        return mask, image
    else:
        # Just use a bland template
        image = np.ones((1200, 1600, 3), dtype=int) * 255
        mask = np.zeros((1200, 1600, 3), dtype=int) 

        return mask, image


def create_wordcloud(text_data, image_file, test_case, save_name=None,):
    """
    A function which generates a wordcloud from a mask and text data.

    text_data: [string] - a string which contains all the relevant data needed to make the 
    word cloud.
    image_file: [string] - the string representing the file location of the image desired.
    save_name: [string] - optional parameter to change the save name of the wordcloud image.

    returns: None
    """

    # generate the mask
    mask_data, original_image = create_image_mask(image_file)

    # generate word cloud
    wc = WordCloud(max_words=2000, mask=mask_data, max_font_size=40, random_state=42, relative_scaling=0)
    wc.generate(text_data)

    # create coloring from image
    image_colors = ImageColorGenerator(original_image)
    wc.recolor(color_func=image_colors)
    
    plt.imshow(wc, interpolation="bilinear")
    plt.xticks([])
    plt.yticks([])

    if test_case is False:
        if save_name is not None:
            wc.to_file(save_name + '.png')
        else:
            wc.to_file("wordcloud.png")
    else: 
        return True



