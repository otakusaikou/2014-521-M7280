function varargout = table(varargin)
% TABLE MATLAB code for table.fig
%      TABLE, by itself, creates a new TABLE or raises the existing
%      singleton*.
%
%      H = TABLE returns the handle to a new TABLE or the handle to
%      the existing singleton*.
%
%      TABLE('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in TABLE.M with the given input arguments.
%
%      TABLE('Property','Value',...) creates a new TABLE or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before table_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to table_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help table

% Last Modified by GUIDE v2.5 25-Feb-2014 00:22:57

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @table_OpeningFcn, ...
                   'gui_OutputFcn',  @table_OutputFcn, ...
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

% --- Executes just before table is made visible.
function table_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to table (see VARARGIN)

% Choose default command line output for table
handles.output = hObject;
% Update handles structure
guidata(hObject, handles);

% 接收表格內容並顯示於表格上

tb_value = cell2mat(varargin(1));
tb_value2 = {'Mean', mean(tb_value(:,10)), mean(tb_value(:,11)), mean(tb_value(:,12)); 'Std.', std(tb_value(:,10)), std(tb_value(:,11)), std(tb_value(:,12))};
set(handles.uitable2, 'data', tb_value);
set(handles.uitable3, 'data', tb_value2);


% UIWAIT makes table wait for user response (see UIRESUME)
% uiwait(handles.figure1);

% --- Outputs from this function are returned to the command line.
function varargout = table_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
close table;


% --- Executes when entered data in editable cell(s) in uitable2.
function uitable2_CellEditCallback(hObject, eventdata, handles)
% hObject    handle to uitable2 (see GCBO)
% eventdata  structure with the following fields (see UITABLE)
%	Indices: row and column indices of the cell(s) edited
%	PreviousData: previous data for the cell(s) edited
%	EditData: string(s) entered by the user
%	NewData: EditData or its converted form set on the Data property. Empty if Data was not changed
%	Error: error string when failed to convert EditData to appropriate value for Data
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function uitable2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to uitable2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
