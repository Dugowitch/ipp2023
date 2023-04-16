Documentation of Project Implementation for IPP 2022/2023  
Name and surname: Jakub Dugovič  
Login: xdugov00

## Overall Design Philosophy
The `Interpreter` class in my code initializes and integrates various components, which collectively enable the interpreter to load, validate, and execute a program in the parsed XML representation of IPPcode23.

The codebase employs the singleton design pattern for implementing several classes that oversee distinct areas of an interpreter. All of them implement `getInstance()` method. The following classes are implemented:
* **ArgParser** for parsing command line arguments
* **FrameManager** for handling frames
* **FlowManager** for handling control flow
* **IOManager** for handling input and output
* **StackManager** for handling the data stack
* **XMLManager** for handling XML parsing and checking
* **InstructionFactory** for generating instructions

### Execution of Instructions
The `interpret()` method of the `Interpreter` class contains the program loop. To dynamically get and generate the appropriate instruction object based on the current opcode, it uses `FlowManager` and `InstructionFactory`.

### Program Arguments
The `ArgParser` class parses command line arguments. It saves the files as attributes of the class for further use. 

## Instrucitons
The `Instruction` abstract class and its subclasses are designed to work together to provide a complete set of instructions for the interpreted language. There are subclasses for all instructions of the IPPcode23 language, which implement the `execute()` abstract method.

### Instruction Factory
The `InstructionFactory` implements the Factory design pattern to generate instruction instances based on their opcode. The class has a generation method:  
`gen(self, ins)` takes an XML instruction element *ins* and returns an instance of the corresponding instruction class.

## Resource Management
The resource managers are designed to systematically manage all resources in a structured way. The managers constitute a comprehensive solution for resource handling.

### Frame Manager
**Frame** is a structure in which variables and their values are stored. `Frame` class uses python dictionary like a hashtable to implement the functionality. The following methods are defined:  
`defvar(self, name)` declares a variable with the given *name*,  
`save(self, name, value)` saves the *value* into frame\[*name*\],  
`getVal(self, name)` returns the value of the variable with the given *name*.

The `FrameManager` class manages the frames - global (`GF`), local (`LF`), and temporary (`TF`). `GF` and `TF` are instances of `Frame` class and `LF` is a list of its instances that is used like a stack. The manager contains several methods to manipulate the frames:  
`pushframe(self)` appends `TF` to `LF` and clears `TF`,  
`popframe(self)` removes the top instance in `LF` and saves it to `TF`,  
`createframe(self)` instantiates new `Frame` class to `TF`,  
`getVal(self, var)` returns the value of a variable *var*,  
`getFrame(self, var)` splits *var* that is in format *'frame@name'* into *frame* and *name*, and returns them,  
`currentLF(self)` is used like property; returns the top `Frame` instace in `LF`.

### Flow Manager
The `FlowManager` class manages the succession of instructions by keeping track of the "instruction pointer" (`ip`) which represents the order of the instruction being executed. It also contains `_labels` dictionary and a `_callstack` list that is used like a stack. Upon initialization, the class stores the order of each label in a dictionary. It implements these methods to control the flow:  
`jump(self, label)` sets `ip` to the order of *label*,  
`call(self, label)` appends the order of *label* to the `_callstack` and jumps to *label*,  
`ret(self)` removes the top of the `_callstack` and jumps to it.

### Input and Output Manager
The `IOManager` class is used to manage input (from `stdin`) and output (to both `stdout` and `stderr`). When initialized, it opens the *input file* for reading; and it is closed in destructor. The following methods are defined:  
`readOne(self)` reads and returns a single line of input stripped of any trailing whitespace,  
`read(self)` reads and returns text from standard input until EOF,  
`write(self, message, isError)` writes *message* to standard output; if optional parameter *isError* will be evaluated as True, it outputs to the standard error instead. Additionally, it parses escape sequences.

### Stack Manager
The `StackManager` class uses a list called `stack` as a stack data structure. The `stack` itself is stored as a static variable within the class. The class provides two methods:  
`push(symb)` adds *symb* to the top of the `stack`,  
`pop()` returns and removes the top of the `stack`.

### XML Manager
The `XMLManager` class is a wrapper for the `xml.etree.ElementTree`. It also provides additional methods for checking XML requirements specific for this project. It defines:  
`getIns(index)` returns the instruction element at *index* from root

## UML Diagram
The following UML diagram shows the class hierarchy of the classes used by my implementation of the interpreter.

![class diagram of the interpreter implementation](./classDiagram.svg)
