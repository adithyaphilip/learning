
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'C103969C63929C08CC2AACB5531DED34'
    
_lr_action_items = {'CB1':([2,6,8,9,10,11,12,13,],[-4,9,-4,-4,-4,-2,-1,-3,]),'B2':([0,1,2,4,8,9,10,],[1,1,1,1,1,1,1,]),'CB3':([4,7,8,9,10,11,12,13,],[-4,10,-4,-4,-4,-2,-1,-3,]),'$end':([0,3,8,9,10,11,12,13,],[-4,0,-4,-4,-4,-2,-1,-3,]),'B1':([0,1,2,4,8,9,10,],[2,2,2,2,2,2,2,]),'CB2':([1,5,8,9,10,11,12,13,],[-4,8,-4,-4,-4,-2,-1,-3,]),'B3':([0,1,2,4,8,9,10,],[4,4,4,4,4,4,4,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'S':([0,1,2,4,8,9,10,],[3,5,6,7,11,12,13,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> S","S'",1,None,None,None),
  ('S -> B1 S CB1 S','S',4,'p_expr','lexy.py',14),
  ('S -> B2 S CB2 S','S',4,'p_expr','lexy.py',15),
  ('S -> B3 S CB3 S','S',4,'p_expr','lexy.py',16),
  ('S -> <empty>','S',0,'p_expr','lexy.py',17),
]