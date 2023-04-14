Documentation of Project Implementation for IPP 2022/2023  
Name and surname: Jakub Dugovič  
Login: xdugov00  

## Parser Structure
As a result of decomposition of the task there are several classes, e.i. Instruction, Arg, Variable, Symbol, Label, and Type. To generate the output XML, XMLWriter library was used. The source script in IPPcode23 language is read line by line. Furtheremore, each line is checked and if correct, the XML is generated.

### Instruction Class
Firstly, it tracks the order of the instructions, it's instances represent instructions. It takes the line from stdin as parameter; the line is trimmed, comments are removed, and spaces are standardized to a single space. Secondly, it has method `checkSyntax()` and `printXML()` that checks that an instruction has corresponding number of arguments that are of correct type - var, symb, label, or type. Moreover, the instructions in `checkSyntax()` are devided into groups by the number and type of arguments they have (e.g. both DEFVAR and POPS require a single var-type argument). An instance of Variable, Symbol, Label, or Type is generated for each of the arguments. Finally, the `printXML()` method generates part of the XML corresponding to the instruction being processed. All methods return $this, which enables method chaining (e.i. `$ins->checkSyntax()->printXML()`).

### Arg Class and Its Subclasses
To begin with, class Arg is an abstract class that implements `checkSyntax()` method and defines abstract method `printXML()`. Moreover, `checkSyntax()` uses `preg_match()` to determine argument corectness. Additionally, there are four classes that extend Arg - Variable, Symbol, Label, and Type. Each of the subclasses provides regex pattern to check the argument, and implements `printXML()`, that creates XML to represent the argument.

## Summary
To summarize, this implementation provides a simple and straight-forward way to process IPPcode23 code files, where the whole program, apart from the XMLWriter document creation and the initial ".IPPcode23" check, is a single while loop with 2 lines of code, which would be as user-frienly as possible.

    $ins = new Instruction($line);
    $ins->checkSyntax()->printXML();
