### Generated by ChatGPT ###

FROM python:3.11-slim
LABEL version="1.1"

# 安裝 mitmproxy
RUN pip install --no-cache-dir mitmproxy

# 建立工作資料夾
WORKDIR /app

# 開放 mitmproxy 的預設 port（8080）
EXPOSE 8080

# 預設執行 mitmproxy 的命令行界面
CMD ["mitmproxy", "--mode", "regular"]
