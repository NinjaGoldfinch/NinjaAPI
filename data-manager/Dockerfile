FROM ubuntu:latest

# Update, then install python3, pip3 and virtualenv
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y virtualenv

# Create virtual environment
RUN virtualenv env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
RUN /env/bin/pip install --upgrade pip

# Set the working directory to /app

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt

RUN pip3 install -r requirements.txt

# Run app.py when the container launches
CMD [ "python3", "app.py" ]