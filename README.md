Imagine world where you can use all the webservices in the world via single
command. Here comes ws - single, generic command-line tool to access all kind of web services.

Add you service to ws service directory and let anyone use it without 
the need to create or deploy any software or installing anything beyond ws client.

Benefits:

* Bring any api to the command line
* Process local files with various cloud-based services
* Try new services without installing any software (you'll need only ws client)
* Learn just one tool
* Use any mix of webservices and locally installed unix tools to slice, dice and filter your data,
  combining them with no effort.


Examples:

```sh
    ws example/cowsay say hello
```

     ------
    < hello >
     -------
     \ ^__^
      \ (oo)\_______
        (__)\ )\/\
             ||----w |
             ||     ||


```sh
    ws example/cowsay help
```
        Welcome to cow-as-as-service. We support following commands:

            help
                display help info

            say TEXT
                draw a cow saying TEXT


    #lets use a file
    ```sh
    ws --file - /proc/version example/cowsay say
    ```

        < Linux version 3.16.0-20-generic (buildd@klock) (gcc version 4.9.1 (Ubuntu 4.9.1-15ubuntu1) ) #27-Ubuntu SMP Wed Oct 1 17:35:12 UTC 2014 >
         ----------------------------------------------------------------------------------------------------------------------------------------- 
             \   ^__^
              \  (oo)\_______
                 (__)\       )\/\
                   ||----w |
                   ||     ||⏎  


    #take standard input and send as a file
    ```sh
    echo "yo" | ws --file - - example/cowsay say
    ```

         ____ 
        < yo >
         ---- 
             \   ^__^
              \  (oo)\_______
                 (__)\       )\/\
                   ||----w |
                   ||     ||⏎


    #Pipe it any way you want
    ```sh
    echo "yo" | ws --file - - example/cowsay say | wc -l
    ```
    
    8

        

    Isn't it awesome?





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
    ./ws --file remotename localname service options
    
    #note: remotename is a name under which file will be sent
    while local name defines which your file will that be.
    "-" as localname refers to standard input,
    so you can pip through ws.


Creating your own service:

    You can find example service here:
    https://github.com/Fiedzia/cow-as-as-service

    Note that this is only an example. You can create your service
    with any language or framework you choose,
    as long as it speaks http.
    The service needs to accept GET or POST request.
		Following parameters will be passed to the request:
				comand: name of the command
				You can define your commands and handle them however you want,
				but you should display list of supported cmmands and brief documentation
				when passed help command.

				arg - any number (possibly none) of additional arguments for command
		
		Its your service responsibility to validate parameters and return meaningfull and helpful
		message if they are wrong.


		Response:
			Return 200 response if you were able to parse command and its arguments,
			and you have data to return. Any output will be printed to standard output.
			
      Return 422 if a command or arguments are invalid.
			
				
    
Adding your service to service directory:

    See https://github.com/Fiedzia/servicedirectory.
    Add simple json file and make a pull request,
    and it should be soon added there.

