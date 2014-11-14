#!/usr/bin/perl


use strict;
use Data::Dumper;
use JSON::XS;
use HTTP::Tiny;


my $CurlBin="/usr/bin/curl";
my $CurlOpts="-k -X GET";
my $Curl="$CurlBin $CurlOpts";

my $Url="https://$ARGV[0]/api/";
my $ApiKey="$ARGV[1]";
my $ApiKeyString="?apikey=$ApiKey";

my $Request = "$ARGV[2]";

my $Debug = 1;

sub do_request {
  my %args = @_;
  my $url = $Url . $args{request} . $ApiKeyString;
  print $url . "\n" if $Debug;
 	my $response = HTTP::Tiny->new->get($url);
	if ( $response->{success} )
	{
		return decode_json $response->{content};
	} else {
    die ("Could not fetch $url: Response: $response->{status}: $response->{reason}\n");
  }
}

sub eventcheck {
  my $data = do_request(
      request => "events"
    );

  print Dumper($data) if $Debug;
  if ( $data->{data}->{total} == 0 ) {
    print "OK: No Events In ScaleArc\n";
    exit 0;
  } else {
    print "ERROR: Events were found in ScaleArc\n";

    foreach my $event ( $data->{data}->{events} ) {
      print Dumper ($event);
 #     print "PRIO=$event['priority'];"
      #TIME=$event->{time};TYPE=$event->{type}:ID=$event->{id};EVENT=$event->{event};\n";
    }
    exit 1; 
  }

}


if ( $Request eq "events" ) {
  eventcheck();
} elsif ( $Request eq "clusters" ) {

} elsif ( $Request eq "ha" ) {
} elsif ( $Request eq "license" ) {
} else {
  die ( "me no understando '$Request'\n");
}








# things to monitor
  # clusters
  # foreach
  #   cluster/-ID-

  # ha/heartbeat_status
  # ha/status

  # events

  # license # check for license expiration (report 30 days in advance?)





