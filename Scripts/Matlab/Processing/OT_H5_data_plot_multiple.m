clear all
close all

%specify the pattern of files to load 
pattern='*.h5';

% Specify the folder where the files live.
Folder_base='C:\Users\lpeka\Documents\MATLAB\OT\data\new\';

myFolder = '2019-12-18-WT-LH - 2A';
myFolder_full=[Folder_base myFolder];
% Specify the folder where the files will be exported.
exFolder_suffix= '_graphs_LF';
exFolder = [myFolder exFolder_suffix];
exFolder_full=[Folder_base exFolder];
mkdir(exFolder_full);
    
% Check to make sure that folder actually exists.  Warn user if it doesn't.
if ~isdir(myFolder_full)
  errorMessage = sprintf('Error: The following folder does not exist:\n%s', myFolder);
  uiwait(warndlg(errorMessage));
  return;
end

% Get a list of all files in the folder with the desired file name pattern.
filePattern = fullfile(myFolder_full,pattern); % Change to whatever pattern you need.
theFiles = dir(filePattern);

for k = 1 : length(theFiles)
  baseFileName = theFiles(k).name;
  fullFileName = fullfile(myFolder_full, baseFileName);
  fprintf(1, 'Now reading %s\n', fullFileName);
  % Now do whatever you want with this file name,
  % such as reading it in as an image array with imread()
  
  
  %% data import
  
  filename=fullFileName;
   % Distance
   
   Distance_1 = h5read(filename, '/Distance/Distance 1'); %Low frequency data
   %Distance_2 = h5read(filename, '/Distance/Distance 2'); %Low frequency data
   Piezo_Distance=h5read(filename, '/Distance/Piezo Distance'); %High frequency data
   
   % Force High Frequency
   Force_1X_HF = h5read(filename, '/Force HF/Force 1x'); %High frequency data
   Force_1Y_HF = h5read(filename, '/Force HF/Force 1y'); %High frequency data
   
   Force_2X_HF = h5read(filename, '/Force HF/Force 2x'); %High frequency data
   Force_2Y_HF = h5read(filename, '/Force HF/Force 2y'); %High frequency data
   
      % Force Low Frequency
   Force_1X_LF = h5read(filename, '/Force LF/Force 1x'); %Low frequency data
   Force_1Y_LF = h5read(filename, '/Force LF/Force 1y'); %Low frequency data
   
   Force_2X_LF = h5read(filename, '/Force LF/Force 2x'); %Low frequency data
   Force_2Y_LF = h5read(filename, '/Force LF/Force 2y'); %Low frequency data
  
  
     %% plotting 
      
   % F-D curve plot LF
    close all

 plot(Distance_1.Value, Force_1X_LF.Value,'Marker','.', 'MarkerEdgeColor', 'k', 'LineStyle', 'none');
  % plot(Piezo_Distance, Force_1X_HF,'Marker','.', 'MarkerEdgeColor', 'k', 'LineStyle', 'none');
   %graph options
    grid on;
    % grid minor
    title('OT F-D curve');
    xlabel('Extension (um)');
    ylabel('Force (pN)');
    legend('Original - LF');
  
  %% export graph 
  
    LL=length(baseFileName)-3;
    ExFilename=[baseFileName(1:LL)];
    ExFile=fullfile(exFolder_full, ExFilename);
    
    print(ExFile,'-dpng');
end
