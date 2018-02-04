import subprocess

from charms.reactive import when, when_not, set_flag

from charmhelpers.core import unitdata
from charmhelpers.core.hookenv import open_port, status_set, config, unit_public_ip
from charmhelpers.core.host import chdir, service_restart
from charmhelpers.core.templating import render

from pathlib import Path


CONFIG = config()
KV = unitdata.kv()


OWNCLOUD_PORT = 80
OWNCLOUD_HOST = CONFIG.get('fqdn') or unit_public_ip()
OWNCLOUD_DATA_DIR = Path('/var/www/owncloud/data')
OWNCLOUD_DIR = OWNCLOUD_DATA_DIR.parent


@when('postgresql.connected')
@when_not('owncloud.postgresql.requested')
def request_owncloud_database(pgsql):
    """Request Owncloud database
    """

    status_set('maintenance',
               'Requesting PostgreSQL database for Owncloud')

    pgsql.set_database(CONFIG.get('db-name', 'owncloud'))

    if CONFIG.get('pgsql-roles'):
        pgsql.set_roles(CONFIG.get('pgsql-roles'))
    if CONFIG.get('pgsql-extensions'):
        pgsql.set_extensions(CONFIG.get('pgsql-extensions'))

    status_set('active', 'Owncloud database requested')
    set_flag('owncloud.postgresql.requested')


@when('postgresql.master.available',
      'owncloud.postgresql.requested')
@when_not('owncloud.postgresql.available')
def save_database_connection_info(pgsql):
    """Save db config to unitdata
    """

    status_set('maintenance',
               'Getting/Setting details for Owncloud database.')
    KV.set('dbname', pgsql.master.dbname)
    KV.set('dbuser', pgsql.master.user)
    KV.set('dbpass', pgsql.master.password)
    KV.set('dbhost', pgsql.master.host)
    KV.set('dbport', pgsql.master.port)
    KV.set('dbtype', 'pgsql')

    status_set('active', 'Owncloud database available')
    set_flag('owncloud.postgresql.available')


@when('apt.installed.owncloud-files',
      'owncloud.postgresql.available')
@when_not('owncloud.init.available')
def init_owncloud():
    """Perform Owncloud init ops
    """

    status_set('maintenance', "Initializing Owncloud")

    db_config = KV.getrange('db')
    admin_user_config = {'admin_username': CONFIG.get('admin-username'),
                         'admin_password': CONFIG.get('admin-password')}
    data_dir_config = {'data_dir': OWNCLOUD_DATA_DIR}

    ctxt = {**db_config, **admin_user_config, **data_dir_config}

    owncloud_init = ("sudo -u www-data /usr/bin/php occ  maintenance:install "
                     "--database {dbtype} --database-name {dbname} "
                     "--database-host {dbhost} --database-pass {dbpass} "
                     "--database-user {dbuser} --admin-user {admin_username} "
                     "--admin-pass {admin_password} "
                     "--data-dir {data_dir} ").format(**ctxt)

    with chdir('/var/www/owncloud'):
        subprocess.call(owncloud_init.split())

    # Hack to get our public ip or fqdn into owncloud php file
    Path('/var/www/owncloud/config/config.php').write_text(
        Path('/var/www/owncloud/config/config.php').open().read().replace(
            "localhost", OWNCLOUD_HOST))

    status_set('active', "Owncloud init complete")
    set_flag('owncloud.init.available')


@when('apt.installed.apache2',
      'owncloud.init.available')
@when_not('owncloud.webserver.available')
def render_apache2_server_config():
    """Remove default apache2.conf, render owncloud apache2.conf
    """

    apache_default_conf_available = \
        Path('/etc/apache2/sites-enabled/000-default.conf')
    owncloud_conf_available = \
        Path('/etc/apache2/sites-available/owncloud.conf')
    owncloud_conf_enabled = \
        Path('/etc/apache2/sites-enabled/owncloud.conf')

    # Remove apache default server
    if apache_default_conf_available.exists():
        apache_default_conf_available.unlink()

    # Remove Owncloud available conf if exists
    if owncloud_conf_available.exists():
        owncloud_conf_available.unlink()

    # Remove Owncloud enabled conf if exists
    if owncloud_conf_enabled.is_symlink():
        owncloud_conf_enabled.unlink()

    # Render apache server to available
    render(source='owncloud.conf.tmpl',
           target=str(owncloud_conf_available),
           context={})

    # Symlink available to enabled
    owncloud_conf_enabled.symlink_to(str(owncloud_conf_available))

    # Enable modules
    for module in ['rewrite', 'headers', 'env', 'dir', 'mime']:
        subprocess.call(['a2enmod', module])

    # Restart apache2
    service_restart('apache2')

    set_flag('owncloud.webserver.available')


@when_not('owncloud.http.available')
@when('owncloud.init.available')
def open_owncloud_port():
    open_port(OWNCLOUD_PORT)
    set_flag('owncloud.http.available')


@when('owncloud.init.available')
def status_persist():
    status_set('active',
               "Owncloud available at http://{}/owncloud".format(
                   OWNCLOUD_HOST))


@when('http.available')
def configure_http(website):
    website.configure(OWNCLOUD_PORT)


@when_not('owncloud.postgresql.available')
def blocked_on_postgresql():
    status_set('blocked', "Need connection to PostgreSQL to continue")
    return
