<?php
ini_set('display_errors', 'stderr');
require_once "./Instruction.php";

if ($argc == 2 && $argv[1] == "--help"){
    echo "Usage: parse.php <SOURCE_FILE\n";
    echo "    --help\tprints the help message\n";
    echo "No other arguments are supported. SOURCE_FILE should be a file in IPPcode23.\n";
    exit(0);
}

$xml = new XMLWriter();

function parseDoc(){
    global $xml;
    $xml->openURI('php://stdout');
    $xml->setIndent(true);
    $xml->setIndentString(' ');
    $xml->startDocument('1.0', 'UTF-8');
    $xml->startElement("program");
    $xml->writeAttribute("language", "IPPcode23");
    
    while (false !== ($line = fgets(STDIN))){
        $ins = new Instruction($line);
        $ins->checkSyntax()->printXML();
    }

    $xml->endElement();
    $xml->endDocument();
}

while (false !== ($line = fgets(STDIN))){
    if ((preg_match("/^\s*(\.IPPcode23)?\s*(#.*)?$/i", $line))){
        if ((preg_match("/\.IPPcode23/i", $line))){
            parseDoc();
            exit(0);
        }
    } else {
        exit(21);
    }
}
?>

