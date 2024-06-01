
# Find the extension of a file based on a string
def find_extension(file_name):
    # Split the file name by the period
    split = file_name.split(".")
    # Return the last element of the split
    return split[-1]


def lambda_handler(event, context):
    bucket_name = event["detail"]["bucket"]["name"]
    object_name = event["detail"]["object"]["key"]
    extension = find_extension(object_name)

    return {
        "bucket_name": bucket_name,
        "object_key": object_name,
        "extension": extension
    }