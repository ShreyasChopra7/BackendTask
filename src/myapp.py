import pandas as pd


# Main entry point
# Reading CSVs using pandas library
def main():
    post_codes_df = pd.read_csv("australian_post_codes.csv")
    address_df = pd.read_csv("sample_addresses.csv", delimiter="\t", header=None)
    # To make sure the result file is blank
    with open('result.txt', 'w'):
        pass
    for i in range(len(address_df)):
        address = str(address_df.iloc[i, 0])
        add_token = address.split(' ')
        if ',' in address:
            write_to_file(address)
        elif add_token[-1].isnumeric():
            parse_and_write(add_token, post_codes_df)
        else:
            parse_and_write_when_no_postcode(add_token)


# Parse and write an address when post code is not available
def parse_and_write_when_no_postcode(add_token):
    state = add_token[-1]
    suburb = add_token[-2]
    street = ' '.join(add_token[:-2])
    result = street + "," + suburb + "," + state
    write_to_file(result)


# Parse and write an address when post code is available in address CSV
def parse_and_write(add_token, post_codes_df):
    postcode = int(add_token[-1])
    state = add_token[-2]
    # Filtering dataframe on the basis of postcode found in post_codes CSV
    matched_codes_df = post_codes_df[post_codes_df['postcode'] == postcode]
    suburb_index = -5
    suburb = add_token[-5] + " " + add_token[-4] + " " + add_token[-3]
    suburb_in_title = add_token[-5].title() + " " + add_token[-4].title() + " " + add_token[-3].title()
    # Matching various combination of address tokens with place_name in post code CSV
    result_df = matched_codes_df[matched_codes_df['place_name'] == suburb_in_title]
    if result_df.empty:
        suburb_index = -4
        suburb = add_token[-4] + " " + add_token[-3]
        suburb_in_title = add_token[-4].title() + " " + add_token[-3].title()
        result_df = matched_codes_df[matched_codes_df['place_name'] == suburb_in_title]
    if result_df.empty:
        suburb_index = -3
        suburb = add_token[-3]
        suburb_in_title = add_token[-3]
        result_df = matched_codes_df[matched_codes_df['place_name'] == suburb_in_title]

    # Joining final token results and writing to write in a file
    street = ' '.join(add_token[:suburb_index])
    result = street + "," + suburb + "," + state + "," + str(postcode)
    print(result)
    write_to_file(result)


# Writing result to a file named result.txt
def write_to_file(result):
    with open('result.txt', 'a') as the_file:
        the_file.write(result + '\n')


# Main function entry point
if __name__ == '__main__':
    main()
