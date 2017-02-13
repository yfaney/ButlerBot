from bs4 import BeautifulSoup
import bs4
import requests

REQURL = "http://www.buick.com/current-offers.html?x-zipcode=66223"
DIV_TRV = [
            {"id":"container"},
            {"class":"mds-area-content"},
            {"class":"mds-area-pf1"},
            {"class":"parbase webclipping"},
            {"class":"webclipping-content"},
            {"id":"wraper_CurrentOffer_New"},
            {"class":"co-filter"},
            {"class":"offers"}]

TARGET_TXT1 = "0% APR"
TARGET_TXT2 = "buick"

def filter_tagsonly(tag_item):
    filtered = [item for item in tag_item.children if type(item) == bs4.element.Tag]
    filtered = [item for item in filtered if item.name not in ['li', 'script', 'noscript', 'meta', 'link']]
    return filtered

def filter_stringsonly(tag_item):
    filtered = [item for item in tag_item.children if type(item) == bs4.element.NavigableString]
    return filtered

def get_zero_apr(offer, car_model):
    resp = requests.get(REQURL)
    soup = BeautifulSoup(resp.text, "html.parser")
    offers = soup.find_all("span", class_="IOM_small")
    msgs = []
    for item in offers:
        res = filter_stringsonly(item)
        if len(res) > 1:
            if offer in str(res[1]) and car_model in str(res[0]).lower():
                msgs.append("%s:%s" %(res[0], res[1]))
    return "\n".join(msgs)

if __name__ == "__main__":
    print get_zero_apr(TARGET_TXT1, TARGET_TXT2)

