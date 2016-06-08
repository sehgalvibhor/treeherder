# Gunicorn configuration file

import newrelic.agent


def worker_abort(worker):
    # Make sure the New Relic agent shuts down cleanly if a worker aborts
    # eg due to hitting the gunicorn request timeout.
    newrelic.agent.shutdown_agent(timeout=5.0)
    worker.log.info("New Relic: Shutdown Agent Complete.")
