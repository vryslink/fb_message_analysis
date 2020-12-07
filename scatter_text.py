import scattertext as st
import nltk
import pandas as pd


def create_scatter_text(writers, names, messages, nonames=False):
    my_df = pd.DataFrame({"author": names, "message": messages})
    nlp = st.tweet_tokenizier_factory(nltk.tokenize.TweetTokenizer())
    my_df['parse'] = my_df['message'].apply(nlp)

    corpus = st.CorpusFromParsedDocuments(
        my_df, category_col='author', parsed_col='parse'
    ).build().get_unigram_corpus().compact(st.AssociationCompactor(2000))

    if nonames:
        html = st.produce_scattertext_explorer(
            corpus,
            category=writers[0], category_name="Author_0", not_category_name="Author_1",
            minimum_term_frequency=0, pmi_threshold_coefficient=0,
            width_in_pixels=1000,
            transform=st.Scalers.dense_rank
        )
    else:
        html = st.produce_scattertext_explorer(
            corpus,
            category=writers[0], category_name=writers[0], not_category_name=writers[1],
            minimum_term_frequency=0, pmi_threshold_coefficient=0,
            width_in_pixels=1000,
            transform=st.Scalers.dense_rank
        )

    with open('./demo_compact.html', 'w') as f:
        f.write(html)
    f.close()
