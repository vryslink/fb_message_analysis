import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from os import path
from wordcloud import WordCloud

from words_processing import get_freq_dict
from stopwords import get_stopwords


stopwords = get_stopwords()


def make_image(text, image_file):
    alice_mask = np.array(Image.open(image_file))

    wc = WordCloud(background_color="white", max_words=1000, mask=alice_mask)
    # generate word cloud
    wc.generate_from_frequencies(text)
    wc.to_file("used_words.png")
    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def create_word_cloud(writers, messages, names, image_file):
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    make_image(get_freq_dict(writers, messages, names, stopwords), image_file)
