from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uvicorn
import os
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/start")
async def start_stream(video_url: str):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # Use Chromedriver provided by Railway plugin
        driver = webdriver.Chrome(options=chrome_options)
        
        logger.info(f"Starting stream for: {video_url}")
        driver.get(video_url)
        
        # Accept cookies if needed
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
            ).click()
            logger.info("Accepted cookies")
        except:
            logger.info("No cookie acceptance needed")
        
        # Play the video
        driver.execute_script("document.querySelector('video').play()")
        logger.info("Video playback started")
        
        # Enter fullscreen
        driver.execute_script("document.querySelector('video').requestFullscreen()")
        logger.info("Entered fullscreen mode")
        
        return {"status": "playing", "stream_url": video_url}
    except Exception as e:
        logger.error(f"Stream error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Keep the driver running in the background
        # Railway will manage the process lifecycle
        pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
