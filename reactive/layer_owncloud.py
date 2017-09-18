from charms.reactive import when, when_not, set_state

from charmhelpers.core.hookenv import open_port, status_set


@when_not('layer-owncloud.installed')
def install_layer_owncloud():
    open_port(80)
    status_set('active', "Owncloud installed")
    set_state('layer-owncloud.installed')


@when('http.available')
def configure_http(website):
    website.configure(80)
