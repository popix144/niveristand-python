import time
import os
import pytest

from niveristand.legacy import NIVeriStand
from niveristand.legacy.NIVeriStand import NIVeriStandException
from tests.testutilities import configutilities

def sleep():
    time.sleep(1)

TEST_ID = 12234


def test_alarm2_api():
    wks = NIVeriStand.Workspace2("localhost")
    print("")
    SYSDEFINITION = os.path.join(configutilities.get_autotest_projects_path(),
                                 "TestAlarmAPI",
                                 "TestAlarmAPI.nivssdf")
    print("Deploying %s" % SYSDEFINITION)
    wks.ConnectToSystem(SYSDEFINITION,1,80000)

    try:
        # Verify the TEST_ID var on test file.
        test_ID = wks.GetSingleChannelValue("TEST_ID")
        assert(test_ID == TEST_ID), "Deployed wrong test file"

        print("Testing Alarm manager Get Alarm List")
        alarmMgr = NIVeriStand.AlarmManager2("localhost")
        result = alarmMgr.GetAlarmList("Controller")
        assert(len(result) == 3), "Expected 3 alarms returned from the system"

        with pytest.raises(NIVeriStandException):
            alarmMgr.GetAlarmList("Invalid Controller")

        print("Testing Alarm manager Read Alarm Data"		)
        alarms = ('Alarm Group/AlarmTest1','Alarm Group/AlarmTest2','ConstantBoundAlarm')
        result = alarmMgr.GetMultipleAlarmsData("Controller",alarms,60000)
        print("Verifying alarm data returned")
        assert(len(result) ==3), "Expected to get 3 alarms data back"

        with pytest.raises(NIVeriStandException):
            alarmMgr.GetMultipleAlarmsData("INVALID CONTROLLER",alarms,60000)

        print("Verifying Alarm Data")
        alarmTest1 = result[0]
        alarmTest2= result[1]
        constantBoundAlarm = result[2]
        print(alarmTest1)
        assert(alarmTest1['WatchChannel'] == r"Aliases/AlarmChannel1"), "Fail to confirm alarm channel"
        assert((alarmTest1['HighLimitIsConstant'] == 0) or (alarmTest1['HighLimitChannel'] == r"AlarmChannel1High")), "Fail to confirm high limit"
        assert((alarmTest1['LowLimitIsConstant'] == 0) or (alarmTest1['LowLimitChannel'] == r"AlarmChannel1Low")), "Fail to confirm low limit"
        assert(alarmTest1['DelayDuration'] == 0.5), "Fail to confirm delay duration"
        assert(alarmTest1['ProcedureName'] == r"ResetAlarmTest1"), "Fail to confirm procedure"
        assert(alarmTest1['Priority'] == 2), "Fail to confirm priority (deprecated)"
        assert(alarmTest1['PriorityNumber'] == 5), "Fail to confirm priority number"
        assert(alarmTest1['State'] == 1), "Fail to confirm state"
        assert(alarmTest1['Mode'] == 0), "Fail to confirm mode"
        assert(alarmTest1['GroupNumber'] == 1), "Fail to confirm alarm group"

        print("Test alarm interface")

        print("Test Alarm constructor mode")
        Constructor1 = NIVeriStand.Alarm('Alarm Group/Alarm Test2')
        Constructor2 = NIVeriStand.Alarm('Alarm Group/Alarm Test2','Controller')
        Constructor3 = NIVeriStand.Alarm('Alarm Group/Alarm Test2',None,'localhost')
        Constructor4 = NIVeriStand.Alarm('Alarm Group/Alarm Test2','Controller','localhost')

        print("Test access to alarm")
        BoundAlarmRef = NIVeriStand.Alarm('ConstantBoundAlarm','Controller','localhost')
        result = BoundAlarmRef.GetAlarmData(30000)
        assert(result == constantBoundAlarm), "Alarm data from alarm interface differ from alarm manager"

        print("Test modifying alarm data")
        modAlarmData = result
        modAlarmData['HighLimit'] = 3
        modAlarmData['LowLimit'] = -3
        BoundAlarmRef.SetAlarmData2(modAlarmData)
        sleep()
        result = BoundAlarmRef.GetAlarmData(30000)
        assert(result == modAlarmData), "Alarm data set cannot be confirmed"

        print("Test modifying alarm state and mode")
        BoundAlarmRef.SetEnabledState(0)
        #indicate only
        BoundAlarmRef.SetAlarmMode(1)
        sleep()

        result = BoundAlarmRef.GetAlarmData(30000)
        assert(result['State'] == 0), "Alarm Mode is wrong"

        assert(result['Mode'] == 1), "Alarm Mode is wrong"

        BoundAlarmRef.SetEnabledState(1)
        BoundAlarmRef.SetAlarmMode(0)
        sleep()
        sleep()
        wks.SetSingleChannelValue(r"Controller/User Channel/AlarmChannel1",20)
        wks.SetSingleChannelValue(r"Controller/User Channel/AlarmChannel2",10)
        sleep()
        sleep()

        print("Testing alarm mutual exclusion within a group")
        AlarmTest2Ref = NIVeriStand.Alarm('Alarm Group/AlarmTest2')
        AlarmTest1Ref = NIVeriStand.Alarm('Alarm Group/AlarmTest1')
        result = AlarmTest1Ref .GetAlarmData(30000)
        result2 = AlarmTest2Ref .GetAlarmData(30000)
        assert(result['State'] == 2), "Alarm should be tripped"
        assert(result2['State'] != 2), "Alarm should not be running due to an execution of a higher priority."

        print("Testing Alarm Execution Across Groups")
        result = BoundAlarmRef.GetAlarmData(30000)
        result2 = AlarmTest2Ref .GetAlarmData(30000)
        assert((result['State'] == 2) and (result2['State'] == 2)), " Two alarms should be tripped simulteneously."

        print("Test PASSED")
        print("")
    finally:
        wks.DisconnectFromSystem("",1)
