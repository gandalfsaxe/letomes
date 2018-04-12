# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# RUN apt-get install g++
# RUN wget https://cmake.org/files/v3.11/cmake-3.11.0.tar.gz
# RUN tar -xzf cmake-3.11.0.tar.gz
# RUN cmake-3.11.0/bootstrap
# RUN cmake-3.11.0/make
# RUN cmake-3.11.0/make install

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
# CMD ["python", "examples/_ex2.py"]