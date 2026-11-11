import math,random,os,json

with open("ann_weights.json", "r") as file:
    model = json.load(file)

neurons = model["hidden_layer"]
Hidden_neuron = model["output_layer"]

inputs = []
def flatten(digit):
    res = []
    for row in digit:
        for pixel in row:
            res.append(pixel)
    return res

#inputs
# inputs = flatten(digit)  


# for creating a neurons

# def Create_Neurons(neuron1,weight1):
#     neurons = []
#     for n in range(neuron1):
#         weights = []
#         for i in range(weight1):
#             weights.append(random.uniform(-1,1))
#         neuron = {
#         'weights' : weights,
#         'bias' : 0.1
#         }
#         neurons.append(neuron)
#     return neurons
# neurons = Create_Neurons(36,81)
def claculate(inputs,neuron):
    z = 0

    for i in range(len(inputs)):
        z = z + (inputs[i]*neuron['weights'][i])
    z = z + neuron['bias']
    return z

def ReLU(z):
    return max(0,z)

def Softmax(output):
    max_value = max(output)

    exp_values = []

    for value in output:
        exp_values.append(math.exp(value - max_value))

    total = sum(exp_values)

    probabilities = []

    for value in exp_values:
        probabilities.append(value / total)

    return probabilities
# For Train Model #
def forward(inputs):

    Hidden_Z = []
    Hidden_Layer1 = []

    # Hidden layer
    for neuron in neurons:
        z = claculate(inputs, neuron)
        Hidden_Z.append(z)
        Hidden_Layer1.append(ReLU(z))

    # Output layer
    logits = []

    for neuron in Hidden_neuron:
        z = claculate(Hidden_Layer1, neuron)
        logits.append(z)

    Output_Layer = Softmax(logits)

    return Hidden_Z, Hidden_Layer1, Output_Layer
# Train two
def train(inputs, target, learning_rate):

    # STEP 1: Forward propagation
    Hidden_Z, Hidden_Layer1, Output_Layer = forward(inputs)

    # STEP 2: Output gradients
    output_gradients = []

    for i in range(10):
        gradient = Output_Layer[i] - target[i]
        output_gradients.append(gradient)

    # STEP 3: Hidden gradients
    hidden_gradients = []

    for j in range(36):

        gradient = 0

        for i in range(10):
            gradient += (
                output_gradients[i] *
                Hidden_neuron[i]["weights"][j]
            )

        # ReLU derivative
        if Hidden_Z[j] <= 0:
            gradient = 0

        hidden_gradients.append(gradient)

    # STEP 4: Update output-layer weights and biases
    for i in range(10):

        for j in range(36):

            weight_gradient = (
                output_gradients[i] * Hidden_Layer1[j]
            )

            Hidden_neuron[i]["weights"][j] -= (
                learning_rate * weight_gradient
            )

        Hidden_neuron[i]["bias"] -= (
            learning_rate * output_gradients[i]
        )

    # STEP 5: Update hidden-layer weights and biases
    for j in range(36):

        for k in range(81):

            weight_gradient = hidden_gradients[j] * inputs[k]

            neurons[j]["weights"][k] -= (
                learning_rate * weight_gradient
            )

        neurons[j]["bias"] -= (
            learning_rate * hidden_gradients[j]
        )

    # STEP 6: Calculate loss
    loss = -math.log(
        max(Output_Layer[target.index(1)], 1e-15)
    )

    return loss

def train_model(inputs, target, epochs, learning_rate):

    for epoch in range(epochs):

        loss = train(inputs, target, learning_rate)

        if epoch % 100 == 0:
            print("Epoch:", epoch, "Loss:", loss)

    # Save trained weights
    model = {
        "hidden_layer": neurons,
        "output_layer": Hidden_neuron
    }

    with open("ann_weights.json", "w") as file:
        json.dump(model, file)

    print("Training completed!")

def run(data):
    inputs = flatten(data)
    
    Hidden_Layer1 = []
    for neuron in neurons:
        z = claculate(inputs,neuron)
        h = ReLU(z)
        Hidden_Layer1.append(h)

    #for creating a neurons
    # Hidden_neuron = Create_Neurons(10,36)

    Output_Layer = []
    for n in Hidden_neuron:
        z = claculate(Hidden_Layer1,n)
        Output_Layer.append(z)
    Output_Layer = Softmax(Output_Layer)
    # print(Output_Layer)
    # print(len(Output_Layer))
    op = []
    for i in range(len(Output_Layer)):
        op.append(round(Output_Layer[i],4)*100)
    result = []
    for i in range(len(op)):
        if(op[i] == max(op)):
            result.append(1)
        else:
            result.append(0)
    return result.index(max(result))
        
def main(c,epoch,learning):
        correct = []
        for i in range(10):
            if i == c:
                correct.append(1)
            else:
                correct.append(0)
            
        train_model(inputs,correct,epoch,learning)
        
# print(run(data))
# main()