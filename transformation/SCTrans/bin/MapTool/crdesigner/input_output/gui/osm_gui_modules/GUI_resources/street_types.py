# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'street_types.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(174, 383)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.chk_unclassified = QtWidgets.QCheckBox(self.frame)
        self.chk_unclassified.setObjectName("chk_unclassified")
        self.gridLayout_2.addWidget(self.chk_unclassified, 5, 0, 1, 1)
        self.chk_primary = QtWidgets.QCheckBox(self.frame)
        self.chk_primary.setObjectName("chk_primary")
        self.gridLayout_2.addWidget(self.chk_primary, 2, 0, 1, 1)
        self.chk_tertiary = QtWidgets.QCheckBox(self.frame)
        self.chk_tertiary.setObjectName("chk_tertiary")
        self.gridLayout_2.addWidget(self.chk_tertiary, 4, 0, 1, 1)
        self.chk_motorway_link = QtWidgets.QCheckBox(self.frame)
        self.chk_motorway_link.setObjectName("chk_motorway_link")
        self.gridLayout_2.addWidget(self.chk_motorway_link, 7, 0, 1, 1)
        self.chk_tertiary_link = QtWidgets.QCheckBox(self.frame)
        self.chk_tertiary_link.setObjectName("chk_tertiary_link")
        self.gridLayout_2.addWidget(self.chk_tertiary_link, 11, 0, 1, 1)
        self.chk_primary_link = QtWidgets.QCheckBox(self.frame)
        self.chk_primary_link.setObjectName("chk_primary_link")
        self.gridLayout_2.addWidget(self.chk_primary_link, 9, 0, 1, 1)
        self.chk_residential = QtWidgets.QCheckBox(self.frame)
        self.chk_residential.setObjectName("chk_residential")
        self.gridLayout_2.addWidget(self.chk_residential, 6, 0, 1, 1)
        self.chk_secondary_link = QtWidgets.QCheckBox(self.frame)
        self.chk_secondary_link.setObjectName("chk_secondary_link")
        self.gridLayout_2.addWidget(self.chk_secondary_link, 10, 0, 1, 1)
        self.chk_trunk_link = QtWidgets.QCheckBox(self.frame)
        self.chk_trunk_link.setObjectName("chk_trunk_link")
        self.gridLayout_2.addWidget(self.chk_trunk_link, 8, 0, 1, 1)
        self.chk_trunk = QtWidgets.QCheckBox(self.frame)
        self.chk_trunk.setObjectName("chk_trunk")
        self.gridLayout_2.addWidget(self.chk_trunk, 1, 0, 1, 1)
        self.chk_secondary = QtWidgets.QCheckBox(self.frame)
        self.chk_secondary.setObjectName("chk_secondary")
        self.gridLayout_2.addWidget(self.chk_secondary, 3, 0, 1, 1)
        self.chk_motorway = QtWidgets.QCheckBox(self.frame)
        self.chk_motorway.setObjectName("chk_motorway")
        self.gridLayout_2.addWidget(self.chk_motorway, 0, 0, 1, 1)
        self.chk_living_street = QtWidgets.QCheckBox(self.frame)
        self.chk_living_street.setObjectName("chk_living_street")
        self.gridLayout_2.addWidget(self.chk_living_street, 12, 0, 1, 1)
        self.chk_service = QtWidgets.QCheckBox(self.frame)
        self.chk_service.setObjectName("chk_service")
        self.gridLayout_2.addWidget(self.chk_service, 13, 0, 1, 1)
        self.chk_path = QtWidgets.QCheckBox(self.frame)
        self.chk_path.setObjectName("chk_path")
        self.gridLayout_2.addWidget(self.chk_path, 14, 0, 1, 1)
        self.chk_footway = QtWidgets.QCheckBox(self.frame)
        self.chk_footway.setObjectName("chk_footway")
        self.gridLayout_2.addWidget(self.chk_footway, 15, 0, 1, 1)
        self.chk_cycleway = QtWidgets.QCheckBox(self.frame)
        self.chk_cycleway.setObjectName("chk_cycleway")
        self.gridLayout_2.addWidget(self.chk_cycleway, 16, 0, 1, 1)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select Street Types"))
        self.chk_unclassified.setText(_translate("Dialog", "unclassified"))
        self.chk_primary.setText(_translate("Dialog", "primary"))
        self.chk_tertiary.setText(_translate("Dialog", "tertiary"))
        self.chk_motorway_link.setText(_translate("Dialog", "motorway_link"))
        self.chk_tertiary_link.setText(_translate("Dialog", "tertiary_link"))
        self.chk_primary_link.setText(_translate("Dialog", "primary_link"))
        self.chk_residential.setText(_translate("Dialog", "residential"))
        self.chk_secondary_link.setText(_translate("Dialog", "secondary_link"))
        self.chk_trunk_link.setText(_translate("Dialog", "trunk_link"))
        self.chk_trunk.setText(_translate("Dialog", "trunk"))
        self.chk_secondary.setText(_translate("Dialog", "secondary"))
        self.chk_motorway.setText(_translate("Dialog", "motorway"))
        self.chk_living_street.setText(_translate("Dialog", "living_street"))
        self.chk_service.setText(_translate("Dialog", "service"))
        self.chk_path.setText(_translate("Dialog", "path"))
        self.chk_footway.setText(_translate("Dialog", "footway"))
        self.chk_cycleway.setText(_translate("Dialog", "cycleway"))

