function[Force, Extension] = OT_csv_data_import(filename)
    sample_data=importdata(filename);
    Force=sample_data.data(:,2);
    Extension=sample_data.data(:,1);