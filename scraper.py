import scraperwiki
import datetime
from bs4 import BeautifulSoup
import os
import sqlitedb
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"

base_html = "https://www.planningportal.nsw.gov.au"

#get html from source
def get_applications(page):
	#pretend to be an ipad to bypass cloudflare protection with user-agent
	userAgent = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
	return scraperwiki.scrape("https://www.planningportal.nsw.gov.au/major-projects/projects?status=Exhibition&lga=All&development_type=All&industry_type=All&case_type=All&page={}".format(page),"",userAgent)

def get_application_exhibition(link):
	# print("Visiting page: ", link)
	userAgent = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
	page = scraperwiki.scrape(link, "", userAgent)
	page = BeautifulSoup(page, "html.parser")
	d = []
	for dates in page.find_all("time"):
		d.append(dates.get_text())
	return d[0], d[1]

#extract needed data from html
def get_data(data, conn):
	page = BeautifulSoup(data, "html.parser")
	if not page.find(class_="card__content"):
		# print("No applications here")
		return False
	for table in page.find_all(class_="card__content"):
		refId = table.find(class_ = "field field-field-case-id field-type-string field-label-hidden").get_text().strip()
		address = table.find(class_ = "card__title").find_next_sibling().get_text().strip()
		council = table.find(class_ = "card__sub").get_text().strip()
		name = table.find(class_ = "card__title").get_text().strip()
		link = table.find("a", href = True)["href"]
		time = datetime.datetime.now().strftime("%x")
		# get exhibition dates
		start, end = get_application_exhibition(base_html + link)
		thisApplication = (refId, address, council, name, base_html + link, time, start, end)
		sqlitedb.store_data(thisApplication, conn)
	return True

def visit_pages(conn):
	page = 0
	html = get_applications(page)
	apps = get_data(html, conn)
	while apps:
		page = page + 1
		html = get_applications(page)
		apps = get_data(html, conn)

def main():
	# Connect to database
	conn = sqlitedb.create_database()
	if conn is not None:
		# Create table if not already created
		sqlitedb.create_table(conn)
		# sqlitedb.update_table(conn)
		visit_pages(conn)
	else:
		print("Error creating table.")
	quit()

if __name__ == '__main__':
	main()
