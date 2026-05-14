<!

-- job-market-research-agent/
├── src/
│   ├── crawler/          # Web scraping logic
│   │   ├── __init__.py
│   │   ├── spider.py     # Main crawling functions
│   │   └── parsers.py    # Logic to extract data from specific sites
│   ├── processor/        # Saving to Elastic
│   │   ├── __init__.py
│   │   └── elastic_svc.py
│   └── ui/               # Streamlit interface
│       ├── __init__.py
│       └── app.py
├── data/                 # Local temp storage for scraps
├── .env                  # API keys (DO NOT COMMIT)
├── .gitignore            # Ignore venv, .env, and data/
├── requirements.txt
└── README.md 

-->

<!-- Clone elastic crawler -->
git clone https://github.com/elastic/crawler.git elastic-crawler
rm -rf elastic-crawler/.git
cd elastic-crawler 

<!-- Docker build local -->
docker build -t local-crawler .

<!-- Run crawler command -->
docker run -it --rm \
  --network="host" \
  -v "$(pwd)/config:/home/app/config" \
  local-crawler \
  jruby /home/app/bin/crawler crawl /home/app/config/crawler.yml

