"""
let int=1,float=2 and double =3
S: id=expr {if type(id)<type(expr): error()}
expr: expr '+' expr {type(expr)>=max(type(expr1),type(expr2))
]
and so on...include real and integer constants as well as identifiers..
use symbol table..in yacc, just print out the derivation rules, in python

"""
import re

def dummy(node):
    pass

def fun1(node):
    'S-> if_block S'
    if node.children[0].correct and 'lambda' not in node.children[1].production:
        print('Following statements are unreachable')
        t.pre_order(node.children[1])
        node.correct=node.children[0].correct
    elif 'lambda' in node.children[1].production: node.correct=node.children[0].correct
    else: node.correct=node.children[1].correct
def fun2(node):
    'S-> statement S'
    'S-> Decl S'
    node.correct=node.children[1].correct
def fun3(node):
    'S-> return *'
    node.correct=True
def fun4(node):
    'S-> Block S'
    Block,S=node.children[0],node.children[1]
    node.correct=Block.correct or S.correct
def fun5(node):
    'S-> lambda'
    node.correct=False
def fun6(node):
    'Block-> OP S CP'
    node.correct=node.children[1].correct

def fun7(node):
    'if_block-> if cond Block temp_if'
    Block,temp_if=node.children[2],node.children[3]
    node.correct=Block.correct and temp_if.correct

def fun8(node):
    'temp_if-> else Block'
    node.correct=node.children[1].correct

def fun9(node):
    'temp_if-> lambda'
    node.correct=False

def fun10(node):
    'expr-> id = expr'
    node.correct = node.children[2].correct and node.children[0].value >= node.children[2].value 

def fun11(node):
    'expr-> expr OPR expr'
    node.correct = node.children[0].correct and node.children[2].correct
    node.value = max(node.children[0].value, node.children[2].value)
def fun12(node):
    'expr-> FNUM'
    node.correct = True
    node.value = 2
def fun13(node):
    'expr-> DNUM'
    node.correct = True
    node.value = 3
def fun14(node):
    'expr-> NUM'
    node.correct = True
    node.value = 1

#rules dictionary
rules={'S : if_block S':fun1,'S : statement S':fun2,'':dummy,'S : Decl S':fun2,"S : Return ID":fun3,"S : Block S":fun4,
"S : lambda": fun5,"Block : OP S CP":fun6,"if_block : IF COND Block temp_if":fun7,'temp_if : ELSE Block':fun8,
'temp_if : lambda':fun9, 'expr : ID = expr':fun10, 'EXPR : EXPR OPR EXPR':fun11, 'EXPR : FNUM':fun12, "EXPR : DNUM":fun13, "EXPR : NUM":fun14 }

class Node:
    def __init__(self):
        self.children=[]
        self.value=''

class Tree:
    def __init__(self):
        self.root=Node()
        self.root.value='Start'
        self.list=[]
    def searchR(self,root,k):
        if root.value==k and root.children==[]:
            self.found=True
            return root
        res=None
        for r in root.children[::-1]:
            if not(self.found):
                res=self.searchR(r,k)
            else:
                break
        return res
    def search(self,k):
        self.found=False
        return self.searchR(self.root,k)

    def insert(self,head,body):
        r=self.search(head)
        if body=='':body='lambda'
        r.production=head.strip()+' : '+body.strip()    
        if body=='':
            t=Node()
            t.value=''
            t.production=''
            r.children.append(t)
            self.list.append(t)
            return
        for i in body.strip().split():
            t=Node()
            if i=='lambda':i=''
            t.value=i
            t.production=''
            r.children.append(t)
            self.list.append(t)
    
    def pre_order(self,root):
        if root.children==[]:
            print root.value,
            return
        for i in root.children:
            self.pre_order(i)

    def check_unreachable(self,root=1):
        if root==1:
            root=self.root.children[3]
        if root!=None:
            for i in root.children:
                if i.value not in ['S','if_block','Block','temp_if']:continue
                self.check_unreachable(i)
            rules[root.production](root)#?ya
    
    def check_returntypes(self,root=1):
        if root==1:
                self.returntype=self.root.children[0].children[0].value
                self.symtab={}
                root=self.root
        if root!=None:
            if 'Decl' in root.production:
                ret_type=root.children[0].children[0].children[0].value
                variable=root.children[1].children[0].value[0]
                self.symtab[variable]=ret_type
            if 'Return' in root.production and len(root.children)>1:
                var=root.children[1].children[0].value[0]
                if self.symtab[var]!=self.returntype:
                    print('Error: '+root.children[0].value+' '+var+';')
                    print(var+' is of type '+self.symtab[var]+'. Expected return type: '+self.returntype);
            for i in root.children:self.check_returntypes(i)
                

    def __str__(self):
        self.pre_order(self)
        return ''

f=open('./op.txt')
l=f.readlines()[::-1] 
t=Tree()
# creating production tree
for i in l:
    i=i.strip()+' '
    prod_head=i[:i.index('->')]
    prod_body=i[i.index('-> ')+3:].strip()
    if 'lambda' in prod_body:
        prod_body=''
    t.insert(prod_head,prod_body)
    #t.pre_order(t.root)
    #print

t.check_returntypes()
t.check_unreachable()
if t.root.children[3].correct!=True:
    print('Function '+t.root.children[1].children[0].value+' may not return anything')

def t_debswag(tree):
    # beginning swag, please wear sunglasses
    root = tree.root
