# KUSA UMD Official Website

**Live Site**: [https://www.umdkusa.com](https://www.umdkusa.com)  
[![License](https://img.shields.io/badge/License-Proprietary-blue.svg)](LICENSE)

---

## 🌟 Highlights  
- **Modern Dependency Management**: Fully powered by Poetry for seamless package handling.  
- **Production-Ready Architecture**: Deployed on GCP Compute Engine with HTTPS/SSL.  
- **Security First**: Rate-limited authentication, encrypted file uploads, and IP blocking.  

---

## 🛠 Tech Stack  
**Backend**: Flask (Python 3.10+) | **Database**: PostgreSQL  
**Frontend**: HTML5, CSS3, Vanilla JS | **Infra**: GCP Compute Engine, Nginx, Certbot  

---

## 🚀 Quick Start with Poetry  

### 1. Clone & Install  
git clone https://github.com/umd-kusa/official-website.git  
cd official-website  
poetry install  # Installs all dependencies  

### 2. Configure Environment  
Create a `.env` file in the root directory:  
DATABASE_URL="postgresql://user:password@localhost:5432/kusa_db"  
SECRET_KEY="your-random-secret-key"  # Used for Flask session encryption   

### 3. Run the App  
poetry shell    # Activates the virtual environment  
python run.py   # Starts the Flask dev server  

---

## 🔒 Security Features  
- **Brute-Force Protection**: Blocks IPs after 5 failed login attempts (24-hour cooldown).  
- **File Upload Safeguards**:  
  - Strict PDF-only policy.  
  - Configurable size limits via `MAX_FILE_SIZE` in `.env`.  
  - Virus scanning for uploaded files (optional GCP integration).  

---

## ☁️ Deployment Guide  
1. **GCP Compute Engine Setup**:  
   - Ubuntu 22.04 LTS instance with firewall rules allowing HTTPS/HTTP.  
2. **HTTPS Configuration**:   
   sudo certbot --nginx -d umdkusa.com -d www.umdkusa.com  
3. **Run as Background Service**:  
   nohup poetry run python run.py &  # Persistent execution  

---

## 📜 License  
Proprietary software owned by the Korean Undergraduate Student Association (KUSA) at the University of Maryland.  
**Unauthorized use, modification, or distribution is strictly prohibited.**  

---

## 🇰🇷 한국어 요약  
**기술 스택**: Flask, PostgreSQL, GCP Compute Engine  
**주요 기능**:  
- Poetry 기반 의존성 관리  
- PDF 전용 안전한 파일 업로드  
- HTTPS 암호화 및 IP 차단 시스템  
**실행 방법**:  
1. `poetry install`으로 패키지 설치  
2. `.env` 파일에 데이터베이스 URL 설정  
3. `python run.py`로 서버 실행  

---


## Developer
**Developer**: Sueun Cho

**E-mail**:  sueun.dev@gmail.com

**LinkedIn**: [LinkedIn](https://www.linkedin.com/in/sueun-cho-625262252/) 


---

_Last Updated: February 05, 2025_