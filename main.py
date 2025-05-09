from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Request model
class LinkedInCommentRequest(BaseModel):
    post_url: str
    comment_text: str

# Setup Chrome WebDriver
def setup_driver():
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Optional: Headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except WebDriverException as e:
        raise HTTPException(status_code=500, detail=f"WebDriver setup failed: {str(e)}")

# LinkedIn login
def authenticate_linkedin(driver, email, password):
    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        email_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        email_input.send_keys(email)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(3)

        if "login" in driver.current_url:
            raise HTTPException(status_code=401, detail="Invalid LinkedIn credentials")
    except NoSuchElementException as e:
        raise HTTPException(status_code=500, detail=f"Login element not found: {str(e)}")
    except TimeoutException:
        raise HTTPException(status_code=500, detail="Login timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.post("/comment-linkedin-post")
def comment_on_post(request: LinkedInCommentRequest):
    driver = None
    try:
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not email or not password:
            raise HTTPException(status_code=400, detail="Missing credentials in environment variables")

        # Setup driver
        driver = setup_driver()

        # Login
        authenticate_linkedin(driver, email, password)

        # Open LinkedIn post
        try:
            driver.get(request.post_url)
            time.sleep(5)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to open post URL: {str(e)}")

        # Scroll down
        try:
            for i in range(0, 1000, 200):
                driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(0.5)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Scrolling failed: {str(e)}")

        # Click comment button
        try:
            wait = WebDriverWait(driver, 10)
            comment_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Comment']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_button)
            time.sleep(1)
            comment_button.click()
            time.sleep(2)
        except TimeoutException:
            raise HTTPException(status_code=500, detail="Comment button not found or not clickable")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to click comment button: {str(e)}")

        # Type the comment
        try:
            comment_area = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ql-editor")))
            comment_area.click()
            comment_area.send_keys(request.comment_text)
            time.sleep(1)
        except TimeoutException:
            raise HTTPException(status_code=500, detail="Comment area not visible")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to type comment: {str(e)}")

        # Submit the comment
        try:
            submit_button = driver.find_element(
                By.CSS_SELECTOR,
                "button.comments-comment-box__submit-button--cr.artdeco-button.artdeco-button--primary"
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(1)
            submit_button.click()
            time.sleep(3)
        except NoSuchElementException:
            raise HTTPException(status_code=500, detail="Submit button not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to submit comment: {str(e)}")

        return {
            "status": "success",
            "message": "Comment posted successfully",
            "post_url": request.post_url
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
