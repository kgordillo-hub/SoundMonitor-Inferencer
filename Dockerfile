FROM public.ecr.aws/lambda/python:3.8
COPY inferencer requirements.txt data lambda.py ${LAMBDA_TASK_ROOT}
RUN pip3 install -r ${LAMBDA_TASK_ROOT}/requirements.txt
CMD [ "lambda.handler" ]