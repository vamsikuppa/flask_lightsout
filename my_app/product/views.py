from my_app import app
from flask import render_template, request, redirect, url_for
from paramiko import client
from my_app.product.models import envLabels
from werkzeug import abort
from flask import Blueprint

#trigger_blueprint = Blueprint('trigger', __name__)


@app.route('/')
def index():
    return render_template('home.html',envlabels=envLabels)


@app.route('/trigger', methods=['POST'])
def trigger():
    selectOption = request.form.get('runName')
    return redirect(url_for('sendCommand_redirected', selectOption=selectOption))
    # return render_template('trigger.html')


@app.route('/trigger/<selectOption>')
def sendCommand_redirected(selectOption):
    Client = client.SSHClient()
    Client.set_missing_host_key_policy(client.AutoAddPolicy())
    Client.connect(hostname="slc10xkv.us.oracle.com", username="atangudu", password="1989@nudeeP")
    if not Client:
        abort(404)
    command = "/usr/local/packages/aime/dte/DTE3/bin/jobReqAgent -topoid 93289 -s /tmp -p LINUX.X64 -l FAINTEG_MAIN_PLATFORMS_170905.1858 -report -e anudeep.tangudu@oracle.com,sandeep.s.srivastava@oracle.com -a /usr/local/packages/aime/dte/DTE -w /scratch/atangudu/AUTO_WORK/job2 -topoalias=""R13_Auto_Sandbox_Run"" PILLAR_TYPE=FSCM RunFaBATS:CMDOPTIONS='-parallel IS_ALM=true FA_TEMPLATE=%FA_TEMPLATE% FAAT_LABEL=FAAT_PT.V2MIBFIND_GENERIC_170907.0130.S ORDER_INPUTFILE=/net/slc10xkv/scratch/atangudu/order_prop/cdrm_test.prop' PROVISIONING_PLAN=/net/slc10xkv/scratch/atangudu/prov_plan/sprint_81.prop REE_PARAM=""OSPlayabackBrowser=Firefox"""
    stdin, stdout, stderr = Client.exec_command(command)
    while not stdout.channel.exit_status_ready():
        # Print data when available
        if stdout.channel.recv_ready():
            alldata = stdout.channel.recv(1024)
            prevdata = b"1"
            while prevdata:
                prevdata = stdout.channel.recv(1024)
                alldata += prevdata
            commandOutput= (str(alldata.encode("utf8")))
    return render_template("trigger.html",commandOutput=commandOutput)
