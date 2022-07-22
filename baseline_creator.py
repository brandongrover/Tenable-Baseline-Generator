import re
from os import listdir


def parse_new_baseline(input_file, exclusion_list):
    # Open the input file and save as object
    with open (f"./Input/{input_file}", 'r') as f:
        audit_file = f.read()
    f.close()

    # Extract using Regex the <custom_item> tag/area
    extractions = []
    if exclusion_list.get(input_file):
        for exception in exclusion_list.get(input_file):
            try:
                new_string = '(?s)(^[^\n]*)<custom_item>.{0,200}([^\n]*description\s*:[^\n]*' + f"\"{re.escape(exception)}\")\n" + ".*?</custom_item>"
                query = re.compile(new_string, re.MULTILINE)
                find = re.search(query, audit_file)
                print("File: " + input_file + " Applied: " + str(re.search(r'\d[^\s]*', find.group(2)).group(0)))
                new_desc = re.sub(re.escape(exception), f'[Exception Applied] {exception}', find.group(2))
                # Craft output to warning with the descriptor of the exception and maintaing spacing (capture group 1)
                new_output = str(find.group(1)) + '<report type:"WARNING">\n'+ str(find.group(1)) + "  " + new_desc + "\n" + str(find.group(1)) + '</report>'
                audit_file = re.sub(query, new_output, audit_file)
                extractions.append(find.group(0))
            except:
                print(f"File: {input_file} | Not Applicable: {exception}")

        # Output extraction file
        extraction_file = re.sub(r'.audit', "-Extractions.txt" , input_file)
        with open (f"./Output/{extraction_file}", 'w') as fx:
            for extraction in extractions:
                fx.write("-" * 200 + "\n")
                fx.write(str(extraction) + "\n")          
        fx.close()

        # Output new custom audit file
        output_file = re.sub(r'.audit', "-Custom.audit" , input_file)
        with open (f"./Output/{output_file}", 'w') as f:
            f.write(str(audit_file))
        f.close()


# Move this to JSON File and maintain as "All server exceptions", add to it adhoc?
exclusion_list = {
        'CIS_Ubuntu_20.04_LTS_v1.1.0_Server_L1.audit': [
            '1.3.2 Ensure filesystem integrity is regularly checked',
            '1.7.2 Ensure local login warning banner is configured properly - banner',
            '1.7.2 Ensure local login warning banner is configured properly - platform flags',
            '1.7.3 Ensure remote login warning banner is configured properly - banner'
        ]
    }

# Parse through every input and create a new baseline
find_inputs = listdir('.\Input')
for audit in find_inputs:
    parse_new_baseline(audit, exclusion_list)
