"""Multi-Domain Yelp Business Reviews.

Parses all datasets, given input Business and Reviews datasets
from the Yelp Dataset Challenge (https://www.yelp.com/dataset).

"""

import collections
import html
import json
import re

import datasets
import numpy as np
import pandas as pd

from constants import HIGH_LEVEL_CATEGORIES

# Loading

def load_business_data(yelp_business_fname):
    rows = []
    with open(yelp_business_fname, "r") as f:
        for line in f:
            data = json.loads(line)
            rows.append({k: data[k] for k in ["business_id", "categories"]})

    df = pd.DataFrame.from_records(rows)
    df = df[~df.categories.isna()]
    return df

def load_reviews_data(yelp_reviews_fname):
    return datasets.load_dataset(
        "json",
        data_files=yelp_reviews_fname,
        split="train"
    )

# Preprocessing

def clean_text(x):
    """Function for cleaning the dataset's text column.
    
    The following steps are carried out:
        - Cleans HTML entities from field, e.g. '&pound;'.
        - Decodes ASCII characters by converting text to
            UTF-8.
        - Removes all URLs and replaces it with a single
            [URL] token
        - Cleans HTML tags from string, e.g. '<head>'
        - Trims excessive whitespace in between words.
        - Strips whitespace at beginning and end of string.
    
    """
    x["text"] = re.sub("<.*?>", "", x["text"])
    x["text"] = (x["text"].encode("ascii", errors="ignore")
                            .decode("utf-8"))
    x["text"] = re.sub(r"http\S+|www.\S+", "[URL]", x["text"])
    x["text"] = html.unescape(x["text"])
    x["text"] = re.sub(r"\s+", " ", x["text"])
    x["text"] = x["text"].strip()
    return x

def filter_star_ratings(x, col_stars):
    """Filters out 5/5 star ratings, as per prior work."""
    return x[col_stars] < 5

def binarize_star_ratings(x, col_stars):
    """Map star ratings to positive/negative sentiment."""
    x["label"] = 0 if x[col_stars] <= 2 else 1
    return x

def map_category_name(x, category):
    """Sets category name that is passed to function."""
    x["category"] = category
    return x

def preprocess_yelp(yelp_reviews_data, category, category_to_bids):
    star_ratings_col = "stars"
    
    # Get all categories as list
    all_bids = np.array(yelp_reviews_data["business_id"])

    if category not in category_to_bids:
        return
    
    # Get business ids for a particular category
    bids = category_to_bids[category]
    
    # Convert business ids to dict_key view object
    # (0(1) > O(n) compared with list)
    bids_view = {bid: 0 for bid in bids}.keys()
    
    # Create list of indices corresponding to business ids
    select_ids = [i for i, x in enumerate(all_bids)
                  if x in bids_view]
    if not len(select_ids):
        return
    
    dataset = yelp_reviews_data.select(select_ids)

    # Format string to lowercase and _ separator
    # e.g. Active Life -> active_life
    cat_fmt = re.sub(r"( & )| ", "_", category.lower())

    # Print number of per category samples
    print(f"{category} -> {cat_fmt}",
          "{:,}".format(len(dataset)))

    # Map category name to new column
    dataset = dataset.map(lambda x: map_category_name(x, cat_fmt))
    
    dataset = dataset.remove_columns([
        "user_id", "business_id",
        "useful", "funny", "cool", "date"
    ])
    return dataset

# Utilities

def map_category_to_business_ids(yelp_business_df):
    category_to_bids = {}
    for category in HIGH_LEVEL_CATEGORIES:
        df = yelp_business_df[
            yelp_business_df["categories"].str.contains(category)
        ]
        bids = df["business_id"].values
        if not len(bids):
            continue
        category_to_bids[category] = bids
    return category_to_bids

def drop_duplicate_review_ids(dataset):
    review_ids = pd.DataFrame(dataset["review_id"], columns=["review_id"])
    review_ids = review_ids.drop_duplicates(subset="review_id")
    return dataset.select(review_ids.index.values)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Multi-Domain Yelp Business Reviews Parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-bf", "--business-file",
                        type=str, help="Filepath of business reviews JSON")
    parser.add_argument("-rf", "--reviews-file",
                        type=str, help="Filepath of main reviews JSON")
    parser.add_argument("-out" ,"--output-dir",
                        type=str, help="Directory to save datasets to")

    args = parser.parse_args()

    yelp_business = load_business_data(args.business_file)
    yelp_reviews = load_reviews_data(args.reviews_file)

    yelp_domains = {}
    for category in HIGH_LEVEL_CATEGORIES:
        category_to_bids = map_category_to_business_ids(yelp_business)
        dataset = preprocess_yelp(
            yelp_reviews, category, category_to_bids)
        dataset = drop_duplicate_review_ids(dataset)

        dataset = dataset.remove_columns(["review_id"])
            
        dataset = dataset.filter(lambda x: filter_star_ratings(x, "stars"))
        dataset = dataset.map(lambda x: binarize_star_ratings(x, "stars"))
        dataset = dataset.remove_columns(["stars"])
        
        dataset = dataset.map(clean_text)

        cat_fmt = re.sub(r"( & )| ", "_", category.lower())
        dataset.save_to_disk(f"{args.output_dir}/{category}")
