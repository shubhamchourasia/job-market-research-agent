import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from src.processor.elastic_svc import index_document

async def crawl_layoffs_locally():
    print("🚀 Starting Deep Crawl for Airtable Data...")

    # Configure the browser to be "human-like"
    browser_cfg = BrowserConfig(headless=True, verbose=True)
    
    # Configure the run to handle iframes and dynamic content
    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        process_iframes=True,      # CRITICAL: Look inside the Airtable iframe
        remove_overlay_elements=True,
        # Wait for the specific Airtable grid to appear
        wait_for="css:.baymax", 
        # Increase delay to let the rows actually load
        delay_before_return_html=10, 
        # New in 2026: forces the crawler to scroll to trigger JS loading
        scan_full_page=True 
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url="https://layoffs.fyi",
            config=run_cfg
        )

        if result.success:
            # We check the length—it should be much higher than 2380 now
            content = result.markdown
            print(f"✅ Success! Characters retrieved: {len(content)}")
            
            if len(content) < 3000:
                print("⚠️ Warning: Content still seems thin. Airtable may have blocked the headless crawl.")
            
            index_document(
                url="https://layoffs.fyi",
                title="Detailed Layoffs Table",
                content=content
            )
        else:
            print(f"❌ Crawl failed: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(crawl_layoffs_locally())