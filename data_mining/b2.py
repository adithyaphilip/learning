import random
import types
import math

class Node:
    def __init__(self, inodes, onodes, bias, l):
        '''
            onodes is list of tuples, first index is node, 2nd index is weight of link to that node
            similarly inodes, excpet onodes is output nodes and inodes is input nodes
        '''
        self.inodes = inodes
        self.onodes = onodes
        self.err = None
        self.bias = bias
        self.op = None
        self.l = l # learning rate
        self.lfunc = None

    def reset(self):
        self.op = None;
        self.err = None;
        for i in self.onodes:
            i[0].reset()

    def act_func(self):
        return math.tanh(self.ip)

    def get_differential(self):
        ip = self.ip
        return 4 * (math.e**(2*ip))/((1 + math.e**(2*ip))**2)

    def output(self):
        if len(self.inodes) == 0:
            return self.ipval;
        if self.op is None:
            self.ip = sum([i[0].output()*i[1] for i in self.inodes]) + self.bias
            self.op = self.act_func()
        return self.op

    def error(self):
        if len(self.onodes) == 0:
            return self.final_op_node_error()
        if len(self.inodes) == 0:
            for pair in self.onodes: pair[0].error() 
            return;
        if self.err is None:
            self.err = self.get_differential()*sum([i[0].error()*i[1] for i in self.onodes])
            for pair in self.onodes:
                pair[1] += self.l * pair[0].error() * self.output()
            self.bias += self.l * self.err;
            # if a callback has been define for changing l, call it before op is invalidated
            if self.lfunc is not None:
                self.l = self.lfunc(self)
        return self.err

    def final_op_node_error(self):
        if self.err is None:
            self.err = self.get_differential() * (self.expected - self.output())
            self.bias += self.l * self.err;
        return self.err

class NeuralNetwork:
    def __init__(self, layers,  max_epoch, min_diff):
        self.layers = layers
        self.inodes = layers[0]
        self.onodes = layers[-1]
        self.max_epoch = max_epoch
        self.min_diff = min_diff
        self.t = 0 # number of iteratons
    
    def _get_op(self):
        return [node.output() for node in self.onodes] # recursive nature ensures feed forward

    def _set_error(self):
        for node in self.inodes: node.error() # recursive nature ensures back propagation

    def do_iteration(self):
        self.prep_iter()
        self.op = self._get_op()
        self._set_error()
        self.t+=1
        return self.op

    def terminate(self):
       return self.t==self.max_epoch or len(list(filter(lambda x: abs(x[0] - x[1]) > self.min_diff,zip([node.expected for node in self.onodes], self.op))))==0 
   
    def prep_iter(self):
        for node in self.inodes:
            node.reset() # resets op and err

    def begin(self):
        while True:
            self.do_iteration()
            if self.t == 1:
                print("----------------------------------------------------------")
                print("First Iteration")
                self.print_wt_bias()
                print("----------------------------------------------------------")
            if self.terminate(): break
        print("No. of Iterations:",self.t)
        print("Termination criterion - iterations reaches ",self.max_epoch,"or error becomes less than or equal to",self.min_diff)
        print("----------------------------------------------------------")
        print("Final Iteration")
        self.print_wt_bias()
        print("----------------------------------------------------------")
        return self.op

    def print_wt_bias(self):
        print("Printing Weights and Biases (as applicable):")
        print()
        print("Input Layer",*["Weights: " + str(list(map(lambda x: x[1],inode.onodes))) for inode in self.layers[0]], sep="\n")
        print()
        for layer in self.layers[1:-1]:
            print("Hidden Layer", *["Bias: " + str(node.bias) + " Weights: " + str(list(map(lambda x: x[1], node.onodes))) for node in layer], sep="\n")
            print()
        print("Output Layer",*["Bias: " + str(node.bias) for node in self.layers[-1]],sep="\n")
        print()
            
    
random.seed(100) 
def get_rand():
    if random.randint(0,1) == 1:
        return random.random()
    else: return -random.random()

def start():
    layers = []
    ip_tuple = eval(input("Please enter input values\n")) # read in input values
    inodes = []
    for ip in ip_tuple:
        node = Node([], [], get_rand(), 1)
        # learning rate set initially to 1, 1/2 next iteration, and so on
        node.lfunc = lambda x: 1/(1/x.l + 1)
        node.ipval = ip;
        inodes.append(node)
    layers.append(inodes)

    hnum = int(input("Enter number of hidden layers\n"))
    for _ in range(hnum):
        # read in number of nodes in hidden layer
        hnodes = [Node([],[],get_rand(), 1) for i in range(int(input("Enter no. of nodes in hidden layer #" + str(_+1) + "\n")))]
        for node in hnodes: 
            node.lfunc = lambda x: 1/(1/x.l + 1)
        layers.append(hnodes)

    # read in expected values in output layer
    op_val = eval(input("Enter values of output nodes\n")) # expected values
    onodes = []
    for op in op_val:
        node = Node([],[], get_rand(), 1)
        node.expected = op
        node.lfunc = lambda x: 1/(1/x.l + 1)
        onodes.append(node)

    layers.append(onodes)

    # builds the links between the layers
    for i in range(1, len(layers)):
        layer = layers[i]
        for node in layer:
            for inode in layers[i-1]:
                w = get_rand()
                node.inodes.append([inode,w])    
                inode.onodes.append([node,w])

    network = NeuralNetwork(layers, int(input("Enter max number of iterations to perform\n")), float(input("Enter acceptable error for stopping iterations\n")))
    print("Final outputs:", network.begin())
start()
