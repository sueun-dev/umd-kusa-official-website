<img width="1026" alt="Screenshot 2024-09-05 at 19 13 02" src="https://github.com/user-attachments/assets/3eb9b34c-c705-4cbf-94e1-9e30dde760a3">

The diagram above represents the architecture of the KUSA UMD official website, showing the interaction between the user, frontend (JavaScript and HTML), backend (Flask), and the database (SQLAlchemy).

### KUSA UMD Official Website

---

This repository contains the source code for the official website of the Korean Undergraduate Student Association (KUSA) at the University of Maryland. The website was built using Flask, HTML, CSS, JavaScript, and PostgreSQL, and has been deployed on a Google Cloud Platform (GCP) Compute Engine instance with HTTPS and domain configuration.

## Key Features

- **Flask Backend**: The backend functionality, such as routing, authentication, and file uploads, was handled using Flask, a Python web framework.
- **PostgreSQL Database**: PostgreSQL was used to securely store and manage user-uploaded files and other structured data.
- **Secure File Uploads**: Users can upload PDFs and other allowed file types to the server, with files stored securely under size and type restrictions.
- **User Authentication and Security**: Basic authentication was implemented for login, with passwords hashed for secure storage. Additionally, after a certain number of failed login attempts, IP addresses are blocked for 24 hours to enhance security.
- **HTTPS Setup**: HTTPS certificates were configured on GCP to enhance website security, ensuring encrypted transmission of user data.
- **Frontend**: The frontend was built using HTML, CSS, and JavaScript, with a responsive design to ensure an optimal user experience across different devices.

## Technology Stack

- **Backend**: Flask (Python), Side (Django)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Google Cloud Platform (GCP) Compute Engine
- **Others**: HTTPS certificate, file upload security, user authentication

## Installation and Running Guide

1. **Activate the Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

2. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   Set the database URL in the `.env` file, then apply the database migrations:
   ```bash
   flask db upgrade
   ```

4. **Start the Server**
   ```bash
   nohup python3 app.py &
   ```

## Contribution and License

This project is the official website of the KUSA at the University of Maryland. The usage and distribution of the code are not permitted without the approval of the copyright holder. Please refer to the LICENSE file for more details.

### KUSA UMD 공식 웹사이트

---

이 저장소는 메릴랜드 대학교 한인 학부생 협회(KUSA)의 공식 웹사이트 소스 코드를 포함하고 있음. 이 웹사이트는 Flask, HTML, CSS, JavaScript, PostgreSQL을 사용해 구축되었으며, HTTPS와 도메인 구성을 통해 Google Cloud Platform(GCP) Compute Engine 인스턴스에서 배포되었음.

## 주요 기능

- **Flask 백엔드**: Flask라는 Python 웹 프레임워크를 사용해 라우팅, 인증, 파일 업로드 등의 백엔드 기능을 처리했음.
- **PostgreSQL 데이터베이스**: PostgreSQL을 사용해 사용자 업로드 파일 및 기타 구조화된 데이터를 안전하게 저장하고 관리했음.
- **안전한 파일 업로드**: 사용자가 PDF 및 허용된 파일 유형을 서버에 업로드할 수 있으며, 업로드된 파일은 크기와 파일 형식 제한과 함께 안전하게 저장되었음.
- **사용자 인증 및 보안**: 기본 인증을 통해 로그인 기능을 구현했고, 비밀번호 해시화를 통해 안전한 사용자 인증을 제공했음. 또한, 잘못된 로그인 시도를 일정 횟수 이상 할 경우 24시간 동안 IP를 차단해 보안을 강화했음.
- **HTTPS 설정**: GCP에서 HTTPS 인증서를 설정해 웹사이트 보안을 강화했음. 이를 통해 사용자 데이터가 암호화되어 안전하게 전송되었음.
- **프론트엔드**: 웹사이트의 프론트엔드는 HTML, CSS, JavaScript로 구축되었으며, 반응형 디자인을 통해 다양한 기기에서 최적의 사용자 경험을 제공했음.

## 기술 스택

- **백엔드**: Flask (Python)
- **데이터베이스**: PostgreSQL
- **프론트엔드**: HTML, CSS, JavaScript
- **배포**: Google Cloud Platform (GCP) Compute Engine
- **기타**: HTTPS 인증서, 파일 업로드 보안, 사용자 인증

## 설치 및 실행 방법

1. **가상환경 활성화**
   ```bash
   source venv/bin/activate
   ```

2. **필요한 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **데이터베이스 설정**
   `.env` 파일에 데이터베이스 URL을 설정한 후, 데이터베이스 마이그레이션을 적용함.
   ```bash
   flask db upgrade
   ```

4. **서버 실행**
   ```bash
   nohup python3 app.py &
   ```

## 기여 및 라이선스

이 프로젝트는 메릴랜드 대학교 KUSA의 공식 웹사이트로, 코드 사용 및 배포는 저작권자의 승인 없이 불가함. 자세한 내용은 LICENSE 파일을 참조 바람.


Developed by Sueun Cho
Blockchain & Full Stack Developer
