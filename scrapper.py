import requests
from bs4 import BeautifulSoup
import pandas

search_catergories = {"audio+audiophile":"https://carousell.com/search/products/?sort_by=time_created%2Cdescending&audio_features=AUDIO_FEATURES_FOR_AUDIOPHILES&query={}&collection_id=207&cc_id=356"\
                        }
tracked_items = ["sennheiser"]
exception_words = ["spoilt", "broken", "1/10", "2/10", "3/10", "4/10"]
labels = tracked_items
data = []

# query and collect listings for each tracked item
def scrap():
    for k, v in search_catergories.items():
        for item in tracked_items:
            search_path = v.format(item)
            try:
                # request data
                r = requests.get(search_path)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                names = soup.find_all("div", {"class": "H-i"})
                info = soup.find_all("dl")
                # process data
                for n, i in zip(names, info):
                    name = n.text
                    x = i.find_all("dd")
                    price = x[0].text
                    desc = x[1].text
                    # filter listings with exception words
                    valid = True
                    for ex in exception_words:
                        if ex in desc:
                            valid = False
                    # process only listings that pass the exception filter
                    if valid:
                        data.append({"name": name, "price": price})

            except requests.exceptions.RequestException:
                print("Connection failed")

# generate additional smart labels based on common words in listing names
def generate_labels():
    word_frequency = {}
    # collect all names in existing labels
    words = []
    for ls in data:
        for w in ls["name"].split(" "):
            words.append(w)
    #print(words)
    for w1 in words:
        word_frequency[w1] = 1
        for w2 in words:
            if w1 == w2:
                word_frequency[w1] += 1
                words.remove(w1)

    max_return = 3  # number of labels to return
    for i in range(max_return):
        top_word = max(word_frequency, key=word_frequency.get)  # returns highest frequency word as label
        word_frequency.pop(top_word)
        new_label = top_word.lower()
        if new_label not in labels:
            labels.append(new_label)


def search_database(label):
    for ls in data:
        if label in ls["name"].lower():
            print(ls)


scrap()
generate_labels()
search_database("headphones")
print(labels)

# df = pandas.DataFrame(data)
# df.to_csv("output.csv")