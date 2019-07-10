import requests

def make_title(text):
    start_point = text.find('<title>') + 7
    end_point = text.find('</title>')
    return text[start_point:end_point]
