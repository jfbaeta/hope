# HOPE - HANA on POWER Enhanced

This project is intended to accelerate SAP HANA Deployments on POWER Systems, helping to create SAN Storage based LVM Components: /etc/multipath.conf file, wwids and aliases, Physical Volumes, Volume Groups, Logical Volumes and File Systems.

## Getting Started

With root user, create a directory called /opt/hope, download the files and place under it.

## Prerequisites

* SuSE Linux Enterprise Server 11 SP 4;
* SuSE Linux Enterprise Server for SAP Applications 11 SP 4;
* Python 2.6.9

## Examples:

To Open a Menu:

```
hope -m
```

To create a /etc/multipath.conf file: interactively (flags c and S):

```
hope -cS
```

To create Volume Groups interactively (flags c and V):

```
hope -cV
```

To list current Logical Volumes (flags l and L):

```
hope -lL
```

To remove File Systems (flags r and F):

```
hope -rF
```

To list all resources (flags l and a):

```
hope -la
```

To create Logical Volumes from a JSON config file (flags C and L):

```
hope -CL
```

To create all resources from a JSON config file (flags C and a):

```
hope -Ca
```

To remove all resources (flags r and a):

```
hope -ra
```

## Known Issues

* Only IBM Storwize Storage is supported at this time (more to come!);
* SuSE Linux Enterprise Server 12 is not supported yet;

## Versioning

[SemVer](http://semver.org/) is (tentatively) used for versioning. 

## Authors

**Juliano Fernandes Baeta** - [jfbaeta](https://github.com/jfbaeta)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

