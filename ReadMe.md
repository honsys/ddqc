How to Perform Data Delivery QC
===============================

\# If the current ADMIN password is the factory preset pin "123456",
please reset it. Instructions for (re)setting a pin are provided by
drive manual (see PDF file attached below) "Password Management" section
or this quick-ref: \[\[PIN instructions for the Impatient\]\]. Example
for generating a unique pin:

    printf "%04d-%04d-%04d-%04d\\n" $((RANDOM%10000)) $((RANDOM%10000)) $((RANDOM%10000)) $((RANDOM%10000)) 

\# Update or create a new USER pin/password for the drive. Example:

    printf "%04d-%04d-%04d-%04d\\n" $((RANDOM%10000)) $((RANDOM%10000)) $((RANDOM%10000)) $((RANDOM%10000))

\# Mount the drive by connecting its USB cable and unlock read access
using the new pin; and check that the mounted drive partition label
shows a PI or CI name (/Volumes/WhomeverPIorCI)

\# Check that the top-level mounted directory has the required ReadMe
file (also showing PI or CI name), and sha512 files. If a sha512
checksum file is present one can start the cross-check now (see step 7.)

\# Remove physical old label or create new and verify with info. from
Redmine Issue. Label templates are provided here:
https://redmine.biotech.ufl.edu/issues/4919

\# Verify runs and projects with the Redmine issue \#. For Illumina
runs, be sure to check the BaseSpace Run directory sym-link.

\# Verify ReadMe file contents match what is in the Redmine discription,
and the USB drive top-level directory. Optionally backup a copy of the
ReadMe somewhere under one's home directory or /var/tmp. Example:

    # check the shasum checksum file(s) in the top level directory is(are) congruent with the indicated shasum filenames in the Readme 
    egrep .sh512 *ReadMe.txt
    # backup ReadMe (there should only be 1 ReadMe file)
    cp -a *ReadeMe.txt /var/tmp

\# Make sure no files are zero in size. The bash find files output piped
to awk can help. Example:

    # find all (relevant) empty files under DirectoryName and count them
    find DirectoryName -exec ls -l {} \; | awk '{print $6, $10}' | egrep '^0 ' | grep -v '.stderr' | wc -l`
    # find and count all (relevant) non-empty files
    find [DirectoryName] -exec ls -l {} \; | awk '{print $6, $10}' | egrep -v '^0 ' | grep -v '.stderr' | wc -l`

\# Verify the delivery and sha512 checksum file contains the full list
of checksumed files, then start the "shasum -c" cross-check process.

    cat [checksum file ] | wc
    find [run and project names] | wc 

**Example:**\
List the contents of the drive

    icbr-ci-ws-m012:Kirst-Dervinis omar.lopez$ ls -laht
    total 2064
    drwxrwxrwt@ 5 root        admin               170B Apr 11 12:43 ..
    drwxr-xr-x  1 omar.lopez  UFAD\Domain Users   4.0K Apr 11 11:39 .
    -rwxr-xr-x  1 omar.lopez  UFAD\Domain Users   706K Apr 11 11:37 Kirst.Illumina.NextSeq.2016-04-07.sha512
    -rwxr-xr-x  1 omar.lopez  UFAD\Domain Users   321K Apr 11 11:35 Kirst.Illumina.NextSeq.2016-04-07.ReadMe.txt
    drwxr-xr-x  1 omar.lopez  UFAD\Domain Users   4.0K Apr  7 14:21 160405_NS500162_0280_AHY3K3BGXX
    drwxr-xr-x  1 omar.lopez  UFAD\Domain Users    28K Apr  7 13:55 NS_MKirst-161119_1-96Pool_4-5-2016-29620595
    drwxr-xr-x@ 1 omar.lopez  UFAD\Domain Users     0B Apr  7 13:48 $RECYCLE.BIN
    drwxr-xr-x@ 1 omar.lopez  UFAD\Domain Users     0B Apr  7 13:13 System Volume Information

Cat the sha512 and then find the amount of files contained within the
run and project directories and compare them.

    icbr-ci-ws-m012:Kirst-Dervinis omar.lopez$ cat Kirst.Illumina.NextSeq.2016-04-07.sha512 | wc
        3036    6528  722610
    icbr-ci-ws-m012:Kirst-Dervinis omar.lopez$ find [1N]* -type f | wc
        3036    3492  327930

Start checksum (optionally time the checksum via [time shasum -c)]()

    shasum -c [checksum file] output to text file for easy review 
    or
    time shasum -c [checksum file] output to text file for easy review

**Example:**

    icbr-ci-ws-m012:Kirst-Dervinis omar.lopez$ shasum -c Kirst.Illumina.NextSeq.2016-04-07.sha512 2>&1 > ~/Desktop/Kirst-Dervinis-QC-04-11-16.txt

    icbr-ci-ws-m012:Austin omar.lopez$ cat ~/Desktop/austin-qc.log | grep -v OK

1.  Upload (verified) ReadMe file to the Redmine Issue page.
2.  If "shasum -c" was timed, optionally edit the Redmine Issue page
    with wall-clock time info.
3.  Complete CI-EXIT tracking info at
    samba-svc.biotech.ufl.edu/uf-icbr/Organization/Sections/Cyberinfrastructure/Purchasing/CI
    Purchase Tracking/ci\_exit\_tracking.xlsx. Note only one person at a
    time can edit this xlsx file.
4.  Draft an email containing the pin created earlier - 7 email
    templates are provided (1 for each drive-type
    and instrument-data-type) \[\[Data Delivery Email Templates\]\].\
    \* Aegis Padlock: PacBio, and Illumina MySeq, NextSeq, and HiSeq.\
    \* Kingston: PacBio, and Illumina MySeq, and NextSeq.
5.  Double check the email content's pin value by locking and unlocking
    the drive; then send the email. To PI, User(s) , and the individual
    who originated the request; also CC to ICBR-CI and (TBD)
6.  Verify box and contents are complete and in good condition
7.  Ship drive or give to request submission
8.  Done

