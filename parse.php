<?php
ini_set('display_errors', 'stderr');

echo("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
echo("<program language=\"IPPcode23\">\n");
echo("</program>\n");

$var = "/(G|L|T)F@[A-z_-$&%*!?][A-z_-$&%*!?0-9]*/";
$label = "/[A-z_-$&%*!?][A-z_-$&%*!?0-9]*/";
$symb = "/(int|string|float|bool|nil))@[A-z_-$&%*!?][A-z_-$&%*!?0-9]*/";
$type = "/(int|string|bool)/";

// read stdin
while (false !== ($line = fgets(STDIN))){
    $line = trim($line);
    
    // rozdeliť podla # => zbaviť sa komentárov
    $temp = explode('#', $line);
    if (strlen($temp[0]) == 0){ // line is just comment
        continue;
    } else if (count($temp) > 1 && $temp[1]){ // there is a comment at the end of a line
        unset($temp[1]);
    }

    // rozdeliť podla ws => na časti
    $parts = explode(' ', $temp[0]);
    foreach ($parts as $part){
        echo $part . "\n";
    }
    switch (strtoupper($parts[0])){
        // nothing
        case "CREATEFRAME": case "PUSHFRAME": case "POPFRAME": case "RETURN": case "BREAK":
            # code...
            break;
        
        // ⟨var⟩
        case "DEFVAR": case "POPS":
            # code...
            break;
        
        // ⟨label⟩
        case "CALL": case "LABEL": case "JUMP":
            # code...
            break;
        
        // ⟨symb⟩
        case "PUSHS": case "WRITE": case "EXIT": case "DPRINT":
            # code...
            break;
        
        // ⟨var⟩ ⟨symb⟩
        case "MOVE": case "INT2CHAR": case "STRLEN": case "TYPE":
            # code...
            break;
        
        // ⟨var⟩ ⟨type⟩
        case "READ":
            # code...
            break;
        
        // ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩
        case "ADD": case "SUB": case "MUL": case "IDIV": case "LT": case "GT": case "EQ": case "AND": case "OR": case "NOT": case "STRI2INT": case "CONCAT": case "GETCHAR": case "SETCHAR":
            # code...
            break;
        
        // ⟨label⟩ ⟨symb1⟩ ⟨symb2⟩
        case "JUMPIFEQ": case "JUMPIFNEQ":
            # code...
            break;
        }
    }

exit(0);
?>

