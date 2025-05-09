# AutoCommentOnLinkedin 🚀

This FastAPI-based automation tool uses Selenium to log into LinkedIn and post comments on a specified LinkedIn post. It is ideal for automating engagement with posts programmatically using a backend API.

---

## 🔧 Features

- 🔐 Secure LinkedIn login via `.env` credentials
- 💬 Auto-comment on any LinkedIn post URL
- 🌐 REST API built with FastAPI
- 🧪 WebDriver automation with Selenium
- 🧰 Built-in exception handling for robust error reporting

---

## 📁 Project Structure

AutoCommentOnLinkedin/
│
├── main.py # FastAPI app with LinkedIn automation logic
├── .env # Your LinkedIn credentials (not pushed)
├── requirements.txt # Python dependencies
└── README.md # Project documentation



---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Muskanrath2234/AutoCommentOnLinkedin.git
cd AutoCommentOnLinkedin

2. Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt


4. Create a .env file with your LinkedIn credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_secure_password
⚠️ Never share this file or commit it to GitHub.

▶️ Run the FastAPI App
bash
uvicorn main:app --reload

API will be available at:
http://127.0.0.1:8000

Interactive Swagger docs:
http://127.0.0.1:8000/docs


📫 API Endpoint
POST /comment-linkedin-post

Request JSON:
json
{
  "post_url": "https://www.linkedin.com/posts/xyz...",
  "comment_text": "Awesome post! Thanks for sharing."
}

Response:
json
{
  "status": "success",
  "message": "Comment posted successfully",
  "post_url": "https://www.linkedin.com/posts/xyz..."
}

🛑 Disclaimer
This project is for educational purposes only.
Use at your own risk — automating actions on LinkedIn may violate their Terms of Service.
It’s highly recommended to use a test account to avoid the risk of account suspension.


















