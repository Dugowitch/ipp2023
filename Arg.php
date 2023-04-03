<?php
abstract class Arg {
    protected static $pattern;

    function __construct($arg){
        $this->arg = $arg;
    }

    public function checkSyntax(){
        global $xml;
        if (!preg_match(static::$pattern, $this->arg)){
            // echo $this->arg;
            // echo static::$pattern."\n"; // REMOVE
            // echo "> TU SA TO POKAZILO"; // REMOVE
            
            exit(23);
        }
        return $this;
    }

    abstract public function printXML($n);
}


class Variable extends Arg {
    protected static $pattern = "/^(G|L|T)F@[A-Za-z_\-$&%*!?][A-Za-z_\-$&%*!?0-9]*$/";
    
    public function printXML($n){
        global $xml;
        $xml->startElement('arg'.$n);
        $xml->writeAttribute('type', "var");
        $xml->text($this->arg);
        $xml->endElement();
    }
    
}

class Symbol extends Arg {
    protected static $pattern = "/^((G|L|T)F@[A-Za-z_\-$&%*!?][A-Za-z_\-$&%*!?0-9]*|int@[\-+]?([0-9]+|0x[A-Fa-f0-9]+)|bool@(true|false)|nil@nil|string@([^\\\\\s#]|\\\\\d{3})*)$/";
    
    private static function _parseArg($str){
        $parts = explode("@", $str);
        switch ($parts[0]){
            case 'int': case "bool": case "string": case "nil": 
                return $parts;
            
            case "GF": case "LF": case "TF":
                return ["var", $str];
        }
    }
    
    public function printXML($n){
        global $xml;
        $xml->startElement('arg'.$n);
        $parts = $this->_parseArg($this->arg);
        $xml->writeAttribute('type', $parts[0]);
        $xml->text($parts[1]);
        $xml->endElement();
    }
}

class Label extends Arg {
    protected static $pattern = "/^[A-Za-z_\-$&%*!?][A-Za-z_\-$&%*!?0-9]*$/";
    
    public function printXML($n){
        global $xml;
        $xml->startElement('arg'.$n);
        $xml->writeAttribute('type', 'label');
        $xml->text($this->arg);
        $xml->endElement();
    }
    
}

class Type extends Arg {
    protected static $pattern = "/^(int|string|bool)$/";
    
    public function printXML($n){
        global $xml;
        $xml->startElement('arg'.$n);
        $xml->writeAttribute('type', 'type');
        // preg_replace(["/</", "/>/", "/&/"], ["&lt;", "&gt;", "&amp;"], $this->line); // TODO
        $xml->text($this->arg);
        $xml->endElement();
    }
    
}
?>