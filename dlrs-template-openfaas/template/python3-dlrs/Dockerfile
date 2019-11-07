FROM openfaas/classic-watchdog:0.15.4 as watchdog

FROM clearlinux/stacks-dlrs-mkl:v0.4.1

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

RUN groupadd -r dlrsfunc && useradd dlrsfunc -r -g dlrsfunc
WORKDIR /home/dlrsfunc
RUN chown dlrsfunc /home/dlrsfunc

COPY function /home/dlrsfunc/function

WORKDIR /home/dlrsfunc/function

RUN pip install -r requirements.txt

RUN touch __init__.py
RUN chown dlrsfunc /home/dlrsfunc/function

RUN chmod +x helper_script.sh && ./helper_script.sh

USER dlrsfunc

ENV fprocess="python3 main.py"

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
