Troubleshooting
===============

.. _troubleshooting-vagrant:

Errors during Vagrant setup
---------------------------

* The Vagrant provisioning process during ``vagrant up`` assumes the presence of a stable internet connection. In the event of a connection interruption during provision, you may see errors similar to *"Temporary failure resolving.."* or *"E: Unable to fetch some archives.."* after the process has completed. In that situation, you can attempt to re-provision using the command:

  .. code-block:: bash

     >vagrant provision

  If that is still unsuccessful, you should attempt a ``vagrant destroy`` followed by another ``vagrant up``.

* If you encounter an error saying *"mount.nfs: requested NFS version or transport protocol is not supported"*, you should restart the kernel server service using this sequence of commands:

  .. code-block:: bash

    systemctl stop nfs-kernel-server.service
    systemctl disable nfs-kernel-server.service
    systemctl enable nfs-kernel-server.service
    systemctl start nfs-kernel-server.service

* If you encounter an error saying *"The guest machine entered an invalid state while waiting for it to boot. Valid states are 'starting, running'. The machine is in the 'poweroff' state. Please verify everything is configured properly and try again."* you should should check your host machine's virtualization technology (vt-x) is enabled in the BIOS (see this guide_), then continue with ``vagrant up``.

  .. _guide: http://www.sysprobs.com/disable-enable-virtualization-technology-bios

* On Windows, if upon running ``vagrant ssh`` you see the error *"/home/vagrant/.bash_aliases: line 1: syntax error near unexpected token `$'{\r''"* - it means your global Git line endings configuration is not correct. On the host machine run:

  .. code-block:: bash

    git config --global core.autocrlf input

  You will then need to delete and reclone the repo (or else do a force checkout).

Using supervisord for development
---------------------------------

On an ubuntu machine you can install supervisord with

.. code-block:: bash

   >sudo apt-get install supervisor

To start supervisord with an arbitrary configuration, you can type:

.. code-block:: bash

   >supervisord -c my_config_file.conf

You can find a supervisord config file inside the deployment/supervisord folder.
That config file contains a section for each service that you may want to run.
Feel free to comment one or more of those sections if you don't need that specific service.
If you just want to access the restful api or the admin for example, comment all those sections but the one
related to gunicorn.
You can stop supervisord (and all processes he's taking care of) with ctrl+c.
Please note that for some reasons you may need to manually kill the celery worker, for example when it's under heavy load.

Why is my celery ingestion not running?
---------------------------------------

If after a ``celery -A treeherder worker -B --concurrency 5`` you experience a static celery console with no output, similar to:

.. code-block:: bash

   09:32:40,010: WARNING/MainProcess] celery@local ready.

You should ctrl+c to shut down celery, remove the ``celerybeat-schedule`` file in the project root, and restart your worker.

Where are my log files?
-----------------------

You can find the various services log files under
  * /var/log/celery
  * /var/log/gunicorn

You may also want to inspect the main treeherder log file ~/treeherder/treeherder.log
