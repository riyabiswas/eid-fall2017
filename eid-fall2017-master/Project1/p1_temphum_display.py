# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temp_humidity.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Adafruit_DHT
import datetime

#Define class for dialog box to display historical values
class HistoryDialog(QtWidgets.QDialog):
    #constructor to initialize parameters
    def __init__(self, parent=None):
        super(HistoryDialog, self).__init__(parent)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        self.textBrowser = QtWidgets.QTextBrowser(self)
        #self.textBrowser.append("This is a QTextBrowser!")

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)


#Define class for dialog box to display alert window
class AlarmDialog(QtWidgets.QDialog):

   #constructor to set parameters
    def __init__(self, parent=None):
        super(AlarmDialog, self).__init__(parent)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.save_alarm)
        self.buttonBox.rejected.connect(self.reject)

        # Create textbox
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textbox)
        self.verticalLayout.addWidget(self.buttonBox)

    #Function to get alarm value from user
    def save_alarm(self):
        global alarm_value
        alarm_value = float(self.textbox.text())
        print("Alarm value=",alarm_value)
        self.close()

#class to define main dialog box
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(505, 296)
        self.pushButton_temp = QtWidgets.QPushButton(Dialog)
        self.pushButton_temp.setGeometry(QtCore.QRect(30, 190, 141, 51))
        self.pushButton_temp.setObjectName("pushButton_temp")
        self.lcd_display = QtWidgets.QLCDNumber(Dialog)
        self.lcd_display.setGeometry(QtCore.QRect(50, 70, 221, 81))
        self.lcd_display.setDigitCount(6)
        self.lcd_display.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcd_display.setProperty("value", 0.0)
        self.lcd_display.setObjectName("lcd_display")
        self.pushButton_humidity = QtWidgets.QPushButton(Dialog)
        self.pushButton_humidity.setGeometry(QtCore.QRect(240, 190, 141, 51))
        self.pushButton_humidity.setObjectName("pushButton_humidity")
        self.pushButton_alarm = QtWidgets.QPushButton(Dialog)
        self.pushButton_alarm.setGeometry(QtCore.QRect(400, 60, 93, 28))
        self.pushButton_alarm.setObjectName("pushButton_alarm")
        self.pushButton_history = QtWidgets.QPushButton(Dialog)
        self.pushButton_history.setGeometry(QtCore.QRect(400, 120, 93, 28))
        self.pushButton_history.setObjectName("pushButton_history")
        self.labelTime_hour = QtWidgets.QLabel(Dialog)
        self.labelTime_hour.setGeometry(QtCore.QRect(358, 10, 141, 28))
        self.labelTime_hour.setObjectName("labelTime_hour")
        self.labelUnit = QtWidgets.QLabel(Dialog)
        self.labelUnit.setGeometry(QtCore.QRect(290, 75, 61, 71))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.labelUnit.setFont(font)
        self.labelUnit.setWordWrap(True)
        self.labelUnit.setObjectName("labelUnit")

        #conect button press events to respective functions 
        self.pushButton_temp.clicked.connect(self.display_temp)
        self.pushButton_humidity.clicked.connect(self.display_humidity)
        self.pushButton_alarm.clicked.connect(self.set_alarm)
        self.pushButton_history.clicked.connect(self.see_history)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)



    #Set texts for labelling gui items
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Temperature-Humidity Sensor"))
        self.pushButton_temp.setText(_translate("Dialog", "Get Temperature"))
        self.pushButton_humidity.setText(_translate("Dialog", "Get Humidity"))
        self.pushButton_alarm.setText(_translate("Dialog", "Set Alarm"))
        self.pushButton_history.setText(_translate("Dialog", "See History"))
        self.labelTime_hour.setText(_translate("Dialog", "Time"))
        self.labelUnit.setText("")
		
    #read temperature from sensor and display
    def display_temp(self):
        global temp_list
        global current_time
        global alarm_value  
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        #temperature = None
        if temperature is None:
            msg = QtWidgets.QMessageBox()
            msg.setText("No data received!");
            msg.exec_()
        else:
            self.lcd_display.display(temperature)
            self.labelUnit.setText(t+"C")
            if temperature >= alarm_value:
                self.show_warning()

            #Add Temperature values to a list
            temp_list += [[current_time, temperature]]
		
    #read humidity from sensor and display. Borrowed from https://github.com/adafruit/Adafruit_Python_DHT/blob/master/examples/AdafruitDHT.py
    def display_humidity(self):
        global humid_list
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is None:
            msg = QtWidgets.QMessageBox()
            msg.setText("No data received!")
            msg.exec_()
        else:
            self.lcd_display.display(humidity)
            self.labelUnit.setText("%")

            #Add Humidity values to a list
            humid_list += [[current_time, humidity]]
            #print("humid_list:",humid_list)

    #Take alarm value from user
    def set_alarm(self):
        self.dialogTextBrowser = AlarmDialog()
        self.dialogTextBrowser.show()

    #Open Warning message box for alarm
    def show_warning(self):
        msg = QtWidgets.QMessageBox()
        msg.warning(msg,"Alert!","Temperature exceeds alarm value");

    #Show list values on a message browser
    def see_history(self):
        #num = 0
        last_element_temp = len(temp_list)
        last_element_humid = len(humid_list)
        self.dialogTextBrowser_temp = HistoryDialog()
        self.dialogTextBrowser_temp.textBrowser.append("Temperature Values:")
        for num in range(last_element_temp):
            self.dialogTextBrowser_temp.textBrowser.append(temp_list[num][0]+" : "+str(temp_list[num][1]))            
        self.dialogTextBrowser_temp.show()

        self.dialogTextBrowser_humid = HistoryDialog()
        self.dialogTextBrowser_humid.textBrowser.append("Humidity Values:")
        for num in range(last_element_humid):
            self.dialogTextBrowser_humid.textBrowser.append(humid_list[num][0]+" : "+str(humid_list[num][1]))            
        self.dialogTextBrowser_humid.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    #Set GPIO pin 4 for sensor input and DHT22 as sensor
    sensor = Adafruit_DHT.DHT22
    pin = 4

    #Unicode for 'degree'
    t = u"\u00b0"
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    temp_list = []
    humid_list = []
    alarm_value = 100.0

    #Get current system time and date
    def update_label():
        global current_time
        current_time = str(datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S"))
        ui.labelTime_hour.setText(current_time)

    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(1000)  # every 1000 milliseconds

    sys.exit(app.exec_())

