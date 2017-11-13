import UVLIF2.gui.analysis_configuration_ui as main
from PyQt5 import QtWidgets, QtCore, QtGui

class analysis_configuration_window(QtWidgets.QDialog, main.Ui_Dialog):

  def __init__(self, parent = None):
    super(analysis_configuration_window, self).__init__(parent)
    self.setupUi(self)
    self.method = None
    self.model = QtGui.QStandardItemModel()
    self.model.setHorizontalHeaderLabels(["Parameter", "Value"])
    self.tableView.setModel(self.model)
    self.tableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
    self.tableView.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

  def update(self):
    self.model.clear()
    self.model.setHorizontalHeaderLabels(["Parameter", "Value"])
    params = {}
    self.shorthand = self.parent().shorthand[self.method]
    for item, value in self.parent().analysis_options.items():
      if self.shorthand + '.' in item:
        params[item.replace(self.shorthand + '.', "")] = value

    for i, (item, value) in enumerate(params.items()):
      self.model.setItem(i, 0, QtGui.QStandardItem())
      self.model.setItem(i, 1, QtGui.QStandardItem())
      self.set_delegate(i, item, value)
      self.model.item(i, 0).setText(str(item))
      self.model.item(i, 0).setEditable(False)
    self.load_settings_from_parent(self.shorthand)
      
    

  def set_delegate(self, i, item, value):
    
    if type(value) == list and value[0] == 'default':
      delegate = None
      if value[-1] == 'int':
        delegate = DefaultDelegate(self, value[1], int)
      elif value[-1] == 'float':
        delegate = DefaultDelegate(self, value[1], float)
      if delegate:
        self.tableView.setItemDelegateForRow(i, delegate)
        self.model.item(i, 1).setText(value[1])
      
    elif type(value) == int:
      self.tableView.setItemDelegateForRow(i, IntDelegate(self))
      self.model.item(i, 1).setText(str(value))
    elif type(value) == float:
      self.tableView.setItemDelegateForRow(i, FloatDelegate(self))
      self.model.item(i, 1).setText(str(value))
    elif type(value) == list:
      self.model.item(i, 1).setData(value)
      self.model.item(i, 1).setText(value[0])
      self.tableView.setItemDelegateForRow(i, ListDelegate(self))

  def load_settings_from_parent(self, shorthand):

    cfg = {}

    for key, value in self.parent().cfg.items():
      if self.shorthand + '.' in key:
        cfg[key.replace(self.shorthand + '.', "")] = value
    
    for i in range(self.model.rowCount()):
      parameter = self.model.item(i, 0).text()
      if parameter in cfg:
        self.model.item(i, 1).setText(cfg[parameter])

  def closeEvent(self, event):
    self.send_selection_to_parent()

  def send_selection_to_parent(self):
    cfg = {}    

    for i in range(self.model.rowCount()):
      cfg[self.shorthand + '.' + self.model.item(i, 0).text()] = self.model.item(i, 1).text()

    self.parent().cfg.update(cfg)
    

class IntDelegate(QtWidgets.QItemDelegate):

  def __init__(self, parent):
    super(IntDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    editor = QtWidgets.QLineEdit(parent)
    editor.setValidator(QtGui.QIntValidator())
    return editor

  

class FloatDelegate(QtWidgets.QItemDelegate):

  def __init__(self, parent):
    super(FloatDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    editor = QtWidgets.QLineEdit(parent)
    editor.setValidator(QtGui.QDoubleValidator())
    return editor

class ListDelegate(QtWidgets.QItemDelegate):

  def __init__(self, parent):
    super(ListDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    editor = QtWidgets.QComboBox(parent)
   
    for item in index.model().itemFromIndex(index).data():
      editor.addItem(item)
    
    return editor


  def setModelData(self, editor, model, index):
    model.setData(index, editor.currentText(), QtCore.Qt.EditRole)

class DefaultDelegate(QtWidgets.QItemDelegate):
  def __init__(self, parent, default, valid_type):
    super(DefaultDelegate, self).__init__(parent)
    self.default = default
    self.valid_type = valid_type

  def createEditor(self, parent, option, index):
    editor = QtWidgets.QLineEdit(parent)
    editor.setValidator(DefaultValidator(self.default, self.valid_type))
    return editor


class DefaultValidator(QtGui.QValidator):

  def __init__(self, default, valid_type):
    super(DefaultValidator, self).__init__()
    self.default = default
    self.valid_type = valid_type

  def validate(self, input, pos):
    if self.valid_type == int:
      state, input, pos = QtGui.QIntValidator().validate(input, pos)
    elif self.valid_type == float:
      state, input, pos = QtGui.QDoubleValidator().validate(input, pos)
    if self.default[:len(input)] == input:
      state = QtGui.QValidator.Intermediate
    if self.default == input:
      state = QtGui.QValidator.Acceptable
    return state, input, pos
          
    
    


