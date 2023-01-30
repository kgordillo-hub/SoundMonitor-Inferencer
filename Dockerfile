FROM public.ecr.aws/lambda/python:3.8
COPY requirements.txt lambda.py ${LAMBDA_TASK_ROOT}
COPY inferencer ${LAMBDA_TASK_ROOT}/
COPY data ${LAMBDA_TASK_ROOT}/
RUN pip3 install -r ${LAMBDA_TASK_ROOT}/requirements.txt
CMD [ "lambda.handler" ]