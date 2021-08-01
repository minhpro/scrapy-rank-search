CREATE TABLE public.keyword
(
    id serial primary key,
    content varchar(100) NOT NULL,
    target_site varchar(200) NOT NULL,
    url varchar(200),
    rank integer,
    last_update timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    error_code smallint NOT NULL DEFAULT 0,
    is_active boolean NOT NULL DEFAULT true,
    priority integer NOT NULL DEFAULT 0
);

COMMENT ON TABLE public.keyword
    IS 'contain keywords and their ranks';

COMMENT ON COLUMN public.keyword.error_code
    IS '0: no error, 1: not found, 2: blocked, 3: other';