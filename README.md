# Lynx

# lynx dump
 URL retrieval extension for [text-generation-webui](https://github.com/oobabooga/text-generation-webui).

 How to use

 Type lynx or links then the URL:

 Type ```!lynx https://www.example.com```

 Type ```!links https://www.example.com```

  Alternatively, you can use Lynx followed the URL with a new line and then a question to be answered, e.g.:

 Type
 ```
 !lynx https://www.example.com`
 Sumarize the above site.
 ```

or

 ```
 !links https://www.example.com`
 Sumarize the above site.
 ```
 

# How to install

*** Make sure to run these commands in the cmd script that came with text-generation-webui. eg ```cmd_linux.sh```(Linux) ***

1. First clone the repo to ```text-generation-webui/extensions``` folder

2. Then ```cd lynx``` and run ```pip install -r requirements.txt```, if any

3. Add ```lynx``` to launch commands of text-generation-webui
   like so ```--extension lynx```

4. Run text-gen-webui. There will be a checkbox with label ```Use Lynx``` in chat tab, this enables or disables the extension.

5. Done

# References
- Used the skeleton for a similar extension from https://github.com/hav0x1014/web_search
