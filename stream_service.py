from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uvicorn
import os

app = FastAPI()
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"  # Path in Railway environment

@app.post("/start")
async def start_stream(video_url: str):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        options=chrome_options
    )
    
    try:
        driver.get(video_url)
        
        # Accept cookies if needed
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
            ).click()
        except:
            pass
        
        # Play the video
        driver.execute_script("document.querySelector('video').play()")
        
        # Enter fullscreen
        driver.execute_script("document.querySelector('video').requestFullscreen()")
        
        return {"status": "playing", "stream_url": video_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Keep the stream running (will be managed externally)
        pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
