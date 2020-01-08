FROM python:3.7.6
COPY s3qlprometheus.py /app/s3qlprometheus.py
RUN pip3 install prometheus_client argparse
EXPOSE 6530
ENTRYPOINT ["python3","/app/s3qlprometheus.py"]
CMD ["--path","/data","--port","6530"]
