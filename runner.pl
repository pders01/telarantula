#!/usr/local/bin/perl

use strict;
use warnings;

my @ids = (
        1127975224,
        1163089897,
        1387359927,
        1118691233,
        1444373955,
        496597454,
        1446651076,
        1240262412,
        1444228991,
        1356469828,
        1478893059,
        1208168979,
        1339253689,
        1421548353,
        1375238175,
        371602955,
        1381836775,
        1429790717,
        1416039419,
        1126016709
        );

foreach(@ids){
    system("/usr/local/opt/python\@3.9/bin/python3.9 /Users/paulderscheid/Documents/Projects/telarantula/scraper.py $_");
}
