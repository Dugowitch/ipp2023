<?php
ini_set('display_errors', 'stderr');
require_once "./Instruction.php";

$xml = new XMLWriter();
$xml->openURI('php://stdout');
$xml->startDocument('1.0', 'UTF-8');
$xml->startElement("program");

// TODO: read program args
// TODO: check for .IPPcode

while (false !== ($line = fgets(STDIN))){
    $ins = new Instruction($line);
    $ins->checkSyntax()->printXML();
}

$xml->endElement();
$xml->endDocument();
exit(0);
?>

