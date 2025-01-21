# Set base image (host OS)
FROM python:3.12

# Set the working directory in the container
WORKDIR /VW_FINANCEIRO_OBRA

# Copy the project files to the working directory
COPY . /VW_FINANCEIRO_OBRA

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run on container start
CMD [ "python", "./app.py" ]
