from flask import Flask, jsonify, request
import base64
import json
import requests
import kiteconnect

app = Flask(__name__)

# Telegram Constants
TESTING_GROUP_ID = "-342024797"
SIGNAL_BOT_TOKEN = "720087545:AAFe4C2JyjB7r3hp2YO53mHfqEzQwKknjoE"
SIGNAL_BOT_URL = "https://api.telegram.org/bot{}".format(SIGNAL_BOT_TOKEN)
SIGNAL_BOT_SEND_URL = SIGNAL_BOT_URL+"/sendMessage?chat_id="+TESTING_GROUP_ID+"&text="
ALGOTRADE_BOT_TOKEN = "878159613:AAFEF_7UtZgkFbaLhsyP0ddlmT1L2m-MjaA"
ALGOTRADE_BOT_URL = "https://api.telegram.org/bot{}".format(ALGOTRADE_BOT_TOKEN)
ALGOTRADE_BOT_SEND_URL = ALGOTRADE_BOT_URL+"/sendMessage?chat_id="+TESTING_GROUP_ID+"&text="

# Zerodha Constants
KITE_API_KEY = "8k89pux7hxe58snm"
KITE_API_SECRET = "24uqvpxbalc9yc8nmnrb0ei4y9crhvke"

@app.route('/')
def hello():
    response = {
    "server": "Aws lambda",
    "status": "Working"
    }
    return jsonify(response)

@app.route("/kite_login", methods=["GET"])
def handle_request_token():
    '''
    Updates Kite Connect access tokens using obtained request token
    '''
    try:
        # Get url parameter request_token
        request_token = request.args.get('request_token')
        login_status = request.args.get('status')
        response = {
            "request_token": request_token,
            "login_status": login_status
        }
    
    except:
        return jsonify({
            'error': True,
            'function': "handle_request_token()",
            'description': "Updates Kite Connect access tokens using obtained request token"
        })
    
    return jsonify(response)

@app.route("/signal/<string:encoded_data>", methods=["GET"])
def get_signal_encoded(encoded_data):
    '''
    handles encoded signals from amibroker 
    and sends telegram notification
    '''
    try:
        # Decode the enoded string
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        # Convert to python dictionary
        trade_signal = json.loads(decoded_data)
        # Construct telegram message from trade signal
        telegram_msg = str(trade_signal).replace("'", "").replace(", ", "%0A").replace("{", "").replace("}", "")
        # Send telegram message
        requests.get(SIGNAL_BOT_SEND_URL+telegram_msg)

    except:
        return jsonify({
            'error': True,
            'function': "get_signal_encoded()",
            'description': "handles encoded signals from amibroker and sends telegram notification"
        })

    return jsonify({
        'status': True,
        'trade_signal': trade_signal
    })


if __name__ == '__main__':
    app.run(debug=True)