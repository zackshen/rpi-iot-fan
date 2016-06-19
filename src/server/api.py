from flask import Flask
from flask import request
from flask.ext.restful import Api, Resource
import RPi.GPIO as GPIO

app = Flask(__name__)
api = Api(app)
PIN_11 = 11
GPIO.setmode(GPIO.BOARD)

STATUS_TABLE = {0: 'off', 1: 'on'}


class Fan(object):

    def __init__(self, pin):
        self.pin = pin

    @property
    def status(self):
        GPIO.setup(self.pin, GPIO.IN)
        status = GPIO.input(self.pin)
        return {'status': STATUS_TABLE[status]}

    def turn_on(self):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)
        return {'status': 'on'}

    def turn_off(self):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        return {'status': 'off'}


class FanResource(Resource):

    def get(self):
        fan = Fan(PIN_11)
        return fan.status

    def put(self):
        fan = Fan(PIN_11)
        action = request.form.get('action')
        if action == 'turn_on':
            return fan.turn_on()
        elif action == 'turn_off':
            return fan.turn_off()


api.add_resource(FanResource, '/fan', endpoint='fan')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
