import UVLIF.gui.analysis_configuration_ui as main
from PyQt5 import QtWidgets, QtCore, QtGui

class analysis_configuration_window(QtWidgets.QDialog, main.Ui_Dialog):

  def __init__(self, parent = None):

    super(analysis_configuration_window, self).__init__(parent)
    self.setupUi(self)

    #set up the param model 
    self.param_model = QtGui.QStandardItemModel()
    self.paramView.setModel(self.param_model)
    self.paramView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    # setup up value models
    self.value_models = []

    # connect the left hand parameter list view change to update the value model
    self.paramView.selectionModel().currentChanged.connect(self.update_value_model)

    # connect add button
    self.addButton.clicked.connect(self.add)
    self.removeButton.clicked.connect(self.remove)
    self.saveButton.clicked.connect(self.save)

  def save(self):

    print(self.value_models)
    cfg = {}
    
    # for every parameter
    for i in range(self.param_model.rowCount()):
      output_list = []

      # look for values
      for j in range(self.value_models[i].rowCount()):
        output_list.append(self.value_models[i].item(j).data())
      

      # if output_list is not empty put it into the cfg
      if output_list != []:
        cfg[self.shorthand + '.' + self.param_model.item(i).text()] = output_list


    self.parent().cfg.update(cfg)
    self.close()

  def add(self):
    nrow = self.valueView.model().rowCount()
    self.valueView.model().setItem(nrow, QtGui.QStandardItem())
    idx = self.paramView.selectionModel().currentIndex()
    value = self.params[self.paramView.model().item(idx.row()).text()]
    self.update_value_model()

  def remove(self):      
    idx = self.valueView.selectionModel().currentIndex()
    self.valueView.model().removeRow(idx.row())
    self.update_value_model()

  def get_params(self):
    # Get params from config file
    params = {}
    self.shorthand = self.parent().shorthand[self.method]
    for item, value in self.parent().analysis_options.items():
      if self.shorthand + '.' in item:
        params[item.replace(self.shorthand + '.', "")] = value
    return params

  def populate_model(self, model, values, set_text = False):

    # populate with the parameters
    for i, value in enumerate(values):
      model.setItem(i, QtGui.QStandardItem()) # add new item
      if set_text:
        model.item(i).setText(str(value))

  def showEvent(self, event):
    params = self.get_params()
    self.params = params

    # set up the parameter model

    self.populate_model(self.param_model, params.keys(), set_text = True)

    # set up the value models 
    self.value_models = []
    for i, value in enumerate(params.values()):
      self.value_models.append(QtGui.QStandardItemModel())
    
    self.valueView.setModel(self.value_models[0])

    #set the current index
    self.paramView.setCurrentIndex(self.param_model.index(0, 0))

    self.load()

  def load(self):
    for key, value in self.parent().cfg.items():
      if key.startswith(self.shorthand + '.'):
        self.load_parameter(key.replace(self.shorthand +'.', ""), value)

  def load_parameter(self, key, value):
    for i in range(self.param_model.rowCount()):
      if key == self.param_model.item(i).text():
        for j, item in enumerate(value):
          self.value_models[i].setItem(j, QtGui.QStandardItem())
          self.value_models[i].item(j).setText(str(item))
          self.value_models[i].item(j).setData(item)

  def update_value_model(self):
    
    
    idx = self.paramView.selectionModel().currentIndex()
    self.valueView.setModel(self.value_models[idx.row()])
    value = self.params[self.paramView.model().item(idx.row()).text()]

    # set delegates
    for i in range(self.value_models[idx.row()].rowCount()):
      self.set_delegate(value, i, self.value_models[idx.row()])



  def set_delegate(self, value, idx, model):

    if type(value) == list and value[0] == 'default':
      delegate = None
      if value[-1] == 'int':
        delegate = DefaultDelegate(self, value[1], int)
      elif value[-1] == 'float':
        delegate = DefaultDelegate(self, value[1], float)
      if delegate:
        self.valueView.setItemDelegateForRow(idx, delegate)
        if model.item(idx).text() == '':
          model.item(idx).setText(str(value[1]))
        if model.item(idx).data() == None:
          model.item(idx).setData(value[1])

    elif type(value) == list and type(value[0]) == tuple:
      self.valueView.setItemDelegateForRow(idx, TupleDelegate(self, int))
      if model.item(idx).text() == '':
        model.item(idx).setText(str(value[0]))
      if model.item(idx).data() == None:
        model.item(idx).setData(value[0])

    elif type(value) == int:
      self.valueView.setItemDelegateForRow(idx, IntDelegate(self))
      if model.item(idx).text() == '':
        model.item(idx).setText(str(value))
      if model.item(idx).data() == None:
        model.item(idx).setData(value)
      

    elif type(value) == float:
      self.valueView.setItemDelegateForRow(idx, FloatDelegate(self))
      if model.item(idx).text() == '':
        model.item(idx).setText(str(value))
      if model.item(idx).data() == None:
        model.item(idx).setData(value)

    elif type(value) == list:
      self.valueView.setItemDelegateForRow(idx, ListDelegate(self, value))
      if model.item(idx).text() == '':
        model.item(idx).setText(str(value[0]))
      if model.item(idx).data() == None:
        model.item(idx).setData(value[0])

    

class IntDelegate(QtWidgets.QItemDelegate):

  def __init__(self, parent):
    super(IntDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    editor = QtWidgets.QLineEdit(parent)
    editor.setValidator(QtGui.QIntValidator())
    return editor

  def setModelData(self, editor, model, index):
    super(IntDelegate, self).setModelData(editor, model, index)
    item = model.itemFromIndex(index)
    item.setData(int(editor.text()))

class FloatDelegate(QtWidgets.QItemDelegate):

  def __init__(self, parent):
    super(FloatDelegate, self).__init__(parent)

  def createEditor(self, parent, option, index):
    editor = QtWidgets.QLineEdit(parent)
    editor.setValidator(QtGui.QDoubleValidator())
    return editor

  def setModelData(self, editor, model, index):
    super(FloatDelegate, self).setModelData(editor, model, index)
    item = model.itemFromIndex(index)
    item.setData(float(editor.text()))

class ListDelegate(QtWidgets.QItemDelegate):

  def __init__(self, parent, value):
    super(ListDelegate, self).__init__(parent)
    self.value = value

  def createEditor(self, parent, option, index):
    editor = QtWidgets.QComboBox(parent)
    for item in self.value:
      editor.addItem(item)
    
    return editor

  def setModelData(self, editor, model, index):
    super(ListDelegate, self).setModelData(editor, model, index)
    item = model.itemFromIndex(index)
    item.setData(editor.currentText())

class DefaultDelegate(QtWidgets.QItemDelegate):
  def __init__(self, parent, default, valid_type):
    super(DefaultDelegate, self).__init__(parent)
    self.default = default
    self.valid_type = valid_type

  def createEditor(self, parent, option, index):
    editor = QtWidgets.QLineEdit(parent)
    editor.setValidator(DefaultValidator(self.default, self.valid_type))
    return editor

  def setModelData(self, editor, model, index):
    super(DefaultDelegate, self).setModelData(editor, model, index)
    item = model.itemFromIndex(index)
    item.setData(editor.text())

class TupleDelegate(QtWidgets.QItemDelegate):
  def __init__(self, parent, valid_type):
    super(TupleDelegate, self).__init__(parent)
    self.valid_type = valid_type
  
  def createEditor(self, parent, option, index):
    editor = QtWidgets.QLineEdit(parent)
    editor.setValidator(TupleValidator(self.valid_type))
    return editor

  def setModelData(self, editor, model, index):
    super(TupleDelegate, self).setModelData(editor, model, index)
    text = editor.text()
    tuple_list = text.replace('(', '').replace(')', '').split(',')
    converted_tuple_list = []
    for item in tuple_list:
      converted_tuple_list.append(self.valid_type(item))
    item = model.itemFromIndex(index)
    item.setData(tuple(converted_tuple_list))


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

class TupleValidator(QtGui.QValidator):

  def __init__(self, valid_type):
    super(TupleValidator, self).__init__()
    self.valid_type = valid_type

  def validate(self, input, pos):

    if input == '':
      return QtGui.QValidator.Intermediate, input, pos

    if input.count('(') > 1 or input.count(')') > 1:
      return QtGui.QValidator.Invalid, input, pos

    if ')' in input and input[-1] != ')':
      return QtGui.QValidator.Invalid, input, pos

    if input[0] != '(':
      return QtGui.QValidator.Invalid, input, pos

    elif input[-1] == ')':
      state = QtGui.QValidator.Acceptable
      input_list = input[1:-1].split(',')
    else:
      state = QtGui.QValidator.Intermediate
      input_list = input[1:].split(',')
    
    

    # if at least one of the list isn't integer then state is set to that state

    for item in input_list:
      if self.valid_type == int:
        cur_state, _, _ = QtGui.QIntValidator().validate(item, pos)
        if cur_state != QtGui.QValidator.Acceptable:
          state = cur_state
    return state, input, pos
