from typing import List, Optional
from enum import Enum

from fastapi import FastAPI

from app.cluster_operator import ClusterOperator
from app.wf_temp_operator import WorkflowTemplateOperator

ClusterOperator = ClusterOperator()
WorkflowTemplateOperator = WorkflowTemplateOperator()

class WorkflowTemplates(str, Enum):
    wf_temp1 = "data_collection_wf_temp"
    wf_temp2 = "data_processing_wf_temp"
    wf_temp3 = "data_validation_wf_temp"


description = """
Dataproc Service API helps you do awesome stuff. 🚀

## Dataproc 
Dataproc is a fully managed and highly scalable GCP service for running Apache Spark, Apache Flink, Presto, and 30+ open source tools and frameworks. 

## Users

You will be able to:

* **Create dataproc clusters**.
* **List all dataproc clusters**.
* **Get a dataproc cluster**.
* **Delete a dataproc cluster**.
* **Use dataproc workflow template** (you need to create demo workflow templates).
"""

app = FastAPI(
    title="Dataproc Service API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Yuya Tinnefeld",
        "url": "https://yuyatinnefeld-resume-xljcoys6wa-ew.a.run.app",
        "email": "yuyatinnefeld@gmail.com",
    },
    license_info={
        "name": "Visit Github",
        "url": "https://github.com/yuyatinnefeld/dataproc-api-service",
    },
    
)

@app.get("/")
def read_root():
    return {"Welcom to Dataproc FastAPI Service": "Setup your Google Environemt and Run Dataproc Clusters in Swagger UI"}

@app.get("/clusters/")
async def get_cluster_list():
    cluster_items = ClusterOperator.get_list()
    return cluster_items

@app.get("/clusters/get/{cluster_name}")
async def get_cluster(cluster_name: str):
    return ClusterOperator.get_a_cluster(cluster_name)

@app.post("/clusters/create/{cluster_name}")
async def create_cluster(cluster_name: str):
    new_cluster = ClusterOperator.create(cluster_name)
    return new_cluster

@app.delete("/clusters/delete/{cluster_name}")
async def delete_cluster(cluster_name: str):
    deleted_cluster = ClusterOperator.delete(cluster_name)
    return deleted_cluster
    
@app.get("/workflow-temp/{wf_temp_name}")
async def run_workflow_template(wf_temp_name: WorkflowTemplates):
    if(
        wf_temp_name.value == "data_collection_wf_temp" or 
        wf_temp_name.value == "data_processing_wf_temp" or
        wf_temp_name.value == "data_validation_wf_temp"
    ):
        WorkflowTemplateOperator.start(wf_temp_name)
        return {"wf_temp_name": wf_temp_name, "job": f"starting..."}
    else:
        return {"wf_temp_name": "use a defined template", "job": " - "}

