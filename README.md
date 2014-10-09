Imagine world where you can use all the webservices in the world via single
command. Here comes ws - single, generic command-line tool to access all kind of web services.

Add you service to ws service directory and let anyone use it without 
the need to create or deploy any software or installing anything beyond ws client.


Examples:


    ws example/cowsay say hello


     ------
    < hello >
     -------
     \ ^__^
      \ (oo)\_______
        (__)\ )\/\
             ||----w |
             ||     ||


    ws example/cowsay help

        Welcome to cow-as-as-service. We support following commands:

            help
                display help info

            say TEXT
                draw a cow saying TEXT



Installation:

    You will need ws client. Its a simple python script, depending only on
    requests library. You can install it from you distribution repository,
    or use virtualenv to create local copy.

    To get it in debian or ubuntu, run:
        sudo apt-get install python3-requests

    Alternatively, you can set up virtualenv:

        sudo aptitude install virtualenv
        virtualenv -p python3 venv
        ./venv/bin/pip install requests

Usage:

    ./ws -h
    ./ws --help
    ./ws --list-services
    ./ws service_provider/service_name command options


Creating your own service:

    You can find example service here:
    https://github.com/Fiedzia/cow-as-as-service

    Note that this is only an example. You can create your service
    with any language or framework you choose,
    as long as it speaks http.
    
Adding your service to service directory:

    See https://github.com/Fiedzia/servicedirectory.
    Add simple json file and make a pull request,
    and it should be soon added there.

