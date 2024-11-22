:- use_module(library(http/http_parameters)).
:- use_module(library(csv)).
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_json)).
:- use_module(library(http/http_cors)).

% Dynamic predicates for storing student data
:- dynamic student/3.

% Load CSV data
load_data :-
    % Read the CSV file, skipping the header row
    csv_read_file("data.csv", [_|Rows], []),
    % Process each row and assert as student fact
    process_rows(Rows).

% Process each row from CSV
process_rows([]).
process_rows([Row|Rows]) :-
    Row =.. [row,ID,Attendance,CGPA],
    assert(student(ID,Attendance,CGPA)),
    process_rows(Rows).

% Eligibility rules
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance, CGPA),
    Attendance >= 75,
    CGPA >= 9.0.

permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance, _),
    Attendance >= 75.

% CORS handling
:- set_setting(http:cors, [*]).

% API endpoints with CORS enabled
:- http_handler('/api/scholarship/', handle_scholarship_check, 
    [methods([options,get])]).
:- http_handler('/api/exam/', handle_exam_check, 
    [methods([options,get])]).

% Options handler for CORS preflight
handle_options(Request) :-
    cors_enable(Request, [methods([get,options])]),
    format('~n').

% Scholarship handler
handle_scholarship_check(Request) :-
    (Request.method == options ->
        handle_options(Request)
    ;
        cors_enable,
        http_parameters(Request, [student_id(StudentID, [])]),
        (eligible_for_scholarship(StudentID) ->
            Reply = json([status=true, message='Eligible for scholarship'])
        ;   
            Reply = json([status=false, message='Not eligible for scholarship'])
        ),
        reply_json(Reply)
    ).

% Exam handler
handle_exam_check(Request) :-
    (Request.method == options ->
        handle_options(Request)
    ;
        cors_enable,
        http_parameters(Request, [student_id(StudentID, [])]),
        (permitted_for_exam(StudentID) ->
            Reply = json([status=true, message='Permitted for exam'])
        ;   
            Reply = json([status=false, message='Not permitted for exam'])
        ),
        reply_json(Reply)
    ).

% Server setup
start_server :-
    load_data,
    http_server(http_dispatch, [port(8000)]).

:- initialization(start_server).