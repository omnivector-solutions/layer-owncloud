# OwnCloud

Owncloud

# Usage

Deploy the Owncloud charm alongside PostgreSQL:
```bash
juju deploy owncloud

juju deploy postgresql

juju relate postgresql:db owncloud:postgresql
```

Once the owncloud charm is has completed its deployment, you can expose it for http access.
```bash
juju expose owncloud
```

Now you can access the owncloud service in your browser at `http://<ipaddress-of-owncloud-instance>/owncloud`.

## TODO
* Enable optional extensions/modules
* Optional relations for memcached and redis
* Enable S3/object storage functionality
* Snap?

### Authors/Contact
* James Beedy <jamesbeedy@gmail.com>

### Copyright
* James Beedy (c) 2017 <jamesbeedy@gmail.com>

### License
* Please see `copyright` file for license information
