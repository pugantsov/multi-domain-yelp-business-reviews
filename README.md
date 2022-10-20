# Multi-Domain Yelp Business Reviews
A multi-domain sentiment classification dataset extended from the Business and Reviews datasets supplied by the [2015 Yelp Dataset Challenge](https://www.yelp.com/dataset).

# Prerequisites
The parsing functionality requires both datasets to be downloaded and supplied to the parsing script.

The following Python packages must be installed:

 - Pandas
 - Numpy
 - Datasets (HuggingFace)

# Usage Instructions
Run `parse.py` with the following, mandatory arguments:

 - `-rf` or `--reviews-file`: Filepath to the Yelp Reviews JSON file (str)
 - `-bf` or `--business-file`: Filepath to the Yelp Business JSON file (str)
 - `-out` or `--output-dir`: Filepath to the directory where the datasets will be saved.

# Domain Metadata
| Domain                    | Positive-class Samples | Negative-class Samples | Total Samples |
| ------------------------- | ---------------------- | ---------------------- | ------------- |
| Restaurants               | 1,673,359              | 971,671                | 2,645,030     |
| Food                      | 698,971                | 420,512                | 1,119,483     |
| Nightlife                 | 579,360                | 306,257                | 885,617       |
| Event Planning & Services | 199,582                | 146,431                | 346,013       |
| Shopping | 120,920 | 142,777 | 263,697 |
| Hotels | Travel | 98,421 | 108,977 | 207,398 |
| Arts | Entertainment | 120,967 | 66,981 | 187,948 |
| Beauty | Spas | 56,199 | 92,444 | 148,643 |
| Automotive | 28,589 | 91,244 | 119,833 |
| Home Services | 22,972 | 91,698 | 114,670 |
| Active Life | 55,747 | 39,946 | 95,693 |
| Local Services | 26,406 | 67,872 | 94,278 |
| Health | Medical | 22,861 | 63,712 | 86,573 |
| Local Flavor | 50,576 | 19,919 | 70,495 |
| Real Estate | 7,612 | 27,346 | 34,958 |
| Pets | 11,188 | 21,926 | 33,114 |
| Professional Services | 6,374 | 20,134 | 26,508 |
| Public Services | Government | 10,922 | 7,469 | 18,391 |
| Education | 7,398 | 6,445 | 13,843 |
| Financial Services | 2,280 | 11,276 | 13,556 |
| Religious Organizations | 1,625 | 657 | 2,282 |
| Mass Media | 926 | 1,320 | 2,246 |