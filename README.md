# Lynx

 URL retrieval extension for [text-generation-webui](https://github.com/oobabooga/text-generation-webui).


# Warning

 No safety checks.

# Use

 Type lynx or links then the URL:

 Type `!lynx https://www.example.com`

 Type `!links https://www.example.com`

  Alternatively, you can use Lynx followed the URL with a new line and then a question to be answered, e.g.:

 Type
 ```
 !lynx https://www.example.com
 Sumarize the above site.
 ```
or

 ```
 !links https://www.example.com
 Sumarize the above site.
 ```
 
# Install

Make sure to run these commands after startign the Python environment
with the cmd script that came with text-generation-webui, e.g. for Linux use:
`cmd_linux.sh`

1. Clone the repository into the extensions folder within the
text-generation-webui project directory using the command:

   ```bash
   git clone https://github.com/yourusername/yourrepository.git lynx
   cd lynx
   # pip install -r requirements.txt
   ```

1. add the extension by modifying the launch commands for text-generation-webui, usually by editing CMD_FLAGS.txt to add `--extension lynx`
			
1. Finally, launch the text-generation-webui application. A new option
labeled "Use Lynx" should appear in the chat tab when
launched. Enabling this checkbox activates the extension; disabling it
deactivates it.

# References
- Used the skeleton for a similar extension from https://github.com/hav0x1014/web_search
