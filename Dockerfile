FROM gkbotzg/kpsmlx:v3

WORKDIR /usr/src/app

RUN chmod 777 /usr/src/app

COPY . .

RUN uv venv --system-site-packages

RUN uv pip install --no-cache-dir -U -r requirements.txt

CMD ["bash", "start.sh"]
