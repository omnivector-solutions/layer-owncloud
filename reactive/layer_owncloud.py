from charms.reactive import when, when_not, set_state

from charmhelpers.core.hookenv import open_port, status_set


OWNCLOUD_PORT = 80

@when_not('owncloud.http.available')
def open_owncloud_port():
    open_port(OWNCLOUD_PORT)
    set_state('owncloud.http.available')


@when('apt.installed.owncloud')
def status_persist():
    status_set('active', "Owncloud listening on port {}".format(OWNCLOUD_PORT))


@when('http.available')
def configure_http(website):
    website.configure(OWNCLOUD_PORT)
