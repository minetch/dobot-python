import DobotDllType as dtype
import time


class DobotWrapper:
    def __init__(self, COM="COM3"):
        self.COM = COM
        self.simulated = False

    def initiate(self, end_effector_type="cup"):
        self.api = dtype.load()

        # connect
        state = dtype.ConnectDobot(self.api, self.COM, 115200)[0]
        if not state == dtype.DobotConnect.DobotConnect_NoError:
            print("could not connect to DOBOT")

        # settings
        dtype.SetCmdTimeout(self.api, 3000)
        dtype.SetQueuedCmdClear(self.api)
        dtype.SetQueuedCmdStartExec(self.api)
        device = "DOBOT Magician"
        dtype.SetDeviceName(self.api, device)

        dtype.SetJOGJointParams(self.api, 50, 50, 50, 50, 50, 50, 50, 50, True)
        dtype.SetJOGCoordinateParams(
            self.api, 50, 50, 50, 50, 50, 50, 50, 50, True)
        dtype.SetJOGCommonParams(self.api, 100, 100, True)
        dtype.SetPTPJointParams(self.api, 100, 100, 100, 100,
                          100, 100, 100, 100, True)
        dtype.SetPTPCoordinateParams(self.api, 100, 100, 100, 100, True)
        dtype.SetPTPJumpParams(self.api, 20, 100, True)
        dtype.SetPTPCommonParams(self.api, 30, 30, True)
        dtype.SetHOMEParams(self.api, 200, 0, 0, 0, True)

        if end_effector_type in ["cup", "gripper"]:
            dtype.SetEndEffectorParams(self.api, 59.7, 0, 0, 0)
        elif end_effector_type in ["pen"]:
            dtype.SetEndEffectorParams(self.api, 61.0, 0, 0, 0)
        else:
            raise ValueError("invalid end effector type")

        # set home
        self.set_home()

    def set_home(self):
        dtype.SetHOMECmdEx(self.api, 0, True)

    def reset_alarm(self):
        dtype.ClearAllAlarmsState(self.api)

    def move_arm(self, x, y, z, w):
        self._check_xy(x, y)
        if not self.simulated:
            dtype.SetPTPCmdEx(self.api, dtype.PTPMode.PTPMOVJXYZMode, x, y, z, w, True)

    def get_position(self):
        return dtype.GetPose(self.api)[:4]

    def _check_xy(self, x, y):
        r = (x**2+y**2)**0.5

        if r < 115 or r > 320:
            raise ValueError(
                f"invalid position! (x^2+y^2)^0.5 ={r} should be 115~320. x={x} y={y}")

    def cup(self, mode=True):
        if mode:
            dtype.SetEndEffectorSuctionCup(self.api, True, True)
        else:
            dtype.SetEndEffectorSuctionCup(self.api, False, True)
        # SetEndEffectorGripper(self.api, 0, True)

    def grip(self, grip=True, sleep=0.5):
        if grip:
            dtype.SetEndEffectorGripper(self.api, True, True)
        else:
            dtype.SetEndEffectorGripper(self.api, True, False)
            time.sleep(sleep)
            dtype.SetEndEffectorGripper(self.api, False, False)