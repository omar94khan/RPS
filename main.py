import json
import base64
import logging
import numpy as np
from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
import itertools
import threading
from RPSGoalSeek import goalSeek, goalSeekwithEMI
import pandas as pd
import os
from os.path import join, dirname
app = Flask(__name__)
CORS(app)

app.config.from_pyfile("env/config.py")

my_blueprint = Blueprint('my_blueprint', __name__, url_prefix=app.config.get("ROUTER_PATH"))

workers = int(os.getenv('GUNICORN_PROCESSES', '2'))

threads = int(os.getenv('GUNICORN_THREADS', '4'))

bind = os.getenv('SERVER_HOST') + ":" + os.getenv('SERVER_PORT')

max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', '50'))
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/hello')
def hello():
    return jsonify(message='Hello, World!')

@my_blueprint.route('/rpsgenerate', methods=['POST'])
def rpsgenerate():
    print("Request Received: ",request.json)
    data = request.json  # Use request.form if data is being sent as form data
    

    FinanceAmount = data.get('FinanceAmount')
    ProfitRate = data.get('ProfitRate')
    TenorMonths = data.get('TenorMonths')
    PayDay = data.get('PayDay')
    DisbursementDate = data.get('DisbursementDate')
    GracePeriodDate = data.get('GracePeriodDate')
    FirstEMIDate = data.get('FirstEMIDate')
    TakafulFactor = data.get('TakafulFactor')
    repaymentMethod = data.get('repaymentMethod')
    GracePeriodProfitRate = data.get('GracePeriodProfitRate')
    

    result = goalSeek(
        FinanceAmount=FinanceAmount,
        ProfitRate=ProfitRate,
        TenorMonths=TenorMonths,
        PayDay=PayDay,
        DisbursementDate=DisbursementDate,
        GracePeriodDate=GracePeriodDate,
        FirstEMIDate=FirstEMIDate,
        TakafulFactor=TakafulFactor,
        repaymentMethod=repaymentMethod,
        GracePeriodProfitRate=GracePeriodProfitRate
    )
 
   
    result_data = json.loads(result)

    return jsonify(result_data)

@my_blueprint.route('/rpsgeneratewithEMI', methods=['POST'])
def rpsgeneratewithEMI():
    print("Request Received: ",request.json)
    data = request.json  # Use request.form if data is being sent as form data

    FinanceAmount = data.get('FinanceAmount')
    Emi = data.get('EMI')
    TenorMonths = data.get('TenorMonths')
    PayDay = data.get('PayDay')
    DisbursementDate = data.get('DisbursementDate')
    GracePeriodDate = data.get('GracePeriodDate')
    FirstEMIDate = data.get('FirstEMIDate')
    TakafulFactor = data.get('TakafulFactor')
    repaymentMethod = data.get('repaymentMethod')
    GracePeriodProfitRate = data.get('GracePeriodProfitRate')

    
    result = goalSeekwithEMI(
        FinanceAmount=FinanceAmount,
        EMI=Emi,
        TenorMonths=TenorMonths,
        PayDay=PayDay,
        DisbursementDate=DisbursementDate,
        GracePeriodDate=GracePeriodDate,
        FirstEMIDate=FirstEMIDate,
        TakafulFactor=TakafulFactor,
        repaymentMethod=repaymentMethod,
        GracePeriodProfitRate=GracePeriodProfitRate
    )
 
   
    result_data = json.loads(result)

    return jsonify(result_data)

app.register_blueprint(my_blueprint)
    
    
if __name__ == "__main__":
    app.run(host=app.config.get("SERVER_HOST"), port=int(app.config.get("SERVER_PORT")), debug=False)

