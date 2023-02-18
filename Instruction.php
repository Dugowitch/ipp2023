<?php
require_once "./Arg.php";

class Instruction {
    private static $global_order = 1;

    function __construct($line){
        $this->line = $line;
        $this->clear = trim(preg_replace("/#.+/", "", $this->line)); // remove comments
        $this->args = preg_split("/[\t\r\v ]+/", $this->clear);
        $this->opcode = trim(array_shift($this->args));
        $this->argc = count($this->args);
        $this->order = self::$global_order;
        if ($this->opcode) self::$global_order++;
    }

    function checkSyntax(){
        switch (strtoupper($this->opcode)){
            case "":
                return $this;
                break;

            // nothing
            case "CREATEFRAME": case "PUSHFRAME": case "POPFRAME": case "RETURN": case "BREAK":
                if ($this->argc !== 0){
                    //! error - incorrectn umber of arguments
                }
                break;
                
            // ⟨var⟩
            case "DEFVAR": case "POPS":
                if ($this->argc !== 1){
                    //! error - incorrectn umber of arguments
                }
                $this->args[0] = new Variable($this->args[0]);
                $this->args[0]->checkSyntax();
                break;
            
            // ⟨label⟩
            case "CALL": case "LABEL": case "JUMP":
                if ($this->argc !== 1){
                    //! error - incorrectn umber of arguments
                }
                $this->args[0] = new Label($this->args[0]);
                $this->args[0]->checkSyntax();
                break;
            
            // ⟨symb⟩
            case "PUSHS": case "WRITE": case "EXIT": case "DPRINT":
                if ($this->argc !== 1){
                    //! error - incorrectn umber of arguments
                }
                $this->args[0] = new Symbol($this->args[0]);
                $this->args[0]->checkSyntax();
                break;
            
            // ⟨var⟩ ⟨symb⟩
            case "MOVE": case "INT2CHAR": case "STRLEN": case "TYPE":
                if ($this->argc !== 2){
                    //! error - incorrectn umber of arguments
                }
                $this->args[0] = new Variable($this->args[0]);
                $this->args[0]->checkSyntax();
                $this->args[1] = new Symbol($this->args[1]);
                $this->args[1]->checkSyntax();
                break;
            
            // ⟨var⟩ ⟨type⟩
            case "READ":
                if ($this->argc !== 2){
                    //! error - incorrectn umber of arguments
                }
                $this->args[0] = new Variable($this->args[0]);
                $this->args[0]->checkSyntax();
                $this->args[1] = new Type($this->args[1]);
                $this->args[1]->checkSyntax();
                break;
            
            // ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩
            case "ADD": case "SUB": case "MUL": case "IDIV": case "LT": case "GT": case "EQ": case "AND": case "OR": case "NOT": case "STRI2INT": case "CONCAT": case "GETCHAR": case "SETCHAR":
                if ($this->argc !== 3){
                    //! error - incorrectn umber of arguments
                }
                $this->args[0] = new Variable($this->args[0]);
                $this->args[0]->checkSyntax();
                $this->args[1] = new Symbol($this->args[1]);
                $this->args[1]->checkSyntax();
                $this->args[2] = new Symbol($this->args[2]);
                $this->args[2]->checkSyntax();
                break;
            
            // ⟨label⟩ ⟨symb1⟩ ⟨symb2⟩
            case "JUMPIFEQ": case "JUMPIFNEQ":
                if ($this->argc !== 3){
                    //! error - incorrectn umber of arguments
                }
                $this->args[0] = new Label($this->args[0]);
                $this->args[0]->checkSyntax();
                $this->args[1] = new Symbol($this->args[1]);
                $this->args[1]->checkSyntax();
                $this->args[2] = new Symbol($this->args[2]);
                $this->args[2]->checkSyntax();
                break;
            }
    return $this;
    }
    
    function printXML(){
        global $xml;
        if ($this->opcode == "") return $this;

        $xml->startElement("instruction");
        $xml->startAttribute("order");
        $xml->text($this->order);
        $xml->endAttribute();
        $xml->startAttribute("opcode");
        $xml->text($this->opcode);
        $xml->endAttribute();
        foreach ($this->args as $i => $arg){
            $arg->printXML($i+1);
        }
        $xml->endElement();
        
        return $this;
    }
}
?>