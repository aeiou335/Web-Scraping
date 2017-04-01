from selenium import webdriver
import requests
import xlwt
from bs4 import BeautifulSoup

def req(url):
    r = requests.get (url)
    html = r.content
    ori_soup = BeautifulSoup ( html, 'html.parser')
    return ori_soup

def get_bestselling_url(url):
    browser = webdriver.Chrome()
    browser.get(url)

    el = browser.find_elements_by_id('sort-dropdown-control')
    for i in el:
        for option in i.find_elements_by_tag_name('option'):
            if option.text == 'Bestselling':
                option.click()
                break
    u = browser.current_url
    browser.quit()
    return u
            
def make_excel(url, s):
    table = file.add_sheet(s ,cell_overwrite_ok = True)
    for j in range(1,31):
        table.write(j,0,j)
    table.write(0,0,'Bestselling')
    table.write(0,1,'Brand')
    table.write(0,2,'Product')
    table.write(0,3,'Price')
    table.write(0,4,'Review_star')
    table.write(0,5,'Review_count')
    table.write(0,6,'Web')        
    browser = webdriver.PhantomJS()
    browser.get(url)
    
    source = browser.page_source

    soup = BeautifulSoup(source,'html.parser')
    name_tag = soup.findAll("div",{"class" : "product-title"})
    price_tag = soup.findAll("div", class_="product-price")
    review_tag = soup.findAll("div", class_="review-data")
    http = 'https://www.rei.com'
    for i in range(len(name_tag)):
        table.write(i+1, 1, name_tag[i].find("span", class_="brand-name").text)
        table.write(i+1, 2, name_tag[i].find("span", class_="text-body").text)
        if price_tag[i].find("span", class_="price") is None:
            table.write(i+1, 3, price_tag[i].find("span", class_="sale-price").text)
        else:
            table.write(i+1, 3, price_tag[i].find("span", class_="price").text)
        if review_tag[i].find("span", {"data-ui" : "rating-text"}) is not None:
            review = review_tag[i].find("span", {"data-ui" : "rating-text"}).text
            if review[13:] != '':
                table.write(i+1, 4, review[13:])
            else:    
                table.write(i+1, 4, "-")
        if review_tag[i].find("span", class_="review-count") is not None:
            table.write(i+1, 5, review_tag[i].find("span", class_="review-count").text.strip())
        else:
            table.write(i+1, 5, "-")
        table.write(i+1, 6, http + name_tag[i].find("a")['href'])
    browser.quit()
    file.save('Rei_Bestselling3.0.xls')


url = "https://www.rei.com/"
original = req(url)

file = xlwt.Workbook()

url = "https://www.rei.com"
original = req(url)
list = []
list2 = []
list3 = []
list4 = []
list.append(original.find("a", {"data-analytics-id" : "rei_nav:mens_tops:tops"})["href"])
list.append(original.find("a", {"data-analytics-id" : "rei_nav:mens_jackets:jackets"})["href"])
list.append(original.find("a", {"data-analytics-id" : "rei_nav:mens_bottoms:bottoms"})["href"])
list.append(original.find("a", {"data-analytics-id" : "rei_nav:womens_tops:tops"})["href"])
list.append(original.find("a", {"data-analytics-id" : "rei_nav:womens_jackets:jackets"})["href"])
list.append(original.find("a", {"data-analytics-id" : "rei_nav:womens_bottoms:bottoms"})["href"])
for m in range(6):
    list2.append(url + list[m])
    list[m] = url + list[m]
for i in range(len(list)):
    new_url = get_bestselling_url(list[i])
    while new_url == list[i]:
        new_url = get_bestselling_url(list[i])
    while new_url[len(new_url)-1] == '1':
        new_url = get_bestselling_url(list[i])
    list4.append(new_url)
    print(new_url[len(new_url)-1])
    new_url = ''


mens_tops_url = list4[0]
mens_jackets_url = list4[1]
mens_bottoms_url = list4[2]
womens_tops_url = list4[3]
womens_jackets_url = list4[4]
womens_bottoms_url = list4[5]
make_excel(mens_tops_url,'mens_tops')
make_excel(mens_jackets_url,'mens_jackets')
make_excel(mens_bottoms_url,'mens_bottoms')
make_excel(womens_tops_url,'womens_tops')
make_excel(womens_jackets_url,'womens_jackets')
make_excel(womens_bottoms_url,'womens_bottoms')
