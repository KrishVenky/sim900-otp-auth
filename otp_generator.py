import logging
import random
from lib.sim900.smshandler import SimGsmSmsHandler, SimSmsPduCompiler
from test_shared import initializeUartPort, initializeLogs, baseOperations

COMPORT_NAME = "COM7"
CONSOLE_LOGGER_LEVEL = logging.INFO
LOGGER_LEVEL = logging.INFO
SMS_CENTER_NUMBER = ""

class OTPGenerator:
    def __init__(self, port_name):
        self.port = initializeUartPort(portName=port_name)
        (formatter, self.logger, consoleLogger) = initializeLogs(LOGGER_LEVEL, CONSOLE_LOGGER_LEVEL)
        self.gsm, self.imei = baseOperations(self.port, self.logger)
        self.sms = SimGsmSmsHandler(self.port, self.logger)

    def generate_otp(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    def send_sms(self, phone_number, message):
        self.logger.info("sending ASCII (Latin-1) SMS")
        pdu_helper = SimSmsPduCompiler(SMS_CENTER_NUMBER, phone_number, message)
        self._print_sca_plus_pdu(pdu_helper)
        if not self.sms.sendPduMessage(pdu_helper, 1):
            self.logger.error(f"Error sending SMS: {self.sms.errorText}")
            return False
        return True

    def _print_sca_plus_pdu(self, pdu_helper):
        d = pdu_helper.compile()
        if d is None:
            return False
        for (sca, pdu) in d:
            self.logger.info(f"sendSms(): sca + pdu = \"{sca + pdu}\"")

if __name__ == "__main__":
    otp_gen = OTPGenerator(port_name=COMPORT_NAME)
    otp = otp_gen.generate_otp()
    otp_gen.send_sms("+919972373015", f"Your OTP is: {otp}")
    print(f"Sent OTP: {otp}")
