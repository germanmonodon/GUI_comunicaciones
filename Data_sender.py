from pymavlink import mavutil
from pubsub import pub


class Sender:
    def __init__(self):
        """
          Se ha creado otro cliente UDP con puerto en el frontend de BlueOS para recibir simultáneamente datos
          de la raspberry pi a este script de python y a QGroundControl
          Puerto sin QgroundControl: udpin:0.0.0.0:14550
          Puerto con QgroundControl simultáneo udpin:0.0.0.0:14551
        """
        self.master = mavutil.mavlink_connection('udpin:0.0.0.0:14551')
        # message_types = {'ATTITUDE', 'SCALED_IMU2', 'AHRS2', 'SCALED_PRESSURE'}
        message_types = {'SCALED_PRESSURE', 'ATTITUDE', 'SCALED_IMU2', 'VFR_HUD'}
        self.message_handlers = {
            'ATTITUDE': self.handle_attitude_message,
            'SCALED_IMU2': self.handle_imu_message,
            'SCALED_PRESSURE': self.handle_pressure,
            'VFR_HUD': self.handle_magnetic
        }
        while "receiving messages":
            message = self.master.recv_match(type=message_types, blocking=True)
            self.handle_message(message)

    def handle_magnetic(self, msg):
        pub.sendMessage(topicName="BlueROV2::Heading", heading=msg.heading)

    def handle_attitude_message(self, msg):
        pub.sendMessage(topicName="BlueROV2::Angles", acc=[msg.roll, msg.yaw, msg.pitch])
        # print('ATTITUDE', roll, pitch, yaw)

    def handle_imu_message(self, msg):
        xacc, yacc, zacc = msg.xacc, msg.yacc, msg.zacc
        pub.sendMessage(topicName="BlueROV2::AccyGyro", acc=[[xacc, yacc, zacc], [msg.xgyro, msg.ygyro, msg.zgyro]])

    def handle_pressure(self, msg):
        # print(msg.press_abs)
        pub.sendMessage(topicName="BlueROV2::Pressure", msg=msg.press_abs)

    def handle_message(self, message):
        type_ = message.get_type()
        if type_ in self.message_handlers:
            self.message_handlers[type_](message)
        else:
            print(type_)

