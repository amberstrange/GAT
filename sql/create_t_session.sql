CREATE TABLE t_session (
    uidpk           integer PRIMARY KEY,
    case_num     integer,
    email           varchar(40),
    time_stamp timestamp default current_timestamp
);