# Yum Post-processor

Run a command when a yum package management command is invoked

## Installation

    cp postprocessor.py /usr/lib/yum-plugins/

    echo -e "[main]\nenabled = 1" > /etc/yum/pluginconf.d/postprocessor.conf

    # example command
    echo -e "command = logger" >> /etc/yum/pluginconf.d/postprocessor.conf

This plugin automatically runs every time yum does. The command can be
replaced with anything you want

## Usage

    $ sudo yum remove strace links

    # In /var/log/messages
    Jul 19 21:41:59 20110813 dw: action=remove name=strace version=4.5.18
    Jul 19 21:41:59 20110813 dw: action=remove name=elinks version=0.11.1
  
    $ sudo yum downgrade nmap -y
    Jul 19 14:26:31 20110813 d.wilson: action=downgrade name=nmap version=5.51 pending=4.85

### Use cases

 * Auditing puppet actions via some other mechanisism than yum log.
 * Raising an event on puppet change
 * Run your local monitoring after package change and check for breaks.

### Author

[Dean Wilson](https://www.unixdaemon.net)

### License

 * GPLv2
