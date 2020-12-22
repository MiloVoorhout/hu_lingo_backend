--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

-- Started on 2020-12-11 15:27:51 CET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 16422)
-- Name: games; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.games (
    id integer NOT NULL,
    language character varying(5) NOT NULL,
    game_status integer NOT NULL,
    active boolean NOT NULL,
    user_id integer NOT NULL,
    score integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.games OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16420)
-- Name: games_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.games_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.games_id_seq OWNER TO postgres;

--
-- TOC entry 3288 (class 0 OID 0)
-- Dependencies: 202
-- Name: games_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.games_id_seq OWNED BY public.games.id;


--
-- TOC entry 205 (class 1259 OID 16435)
-- Name: rounds; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rounds (
    id integer NOT NULL,
    active boolean NOT NULL,
    word character varying(7) NOT NULL,
    game_id integer NOT NULL
);


ALTER TABLE public.rounds OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16433)
-- Name: rounds_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rounds_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rounds_id_seq OWNER TO postgres;

--
-- TOC entry 3289 (class 0 OID 0)
-- Dependencies: 204
-- Name: rounds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rounds_id_seq OWNED BY public.rounds.id;


--
-- TOC entry 207 (class 1259 OID 16448)
-- Name: turns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.turns (
    id integer NOT NULL,
    guessed_word character varying(7),
    started_at timestamp without time zone NOT NULL,
    round_id integer
);


ALTER TABLE public.turns OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16446)
-- Name: turns_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.turns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.turns_id_seq OWNER TO postgres;

--
-- TOC entry 3290 (class 0 OID 0)
-- Dependencies: 206
-- Name: turns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.turns_id_seq OWNED BY public.turns.id;


--
-- TOC entry 201 (class 1259 OID 16412)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(40) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 16410)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 3291 (class 0 OID 0)
-- Dependencies: 200
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 3136 (class 2604 OID 16425)
-- Name: games id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games ALTER COLUMN id SET DEFAULT nextval('public.games_id_seq'::regclass);


--
-- TOC entry 3138 (class 2604 OID 16438)
-- Name: rounds id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rounds ALTER COLUMN id SET DEFAULT nextval('public.rounds_id_seq'::regclass);


--
-- TOC entry 3139 (class 2604 OID 16451)
-- Name: turns id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.turns ALTER COLUMN id SET DEFAULT nextval('public.turns_id_seq'::regclass);


--
-- TOC entry 3135 (class 2604 OID 16415)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3145 (class 2606 OID 16427)
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (id);


--
-- TOC entry 3141 (class 2606 OID 16419)
-- Name: users name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT name_unique UNIQUE (username);


--
-- TOC entry 3147 (class 2606 OID 16440)
-- Name: rounds rounds_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rounds
    ADD CONSTRAINT rounds_pkey PRIMARY KEY (id);


--
-- TOC entry 3149 (class 2606 OID 16453)
-- Name: turns turns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.turns
    ADD CONSTRAINT turns_pkey PRIMARY KEY (id);


--
-- TOC entry 3143 (class 2606 OID 16417)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3151 (class 2606 OID 16479)
-- Name: rounds game_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rounds
    ADD CONSTRAINT game_fk FOREIGN KEY (game_id) REFERENCES public.games(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3152 (class 2606 OID 16484)
-- Name: turns round_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.turns
    ADD CONSTRAINT round_fk FOREIGN KEY (round_id) REFERENCES public.rounds(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3150 (class 2606 OID 16474)
-- Name: games user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES public.users(id) NOT VALID;


-- Completed on 2020-12-11 15:27:52 CET

--
-- PostgreSQL database dump complete
--

INSERT INTO public.users(
	username, password)
VALUES ('tester', 'testing');
