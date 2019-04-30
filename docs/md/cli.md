## Listing projects

```
$ labler projects
[-] listing projects
    
    project name        project type        classes             directory
    ---------------------------------------------------------------------
    some-project-name   localization        3                   /data/dw/images/2019
```

## Listing examples

```
$ labler examples some-project-name
[-] listing examples for project some-project-name
    
    width               height              file path                                file name
    ------------------------------------------------------------------------------------------
    433                 768                 /data/dw/images/2019                     10044.jpg
    1024                768                 /data/dw/images/2019                     10003.jpg
    1024                576                 /data/dw/images/2019                     10090.jpg
    432                 768                 /data/dw/images/2019                     10023.jpg
    433                 768                 /data/dw/images/2019                     10064.jpg
```

## Creating a new project

```
$ .labler create my-new-project-name --type localization --classes 2 --dir /data
[-] creating project: my-new-project-name
```

## Adding training data to a project

```
$ labler add my-new-project-name --dir /data/dw/images/2019 --cores 6
[-] adding directly "/data/dw/images/2019" to project: my-new-project-name
    
finding data        100%|███████████████████████████████████████████████████████| 94/94 [00:00<00:00, 5822.93it/s]
creating thumbs     100%|█████████████████████████████████████████████████████████| 94/94 [00:12<00:00,  7.55it/s]
```

## Syncing examples with file system

Remove examples from db if they no longer exist on the file system.

```
$ rm /data/dw/images/2019/10007.jpg
$ rm /data/dw/images/2019/10008.jpg
$ ./bin/labler sync my-new-project-name
[-] syncing project: my-new-project-name
[!] example for /data/dw/images/2019/10007.jpg does not exist, disabling
[!] example for /data/dw/images/2019/10008.jpg does not exist, disabling
```
