twitter:
	source venv/bin/activate; bin/twitter.sh

hn:
	source venv/bin/activate; foreman run scrapy crawl hn

reddit:
	source venv/bin/activate; foreman run scrapy crawl reddit

youtube:
	source venv/bin/activate; foreman run scrapy crawl youtube

medium:
	source venv/bin/activate; foreman run scrapy crawl medium

upload_csv:
	bin/upload_csv.sh
