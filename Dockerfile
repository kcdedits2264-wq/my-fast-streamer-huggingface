FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV PORT=7860
EXPOSE 7860
CMD ["python", "bot.py"]
