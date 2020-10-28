clear all
close all

%% multiplefiles parameters

%specify the pattern of files to load 
pattern='*.h5';

% Specify the folder where the files live.
Folder_base='C:\Users\lpeka\Documents\MATLAB\OT\data\new\';

myFolder = '2019-12-18-WT-LH';
myFolder_full=[Folder_base myFolder];
% Specify the folder where the files will be exported.
exFolder_suffix= '_smoothening';
exFolder = [myFolder exFolder_suffix];
exFolder_full=[Folder_base exFolder];
mkdir(exFolder_full);
    
% Check to make sure that folder actually exists.  Warn user if it doesn't.
if ~isdir(myFolder_full)
  errorMessage = sprintf('Error: The following folder does not exist:\n%s', myFolder);
  uiwait(warndlg(errorMessage));
  return;
end





%% sorting/smoothing parameters


% 1st sorting
    step1=40;
% moving average window size
    windowSize = 100; %defines how many values are averaged in one "window" (one turn)
% butterworth filter 
    fc=0.05; %critical frequency
    fo = 3; %filter order
% 2nd sorting
    step2=50;

    
    
    % Get a list of all files in the folder with the desired file name pattern.
filePattern = fullfile(myFolder_full,pattern); % Change to whatever pattern you need.
theFiles = dir(filePattern);

for k = 1 : length(theFiles)
    close all
    clear Distance_1 Distance_2 Piezo_Distance
    clear  Force_1X_HF Force_2X_HF Force_1X_LF Force_2X_LF Force_1Y_HF Force_1Y_LF Force_2Y_HF Force_2Y_LF
    clear Force_1X_HF_1st_sort Piezo_Distance_1st_sort Force_1X_HF_1st_sort_butter
    clear  Force_1X_HF_smooth Piezo_Distance_smooth
    clear T
    
    
    
    baseFileName = theFiles(k).name;
  fullFileName = fullfile(myFolder_full, baseFileName);
  fprintf(1, 'Now reading %s\n', fullFileName);
  % Now do whatever you want with this file name,
  % such as reading it in as an image array with imread()
   % data import

    
    
   filename=fullFileName;
   


   % Distance
  % Distance_1 = h5read(filename, '/Distance/Distance 1'); %Low frequency data
  % Distance_2 = h5read(filename, '/Distance/Distance 2'); %Low frequency data
   Piezo_Distance=h5read(filename, '/Distance/Piezo Distance'); %High frequency data
   
   % Force High Frequency
   Force_1X_HF = h5read(filename, '/Force HF/Force 1x'); %High frequency data
  % Force_1Y_HF = h5read(filename, '/Force HF/Force 1y'); %High frequency data
   
  % Force_2X_HF = h5read(filename, '/Force HF/Force 2x'); %High frequency data
  % Force_2Y_HF = h5read(filename, '/Force HF/Force 2y'); %High frequency data
   
      % Force Low Frequency
  % Force_1X_LF = h5read(filename, '/Force LF/Force 1x'); %Low frequency data
  % Force_1Y_LF = h5read(filename, '/Force LF/Force 1y'); %Low frequency data
   
  % Force_2X_LF = h5read(filename, '/Force LF/Force 2x'); %Low frequency data
  % Force_2Y_LF = h5read(filename, '/Force LF/Force 2y'); %Low frequency data
  
    plot(Piezo_Distance,Force_1X_HF)
    
%% sorting / smoothening 
% 1st selection
i=1;
for n=1:(length(Piezo_Distance)/step1); %selection of every step1-th x as the xnew
    Force_1X_HF_1st_sort(n)=Force_1X_HF(i);
    Piezo_Distance_1st_sort(n)=Piezo_Distance(i);
    i=i+step1;
    end
    %finds the y values corresponding to the sorted x values
     %rewrites the x 
    hold on
    plot(Piezo_Distance_1st_sort,Force_1X_HF_1st_sort,'g');
    
%Butterworth's filter
      %[b,a]=butter(2,0.02,'low');
    %y=filtfilt(b,a,y);
    %hold on
    %plot(x,y,'k')
    d = designfilt('lowpassiir','FilterOrder',fo,...
       'HalfPowerFrequency',fc,'DesignMethod','butter');
   Force_1X_HF_1st_sort_butter = filtfilt(d,Force_1X_HF_1st_sort);
    Piezo_Distance_1st_sort_butter =filtfilt(d,Piezo_Distance_1st_sort);
    
    hold on
    plot(Piezo_Distance_1st_sort_butter,Force_1X_HF_1st_sort_butter,'r')
    
%smoothdata after butterworth
    Force_1X_HF_smooth=smoothdata(Force_1X_HF_1st_sort_butter,'gaussian');
    Piezo_Distance_smooth=smoothdata(Piezo_Distance_1st_sort_butter, 'gaussian');
    hold on
    plot( Piezo_Distance_smooth,Force_1X_HF_smooth,'k')
    
%graph options
    title('OT pulling experiment');
    xlabel('Extension (um)');
    ylabel('Force (pN)');
    legend('Original','1st sort','butter','smoothed');
    grid on
    

 %% export graph 
  
    LL=length(baseFileName)-3;
    ExFilename=[baseFileName(1:LL)];
    ExFile=fullfile(exFolder_full, ExFilename);
    
    print(ExFile,'-dpng');
    
    close all
    
    plot(Piezo_Distance_1st_sort_butter,Force_1X_HF_1st_sort_butter,'r')
    title('OT pulling experiment');
    xlabel('Extension (um)');
    ylabel('Force (pN)');
    legend('butter');
      grid on
      grid minor
    

    LL=length(baseFileName)-3;
    ExFilename2=[ExFilename '_butt_filter'];
    ExFile=fullfile(exFolder_full, ExFilename);
    
    print(ExFile,'-dpng');

%% export the butterworth data as a csv
    
Piezo_distance=Piezo_Distance_1st_sort_butter.';
Force=Force_1X_HF_1st_sort_butter.';

T=table(Piezo_distance, Force); %Creates table with anotated columns
NewSuffix='_Butt_filtered.csv';
    ExFilename_csv=[baseFileName(1:LL),NewSuffix];
    ExFile_csv=fullfile(exFolder_full, ExFilename_csv);
    writetable(T, ExFile_csv); %Exports the table, output format depends on the ExFile    
end


    