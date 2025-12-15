# Networking Basics for Cyber

## Learning objectives
- Explain IP addresses, ports, and protocols in plain language
- Describe DNS and why it matters for security
- Identify common “network-level” failure and attack patterns

## Minimum viable networking
- **IP address**: identifies an endpoint on a network
- **Port**: identifies a service on that endpoint
- **Protocol**: the rules for communication (TCP/UDP, HTTP/S, DNS)

## DNS (critical dependency)
DNS turns names into IP addresses.
If DNS is manipulated, users can be redirected to the wrong destination.

### Teaching demo ideas (portable)
- `nslookup example.com`
- `ping example.com`
- `traceroute` / `tracert` (show the path conceptually)

## Security lens
- Open ports expose services (attack surface)
- Misconfigured networks can leak internal services
- DNS and routing failures can look like “the internet is down,” but have many causes

## Optional visual
Place images in `images/` and reference them relatively:

`![DNS resolution flow](images/dns-flow.png)`
