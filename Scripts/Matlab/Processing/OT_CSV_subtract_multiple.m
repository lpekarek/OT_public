clear all 
close all



%set the treshold to sort the enriched ions


D= 0.001;


%% multiplefiles parameters

%specify the pattern of files to load 
pattern='*.csv';

    Folder_base='C:\Users\lpeka\Documents\MATLAB\OT\data\sorted\2019-12-18-WT-LH - 2A_smoothening\';

    myFolder = '02_forward\';
    
    
    Folder=[Folder_base myFolder];
     
% Specify the folder where the files will be exported.
exFolder_suffix= 'subtracted';
exFolder = [myFolder exFolder_suffix];
exFolder_full=[Folder_base exFolder];
mkdir(exFolder_full);

% Check to make sure that folder actually exists.  Warn user if it doesn't.
if ~isdir(Folder)
  errorMessage = sprintf('Error: The following folder does not exist:\n%s', myFolder);
  uiwait(warndlg(errorMessage));
  return;
end




%% import background from a file
    background='20191218-183414 FD Curve wt-lh-9-background_Butt_filtered_combined.csv'; %adresa k souboru
 
    Folder_background=[Folder_base '04_background\'];
 
    Whole_address_background=[Folder_background background] ;%adresa k souboru
    background_data=importdata(Whole_address_background);
    
   
    FC_background_PD=background_data.data(:,1);
    SC_background_F=background_data.data(:,2);
    
  % Get a list of all files in the folder with the desired file name pattern.
filePattern = fullfile(Folder,pattern); % Change to whatever pattern you need.
theFiles = dir(filePattern);

for k = 1 : length(theFiles)
    close all
    
     baseFileName = theFiles(k).name;
  fullFileName = fullfile(Folder, baseFileName);
  fprintf(1, 'Now reading %s\n', fullFileName);
  % Now do whatever you want with this file name,
  % such as reading it in as an image array with imread()
   % data import
   
   filename=fullFileName
   sample_data=importdata(filename);
    
    FC_sample_PD=sample_data.data(:,1);
    SC_sample_F=sample_data.data(:,2);
        
   
        
        for j=1:length(FC_sample_PD); %for each row (each detected m/z value)
            
            
            if FC_sample_PD(j) < max(FC_background_PD)
            [correspond_row, correspond_column, correspond_value]=find(FC_background_PD < FC_sample_PD(j) +D & FC_background_PD > FC_sample_PD(j)-D);
                %finds matches that are in the +-D interval
           % sorts the closest match 
             d= abs(FC_sample_PD(j)-FC_background_PD(correspond_row(1)));
           for m=1:length(correspond_row) ;
               
                if abs(FC_sample_PD(j)-FC_background_PD(correspond_row(m)))<= d ;
                d=abs(FC_sample_PD(j)-FC_background_PD(correspond_row(m)));
                closest_match=m;
                end 
            
           
            %subtracts the background
            difference(j)= SC_sample_F(j)-SC_background_F(correspond_row(closest_match));
            difference_trans=difference.'; %transpose the difference vector 
           end
            
            else
             difference(j)= SC_sample_F(j)-SC_background_F(length(FC_background_PD));
            difference_trans=difference.'; %transpose the difference vector    
            end
            
           
        end
    
    
    
    

    %% Subtracted background  


    Subtracted_sample=[FC_sample_PD,difference_trans]; %creates new matrix containing the first column with m/z values and second with the subtracted counts

    
    %% plot the data 
    close all
    plot(Subtracted_sample(:,1),Subtracted_sample(:,2)); %
    
    xlabel('Distance (um)');
    ylabel('Force (pN)');
    legend('Sample - Background', 'Location', 'best');
    title(baseFileName)
    
    grid on
    grid minor
    

    
    

%% export the subtracted data as a new excel file

%export dat
    lastletter=length(baseFileName)-4;
    
 %Subtracted sample
    
    Force=(Subtracted_sample(:,2));
    Piezo_Distance=(Subtracted_sample(:,1));
   
 
    T=table(Piezo_Distance, Force); %Creates table with anotated columns
    
    NewSuffix='_subtracted.csv';
    ExFilename=[baseFileName(1:lastletter),'_',NewSuffix];
    ExFile=fullfile(exFolder_full, ExFilename);
    writetable(T, ExFile); %Exports the table, output format depends on the ExFile
    
     clear difference
     clear difference_trans
     clear subtracted_sample
    
    %export grafu
    n=length(ExFile)
    ll=n-4
    print(ExFile(1:ll),'-dpng');
    close all
end


    



    


    