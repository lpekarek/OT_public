function varargout = OT_FD_manually_comment_number(varargin)
% OT_FD_MANUALLY_COMMENT_NUMBER MATLAB code for OT_FD_manually_comment_number.fig
%      OT_FD_MANUALLY_COMMENT_NUMBER, by itself, creates a new OT_FD_MANUALLY_COMMENT_NUMBER or raises the existing
%      singleton*.
%
%      H = OT_FD_MANUALLY_COMMENT_NUMBER returns the handle to a new OT_FD_MANUALLY_COMMENT_NUMBER or the handle to
%      the existing singleton*.
%
%      OT_FD_MANUALLY_COMMENT_NUMBER('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in OT_FD_MANUALLY_COMMENT_NUMBER.M with the given input arguments.
%
%      OT_FD_MANUALLY_COMMENT_NUMBER('Property','Value',...) creates a new OT_FD_MANUALLY_COMMENT_NUMBER or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before OT_FD_manually_comment_number_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to OT_FD_manually_comment_number_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help OT_FD_manually_comment_number

% Last Modified by GUIDE v2.5 11-Mar-2020 08:28:44

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @OT_FD_manually_comment_number_OpeningFcn, ...
                   'gui_OutputFcn',  @OT_FD_manually_comment_number_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before OT_FD_manually_comment_number is made visible.
function OT_FD_manually_comment_number_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to OT_FD_manually_comment_number (see VARARGIN)
global dataMatrix
dataMatrix=[];
handles.comment=[];
% Choose default command line output for OT_FD_manually_comment_number
handles.output = hObject;


% Update handles structure
guidata(hObject, handles);

% UIWAIT makes OT_FD_manually_comment_number wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = OT_FD_manually_comment_number_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in Load_button.
function Load_button_Callback(hObject, eventdata, handles)
% hObject    handle to Load_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%Load a file
[file,path,indx] = uigetfile( ...
{
   '*.*',  'All Files (*.*)'}, ...
   'Select a File');
handles.file=file;
handles.path=path;
handles.indx=indx;
[Force Extension]=OT_csv_data_import([path file]);
handles.csv_imported_force=Force;
handles.csv_imported_extension=Extension;
handles.graph=plot(Extension, Force);
handles.graph.Marker='.';
%handles.graph.LineStyle='none';
title(file);
grid on
guidata(hObject, handles);



% --- Executes on button press in Write_button.
function Write_button_Callback(hObject, eventdata, handles)
% hObject    handle to Write_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
             [c_x, c_y]=ginput(2);
handles.coordinates_x=c_x;
handles.coordinates_y=c_y;

global dataMatrix
distance_f=num2str(c_x(1));
distance_u=num2str(c_x(2));
Force_f=num2str(c_y(1));
Force_u=num2str(c_y(2));
Force_half=num2str((c_y(1)+c_y(2))/2);
Delta_x=num2str((c_x(2)-c_x(1))*1000);
name=handles.file;
Comment=handles.comment;
global i
LR=size(dataMatrix);
tf_2=strcmp(handles.comment,'no clear event')
if tf_2==1
    i=0;
elseif LR(1)==0
    i=1;
else
    tf=strcmp(handles.file,dataMatrix(LR(1),1));
    if tf==1
        i=i+1;
    else
        i=1;
    end 
end
step_number=num2str(i);

dataMatrix=[dataMatrix; [{name} {step_number} {Force_f} {distance_f} {Force_u} {distance_u} {Force_half} {Delta_x} {Comment}]];
%table_as_cell = num2cell(dataMatrix);
table_handle = uitable(handles.table1);
set(table_handle, 'Data', dataMatrix);
%handles.coordinates = cell2mat({cursor_info.Position}');
guidata(hObject, handles);

   
  
% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu1


% --- Executes on button press in Export_button.
function Export_button_Callback(hObject, eventdata, handles)
% hObject    handle to Export_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global dataMatrix
%[{name} {Force_f} {distance_f} {Force_u} {distance_u}]]
Filter={'*.csv', 'CSV file (.csv)'};
[Exfilename, Expath, Exindex]=uiputfile(Filter);
File_name=dataMatrix(:,1);
step_number=dataMatrix(:,2);
Force_folded=dataMatrix(:,3);
Distance_folded=dataMatrix(:,4);
Force_unfolded=dataMatrix(:,5);
Distance_unfolded=dataMatrix(:,6);
Force_half=dataMatrix(:,7);
Delta_x=dataMatrix(:,8);
Comment=dataMatrix(:,9);
varNames = {'Filename','Step number','Force folded (pN)','Distance folded (um)','Force unfolded (pN)','Distance unfolded (um)','Force 1/2 (pN)','Delta x (nm)', 'Comment'};
T=table(File_name,step_number, Force_folded, Distance_folded, Force_unfolded, Distance_unfolded, Force_half, Delta_x, Comment, 'VariableNames',varNames);
%NewSuffix='_unfolding_events.csv';
%ExFilename_csv=[handles.file NewSuffix];
%ExFile_csv=fullfile(handles.path, ExFilename_csv);
ExFilename_full=[Exfilename];
ExFile_csv=fullfile(Expath, ExFilename_full);

writetable(T, ExFile_csv); %Exports the table, output format depends on the ExFile 

guidata(hObject, handles);



% --- Executes on button press in Delete_button.
function Delete_button_Callback(hObject, eventdata, handles)
% hObject    handle to Delete_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global dataMatrix
Last_row=size(dataMatrix);
global i 
if i <1
    i=1;
else 
    i=i-1;
end

dataMatrix=dataMatrix(1:Last_row(1)-1,:);
table_handle = uitable(handles.table1);
set(table_handle, 'Data', dataMatrix);

guidata(hObject, handles);


% --- Executes on button press in Clear_button.
function Clear_button_Callback(hObject, eventdata, handles)
% hObject    handle to Clear_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global dataMatrix
dataMatrix=[];
global i
i=1
table_handle = uitable(handles.table1);
set(table_handle, 'Data', dataMatrix);
guidata(hObject, handles);



function Comment_text_Callback(hObject, eventdata, handles)
% hObject    handle to Comment_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Comment_text as text
%        str2double(get(hObject,'String')) returns contents of Comment_text as a double
handles.comment=get(hObject,'String');
guidata(hObject, handles);


% --- Executes during object creation, after setting all properties.
function Comment_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Comment_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
