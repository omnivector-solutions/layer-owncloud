# OwnCloud

Quick fast layer to demonstrate charming + owncloud

# Usage

Deploy the owncloud charm:
```bash
juju deploy cs:~jamesbeedy/owncloud-4
```

Once the owncloud charm is finished deploying, expose it to access the web interface:
```bash
juju expose owncloud
```

Now you can access the owncloud service in your browser at `http://<ipaddress-of-owncloud-instance>/owncloud`.


### Authors/Contact
* James Beedy <jamesbeedy@gmail.com>

### Copyright
* James Beedy (c) 2017 <jamesbeedy@gmail.com>

### License
* Please see `copyright` file for license information
