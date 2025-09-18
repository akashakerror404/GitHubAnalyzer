

---

# 📊 GitHub Analyzer

GitHub Analyzer is a Django-based web application that allows users to fetch and analyze GitHub user profiles and their repositories.
It uses the **GitHub REST API** to retrieve profile details, repository statistics, and stores them in a local database for future access.

---

## 🚀 Features

* 🔍 Search GitHub users by username
* 📑 Fetch profile details (name, followers, following, public repositories, account creation date)
* 📦 Retrieve repository details (language, stars, forks, last updated)
* 💾 Store and update data in the database
* 🗄️ Option to fetch stored data from the local database
* ⚡ Django messages for error handling and notifications

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Database:** SQLite (default) / PostgreSQL (optional)
* **Frontend:** HTML, CSS (Django Templates)
* **API Integration:** GitHub REST API (no authentication required for public data)

---

## 📂 Project Structure

```
github_analyzer/
│── github_analyzer/        # Main project configuration
│── github_api/             # Application for GitHub data handling
│   ├── models.py           # Database models
│   ├── views.py            # Core logic for API & DB fetch
│   ├── urls.py             # URL routing for app
│   ├── templates/          # HTML templates
│   └── static/             # CSS/JS assets (optional)
│── db.sqlite3              # Default SQLite database
│── manage.py               # Django management script
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/github-analyzer.git
   cd github-analyzer
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the development server**

   ```bash
   python manage.py runserver
   ```

6. **Access the app**
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📌 Usage

* Enter a GitHub username on the homepage.
* The app will fetch user profile + repositories from GitHub API.
* If data already exists in the DB, you can retrieve it using the **Fetch from DB** option.
* View detailed information such as:

  * User profile
  * Followers & following
  * Public repositories count
  * Repository details (stars, forks, last update, languages)

---





