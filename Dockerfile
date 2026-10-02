# أسس التعلّم في الذكاء الاصطناعي — Dr Merwan Roudane
# صورة للاستضافة الذاتية (Render / Railway / Fly.io / VPS).
# لا حاجة إليها إطلاقًا على Streamlit Community Cloud.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# منصّات كثيرة تُمرّر المنفذ عبر المتغيّر PORT؛ و8501 هو الافتراضي محلّيًّا.
ENV PORT=8501
EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import os,urllib.request;urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",8501)}/_stcore/health')"

CMD ["sh", "-c", "streamlit run streamlit_app.py \
     --server.port=${PORT:-8501} \
     --server.address=0.0.0.0 \
     --server.headless=true \
     --server.runOnSave=false \
     --browser.gatherUsageStats=false"]
