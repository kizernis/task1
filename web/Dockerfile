FROM python:3.11.3-alpine
RUN pip install --root-user-action=ignore --no-cache-dir --upgrade pip setuptools
RUN addgroup app && adduser -S -G app app
WORKDIR /app
COPY . .
RUN chown -R app:app /app
USER app
ENV PATH="/home/app/.local/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt && chmod +x docker-entrypoint.sh wait-for
# EXPOSE 8000
CMD ["./docker-entrypoint.sh"]
