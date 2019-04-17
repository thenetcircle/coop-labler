# coop-labler

Cooperative labeling of training data.

![Project Types](docs/project-types.png)

## CLI tool to create/manage projects

For more details, see [README](labler/cli/README.md) in cli project.

    labler - Cooperative labeling of images
    Usage: labler [option(s)] <operation [parameters]>

        Options:
            --version (or -V):
                Echo version information and exit.
            --pretend (or -p):
                Just pretend to do actions, telling what you would do.
            --silent (or -s):
                Suppresses what is defined in 'suppressed'.
            --verbose (or -v):
                Makes labler more talkative.
            --classes (or -c):
                Specify how many classes a project has.
            --dir (or -d):
                Specify where the training data exists for this project (local fs only a of now) 
            --type (or -t):
                Specify the type of project, one of [classification (c), localization (l), detection (d), segmentation (s)]

        Operations:
            create <project name>
                Create a new project
            update <project name>
                Update an existing project
            claims <project name>
                List claims for a project
            projects
                List information about all projects
            help
                Show the help text and exit.

Listing available projects:

    $ ./bin/labler projects
    [-] listing projects
        
        project name        project type        classes             directory
        ---------------------------------------------------------------------
        test6               localization        3                   /tmp9/

Listing claims for above project:

    $ ./bin/labler claims test6
    [-] listing claims for project test6
        
        file name           status              claimed by          claimed at
        ----------------------------------------------------------------------
        g.jpg               finished            a-user              2019-04-17T03:49:06Z
        d.jpg               waiting             a-user              2019-04-17T03:49:06Z
        c.jpg               waiting             a-user              2019-04-17T03:49:06Z
        f.jpg               waiting             a-user              2019-04-17T03:49:06Z
        e.jpg               waiting             a-user              2019-04-17T03:49:06Z
        a.jpg               waiting             a-user              2019-04-17T03:49:06Z
        b.jpg               waiting             a-user              2019-04-17T03:49:06Z
        h.jpg               waiting             a-user              2019-04-17T03:49:06Z

## Vue.js frontend to label training data

See [README](web/README.md) in web project for more information.

## Flask backend for serving claims on training data to a group of users for different projects

Temporarily claim a batch of unlabelled examples as a user:

    $ curl localhost:4343/claim/project/test6/user/a-user
    {
        "data": [{
            "claimed_at": "2019-04-17T03:49:06Z",
            "claimed_by": "a-user",
            "file_name": "g.jpg",
            "file_path": "a",
            "id": 1,
            "project_name": "test6",
            "status": "finished"
        },
        [...]
        {
            "claimed_at": "2019-04-17T03:49:06Z",
            "claimed_by": "a-user",
            "file_name": "c.jpg",
            "file_path": "a",
            "id": 7,
            "project_name": "test6",
            "status": "waiting"
        }],
        "message": "",
        "status_code": 200
    }

Submit labels for a claim will resolve the claim:

    $ curl -H 'Content-Type: application/json' localhost:4343/submit/1 -X PUT -d \
         '{"project_type":"localization","xmin":1,"xmax":95,"ymin":50,"ymax":120,"target_class":"1"}'

See [README](labler/README.md) in labler project for more information.
