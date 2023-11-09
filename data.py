import requests 

# data = requests.get('https://en.wikipedia.org/wiki/Punjab,_Pakistan')

# text_data = data.text
# data_chunks = text_data.split('\n')
# print(len(data_chunks))

def get_data(url):
    data = requests.get(url)
    text_data = data.text
    data_chunks = text_data.split("\n")
    return data_chunks

# print(data.text)