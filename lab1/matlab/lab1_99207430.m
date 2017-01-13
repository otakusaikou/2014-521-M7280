function varargout = lab1_99207430(varargin)
% LAB1_99207430 MATLAB code for lab1_99207430.fig
%      LAB1_99207430, by itself, creates a new LAB1_99207430 or raises the existing
%      singleton*.
%
%      H = LAB1_99207430 returns the handle to a new LAB1_99207430 or the handle to
%      the existing singleton*.
%
%      LAB1_99207430('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in LAB1_99207430.M with the given input arguments.
%
%      LAB1_99207430('Property','Value',...) creates a new LAB1_99207430 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before lab1_99207430_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to lab1_99207430_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help lab1_99207430

% Last Modified by GUIDE v2.5 25-Feb-2014 18:22:33

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @lab1_99207430_OpeningFcn, ...
                   'gui_OutputFcn',  @lab1_99207430_OutputFcn, ...
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

% --- Executes just before lab1_99207430 is made visible.
function lab1_99207430_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to lab1_99207430 (see VARARGIN)

% Choose default command line output for lab1_99207430
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% 建立全域變數&調整三軸比例
axis square;
xlabel('X');
ylabel('Y');
zlabel('Z');

% UIWAIT makes lab1_99207430 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = lab1_99207430_OutputFcn(hObject, eventdata, handles) 
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
close all


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% 產生均勻分布的50個點
global x y z Pt_ID err;
x = zeros(50, 1); y = zeros(50, 1); z = zeros(50, 1); Pt_ID = zeros(50, 1);
index = 1;
for i = 30:60:330
    for j = -70:20:70
        x(index) = 6371 * cos(j * (pi / 180)) * cos(i * (pi / 180));
        y(index) = 6371 * cos(j * (pi / 180)) * sin(i * (pi / 180));
        z(index) = 6371 * sin(j * (pi / 180));
        Pt_ID(index) = index;
        index = index + 1;
    end
end

Pt_ID(49) = 49;
Pt_ID(50) = 50;
x(49) = 6371 * cos(90 * (pi / 180)) * cos(0 * (pi / 180));
y(49) = 6371 * cos(90 * (pi / 180)) * sin(0 * (pi / 180));
z(49) = 6371 * sin(90 * (pi / 180));
x(50) = 6371 * cos(-90 * (pi / 180)) * cos(0 * (pi / 180));
y(50) = 6371 * cos(-90 * (pi / 180)) * sin(0 * (pi / 180));
z(50) = 6371 * sin(-90 * (pi / 180));

err = random('unif', -1, 1, 50, 3) * 0.025; % 產生隨機25公尺誤差
x_er = x + err(:,1); 
y_er = y + err(:,2);
z_er = z + err(:,3);

% 繪圖
hold on;
plot3(x, y, z, 'bx');
plot3(x_er, y_er, z_er, 'r*');
quiver3(x, y, z, err(:,1), err(:,2), err(:,3));
hold off;

% 移動視角
for az = -30 : .5 : 30
    view(az, 30);
    drawnow;
end

% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% 計算表格內容並傳入table
global Pt_ID x y z err;
So = sqrt(x.^2 + y.^2 + z.^2);
x_er = x + err(:,1); 
y_er = y + err(:,2);
z_er = z + err(:,3);
Sr = sqrt(x_er.^2 + y_er.^2 + z_er.^2);

tb_value = [Pt_ID, x, y, z, So, x_er, y_er, z_er, Sr, err(:,1), err(:,2), err(:,3)];
table(tb_value);
