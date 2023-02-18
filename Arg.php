<?php
abstract class Arg {
    protected static $pattern;

    function __construct($arg){
        $this->arg = $arg;
    }

    public function checkSyntax(){
        if (!preg_match(static::$pattern, $this->arg)){
            echo "ERROR: pattern does not match!\n"; //! FIXME: temporary error message
            echo static::$pattern."\n";
        }
        return $this;
    }

    abstract public function printXML($n);
}


class Variable extends Arg {
    protected static $pattern = "/(G|L|T)F@[A-z_\-$&%*!?][A-z_\-$&%*!?0-9]*/";
    
    public function printXML($n){
        global $xml;
        $xml->startElement('arg'.$n);
        $xml->startAttribute('type');
        $xml->text('placeholder'); //! FIXME: add type
        $xml->endAttribute();
        $xml->endElement();
    }
    
}

class Symbol extends Arg {
    protected static $pattern = "/(G|L|T)F@[A-z_\-$&%*!?][A-z_\-$&%*!?0-9]*|(int|string|float|bool|nil)@[A-z_\-$&%*!?0-9]*/";
    
    public function printXML($n){
        global $xml;
        $xml->startElement('arg'.$n);
        $xml->startAttribute('type');
        $xml->text('placeholder'); //! FIXME: add type
        $xml->endAttribute();
        $xml->endElement();
    }
    
    
}

class Label extends Arg {
    protected static $pattern = "/[A-z_\-$&%*!?][A-z_\-$&%*!?0-9]*/";
    
    public function printXML($n){
        global $xml;
        $xml->startElement('arg'.$n);
        $xml->startAttribute('type');
        $xml->text('placeholder'); //! FIXME: add type
        $xml->endAttribute();
        $xml->endElement();
    }
    
}

class Type extends Arg {
    protected static $pattern = "/(int|string|bool)/";
    
    public function printXML($n){
        global $xml;
        $xml->startElement('arg'.$n);
        $xml->startAttribute('type');
        $xml->text('placeholder'); //! FIXME: add type
        $xml->endAttribute();
        $xml->endElement();
    }
    
}
?>