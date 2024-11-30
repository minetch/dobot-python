#DOBOT STUDIOのスクリプト機能で実行する際はDobotのパッケージの宣言をコメントアウトしてください
import DobotDllType as dType    
from DobotControl import api


print('[SETTING UP]')


# DICTIONARY
unit1 = {"RED":False, "BLUE":False, "GREEN":False}
unit2 = {"RED":False, "BLUE":False}
count = {"RED":0,"BLUE":0,"GREEN":0,"BLOCK":0,"TRASH":0,"UNIT":0,"EFFECT":0}



# DOBOT XYZ
# 任意の値に動的に変更してください
Grab_X = 272.1
Grab_Y = 138.7
Grab_Z = 17

ColorSensor_X = 195.3
ColorSensor_Y = 110.8
ColorSensor_Z = 26

Place1_X = 173
Place1_Y = -150
Place_Z = -40

Place2_X = 173
Place2_Y = -150

Place3_X = 173
Place3_Y = -150
Place3_Z = -40



# CONSTANT
BOX_HEIGHT = 25



# VARIABLES
RedCount = 0
BlueCount = 0
GreenCount = 0

BlockCount = 0
TrashCount = 0
UnitCount = 0


# SETUP
dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)

dType.SetColorSensor(api, 1 ,2, 1)
dType.SetInfraredSensor(api, 1 ,1, 1)

dType.dSleep(100)

dType.SetPTPJointParamsEx(api,400,400,400,400,400,400,400,400,1)
dType.SetPTPCommonParamsEx(api,50,50,1)
dType.SetPTPJumpParamsEx(api,50,100,1)

current_pose = dType.GetPose(api)

dType.SetPTPCmdEx(api, 2, Grab_X,  Grab_Y,  ColorSensor_Z, current_pose[3], 1)
dType.SetEndEffectorSuctionCupEx(api, 0, 1)


print('[DONE]')

def reset():
  global UnitCount
  for key in unit1:
    unit1[key] = False
  for key in unit2:
    unit2[key] = False
  UnitCount += 1
  print('/t/t#####################')
  print('/t/t#/t/t/t#')
  print('/t/t#/tTAKE BLOCKS OFF/t#')
  print('/t/t#/t/t/t#')
  print('/t/t#####################')
  

def trash(color):
  global TrashCount
  dType.SetPTPCmdEx(api, 0, Place3_X,  Place3_Y,  Place3_Z, 0, 1)
  print('put {} trash(place3)'.format(color))
  TrashCount += 1

def sortColor():
  global R, G, B, MAX, RedCount, GreenCount, BlueCount
  
  dType.SetPTPCmdEx(api, 0, ColorSensor_X,  ColorSensor_Y,  ColorSensor_Z, 0, 1)
  dType.dSleep(100)
  
  R = dType.GetColorSensorEx(api, 0)
  G = dType.GetColorSensorEx(api, 1)
  B = dType.GetColorSensorEx(api, 2)
  
  MAX = max([R, G, B])
  
  if MAX == R:
    print('Red')
    RedCount += 1
    if unit1['RED'] == False:
      print('put red place1')
      print('place1の数は'.format(sum(value for value in unit1.values())))
      dType.SetPTPCmdEx(api, 0, Place1_X,  Place1_Y,  Place_Z + sum(value for value in unit1.values())*BOX_HEIGHT, 0, 1)
      unit1['RED'] = True
    elif unit2['RED'] == False:
      print('put red place1')
      print('place1の数は'.format(sum(value for value in unit2.values())))      
      dType.SetPTPCmdEx(api, 0, Place2_X,  Place2_Y,  Place_Z + sum(value for value in unit2.values())*BOX_HEIGHT, 0, 1)
      unit2['RED'] = True
      if (sum(value for value in unit1.values())+sum(value for value in unit2.values())) == 5:
        reset()
    else:
      trash('red')
  elif MAX == G:
    print('Green')
    GreenCount += 1
    if unit1['GREEN'] == False:
      print('put red place1')
      print('place1の数は'.format(sum(value for value in unit1.values())))
      dType.SetPTPCmdEx(api, 0, Place1_X,  Place1_Y,  Place_Z + sum(value for value in unit1.values())*BOX_HEIGHT, 0, 1)
      if (sum(value for value in unit1.values())+sum(value for value in unit2.values())) == 5:
        reset()
    else:
      trash('green')
  else:
    print('Blue')
    BlueCount += 1
    if unit1['BLUE'] == False:
      print('put blue place1')
      print('place1の数は'.format(sum(value for value in unit1.values())))
      dType.SetPTPCmdEx(api, 0, Place1_X,  Place1_Y,  Place_Z + sum(value for value in unit1.values())*BOX_HEIGHT, 0, 1)
      unit1['BLUE'] = True
    elif unit2['BLUE'] == False:
      print('put blue place1')
      print('place1の数は'.format(sum(value for value in unit2.values())))      
      dType.SetPTPCmdEx(api, 0, Place2_X,  Place2_Y,  Place_Z + sum(value for value in unit2.values())*BOX_HEIGHT, 0, 1)
      unit2['BLUE'] = True
      if (sum(value for value in unit1.values())+sum(value for value in unit2.values())) == 5:
        reset()
    else:
      trash('blue')
  dType.SetEndEffectorSuctionCupEx(api, 0, 1)
  dType.dSleep(0)

while True:
  if (dType.GetInfraredSensor(api, 1)[0]) == 1:
    dType.SetEndEffectorSuctionCupEx(api, 1, 1)
    dType.SetPTPCmdEx(api, 0, Grab_X,  Grab_Y,  Grab_Z, 0, 1)
    sortColor()
    dType.SetPTPCmdEx(api, 0, Grab_X,  Grab_Y,  ColorSensor_Z, 0, 1)
    
    BlockCount = 0
    BlockCount = RedCount + BlockCount + GreenCount
    
    count = {
      "RED"     :RedCount,
      "BLUE"    :BlueCount,
      "GREEN"   :GreenCount,
      "BLOCK"   :BlockCount,
      "TRASH"   :TrashCount,
      "UNIT"    :UnitCount,
      "EFFECT"  :((UnitCount*5)/BlockCount)*100
    }
    
    for key, value in count.items():
      print("{}\t".format(key))
      print("{}\t".format(value))
