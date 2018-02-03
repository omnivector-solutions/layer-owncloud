# OwnCloud

Owncloud

# Usage
This charm requires a PostgreSQL database as a dependency, the easiest way to accomodate this is to deploy
the PostgreSQL charm along side this charm and relate the two.

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
* Enable Juju storage functionality
* Better config mgmt for `/var/www/owncloud/config/config.php`
* Snap?

### Authors/Contact
* James Beedy <jamesbeedy@gmail.com>

### Copyright
* James Beedy (c) 2017 <jamesbeedy@gmail.com>

### License
* Please see `copyright` file for license information
