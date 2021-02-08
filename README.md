# Simple Echo Server

A simple Flask-based echo server.

---

## Setup

### Prerequisites

- Python 3.7+

### Local config

<!-- add git clone steps -->
```bash
cd SimpleEchoServer
make venv

# make runs in a subprocess, so we need to activate the virtualenv manually before proceeding

source .venv/bin/activate

make install
make secret ReplaceThisWithYourSecretKey
```

At this point, you should be able to run the following command:

```bash
pytest
```

and finally, to get the endpoint at ```http://localhost:8000``` up and running:

```bash
flask run
```

To enable ```HTTPS```, you can use the ```make secure``` command provided to generate self-signed cert/key pem files - this will keep you from needing to click through the self-signed cert warning should you wish to check the endpoint in a browser. Once you've filled out the interactive prompt, pass the key files to flask with this new command:

```bash
flask run --cert=cert.pem --key=key.pem
```

Alternatively, if OpenSSL isn't an option and don't mind clicking through the self-signed cert warning, use Flask's built-in "adhoc" cert:

```bash
flask run --cert=adhoc
```

_Note:_ this option requires the PyOpenSSL package to be installed in the virtual environment. It's included, but wanted to highlight that this package is only required if using flask's adhoc cert feature.

## POST request to "/" endpoint

This simple API endpoint was tested using Postman, but cURL, the Python Requests library or any other RESTful POST request will work. The endpoint expects for both POSTs and GETs to contain the unique `server_key` you configured using `make secret`. It's stored in `.env` to keep secrets 12 factor and ephemeral.

## Measuring and observing

This is a small echo server, with one endpoint at `"/"` or root. Due to time constraints this project has no logging and very basic error handling. It does require the `SECRET_KEY` to be passed with all requests, and only supports GET and POST.

Good first steps to observe this endpoint would be:

### Configure all stout logs to be captured and routed to a separate server, logging service or both

Capturing logs and routing them to a service that allows searching and data exploration can be really helpful to diagnose tricky system behavior or look for new important metrics to track. I'm a firm believer in not reinventing perfectly good wheels, so I like tools like Papertrail and Splunk for log management - but ultimately the engineers working on the relevant product areas should also be comfortable with whatever tool is chosen as well.

Its also important to get these logs off of the server they originated from, because in the event of a breach, a red team or security threat could delete the logs and thus parts of their attack if stored on the same server. 

### Observe and capture all requests made to the endpoint

Understanding customer/user behavior helps SRE teams make better predictions and preparations, as well as helps product and engineering teams gain insight on their customers. Storing how this endpoint is used is a cross-team benefit.

### Surfacing relevant HTTP error codes

Surfacing 4xx and 5xx errors in a more digestible way - filtered out from the general appplication logs, perhaps with dashboards, alerting or paging attached - would allow a team to respond to issues with potential customer impact more quickly. 

In addition, this API explicitly returns a 403 when access is attempted with an incorrect or missing `server_key`. A lot of 403s at once would be a quick tip-off for either malicious or misinformed user behavior - for example, a typo in the documentation.

The HTTP codes surfaced and their relative severity would also be a good health check itself - say an endpoint gets a lot of timeout errors, what does that say about the API's health? Perhaps there's an upstream service that affects the performance of this API. Surfacing and documenting frequent but non-critical error codes would inform more sophisticated improvements to uptime and API performance down the road.

### More tests

Another easy win to observe this service would be to expand the test suite. In previous projects, it's been a great step to add a test suite for each time a repeatable customer issue was discovered - for example, these tests currently only check that strings are successfully echoed. Right now, the effect of POSTing a string of special characters, code, or anything else is unobserved.

### Team Process

Moving over to the people side of reliability, next steps for this project would be to work with the team of origin (me, in this case) to develop documentation and playbooks for the alerts or incidents we're currently observing. 

For example, as currently written, to productionize this codebase we'd eventually need a way to track and make sure our certs are kept up-to-date. Does cert-sharing between teams need to occur, or does this team have a group email + calendar that isn't dependent on any one team member? Product engineers should absolutely be able to take the occasional half-day friday without a missed reminder email causing weekend Sev2s, and thinking through the lifecycle of the service as a whole will catch some important and preventable issues up front.


## What I wish I had more time for!

Things that I had to skip or wish the experience was improved:

### Makefile

Makefiles run in subprocesses! I wanted _so bad_ for the initial project setup to be a single `make` command for onboarding simplicity, but no dice. `source` as a command doesn't work within Makefiles (at least on Mac) because `source` isn't POSIX compliant (or apparently even a command per se). Technically files can be sourced using the dot `. my_file` command, but that still wouldn't effect the current running process. `flask run` won't work outside of the virtual env, because Flask the dependency is only accessible from that context.

### .flaskenv

It's a huge security risk to include dotfiles in repos, but as no important secrets are stored and the contents are required to make the application run as intended, I broke that rule to keep the onboarding simple. 

Normally for onboarding documentation, even with simple non-secret-containing dotfiles, I prefer to include a `dotfile_EXAMPLE` to avoid any risk of the real thing being checked. But, I did not want onboarding steps that I could easily include for reviewer convenience, and the only secret involved is set using the `make secret` command at the beginning.

### pytest.ini

I spent more time than I wish to admit fighting to get environment-aware tests due to a bit of unfamiliarity with pytest env management. This is a restriction of pytest, and while it's actually good for a testing framework to force users to be explicit about testing assumptions, I could have bailed on demonstrating the `secret_key` functionality in tests and focused on a wider variety of test inputs, or perhaps restricted endputs. I did not do that - I traded more robust testing on part of my features for complete but shallow testing for all of my intended features. It would have been great to have both, but I stand by my choice.