from my_app import db


# envLabels = {
#     'env1': {'name': 'Rel11_GA_CDRM_OVM_FSCM_Pillar_Patch_(fuscdrmovm104)',
#              'orderprop': '/net/slc10xkv/scratch/atangudu/order_prop/Rel11OVM.prop',
#              'provfile': '/net/slc10xkv/scratch/atangudu/prov_plan/sprint_81.prop'},
#     'env2': {'name': 'Rel13_17.09A_CDRM_OVM_Long_Running',
#              'orderprop': '/net/slc10xkv/scratch/atangudu/order_prop/1709A.prop',
#              'provfile': '/net/slc10xkv/scratch/atangudu/prov_plan/sprint_81.prop'},
#     'env3': {'name': 'Rel13_17.11A_CDRM_DIT_(fuscdrmsmc166)',
#              'orderprop': '/net/slc10xkv/scratch/atangudu/order_prop/1711A.prop',
#              'provfile': '/net/slc10xkv/scratch/atangudu/prov_plan/sprint_81.prop'},
#     'env4': {'name': 'Rel13_FINC_Automation_Sandbox',
#              'orderprop': '/net/slc10xkv/scratch/atangudu/order_prop/FINCSandBox.prop',
#              'provfile': '/net/slc10xkv/scratch/atangudu/prov_plan/sprint_81.prop'},
#     'env5': {'name': 'CDRM_Test', 'orderprop': '/net/slc10xkv/scratch/atangudu/order_prop/cdrm_test.prop',
#              'provfile': '/net/slc10xkv/scratch/atangudu/prov_plan/sprint_81.prop'},
# }

class envLabels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    envLabel = db.Column(db.String(255))
    envName = db.Column(db.String(255))
    orderProp = db.Column(db.String(255))
    provFile = db.Column(db.String(255))

    def __init__(self, envLabel, envName, orderProp, provFile):
        self.envLabel = envLabel
        self.envName = envName
        self.orderProp = orderProp
        self.provFile = provFile

    def __repr__(self):
        return '<Environment %d>' % self.id


class faatLabels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faatLabel = db.Column(db.String(255))

    def __init__(self, faatLabel):
        self.faatLabel = faatLabel

    def __repr__(self):
        return '<FAAT LAbel : %d>' % self.faatLabel


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.BINARY(64))

    def __init__(self, username):
        self.username = username

class centralenvs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    envLabel = db.Column(db.String(255))
    envName = db.Column(db.String(255))
    orderProp = db.Column(db.String(255))
    provFile = db.Column(db.String(255))

    def __init__(self, envLabel, envName, orderProp, provFile):
        self.envLabel = envLabel
        self.envName = envName
        self.orderProp = orderProp
        self.provFile = provFile

    def __repr__(self):
        return '<Environment %d>' % self.id