from my_app import app, db
from flask import render_template, request, redirect, url_for
from paramiko import client
from my_app.product.models import envLabels, faatLabels
from werkzeug import abort
from flask import Blueprint
import re


# trigger_blueprint = Blueprint('trigger', __name__)

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    envlabels = envLabels.query.all()  # Getting Env labels
    resEnvLabels = {}
    for envlabel in envlabels:
        resEnvLabels[envlabel.id] = {
            'envLabel': envlabel.envLabel,
            'envName': envlabel.envName,
            'orderProp': envlabel.orderProp,
            'provFile': envlabel.provFile
        }
    Client = connect_ssh("slc10xkv.us.oracle.com", "atangudu", "1989@nudeeP")
    command = "ade showlabels -series FAAT_PT.V2MIB_GENERIC | tail -10"
    commandOutput = []
    stdin, stdout, stderr = Client.exec_command(command)
    while not stdout.channel.exit_status_ready():
        # Print data when available
        if stdout.channel.recv_ready():
            alldata = stdout.channel.recv(1024)
            prevdata = b"1"
            while prevdata:
                prevdata = stdout.channel.recv(1024)
                alldata += prevdata
            commandOutput = (str(alldata.encode("utf8")).split('\n'))
    commandOutput = filter(None, commandOutput)
    # faatlabels = faatLabels.query.all() # Getting FAAT Labels
    # resFaatLabels={}
    # for faatLabel in faatlabels:
    #     resFaatLabels[faatLabel.id] = {
    #         'faatLabel':faatLabel.faatLabel
    #     }
    return render_template('home.html', envlabels=resEnvLabels, faatlabels=commandOutput)


@app.route('/welcome', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form['uname'] != 'admin' or request.form['psw'] != 'admin':
            return redirect(url_for('error'))
        else:
            return redirect(url_for('home'))  # url for uses def name for home.html


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/trigger', methods=['POST'])
def trigger():
    selectOption = request.form.get('runName')
    faatLabel = request.form.get('faatLabel')
    # Client = client.SSHClient()
    # Client.set_missing_host_key_policy(client.AutoAddPolicy())
    # Client.connect(hostname="slc10xkv.us.oracle.com", username="atangudu", password="1989@nudeeP")
    # if not Client:
    #     abort(404)
    Client = connect_ssh("slc10xkv.us.oracle.com", "atangudu", "1989@nudeeP")
    query_string = "SELECT orderProp,provFile FROM env_labels WHERE envLabel='{}'".format(selectOption.encode('utf-8'))
    result = db.engine.execute(query_string)
    envResult = result.fetchall()
    for row in envResult:
        envOrderProp = row[0].encode('utf-8')
        envProvFile = row[1].encode('utf-8')
    command = "/usr/local/packages/aime/dte/DTE3/bin/jobReqAgent -topoid 93289 -s /tmp -p LINUX.X64 -l " \
              "FAINTEG_MAIN_PLATFORMS_170905.1858 -report -e anudeep.tangudu@oracle.com,sandeep.s.srivastava@oracle.com -a /usr/local/packages/aime/dte/DTE -w " \
              "/scratch/atangudu/AUTO_WORK/job2 -topoalias=""R13_Auto_Sandbox_Run"" " \
              "PILLAR_TYPE=FSCM RunFaBATS:CMDOPTIONS='-parallel IS_ALM=true FA_TEMPLATE=%FA_TEMPLATE% " \
              "FAAT_LABEL={} " \
              "ORDER_INPUTFILE={}' " \
              "PROVISIONING_PLAN={} REE_PARAM=""OSPlayabackBrowser=Firefox""".format(faatLabel, envOrderProp,
                                                                                     envProvFile)
    stdin, stdout, stderr = Client.exec_command(command)
    while not stdout.channel.exit_status_ready():
        # Print data when available
        if stdout.channel.recv_ready():
            alldata = stdout.channel.recv(1024)
            prevdata = b"1"
            while prevdata:
                prevdata = stdout.channel.recv(1024)
                alldata += prevdata
            commandOutput = (str(alldata.encode("utf8")))
    dteId = refactor_commandOutput(commandOutput)
    return render_template("trigger.html", commandOutput=dteId)

    # return redirect(url_for('sendCommand_redirected', selectOption=selectOption, faatLabel=faatLabel))


def refactor_commandOutput(commandOutput):
    dteidMatch = re.search(r'\d{8} : SMC_LIGHTS_OUT_BATS', commandOutput, re.MULTILINE)  # PERL compatible
    dteId = re.search(r'\d{8}', dteidMatch.group(0))
    return dteId.group(0)


def connect_ssh(hostname, username, password):  # store credentials it in db
    Client = client.SSHClient()
    Client.set_missing_host_key_policy(client.AutoAddPolicy())
    Client.connect(hostname=hostname, username=username, password=password)
    if not Client:
        abort(404)
    return Client

# @app.route('/trigger/<faatLabel>/<selectOption>')
# def sendCommand_redirected(selectOption,faatLabel):
#     Client = client.SSHClient()
#     Client.set_missing_host_key_policy(client.AutoAddPolicy())
#     Client.connect(hostname="slc10xkv.us.oracle.com", username="atangudu", password="1989@nudeeP")
#     if not Client:
#         abort(404)
#     env = envLabels.get(selectOption.encode('utf-8'))
#     if not env:
#         abort(404)
#     envOrderProp = env['orderprop']
#     envProvFile = env['provfile']
#     command = "/usr/local/packages/aime/dte/DTE3/bin/jobReqAgent -topoid 93289 -s /tmp -p LINUX.X64 -l " \
#               "FAINTEG_MAIN_PLATFORMS_170905.1858 -report -e anudeep.tangudu@oracle.com,sandeep.s.srivastava@oracle.com -a /usr/local/packages/aime/dte/DTE -w " \
#               "/scratch/atangudu/AUTO_WORK/job2 -topoalias=""R13_Auto_Sandbox_Run"" " \
#               "PILLAR_TYPE=FSCM RunFaBATS:CMDOPTIONS='-parallel IS_ALM=true FA_TEMPLATE=%FA_TEMPLATE% " \
#               "FAAT_LABEL=FAAT_PT.V2MIBFIND_GENERIC_170907.0130.S " \
#               "ORDER_INPUTFILE={}' " \
#               "PROVISIONING_PLAN={} REE_PARAM=""OSPlayabackBrowser=Firefox""".format(envOrderProp, envProvFile)
#     stdin, stdout, stderr = Client.exec_command(command)
#     while not stdout.channel.exit_status_ready():
#         # Print data when available
#         if stdout.channel.recv_ready():
#             alldata = stdout.channel.recv(1024)
#             prevdata = b"1"
#             while prevdata:
#                 prevdata = stdout.channel.recv(1024)
#                 alldata += prevdata
#             commandOutput = (str(alldata.encode("utf8")))
#     return render_template("trigger.html", commandOutput=commandOutput)
