#!/usr/bin/perl -w

use strict;
use CGI::Carp qw(fatalsToBrowser);

# DISPLAY ERROR MESSAGES
BEGIN { $| = 1; open (STDERR, ">&STDOUT"); print qq~Content-type: text/html\n\n~; }

print time;
