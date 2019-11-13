#!/usr/bin/perl -w

use strict;
use CGI qw( :standard );

# DISPLAY ERROR MESSAGES
#BEGIN { $| = 1; open (STDERR, ">&STDOUT"); print qq~Content-type: text/html\n\n~; }

# GET PAGE VAR
my $page = "pages_home.html";
if ( defined(param( "page" )) 
  && !(param( "page" ) =~ /^(\/|\.|(ht|f)tp:\/\/)/)
  && "" ne param( "page" )
) { $page = param( "page" ); }

my $now_date = `date +'%Y%m%d%H%M%S'`;
chomp $now_date;
my @months = ("", "Jan.", "Feb.", "Mar.", "Apr.", "May"
  , "June", "July", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."
);

# PRINT MIME HEADER
print qq~Content-type: text/html\n\n~;

# INSERT TEMPLATE
our $template = "template.html";
#if ( defined(param( "p" )) ) { $template = "template_print.html"; }
#elsif ( "pages_home.html" ne $page ) { $template = "template_sub.html"; }

# TEMPLATE
open(TEMPLATE,$template) or die "Can't open TEMPLATE $!";
while(<TEMPLATE>) { 



  if ( $_ =~ /<!-- PAGE TITLE GOES HERE -->/ ) {
    my $filename = $page;
    $filename =~ s/\.html//;
    $filename =~ s/_/ /;
    #$filename =~ s/((^\w)|(\s\w))/\U$1/xg;
    #$filename =~ s/([\w']+)/\u\L$1/g;    
    print $filename;
  }



  elsif ( $_ =~ /<!-- PAGES GO HERE -->/ ) {
    opendir PAGES, "." or die "Can't open PAGES $!";
    my @pages = grep /^pages_.+\.html(?!\.bak)/, readdir PAGES;
    closedir PAGES;

    my @pages_info = ();
    foreach ( @pages ) {
      open PAGE, "./$_" or die "Can't open PAGE $_ $!";

      # GET CATEGORY ORD
      my $cat_ord = <PAGE>;
      chomp $cat_ord;
      $cat_ord =~ s/(^<!-- | -->)//g;

      # GET PAGE ORD
      my $ord =  <PAGE>;
      chomp $ord;
      $ord =~ s/(^<!-- | -->)//g;

      # GET CATEGORY
      my $category = <PAGE>;
      chomp $category;
      $category =~ s/(^<!-- | -->)//g;

      # GET LABEL
      my $label =  <PAGE>;
      chomp $label;
      $label =~ s/(^<!-- | -->)//g;

      # GET PUBLISH DATE
      my $publish_date =  <PAGE>;
      chomp $publish_date;
      $publish_date =~ s/(^<!-- | -->)//g;

      close PAGE;

      # GET LINK
      my $link = $_;
      chomp $link;
      $link =~ s/^pages_//;

      push @pages_info, [$cat_ord, $ord, $category, $link, $label]
        if $publish_date < $now_date; 
    }

    my @sorted_pages_info = 
      sort { 
        @{$a}[0] <=> @{$b}[0] or @{$a}[1] <=> @{$b}[1] 
      } @pages_info;


    my $old_category = "";
    my $delimiter = "";
    foreach ( @sorted_pages_info ) {

      # PRINT PAGES
      if ( $old_category ne ${$_}[2] ) {
        print $delimiter, qq~  <div class="pages" id="pages_${$_}[0]">\n~;
        if ( "" ne ${$_}[2] ) {
        print qq~    <div class="pagescategory">~;
          print ${$_}[2], "</div>\n";
        }
        print "    <ul>\n";
        $delimiter = "    </ul>\n  </div>\n\n";
        $old_category = ${$_}[2];
      }
      print "      <li>";
      if ( "pages_" . ${$_}[3] ne $page ) {
        print qq~<a class="pagelink"~;
        print qq~ href="~, ${$_}[3], qq~">~;
      }
      else {
        print qq~<span class="currentpage">~;
      }
      print ${$_}[4];
      if ( "pages_" . ${$_}[3] ne $page ) { print "</a>"; }
      else { print "</span>"; }   
      print "</li>\n";
    }
    print "    </ul>\n";
    print "  </div>\n";
  }



  elsif ( $_ =~ /<!-- EVENTS GO HERE -->/ ) {

    # GET EVENTS
    opendir EVENTS, "." or die "Can't open EVENTS $!";
    my @events = grep { /^events_(\d{14}).*\.html(?!\.bak)/ and $1 ge $now_date } readdir EVENTS;
    closedir EVENTS;

    my @events_info = ();
 
    foreach ( @events ) {
      open EVENT, "./$_" or die "Can't open EVENT $_ $!";

      # GET EVENT LABEL
      my $event = <EVENT>;
      chomp $event;
      $event =~ s/(^<!-- | -->)//g;

      close EVENT;

      # GET EVENT DATE
      my $event_date = $_;
      chomp $event_date;
      $event_date =~ s/^.*(\d{14}).*$/$1/g;

      push @events_info, [$_, $event, $event_date]; 
    }

    if ( 0 < ($#events_info + 1) ) {
      print qq~  <div class="events">\n~;
      print qq~    <div class="eventscategory">Events:</div>\n~;

      print "    <ul>\n";
      foreach ( @events_info ) {

        # PRINT EVENTS
        print "      <li>", $months[(substr(${$_}[2], 4, 2) + 0)];
        print " ", substr(${$_}[2], 6, 2);
        print ", ", substr(${$_}[2], 0, 4);
        print qq~ <a href="~, ${$_}[0], qq~">~, ${$_}[1] , "</a></li>\n";
      }
      print "    </ul>\n";
      print "  </div>\n";
    }
  }



  elsif ( $_ =~ /<!-- ARTICLES GO HERE -->/ ) {

    # GET ARTICLES
    opendir ARTICLES, "." or die "Can't open ARTICLES $!";
    my @articles = grep { /^articles_(\d{14}).*\.html(?!\.bak)/ and $1 le $now_date } readdir ARTICLES;
    closedir ARTICLES;

    my @articles_info = ();
    foreach ( @articles ) {
      open ARTICLE, "./$_" or die "Can't open ARTICLE $_ $!";

      # GET ARTICLE LABEL
      my $article_label = <ARTICLE>;
      chomp $article_label;
      $article_label =~ s/^<!-- | -->//g;

      close ARTICLE;

      # GET ARTICLE PUBLISH DATE
      my $article_date = $_;
      chomp $article_date;
      $article_date =~ s/^.*(\d{14}).*$/$1/g;

      push @articles_info, [$_, $article_label, $article_date]; 
    }

    if ( 0 < ($#articles_info + 1) ) {
      print qq~  <div class="articles">\n~;
      print qq~    <div class="articlescategory">Articles:</div>\n~;

      print "    <ul>\n";
      foreach ( sort { @{$b}[2] <=> @{$a}[2] } @articles_info ) {

        # PRINT ARTICLES
        print "      <li>";
        if ( ${$_}[0] ne $page ) {
          print qq~ <a href="~, ${$_}[0], qq~">~;
        }
        else { print qq~<span class="currentpage">~; }
        print ${$_}[1];
        if ( ${$_}[0] ne $page ) { print "</a>"; }
        else { print "</span>"; }   
        print qq~ <span style="font-size: 12px;">~;
        print "(" , $months[(substr(${$_}[2], 4, 2) + 0)];
        print " ", substr(${$_}[2], 6, 2);
        print ", ", substr(${$_}[2], 0, 4), ")</span>";
        print "</li>\n";
      }
      print "    </ul>\n";
      print "  </div>\n";
    }
  }



  elsif ( $_ =~ /<!-- PAGE CONTENT GOES HERE -->/ ) {

    # PAGE NOT FOUND
    if ( !(-e $page) ) {
      print "Sorry, the page <span style=\"color: red;\">";
      print $page."</span> could not be found.";
      print "<br /><br />\n";
      print "<a href=\"home.html\">Return Home</a>\n";
    }

    # INSERT PAGE CONTENT
    else {
      open(CONTENT, $page) or die "Can't open CONTENT $!";
      while(<CONTENT>) { print $_; }
      close(CONTENT);
    }
  }



  else { print $_; } # PRINT TEMPLATE
}
close(TEMPLATE);
exit;

1;

