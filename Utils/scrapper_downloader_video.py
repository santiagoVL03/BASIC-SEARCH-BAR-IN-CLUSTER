import asyncio
import os
import re
from pathlib import Path
from playwright.async_api import async_playwright
import aiohttp
import tqdm

async def download_file(session, url, filepath):
    """Download a file from a URL and save it to a specific path with progress bar"""
    async with session.get(url, ssl=False) as response:
        total_size = int(response.headers.get('content-length', 0))
        with open(filepath, 'wb') as f:
            with tqdm.tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(filepath)) as pbar:
                chunk_size = 8192
                async for chunk in response.content.iter_chunked(chunk_size):
                    f.write(chunk)
                    pbar.update(len(chunk))

async def scrape_and_download_videos():
    # URL of the collection
    url = "https://www.youtube.com/"
    
    # Create videos directory if it doesn't exist
    videos_dir = Path("./videos")
    videos_dir.mkdir(exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to the collection page...")
        await page.goto(url)
        
        # Wait for the content to load
        await page.wait_for_selector(".g-item-list-entry", timeout=60000)
        print("Page loaded successfully!")
        
        # Extract all download links
        download_links = await page.evaluate("""
            () => {
                const items = document.querySelectorAll('.g-item-list-entry');
                return Array.from(items).map(item => {
                    const downloadLink = item.querySelector('.icon-download').parentElement.href;
                    const filename = item.querySelector('.g-item-list-link').textContent.trim();
                    return { url: downloadLink, filename: filename };
                });
            }
        """)
        total_videos = len(download_links)
        
        # Read node value from file
        node = None
        try:
            with open('node.txt', 'r') as f:
                node = f.read().strip()
        except FileNotFoundError:
            print("node.txt file not found. Using default node.")
            node = None
        
        videos_per_node = total_videos // 4  # Assuming 4 nodes for distribution

        if node is not None:
            try:
                node_num = int(node)
                start_index = (node_num - 1) * videos_per_node
                end_index = start_index + videos_per_node
                download_links = download_links[start_index:end_index]
                print(f"Running as node {node_num}, downloading videos {start_index+1} to {min(end_index, total_videos)}")
            except ValueError:
                print(f"Invalid node value: {node}. Downloading all videos.")
        print(f"Found {len(download_links)} video files to download.")
        
        async with aiohttp.ClientSession() as session:
            for item in download_links:
                video_path = videos_dir / item['filename']
                if video_path.exists():
                    print(f"File {item['filename']} already exists. Skipping...")
                    continue
                
                print(f"Downloading {item['filename']}...")
                try:
                    await download_file(session, item['url'], video_path)
                    print(f"Successfully downloaded {item['filename']}")
                except Exception as e:
                    print(f"Error downloading {item['filename']}: {e}")
        
        await browser.close()
        print("All downloads completed!")

if __name__ == "__main__":
    asyncio.run(scrape_and_download_videos())