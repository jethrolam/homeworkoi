import argparse
import pandas as pd
import re


def normalize(word):
    """ Normalize a word into token, with scan error according to spec """
    token = word
    token = re.sub(r"[0O]", "O", token)
    token = re.sub(r"[b6]", "b", token)
    token = re.sub(r"[B8]", "B", token)
    token = re.sub(r"[1Il]", "I", token)
    token = token.lower()
    return token


def compute_token_df(text):
    """ Return a dataframe describing tokens generated from text """

    # NOTE: If text cannot fix in local memory, the caller of this function
    # may break the text into chunks, call this function on each chunk, 
    # and aggregate all token_df's into a final token_df

    # Split into words according to spec
    # NOTE: Added \n as delimiter even it is not mentioned in spec
    words = filter(None, re.split(r"[.,\- \n]+", text))

    # Turn words into token_df
    word_df = pd.DataFrame(words, columns=['word'])
    word_df = word_df.assign(token=word_df.word.apply(normalize))
    grouped = word_df.groupby('token')
    token_df = grouped.count()
    token_df.columns = ['freq']
    variation_ser = grouped.apply(lambda df : df.word.unique().tolist()).rename('variation')
    token_df = token_df.join(variation_ser)
    summary_ser = (
        token_df.variation.apply(lambda x : '|'.join(x))
        + '@' + token_df.freq.astype(str)
    ).rename('summary')
    token_df = token_df.join(summary_ser)

    return token_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='gettysburg.txt')
    parser.add_argument('-k', type=int, dest='k', help="Number of most common tokens to output (default: 10)", default=10)
    args = parser.parse_args()

    text = open(args.filename).read()
    k = args.k

    token_df = compute_token_df(text)

    print '\n'.join(token_df.sort_values('freq', ascending=False).head(k)['summary'].values)
