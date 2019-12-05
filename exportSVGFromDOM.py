from selenium import webdriver
from bs4 import BeautifulSoup
import requests, os

urlToFetchComponentFrom = "http://localhost:3000/autocodegenerator"
outputSVGPath = "Output.svg"

# https://stackoverflow.com/questions/39428042/use-selenium-with-chromedriver-on-mac
# Put the  chrome driver executable in the same folder as script
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) 
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

# Fetch the page from URL and render on Chrome
driver = webdriver.Chrome(executable_path = DRIVER_BIN)
driver.get(urlToFetchComponentFrom)

# Save the rendered page as HTML
with open("temp.html", "w") as f:
    f.write(driver.page_source)
driver.quit()

# Parse the HTML to get the SVG tag
soup = BeautifulSoup(open("temp.html"), "html.parser")
svg = soup.findAll('svg')[0] # ASsumes only one SVG in page

style = ''
styleFromHTML = soup.findAll('style')

# Find and append all style tags containing CSS for this component
for item in styleFromHTML:	
	style = style + str(item.string)

# Create a new style tag and insert into the svg
stylesTag = soup.new_tag('style')
stylesTag.string = style

svg.append(stylesTag)

# Export the SVG file
with open(outputSVGPath, "w") as text_file:
    text_file.write("%s" % svg)
