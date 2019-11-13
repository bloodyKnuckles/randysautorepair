#!/usr/bin/perl -w

use strict;
use CGI qw( :standard );
#use File::HomeDir;
use lib '/usr/home/jayblu/inc';
use lib '/usr/www/users/jayblu/re/common';

# DISPLAY ERROR MESSAGES
#BEGIN { $| = 1; open (STDERR, ">&STDOUT"); print qq~Content-type: text/html\n\n~; }


# GET PAGE VAR
my $page = "home.html";
if ( defined(param( "page" )) 
  && !(param( "page" ) =~ /^(\/|\.|(ht|f)tp:\/\/)/)
  && "" ne param( "page" )
) { $page = param( "page" ); }
# CHECK IF PAGE EXISTS
if ( !(-e "pages/" . $page) ) { 
  our $old_page = $page;
  $page = "error_page.pl"; 
}


# PREPARSE CGI FILES
my $pre_parse = 0;
our $body = "";
if ( $page =~ /.*\.cgi$/ ) { 
  require "pages/".$page or die "Can't require $page."; 
  $pre_parse = 1;
}

# PRINT MIME HEADER
print qq~Content-type: text/html\n\n~;

# TRAFFIC COUNTER
#require("counter.pl");
#our $counter = &counter;
#if ( "home.html" eq $page && !defined(param( "me" )) ) { $counter += 30000; }
our $counter = -1;

# INSERT TEMPLATE
our $template = "cobb_sub.html";
if ( defined(param( "p" )) ) { $template = "cobb_print.html"; }
elsif ( "home.html" eq $page ) { 
  $template = "cobb_home.html"; 

  use DBI;

  require "db_jayblu_re_read.pl";
  my $dbh = DBI->connect(&db_jayblu_re_read) or die "Could not connect to DB";

  my $sql = "SELECT";
  $sql .= " hits";
  $sql .= " FROM Counter";
  $sql .= " WHERE page = 'site'";
  my ($hits) = $dbh->selectrow_array($sql);
  $counter = $hits if defined($hits);

  $dbh->disconnect();
}

# TEMPLATE
open(TEMPLATE,$template) or die "Can't open TEMPLATE";
while(<TEMPLATE>) { 


  if ( $_ =~ /<!-- MARQUEE GOES HERE -->/ ) {
    my $marquee = '';
    open MARQUEE, 'marquee.txt' or die "Can't open MARQUEE for reading $!";
    $marquee =  <MARQUEE>;
    close MARQUEE;
    $marquee = qq~<marquee>$marquee</marquee>~;
    print $marquee if '' ne $marquee;
  }

  elsif ( $_ =~ /<!-- AGENT GOES HERE -->/ ) {
    # temporarily  removed julie
    my @agents = ('shelly', 'charley', 'robert', 'wes', 'tony', 'david', 'brenda', 'alan', 'monica', 'john', 'lisa', 'michael', 'shelly', 'charley', 'robert', 'wes', 'tony', 'david', 'brenda', 'alan', 'monica', 'john', 'lisa', 'michael');
    print '<img src="images/';
    if ( defined(param( 'me' )) ) { print param( 'me' ); }
    else { print $agents[int rand($#agents + 1)]; }
    print '.jpg" width="234" height="282" alt="">';
  }

  elsif ( $_ =~ /<!-- BODY GOES HERE -->/ ) {

    # PARSE PL FILES
    if ( $page =~ /.*\.pl$/ ) { 
      require "pages/".$page or die "Can't require $page."; 
    }

    # INSERT CONTENT
    elsif ( $page =~ /.*\.html$/ && 0 == $pre_parse ) {
      open(CONTENT,"pages/".$page) or die "Can't open CONTENT";
      while(<CONTENT>) { print $_; }
      close(CONTENT);
    } 

    # PRINT PRE-PARSED OUTPUT
    else { print $body."\n"; }
  }

  elsif ( $_ =~ /<!-- COUNTER GOES HERE -->/ && -1 < $counter ) {
    $counter = sprintf "%06d", $counter;
    my @counter_array = split //, $counter;
    foreach ( @counter_array ) {
      print "<img src=\"images/counter_" . $_ . ".gif\"";
      print " width=\"15\" height=\"18\" alt=\"\">";
    }
  }

  else { print $_; }
}
close(TEMPLATE);
#print $page;
exit;
