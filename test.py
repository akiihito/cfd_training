from __future__ import print_function
import sys
import ssl
import time
import datetime
import logging, traceback
import paho.mqtt.client as mqtt

IoT_protocol_name = "mqtt" ### 変更
aws_iot_endpoint = "a3u3pwl0o17i3l-ats.iot.ap-northeast-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)

# ca = "YOUR/ROOT/CA/PATH" ### 変更
# cert = "YOUR/DEVICE/CERT/PATH" ### 変更
# private = "YOUR/DEVICE/KEY/PATH" ### 変更

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

def ssl_alpn():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        # ssl_context.load_verify_locations(cafile=ca) ### 変更
        # ssl_context.load_cert_chain(certfile=cert, keyfile=private) ### 変更

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

if __name__ == '__main__':
    topic = "telemetry/myClientName" ### 変更
    try:
        mqttc = mqtt.Client(client_id='myClientName') ### 変更
        ssl_context= ssl_alpn()
        mqttc.tls_set_context(context=ssl_context)
        mqttc.username_pw_set('username', 'test') ### 変更
        logger.info("start connect")
        mqttc.connect(aws_iot_endpoint, port=443)
        logger.info("connect success")

        mqttc.loop_start()

        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            logger.info("try to publish:{}".format(now))
            info = mqttc.publish(topic, now)
            
            time.sleep(1)

    except Exception as e:
        logger.error("exception main()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)