#!/usr/bin/perl -w 
#
# Copyright 2006 VMware, Inc.  All rights reserved.
#

use strict;
use warnings;
use Data::Dumper;
use VMware::VIRuntime;

use constant ORPHAN=>0;
use constant VM=>1;
use constant DIRPOSTFIX=>"_orphaned";



my %opts = (
   ds => {
      type => "=s",
      help => "Name (regex) of the datastore(s) to be looked at.",
      required => 1,
   },
   print => {
      type => "!",
      help => "Print the identified files on the screen",
      required => 0,
   },
   delete => {
      type => "!",
      help => "Delete the identified files",
      required => 0,
   },
   move => {
      type => "=s",
      help => "Name of the datastore where selected files should be moved to.",
      required => 0,
   },
   simulate => {
      type => "!",
      help => "Go through all the code flow, but when it's time to apply the changes, just don't",
      required => 0,
   },
);
$ENV{PERL_LWP_SSL_VERIFY_HOSTNAME} = 0;
use IO::Socket::SSL ;
IO::Socket::SSL::set_defaults(SSL_verify_mode=>SSL_VERIFY_NONE);

select STDERR;
Opts::add_options(%opts);
Opts::parse();
Opts::validate();
Util::connect();


sub WaitForTask
{
  my %args = @_;
  my $taskMoRef=$args{mo_ref};
  #ManagedObjectReference
  my $LinePrefix=$args{prefix};
  my $task=Vim::get_view(mo_ref=>$taskMoRef);
  my $message='';
  my $oldmessage=".";

  while ($$task{info}{state}{val} =~ /queued|running/)
  {
    $message=$$task{info}{state}{val};
    if ($$task{info}{state}{val} eq 'queued')
    {
      sleep 1;
    }
    if ($$task{info}{state}{val} eq 'running')
    {
      if (defined($$task{info}{progress}))
      {
        $message=$message." ".$$task{info}{progress}."%";
      }
    }
    if ($$task{info}{description})
    {
      if ($$task{info}{description}{message})
      {
        $message=$message.": ".$$task{info}{description}{message};
      }
    }
    if ($message ne $oldmessage)
    {
      $oldmessage=$message;
      print STDERR $LinePrefix.$message."\n" if defined($LinePrefix);
    }
    #Update the task
    $task=Vim::get_view(mo_ref=>$$task{mo_ref});
  }
  if (defined($LinePrefix))
  {
    print $LinePrefix.$$task{info}{state}{val};
    if ($$task{info}{state}{val} eq 'error')
    {
      print STDERR ": ".$$task{info}{error}{localizedMessage};
    }
    print STDERR "\n";
  }
  return $task;
}

my $APIVersion = Vim::get_service_content()->about->apiVersion;
Util::trace(1, "API Version = $APIVersion\n");

my $dsregex = Opts::get_option('ds');
my $dsFilter={
  name => qr/$dsregex/,
};
my $print = Opts::get_option('print');
my $delete = Opts::get_option('delete');
my $move = Opts::get_option('move');
my $simulate = Opts::get_option('simulate');
if (Opts::option_is_set('move') && Opts::option_is_set('delete'))
{
  if ($move && $delete)
  {
    print "Error: please specify move OR delete\n";
    Opts::usage();
  }
}

for my $ds (@{Vim::find_entity_views(view_type => 'Datastore', filter=>$dsFilter, properties => [qw/name browser vm parent/])} )
{
  my $br=Vim::get_view(mo_ref => $ds->browser);
  my $task = WaitForTask (mo_ref => $br->SearchDatastoreSubFolders_Task(datastorePath=>"[$$ds{name}]",
      searchSpec => HostDatastoreBrowserSearchSpec->new( 
        details =>FileQueryFlags->new(fileType=>'true',fileOwner=>'false',
        fileSize=>'false',modification=>'false'),
        query => $br->supportedType ,sortFoldersFirst=>'true' 
      )
    ),
    prefix=>"Scanning $$ds{name} " 
    );
  my %ExistingFiles=();
  if ($$task{info}{state}{val} eq 'success')
  {
    for my $d (@{$$task{info}{result}})
    {
      my $fname;
      for my $f (@{$d->file})
      {
        $fname=$d->folderPath;
        $fname.=' ' if (substr($d->folderPath,-1,1) ne '/');
        $fname.= $f->path;
        $fname.= "/" if ($f->isa('FolderFileInfo'));
        if (!$f->isa('FolderFileInfo'))
        {
          $ExistingFiles{$fname}=ORPHAN;#By default they are all marked as not part of a VM
        }
        #print STDOUT "$fname\n";
      }
    }
  }
  #Now: we have the list of DS files,
  #We need to go through every VM, and get the list of the VM's files,
  #and with that we create 2 lists: files that belong to VMs, and files that don't.

  for my $vm (@{Vim::get_views(mo_ref_array=>$ds->vm,properties=>[qw/layoutEx/])})
  {
    for my $f (@{$vm->layoutEx->file}) 
    {
      $ExistingFiles{$f->name}=VM;
    }
  }
  #Get the datacentre, as ds->parent->parent
  my $DC = Vim::get_view(mo_ref=>$ds->parent,properties=>[qw/parent/])->parent;
  my $fm = Vim::get_view(mo_ref=>Vim::get_service_content()->fileManager);
  my $moveds ;
  my $movedc ;

  if (defined($move))
  {
    $moveds = Vim::find_entity_view(view_type => 'Datastore', filter=>{name=>$move}, properties => [qw/name browser vm/]);
    $movedc = Vim::get_view(mo_ref=>$moveds->parent,properties=>[qw/parent/])->parent;
  }
  #Now, we can work on the set of files we need
  for my $f (keys(%ExistingFiles))
  {
    if ($ExistingFiles{$f}==ORPHAN)
    {
      print STDOUT "$f\n" if defined($print) && $print;
      if ($delete)
      {
        if ($simulate)
        {
          print "Deleting $f\n";
        }
        else
        {
          my $task = WaitForTask (mo_ref => $fm->DeleteDatastoreFile_Task(name=>$f,datacenter=>$DC),prefix=>"deleting $f ");
        }
      }
      elsif ($move)
      {
        #Get the same name on the other datastore
        my $d = $f  =~ s/^\[.+\] (.+)\/[^\/]+$/[$move] $1/r;
        my $task = WaitForTask (mo_ref => $br->SearchDatastoreSubFolders_Task(datastorePath=>$d,
            searchSpec => HostDatastoreBrowserSearchSpec->new( 
              details =>FileQueryFlags->new(fileType=>'true',fileOwner=>'false',
                fileSize=>'false',modification=>'false'),
              query => $br->supportedType ,sortFoldersFirst=>'true' 
            )
          ),
          prefix=>"Scanning $d" 
        );

        #Check if dirctory exists, if it does, add a postfix to make unique
        if ($$task{info}{state}{val} eq 'success')
        {
          $d .= DIRPOSTFIX;
        }
        
        #MakeDirectory
        if ($simulate)
        {
          print "Mkdir $d\n";
        }
        else
        {
          $fm->MakeDirectory(name=>$d,datacenter=>$DC);
        }
        #MoveDatastoreFile_Task
        if ($simulate)
        {
          print "move $f to $d\n";
        }
        else
        {
        }
      }
    }
  }
}

Util::disconnect();
# vim: se tabstop=2 shiftwidth=2 expandtab:
