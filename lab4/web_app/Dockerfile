FROM python:3.8-alpine
COPY server/ /server/
WORKDIR /server
EXPOSE 8080
#CMD python3 -m http.server 8080


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
