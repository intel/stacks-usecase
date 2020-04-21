FROM alpine:latest
COPY template template
RUN tar -C template -cf init.tar .
CMD cat init.tar
