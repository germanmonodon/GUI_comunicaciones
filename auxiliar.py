from time import perf_counter
from pymavlink import mavutil
from pubsub import pub


class Receiver():
    def __init__(self):

        self.master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
        # message_types = {'ATTITUDE', 'SCALED_IMU2', 'AHRS2', 'SCALED_PRESSURE'}
        message_types = {'SCALED_PRESSURE', 'ATTITUDE', 'SCALED_IMU2'}
        self.message_handlers = {
            'ATTITUDE': self.handle_attitude_message,
            'SCALED_IMU2': self.handle_imu_message,
            'SCALED_PRESSURE': self.handle_pressure
        }
        print('press CTRL+C to stop')
        while "receiving messages":
            message = self.master.recv_match(type=message_types, blocking=True)
            self.handle_message(message)

    def handle_attitude_message(self, msg):
        "Creo que no es correcto usar en esta función el yaw como lo tengo representado en el GUI pero para empezar."
        pub.sendMessage(topicName="BlueROV2::Angles", acc=[msg.roll, msg.yaw, msg.pitch])
        pub.sendMessage(topicName="BlueROV2::Heading", heading=msg.yaw)
        # print('ATTITUDE', roll, pitch, yaw)

    def handle_imu_message(self, msg):
        xacc, yacc, zacc = msg.xacc, msg.yacc, msg.zacc
        print('SCALED_IMU2', xacc, yacc, zacc)
    def handle_pressure(self, msg):
        # print(msg.press_abs)
        pub.sendMessage(topicName="BlueROV2::Pressure", msg=msg.press_abs)

    def handle_message(self, message):
        type_ = message.get_type()
        if type_ in self.message_handlers:
            self.message_handlers[type_](message)
        else:
            print(type_)

