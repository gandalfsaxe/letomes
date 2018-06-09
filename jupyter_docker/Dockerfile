# Use an official Python runtime as a parent image
FROM jupyter/datascience-notebook

# Copy the current directory contents into the container at /app
ADD . .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container


# Define environment variable
ENV LD_LIBRARY_PATH /app/libsnopt7_cpp.so
