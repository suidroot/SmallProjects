#!/opt/local/bin/perl -w
# This script is used to Read and Write Investment transaction data to and from CSV and QIF format.
#
# CSV data is returned to the Terminal
# QIF formant is written to a with the same name as input file only with .qif appended.


use Getopt::Std;
use Text::CSV;
use Finance::QIF;

# global options
use vars qw/ %opt /;
my $opt_string = 'h?wrf:';
getopts( "$opt_string", \%opt );

my $input_file = "";
if ($opt{'f'} ) {
    $input_file = $opt{'f'} ;
} else {
    die "You must specify an input file with the -f switch.";
}

sub readqif {
  
	my $qif = Finance::QIF->new( file => $input_file,record_separator => "\n"  );

	my $csv = Text::CSV->new(); 
 
	#print '"Date","Payee","Transaction","Category"', "\n";

	while ( my $record = $qif->next ) {
	
		if ($record->{'header'} eq 'Type:Invst') {
	
			$csv->combine($record->{'header'}, 
				$record->{'date'},
				$record->{'action'},
				$record->{'security'},
				$record->{'price'},
				$record->{'quantity'},
				$record->{'transaction'},
				$record->{'memo'},
				$record->{'commission'},
				$record->{'account'},
				$record->{'total'});
			print $csv->string(), "\n";
	
		} elsif ($record->{'header'} eq 'Type:CCard' || $record->{'header'} eq 'Type:Bank' 
		|| $record->{'header'} eq 'Type:Cash' || $record->{'header'} eq 'Type:CCard' 
		|| $record->{'header'} eq 'Type:Oth A' || $record->{'header'} eq 'Type:Oth L') {

			$csv->combine($record->{'date'},
				$record->{'payee'},
				$record->{'transaction'},
				$record->{'category'});
			print $csv->string(), "\n";
		} else {
			print "unrecognized\n";
			next;
	
		}
	}
}

sub writeqif {

  	$newfile = $input_file . '.qif';
	my $qif = Finance::QIF->new( file => ">$newfile", record_separator => "\n", debug => 1 );
	$qif->open();
	my $csv = Text::CSV->new ();
 	open my $io, "<", $input_file or die "$input_file: $!";
 	while (my $row = $csv->getline ($io)) {
     	my @fields = @$row; 
     	
     	$qif->header($fields[0]); 

		my $record = {
			header => $fields[0],
			date => $fields[1],
			action =>  $fields[2],
			security =>  $fields[3],
			price =>  $fields[4],
			quantity =>  $fields[5],
			transaction =>  $fields[6],
			memo =>  $fields[7],
			commission =>  $fields[8],
			account =>  $fields[9],
			total =>  $fields[10]
		};
		
		$qif->write($record);
			
     	print @fields, "\n";
     }
     
     $qif->close();
}


if ($opt{'r'} ) {
	&readqif;
} elsif ($opt{'w'} ) {
	&writeqif;
} else {
	die "You must specify an action -w to write or -r to read";
}
 
1;