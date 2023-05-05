import os
import tempfile
import csv
import gzip
import random

root_dir = '/Users/siddharthmadhavan/Desktop/CS598/mimiciv/1.0'

currFile = "/Users/siddharthmadhavan/Desktop/CS598/DatasetMaker/core/patients.csv.gz"
subject_ids = set()

def updateSubjects(f=currFile):
    with gzip.open(f, 'rb') as f_in:
        with tempfile.NamedTemporaryFile(delete=False) as f_out:
            f_out.write(f_in.read())
    
    with open(f_out.name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if the row has a subjectId field
            if 'subject_id' in row:
                subject_ids.add(row['subject_id'])
        return random.sample(sorted(subject_ids), 500)

    


for r, d, f in os.walk(root_dir):
    for dir in d:
        if dir != "icu":
            continue
        for root, dirs, files in os.walk(root_dir + "/" + dir):
            for file in files:
                # Check if the file is a CSV file compressed as Gzip
                if file.endswith('.csv'):
                    # Extract the file to a temporary directory
                    # with gzip.open(os.path.join(root, file), 'rb') as f_in:
                    #     with tempfile.NamedTemporaryFile(delete=False) as f_out:
                    #         f_out.write(f_in.read())
                            
                    if len(subject_ids) == 0:
                        subject_ids = updateSubjects()

                    # Open the CSV file and loop through each row
                    rows = []
                    with open("{}/{}/{}".format(root_dir,dir,file), 'r') as csvfile:
                        reader = csv.DictReader(csvfile)
                        headers = reader.fieldnames
                        for row in reader:
                            # Check if the row has a subjectId field
                            if 'subject_id' in row:
                                if row['subject_id'] in subject_ids:
                                    rows.append(row)
                        
                        new_file_name = file.split(".gz")[0]
                        with open("{}/{}".format(dir, new_file_name), 'w', newline='') as cf:
                            writer = csv.DictWriter(cf, fieldnames=headers)
                            writer.writeheader()
                            # Write the data to the CSV file
                            writer.writerows(rows)

                        # Open the CSV file for reading and compress it as a Gzip file
                        with open("{}/{}".format(dir, new_file_name), 'rb') as f_rin:
                            with gzip.open('{}/{}.gz'.format(dir, new_file_name), 'wb') as f_rout:
                                f_rout.writelines(f_rin)
                        os.remove("{}/{}".format(dir, new_file_name))
        
                # Delete the temporary file
                # os.remove(f_out.name)
                