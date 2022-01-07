FROM python:3.7-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./resources /code/resources
COPY ./app /code/app
##########
#COPY CMD DEACTIVATED !!! 
#reason: This demo api service is public
#COPY ./conf /code/conf
##########
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]