# Platform configuration
APPNAME = 'DigiPay'
TOKEN_SECKEY = 'c780e7ea39c7c94d4eed4650a3ed5c7b96531cabe9344c3d'
TOKEN_SALT = '5acfbac31a52b54862f8f8cc9f63f6qw'
MOB_ENC_SALT = '5acfbac31a52b54862f8f8cc9f63f6qw'
ENCRYPTION_SALT = '5acfbac31a52b54862f8f8cc9f63f6qw'
STATIC_ENCKEY = 'c780e7ea39c7c94d4eed4650a3ed5c7b96531cabe9344c3d'
FCM_TOKEN = 'AAAATBoWwtM:APA91bEv28A0Ev_ZRkmY4FGteqZWmpIPHkemb1RwnGHTQqBHckFey56beZSE-AVR3G2RhF6apV6uqDUhaSH_qvMRjdQBRp10aHgt6ZT_sxWkAgvhdByL8MftTf-I8_L3UNMM3rtgYpzv'

OPT_AACCESS_MOB = 'N'
OPT_AACCESS_WIN = 'Y'
CHECKSUM_SALT = '5acfbac31a52b54862f8f8cc9f63f6qw'
MAX_TERMINALS = 2
SERVICE_START = '00:02:00'
SERVICE_END = '23:05:00'
FT_STARTTIME = '00:02:00'
FT_ENDTIME = '23:05:00'

# RECON APP configuration
RECON_CLIENT = 'R001'
RECON_TOKEN = 'c+cNh7y44v4wLjb30U2xwcbimGz0ci4VoSxmQvhC94o='

# Profile API configuration
PRO_CLIENT = 'P001'
PRO_TOKEN = 'c+cNh7y44v4wLjb30U2xwcbimGz0ci4VoSxmQvhC94o='
PRO_URL = 'http://10.1.82.59/profile/'
PRO_VLEINFO = 'info/vle'
PRO_MASTER = 'info/master'
PRO_TIMEOUT = 45

# AUA API Configs
AUA_CLIENT = 'CSC-DGP'
AUA_TOKEN = 'd911017ca56b2a76bh319d9110176bh3'
AUA_TIMEOUT = 10
AUA_ATTEMPT = 3
AUA_URL = 'http://demogateway.csccloud.in/v2/gateway/appmanage/engine/format/json'
AUA_LAG = 5
AUA_CNT = 200
AUA_AC = 'STGCSC0001'
AUA_SA = 'STGCSC0001'
AUA_LK = 'MKIbBQSdws92gemAaS8xknFtikACUtQPqQE-1Wfhf7T_SjCN7lsULFA'
BIOAUA_LK = 'MGLinxdXM_0QaVAf0aNAuxPPz2kiI8P-zvELTILqXUM4TAQKfFJO3lo'
UID_AUTH_VER = '2.5'

# PINPAD CONFIG
PINPAD_SALT = 'sPJ3lM9GaxPEdeC6OqJmdsE8wdOWdDh4'
PINPAD_KEY = '4LVxNoqnUBTB8Kpzlyu4r8mfs2YRHuT9cjNZ0ghKRqAdYu'
PINPAD_RATE = 0.5
PINPAD_CSCCOM = 80
PINPAD_MINSLAB = 20000
PINPAD_MAXCOM = 1500
PINPAD_REQCODE = 61
PINPAD_TXNTYPE = 'CP'

# AEPS PRE-PRODUCTION 
ACQ_1 = {
    'ACQUIRER_CODE': '210019',
    'ACQUIRER_ID': 'CZU',
    'GATEWAY_URI': 'http://122.15.117.170:8081/aeps',
    'ACQUIRER_BANK': 'IndusInd Bank Limited',
    'ACQUIRER_STATUS': 'Y'
}

ACQ_2 = {
    'ACQUIRER_CODE': '210019',
    'ACQUIRER_ID': 'CZU',
    'GATEWAY_URI': 'http://122.15.117.170:8081/aeps',
    'ACQUIRER_BANK': 'IndusInd Bank Limited',
    'ACQUIRER_STATUS': 'Y'
}

ACQUIRER_CODE = '210019'
ACQUIRER_ID = 'CZU'
GATEWAY_URI = 'http://122.15.117.170:8081/aeps'

# ARCHIVE CONNECT TEMPLATE  
AEPS = {
    'BE_REQCODE': '31',
    'BE_TXNTYPE': 'BE',
    'BE_TIMEOUT': 45,
    'BE_INTERFEE': 'N',
    'MS_REQCODE': '90',
    'MS_TXNTYPE': 'MS',
    'MS_TIMEOUT': 45,
    'MS_INTERFEE': 'Y',
    'MS_FEETYPE': 'F',
    'MS_FEEAMT': '300',
    'CW_REQCODE': '01',
    'CW_TXNTYPE': 'CW',
    'CW_TIMEOUT': 65,
    'CW_REVTIME': 65,
    'CW_REVMAXNO': 4,
    'CW_INTERFEE': 'Y',
    'CW_FEETYPE': 'D',
    'CW_FEEAMT': '0.5',
    'CW_MINSLAB': '10000',
    'CW_MAXIFEE': '1500',
    'CW_SPAMTXN': 5,
    'CW_SPAMAMT': '4000000',
    'CW_MINAMT': 10000,
    'CW_MAXAMT': 1000000,
    'CW_AMTMOD': 100,
    'CD_BAVREQCODE': '32',
    'CD_CDAREQCODE': '21',
    'CD_BAVTXNTYPE': 'BAV',
    'CD_CDATXNTYPE': 'CDA',
    'CD_CDACOUNTER': 4,
    'CD_BAVTIMEOUT': 65,
    'CD_CDATIMEOUT': 65,
    'CD_CDRTIMEOUT': 25,
    'CD_INTERFEE': 'Y',
    'CD_FEETYPE': 'D',
    'CD_FEEAMT': '0.5',
    'CD_MINSLAB': '10000',
    'CD_MAXIFEE': '1500',
    'CD_MINAMT': 10000,
    'CD_MAXAMT': 1000000,
    'CD_AMTMOD': 100
}

#  DMT OTP CONFIGURATION 
DMTOTP = {
    'REMADD_TPL': '',
    'BENEADD_TPL': '1007981150630218684',
    'DMT_AUTHORIZE': '1007646419394704825',
    'DMT_RECEIPT': '',
    'OTP_KEYTOKEN': 'H0Ioi0S55Hbm544zGl525DZmwnKEsAhg3cLyvP4VqpY=',
    'OTP_DAYLIMIT': 100,
    'OTP_VALIDITY': 1800,
    'OTP_RES_MINL': 60,
    'OTP_RES_MAXL': 600,
    'OTP_RTRY': 3,
    'OTP_VERIFYCALL': 'N'
}

# DMT charges configuration
DMT_MINAMOUNT = 100
DMT_MINCHARGE = 1000
DMT_CHARGERATE = 1
DMT_REMITTERMAX = 2500000
DMT_BENEMAX = 5000000
DMT_TRANSFERMAX = 500000
DMT_REQCODE = '81'
DMT_TXNTYPE = 'MT'
DMT_IBLCHARGE = 250
GST_RATE = 18
VLE_SHARE = 80
TDS_RATEPAN = 5
TDS_RATENOPAN = 20
TDS_RATENORET = 10

#  IMPS/NEFT transfer charges 
NEFT_CHARGES = 0
IMPS_UP25000 = 200
IMPS_GT25000 = 700
IMPS_CSCSHARE = 300
DSP_TXNCHARGE = 0
MIN_PAYOUT = '5000'
IMPS_MAXPAYOUT = '20000000'
NEFT_MAXPAYOUT = '50000000'
DSP_MAXPAYOUT = '20000000'
PT_REQCODE = '99'
PT_TXNTYPE = 'PT'

# INDUS DMT OTP CONFIGURATION 
IBLDMT = {
    'DMT_TRANMODE': 'NEFT',
    'DEBITAC': '100034654715',
    'CUSTOMER_ID': '31961106',
    'CHECKER_ID': 'swapnil',
    'AGENT_ID': 'AGT2308',
    'CLIENT_ID': 'c6af0546-8ee7-4dc1-b0e7-57eaf9021d0d',
    'CLIENT_SECRET': 'mL5eG1sH5wP0fO1iK8kG7gY3jI2pO8pW6aG7vT5dM5pJ4hA3cP',
    'DMT_BASEURI': 'https://ibluatapig.indusind.com/app/uat/bcsynchronousapi/',
    'DMT_TIMEOUT': 120,
    'API_VERBOSE': 'NO',
    'DMT_PROCESSURI': 'ISync/ProcessTxn',
    'DMT_STATUSURI': 'ISync/StatusEnq',
    'DMT_OTPVALURI': 'ConfirmReturnTransaction',
    'DMT_OTPGENURI': 'RetriggerOTP',
    'DMT_RETSTATUSURI': 'ReturnTrxnStatus'
}

# INDUS NEFT/IMPS CONFIGURATION 
IBLFT = {
    'DEBITAC': '200000250043',
    'CUSTOMER_ID': '11218819',
    'CHECKER_ID': 'swapnil',
    'AGENT_ID': 'AGT2308',
    'CLIENT_ID': 'c6af0546-8ee7-4dc1-b0e7-57eaf9021d0d',
    'CLIENT_SECRET': 'mL5eG1sH5wP0fO1iK8kG7gY3jI2pO8pW6aG7vT5dM5pJ4hA3cP',
    'FT_BASEURI': 'https://ibluatapig.indusind.com/app/uat/ISync/',
    'FT_TIMEOUT': 120,
    'API_VERBOSE': 'NO',
    'FT_PROCESSURI': 'ProcessTXn',
    'FT_STATUSURI': 'StatusEnq'
}

# DSP EWALLET API configuration
DSPW_CLIENT = 'EW01'
DSPW_TOKEN = 'c+cNh7y44v4wLjb30U2xwcbimGz0ci4VoSxmQvhC94o='
DSPW_URL = 'https://payuat.csccloud.in/'
DSPW_TRANSFER = 'topup/digipay'
DSPW_TXNSTATUS = 'topup/digipay/status'
DSPW_TIMEOUT = 45

API_VERBOSE = 'N'
WT_REQCODE = '85'
WT_TXNTYPE = 'WT'

# Wallet API configuration
WAL_CLIENT = 'W01'
WAL_TOKEN = 'c+cNh7y44v4wLjb30U2xwcbimGz0ci4VoSxmQvhC94o='
WAL_URL = 'http://10.1.82.165/'
WAL_FETCH = 'digipay/fetch'
WAL_DEBIT = 'digipay/debit'
WAL_CREDIT = 'digipay/credit'
WAL_REVERSAL = 'digipay/reversal'
WAL_RECOVERY = 'digipay/recovery'
WAL_TIMEOUT = 90
WAL_MINBALANCE = 10000
LOG_DEBUG = 'DEBUG'
LOG_INFO = 'INFO'
LOG_ERROR = 'ERROR'
LOG_CRIT = 'CRITICAL'
LOG_WARNING = 'WARNING'
LOG_FILENAME = '/var/log/digipay.log'
LOG_LEVEL = 'DEBUG'

# Kafka configurations
KAFKA_HOST = '10.1.82.196'
KAFKA_PORT = '9092'
KAFKA_BROKER = '10.1.82.196:9092'
KAFKA_TOPIC = 'CP'
KAFKA_GROUP = 'DigiPay'
KAFKA_SUBSCRIBE = 'PUSH'

# SMS configurations
SMS_URL = 'http://bulksms.mysmsmantra.com:8080/WebSMS/SMSAPI.jsp'
SMS_USER = 'CSCIND'
SMS_PASSWORD = 'digi123'
SMS_SENDER_ID = 'CSCIND'
SMS_TEMPLATE = 'Thank you for using DigiPay. Your transaction of Rs.{amount} for {service} was successful. Txn ID: {txn_id}.'

# EMAIL configurations
EMAIL_SENDER = 'noreply@csc.gov.in'
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USERNAME = 'digipay@gmail.com'
EMAIL_PASSWORD = 'digipay@123'
EMAIL_TEMPLATE = 'templates/email_template.html'

# TRANSACTION STATUS
TXN_PENDING = 'Pending'
TXN_SUCCESS = 'Success'
TXN_FAILURE = 'Failure'
TXN_REVERSAL = 'Reversal'
TXN_INITIATED = 'Initiated'
TXN_INITREVERSE = 'InitReverse'

# SERVICE STATUS
SERVICE_ACTIVE = 'Active'
SERVICE_INACTIVE = 'Inactive'

# REPORTS
REPORTS_PATH = '/home/ubuntu/DigiPay/reports/'


# Logs Enabler
LOG_IBL_REQ = 'N'
LOG_DEBIT_WAL = 'N'

PAYOUT_DISABLE = 'N'
BALENQ_DISABLE = 'Y'
CASHWD_DISABLE = 'N'
CASHDP_DISABLE = 'N'
MINIST_DISABLE = 'N'
WALTOP_DISABLE = 'N'

# Taru Changes Below this line
BANKCODE = 'CZU'  # Bank code for acquirer  CZU
SWITCH_TYPE = 'AEPS'  # AEPS Switch Type
ACQUIRERID = '210031'  # Acquirer ID
AEPS_DATE = 'Y-m-d\TH:i:s+05:30'  # AEPS Date Time format
AEPS_VER = '2.0'  # AEPS Version configured
GW_SWITCHIP = '192.168.48.237'  # AEPS Date Time format
# Auth AUA Config
AUTHAC = 'STGCSC0001'  # Bank IN code for acquirer 210031
AUTHSA = 'STGCSC0001'  # Bank code for acquirer  CZU
BIOAUTHLK = 'MKIbBQSdws92gemAaS8xknFtikACUtQPqQE-1Wfhf7T_SjCN7lsULFA'
AUTHLK = 'MFnHlEPlzdulGfAr_1Ao0tJ1G-Z1G5g0lanUuU0HoYE8IDykZjKIMwo'
AEPS_ENUM = {
    'BIOAUTH': '00',  # bio auth - bioauth
    'PURCHASE': '21',  # purchase - purchase
    'WITHDRAW': '22',  # cash withdraw - withdraw
    'DEPOSIT': '23',  # cash deposit - deposit
    'TRANSFER': '25',  # fund trasnfer - transfer
    'ISSBIOAUTH': '26',  # issuer bio auth - issuerbio
    'SHGWITHDRAW': '27',  # SHG cash withdraw - shgwithdraw
    'SHGDEPOSIT': '28',  # shg cash deposit - shgdeposit
    'SHGTRANSFER': '29',  # shg fund transfer -  shgtransfer
    'REQBIOAUTH': '32',
}
# AEPS Time out
CD_TIMEOUT = 65  # Cash Deposit Timeout
CP_TIMEOUT = 65  # Purchase Timeout

# HSM Digital Signature Configs
REQ_SIGN = 'HSM'
HSM_CLIENTID = 'HSM001'
HSMS_URI = 'http://10.1.79.150:8080/cryptogateway/sign/hsm/bbps'  # NOIDA

# Changes done by Taru Below this line
CRYPT_KEY = 'c+cNh7y44v4wLjb30U2xwcbimGz0ci4VoSxmQvhC94o='
AEPS_URI = 'http://10.1.76.91:80/aeps'
CW_TIMEOUT = 65  # Cash Withdraw Timeout
AEPS_GENOUT = 65  # AEPS timeout for generic
AEPS_TXNOUT = 90  # AEPS timeout for transaction

# Log Configuration
LOG_FLAG = 'Y'  # Enable file Logging across
LOG_SET = {
    'HEARBEAT_REQ': 'Y',  # heartbeat
    'HEARBEAT_RES': 'Y',

    'BIOAUTH_REQ': 'Y',  # bio authentication
    'BIOAUTH_RES': 'Y',

    'MINIBAL_REQ': 'Y',  # mini statement balance
    'MINIBAL_RES': 'Y',

    'CASHWITH_REQ': 'Y',  # withdrawal
    'CASHDEPO_REQ': 'Y',  # deposit
    'FUNDTRNS_REQ': 'Y',  # fund transfer
    'PURCHASE_REQ': 'Y',  # purchase

    'RESPPAY_LOG': 'Y',  # pay response logs
    'RESPCHK_LOG': 'Y',  # pay response logs
}
CLIENT_ID = 'APP01'  # onboarding client ID
QUEUE_URL = 'http://localhost/aeps/nodesim'
QUEUE_TIMEOUT = 30
BANKIN = '100031'
GW_BASEURL = 'https://192.168.48.237/aeps/'  # AEPS Date Time format

EOD_START = '23:00:00'  # EOD Heartbeat Start
EOD_END = '23:03:00'
AEPS_STATUS_URI = 'http://10.1.76.91:80/'  # EOD Heartbeat end
