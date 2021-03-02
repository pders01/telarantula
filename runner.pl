#!/usr/bin/perl

use strict;
use warnings; 

my @ids = `cat targets.txt`;

foreach(@ids){
    system("/usr/bin/python /home/pauld/Projects/dut/telarantula/scraper.py $_");
}
