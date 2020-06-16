#import all dependancies 
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
import re

def init_browser():
    #open chrom browser for windows 
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

mars_data = {}

def mars_news_scrape():
    browser = init_browser()
    #nasa news url
    url_nasa = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url_nasa)

    #create HTMl Object
    html = browser.html

    #parse HTML with beautiful soup
    soup_nasa = bs(html, 'html.parser')
    # Extract title text
    news_title = soup_nasa.find_all('div',class_='content_title')[1].text
    # Extract Paragraph text
    news_p = soup_nasa.find('div',class_='article_teaser_body').text
    
    mars_data['nasa_news_title'] = news_title
    mars_data['nasa_news_paragraph'] = news_p

    #print the scraped data
    print(f" title {news_title}")
    print(f" Nasa news {news_p}")

    return mars_data

def jpl_img_scrape():
    browser = init_browser()

    # JPL Mars space images url
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    html = browser.html
    soup_jpl = bs(html, 'html.parser')

    #extract the latest featured Mars image
    main_url_jpl = 'https://www.jpl.nasa.gov'
    image_url = soup_jpl.find('li', class_='slide').a['data-fancybox-href']
    featured_image_url = main_url_jpl + image_url
    mars_data['full_image_url'] = featured_image_url

    print(f" image_url {featured_image_url}")

    return mars_data

def mars_weather_scrape():
    browser = init_browser()

    url_mars_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_mars_twitter)
    page = requests.get(url_mars_twitter)

    browser.find_by_css('div[class="css-1dbjc4n r-1awozwy r-18u37iz r-1wtj0ep"').first.click()
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find_all("span",class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")

    filtered_weather_tweets=[]

    for n in range(8):
        if "low" in mars_weather[n].text and "high" in mars_weather[n].text and "winds" in mars_weather[n].text and "pressure" in mars_weather[n].text:
            filtered_weather_tweets.append(mars_weather[n].text)

    weather_tweet=filtered_weather_tweets[0]

    print(f"mars_weather {weather_tweet}")
    mars_data['mars_weather'] = weather_tweet
    return mars_data

def mars_facts_scrape():
    browser = init_browser()

    url_mars_facts = 'https://space-facts.com/mars/'

    tables = pd.read_html(url_mars_facts)
    mars_fact_df = tables[0]
    mars_fact_df.columns = ['Description', 'Values']
    #mars_fact_df
    html_table = mars_fact_df.to_html()
    mars_data['mars_facts'] = html_table

    #print(html_table)
    return mars_data

def mars_hemispheres_scrape():
    browser = init_browser()

    url_mars_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url_mars = 'https://astrogeology.usgs.gov'
    browser.visit(url_mars_hemisphere)

    html = browser.html
    soup_mars_hemisphere = bs(html, 'html.parser')

    hemisphere_image_urls =[]
    url_to_image = soup_mars_hemisphere.find_all('div',class_='item')

    for url in url_to_image:
        title = url.find('h3').text
        #print(title)
        
        url_to_image_page = url_mars + url.a['href']
        #print(url_to_image_page)
    
        browser.visit(url_to_image_page)
        html= browser.html
        soup_mars_image_page = bs(html, 'html.parser')
    
        image_url = soup_mars_image_page.find('div', class_='downloads').a['href']
    
        #print(image_url)
        #print('--------------------------------------------------------')
        img_data=dict({'title':title, 'img_url':image_url})
        hemisphere_image_urls.append(img_data)
    
    mars_data['hemispheres_img_url'] = hemisphere_image_urls
    return mars_data






