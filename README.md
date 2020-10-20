# mockyer-maker

This application creates Tshield shaped mocks from Hoverfly's exported files.

# How to create my mocks?

Start Hoverfly then change it to capture mode:
``` hoverctl start ```
``` hoverctl mode capture --all-headers ```

Add Hoverfly as a proxy on your application:
``` HTTP_PROXY=http://localhost:8500 ```

Execute the request you want, then after the request is complete, export it from Hoverfly:
``` hoverctl export your_simulation.json ```

Run the mockyer-maker passing the exported file as an argument.

All the mocks will be generated on a folder that has your file's name:

``` If your file is called your_simulation.json, mocks will be created on a folder called your_simulation```