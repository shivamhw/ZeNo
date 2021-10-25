FROM zakaryan2004/userbot_docker:latest
ENV PATH="/usr/src/app/bin:$PATH"
WORKDIR /usr/src/app
RUN git clone https://github.com/shivamhw/ZeNo.git -b zeno-docker ./
RUN pip install -r requirements.txt
CMD ["bash","scripts/start.sh"]
