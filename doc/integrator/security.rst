.. _integrator_security:

Security
========

Enable / Disable WMS GetCapability
----------------------------------

Set ``hide_capabilities`` to ``true`` in your ``vars_<project>.yaml`` to disable
the WMS GetCapability when accessing the Mapserver proxy (mapserverproxy).

Default: ``false``

Enable / Disable layer(s) in the WMS GetCapability
--------------------------------------------------

To hide protected layers from the WMS GetCapabilities, set ``use_security_metadata`` to ``true`` in your ``vars_<project>.yaml``.

Be careful that too many protected layers will cause an error because Apache has a
8190 characters hard limit for GET query length.

Default: ``false``

Enable / Disable the admin interface
------------------------------------

To disable the admin interface, set ``enable_admin_interface`` to ``false``
in your ``vars_<project>.yaml`` file.

Default: ``true``

Enable / Disable the OGC proxy
------------------------------

To disable the OGC proxy, set ``ogcproxy_enable`` to ``false`` in your
``vars_<project>.yaml`` file.

Default: ``true``

In the ``viewer.js`` files you should also remove the ``OpenLayers.ProxyHost`` configuration.

This implies that all external WMS services (from the database and from the WMS browser) should
have the CORS headers (`enable-cors.org <http://enable-cors.org/server.html>`_).

Using a proxy for the OGC proxy
--------------------------------

When the requests made by the OGC proxy should be made through a proxy, an
additional Python package (``pysocks``) has to be used. Add this package to
the ``install_requires`` section of your ``setup.py`` file::

    install_requires=[
        ...
        'pysocks'
    ],

Install the package with::

    make -f <user>.mk install

The proxy is configured in ``<project>/__init__.py``. Add the following lines
after the call to ``config.include('c2cgeoportal')``::

        config.include('c2cgeoportal')

        from papyrus_ogcproxy import views as ogcproxy_views
        from httplib2 import ProxyInfo
        import socks
        ogcproxy_views.proxy_info = ProxyInfo(socks.SOCKS5, 'localhost', 1080)

This makes the OGC proxy use a proxy service at ``localhost:1080``. For more
information on how to configure the proxy, please refer to the documentation of
`PySocks <https://github.com/Anorov/PySocks>`_ and
`httplib2 <http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html#httplib2.ProxyInfo>`_.
