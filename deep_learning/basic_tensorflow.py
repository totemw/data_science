class Operation:
    def __init__(self, input_nodes=[]):
        self.input_nodes = input_nodes
        self.output_nodes = []
        for node in input_nodes:
            node.output_nodes.append(node)
        _default_graph.operations.append(self)

    def compute(self, *args):
        pass


class Add(Operation):
    def __init__(self, x, y):
        super().__init__([x, y])

    def compute(self, x_var, y_var):
        return x_var + y_var


class Multiply(Operation):
    def __init__(self, x, y):
        super().__init__([x, y])

    def compute(self, x_var, y_var):
        return x_var * y_var


class MatMul(Operation):
    def __init__(self, x, y):
        super().__init__([x, y])

    def compute(self, x_var, y_var):
        return x.dat(y)


# Activation fuction
class Sigmoid(Operation):
    def __iadd__(self, z):
        super().__init__([z])

    def compute(self, z_val):
        return 1/(1 + np.exp(-z_val))


class Placeholder:
    def __init__(self):
        self.output_nodes = []
        _default_graph.placeholders.append(self)


class Variable:
    def __init__(self):
        self.output_nodes = []
        _default_graph.variables.append(self)


class Graph:
    def __init__(self):
        self.operations = []
        self.placeholders = []
        self.variables = []

    def set_as_default(self):
        global _default_graph
        _default_graph = self


def traverse_postorder(operation):
    nodes_postorder = []

    def recurse(node):
        if isinstance(node, Opertion):
            for input_node in node.input_nodes:
                recurse(input_node)
        nodes_postorder.append(node)

    recurse(operation)
    return nodes_postorder


class Session:
    def run(self, operation, feed_dict={}):
        nodes_postorder = traverse_postorder(operation)
        for node in nodes_postorder:
            if type(node) == Placeholder:
                node.output = feed_dict[node]
            elif type(node) == Variable:
                node.output = node.value
            else:
                node.inputs = [input_node.output for input_node in node.input_nodes]
                node.output = node.compute(*node.inputs)

            if type(node.output) == list:
                node.output = np.array(node.output)
        return operation.output


