# 🐍 Minimal Python image
FROM python:3.11-slim

# 🔧 Install Firefox ESR & Geckodriver dependencies
RUN apt-get update && apt-get install -y \
    curl wget unzip gnupg \
    firefox-esr \
    libglib2.0-0 libnss3 libgconf-2-4 libxss1 \
    libasound2 libxtst6 libxrandr2 libgtk-3-0 \
    libdbus-glib-1-2 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxfixes3 libxrender1 \
    fonts-liberation xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# 🦊 Install Geckodriver
ENV GECKODRIVER_VERSION=v0.34.0
RUN curl -sL "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" | \
    tar -xz -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver \
    && geckodriver --version

# 💻 Set Streamlit-friendly environment
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 📁 App directory setup
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 🚀 Entry point
CMD streamlit run home_page.py --server.port=${PORT:-8501}