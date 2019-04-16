# CLI tool to create/manage projects.

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
