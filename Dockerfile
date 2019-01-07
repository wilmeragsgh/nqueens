FROM alejandrox1/ubuntu_miniconda

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
