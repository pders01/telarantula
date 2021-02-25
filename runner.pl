#!/usr/bin/perl

use strict;
use warnings; 

<<<<<<< HEAD
my @ids = `cat targets.txt`;
=======
my @ids = `cat channel_ids.txt`;
>>>>>>> a48f43aeda54445fd1c57754ad6d3af9808b4c68

foreach(@ids){
    system("/usr/bin/python /home/pauld/Projects/dut/telarantula/scraper.py $_");
}
