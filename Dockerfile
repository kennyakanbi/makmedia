COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Replace CMD with entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
