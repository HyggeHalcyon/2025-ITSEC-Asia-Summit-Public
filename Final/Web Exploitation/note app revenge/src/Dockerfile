FROM python:3.10

ENV USER=dreamhack
RUN adduser --disabled-password -u 1337 $USER

RUN apt-get update -y && apt-get install -y \
    python3-pip \
    build-essential \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN install -d -m 0755 /etc/apt/keyrings && \
    wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null && \
    gpg -n -q --import --import-options import-show /etc/apt/keyrings/packages.mozilla.org.asc | awk '/pub/{getline; gsub(/^ +| +$/,""); if($0 == "35BAA0B33E9EB396F59CA838C0BA5CE6DC6315A3") print "\nThe key fingerprint matches ("$0").\n"; else { print "\nVerification failed: the fingerprint ("$0") does not match the expected one.\n"; exit 1; } }' && \
    echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | tee /etc/apt/sources.list.d/mozilla.list > /dev/null && \
    printf 'Package: *\\nPin: origin packages.mozilla.org\\nPin-Priority: 1000\\n' | tee /etc/apt/preferences.d/mozilla > /dev/null && \
    apt-get update && \
    apt-get install -y firefox && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

ENV GECKODRIVER_VERSION v0.34.0
RUN wget https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz \
    && tar -xzf geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz \
    && chmod +x /usr/local/bin/geckodriver

WORKDIR /challenge/app
COPY ./app /challenge/app
COPY main.py /challenge

RUN chmod 777 /challenge/app
RUN chmod 555 /challenge/main.py
RUN rm -rf /challenge/Dockerfile


COPY requirements.txt /challenge/app
RUN pip3 install -r requirements.txt

CMD ["python3","-u","/challenge/main.py"]